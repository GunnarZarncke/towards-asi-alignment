"""End-to-end pipeline: simulate -> audit -> detect -> evaluate."""

from __future__ import annotations

import itertools
import json
import time
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from .bootstrap import (
    bootstrap_interventional,
    hierarchical_bootstrap,
    hierarchical_bootstrap_episode,
    hierarchical_bootstrap_rate,
    percentile_ci,
)
from .calibration import (
    FROZEN_CAPTURE_RULES,
    FROZEN_VALIDATION_SEEDS,
    fit_calibration,
    frozen_handle_calibration,
)
from .cci_audit import audit_cci
from .detector import run_detector, structural_coupling_mi
from .evaluate import evaluate, safety_decision
from .observation import build_audit_trace
from .schemas import (
    CALIBRATION_SCENARIOS,
    HELD_OUT_SCENARIOS,
    ALL_SCENARIOS,
    HANDLE_INSTRUMENTATION_LEVELS,
    INSTRUMENTATION_LEVELS,
    CCICalibration,
    InstrumentationLevel,
    ScenarioName,
    SimConfig,
)
from .resources import ResourceGovernor, execute_run_tasks, resource_suffix
from .simulator import scenario_config, simulate

# Fast regression subset: honest + capture + MB1 + MB9
SLICE_SCENARIOS: tuple[ScenarioName, ...] = (
    "honest",
    "capture_theater",
    "grounding_silent_gap",
    "boundary_alias",
)

CERTIFICATION_RATE_THRESHOLD = 0.95


def run_one(
    scenario: ScenarioName,
    seed: int,
    T: int,
    proposal_k: int = 8,
    calibration: CCICalibration | None = None,
    cfg_override: SimConfig | None = None,
    instrumentation: InstrumentationLevel = "none",
    bootstrap: bool = False,
    n_boot: int = 200,
) -> dict[str, object]:
    t0 = time.perf_counter()
    micro, ledger, episode_meta = simulate(scenario, seed, T=T, cfg_override=cfg_override)
    audit, lineage = build_audit_trace(
        micro, scenario, seed, episode_meta, instrumentation=instrumentation
    )
    ledger.lineage = lineage

    cal = calibration
    if cal is None and instrumentation in HANDLE_INSTRUMENTATION_LEVELS:
        cal = frozen_handle_calibration()

    detector = run_detector(audit, proposal_k=proposal_k)
    cci = audit_cci(audit, calibration=cal)
    safety = safety_decision(cci, detector)
    ev = evaluate(ledger, lineage, detector, cci, audit, episode_meta)

    boot_stats: dict[str, float] = {}
    if bootstrap and instrumentation != "none":
        boot_stats = bootstrap_interventional(
            audit, seed=seed, n_boot=n_boot, store_samples=True
        )

    elapsed = time.perf_counter() - t0
    result: dict[str, object] = {
        "scenario": scenario,
        "seed": seed,
        "T": T,
        "instrumentation": instrumentation,
        "runtime_seconds": round(elapsed, 3),
        "detector_runtime_seconds": round(detector.runtime_seconds, 3),
        "structural_coupling_mi": round(structural_coupling_mi(audit), 4),
        "n_audit_vars": len(audit.variables),
        "n_handle_channels": audit.n_handle_channels,
        "trace_bandwidth": audit.trace_bandwidth,
        "n_exogenous_vars": sum(1 for v in audit.variables if v.is_exogenous),
        "n_alias_vars": sum(1 for v in audit.variables if v.is_alias),
        "detector": {
            "proposal_k": detector.proposal_k,
            "n_clusters": len(detector.clusters),
            "substrate_failed": detector.substrate_failed,
            "clusters": [asdict(c) for c in detector.clusters],
        },
        "cci": asdict(cci),
        "safety": asdict(safety),
        "evaluation": asdict(ev),
        "oracle": {
            "judge_captured": ledger.judge_captured,
            "n_controller_vars": len(ledger.controller_object_ids),
            "n_board_vars": len(ledger.board_object_ids),
        },
    }
    if boot_stats:
        result["bootstrap_interventional"] = boot_stats
    return result


def run_one_task(task: dict[str, object]) -> dict[str, object]:
    """Picklable wrapper for parallel batch execution."""
    return run_one(
        task["scenario"],  # type: ignore[arg-type]
        int(task["seed"]),
        int(task["T"]),
        proposal_k=int(task.get("proposal_k", 8)),
        calibration=task.get("calibration"),
        cfg_override=task.get("cfg_override"),
        instrumentation=task.get("instrumentation", "none"),  # type: ignore[arg-type]
        bootstrap=bool(task.get("bootstrap", False)),
        n_boot=int(task.get("n_boot", 200)),
    )


def _run_task_specs(
    specs: list[dict[str, object]],
    governor: ResourceGovernor | None,
) -> list[dict[str, object]]:
    return execute_run_tasks(specs, run_one_task, governor)


def _one_task(
    scenario: ScenarioName,
    seed: int,
    T: int,
    *,
    proposal_k: int = 8,
    calibration: CCICalibration | None = None,
    instrumentation: InstrumentationLevel = "none",
    bootstrap: bool = False,
    n_boot: int = 200,
) -> dict[str, object]:
    return {
        "scenario": scenario,
        "seed": seed,
        "T": T,
        "proposal_k": proposal_k,
        "calibration": calibration,
        "instrumentation": instrumentation,
        "bootstrap": bootstrap,
        "n_boot": n_boot,
    }


def _summarize(runs: list[dict[str, object]]) -> dict[str, object]:
    by_scenario: dict[str, list[dict]] = {}
    for run in runs:
        by_scenario.setdefault(str(run["scenario"]), []).append(run)

    summary: dict[str, object] = {}
    for scen, scen_runs in by_scenario.items():
        correct = sum(1 for r in scen_runs if r["evaluation"]["cci_status_correct"])
        substrate_fail = sum(
            1 for r in scen_runs if r["detector"]["substrate_failed"]
        )
        summary[scen] = {
            "n_runs": len(scen_runs),
            "cci_status_correct_rate": correct / len(scen_runs),
            "detector_substrate_fail_rate": substrate_fail / len(scen_runs),
            "mean_controller_jaccard": sum(
                r["evaluation"]["controller_jaccard"] for r in scen_runs
            )
            / len(scen_runs),
            "mean_board_jaccard": sum(r["evaluation"]["board_jaccard"] for r in scen_runs)
            / len(scen_runs),
            "mean_naive_cci": sum(r["cci"]["naive_reported_cci_bits"] for r in scen_runs)
            / len(scen_runs),
            "mean_behavioral_cci": sum(r["cci"]["behavioral_cci_bits"] for r in scen_runs)
            / len(scen_runs),
            "mean_correction_episode_rate": sum(
                r["cci"]["correction_episode_rate"] for r in scen_runs
            )
            / len(scen_runs),
            "mean_intervention_rate": sum(
                r["cci"].get("intervention_episode_rate", 0.0) for r in scen_runs
            )
            / len(scen_runs),
            "mean_interventional_cci": sum(
                r["cci"].get("interventional_cci_bits", 0.0) for r in scen_runs
            )
            / len(scen_runs),
            "mean_trace_bandwidth": sum(r.get("trace_bandwidth", 0) for r in scen_runs)
            / len(scen_runs),
            "mean_capture_gap": sum(r["evaluation"]["naive_vs_behavioral_gap"] for r in scen_runs)
            / len(scen_runs),
            "capture_detected_rate": sum(
                1 for r in scen_runs if r["evaluation"]["capture_detected"]
            )
            / len(scen_runs),
            "mean_visible_probe_uptake": sum(
                r["evaluation"].get("visible_probe_uptake", 0.0) for r in scen_runs
            )
            / len(scen_runs),
            "mean_hidden_probe_uptake": sum(
                r["evaluation"].get("hidden_probe_uptake", 0.0) for r in scen_runs
            )
            / len(scen_runs),
            "mean_silent_harm_count": sum(
                r["evaluation"].get("silent_harm_count", 0) for r in scen_runs
            )
            / len(scen_runs),
            "mean_ground_drift_range": sum(
                r["evaluation"].get("ground_drift_range", 0.0) for r in scen_runs
            )
            / len(scen_runs),
            "mean_bundle_geometry_spread": sum(
                r["evaluation"].get("bundle_geometry_spread", 0.0) for r in scen_runs
            )
            / len(scen_runs),
            "mean_hidden_memory_step_rate": sum(
                r["evaluation"].get("hidden_memory_step_rate", 0.0) for r in scen_runs
            )
            / len(scen_runs),
        }
        boot_runs = [r for r in scen_runs if r.get("bootstrap_interventional")]
        if boot_runs:
            uptake_means = [r["bootstrap_interventional"]["uptake_mean"] for r in boot_runs]
            ivl_means = [r["bootstrap_interventional"]["interventional_cci_mean"] for r in boot_runs]
            across_uptake = percentile_ci(uptake_means)
            across_ivl = percentile_ci(ivl_means)
            summary[scen]["bootstrap"] = {
                "n_runs_with_bootstrap": len(boot_runs),
                "mean_uptake": sum(uptake_means) / len(boot_runs),
                "uptake_lo": sum(
                    r["bootstrap_interventional"]["uptake_lo"] for r in boot_runs
                )
                / len(boot_runs),
                "uptake_hi": sum(
                    r["bootstrap_interventional"]["uptake_hi"] for r in boot_runs
                )
                / len(boot_runs),
                "mean_interventional_cci": sum(ivl_means) / len(boot_runs),
                "interventional_cci_lo": sum(
                    r["bootstrap_interventional"]["interventional_cci_lo"] for r in boot_runs
                )
                / len(boot_runs),
                "interventional_cci_hi": sum(
                    r["bootstrap_interventional"]["interventional_cci_hi"] for r in boot_runs
                )
                / len(boot_runs),
                "across_seed_uptake": across_uptake,
                "across_seed_interventional_cci": across_ivl,
                "hierarchical_uptake": hierarchical_bootstrap_episode(
                    boot_runs, "uptake_samples", "uptake_mean", seed=hash(scen) % 10_000
                ),
                "hierarchical_interventional_cci": hierarchical_bootstrap_episode(
                    boot_runs,
                    "interventional_cci_samples",
                    "interventional_cci_mean",
                    seed=hash(scen + "ivl") % 10_000,
                ),
                "hierarchical_uptake_legacy": hierarchical_bootstrap(boot_runs, "uptake"),
                "hierarchical_interventional_cci_legacy": hierarchical_bootstrap(
                    boot_runs, "interventional_cci"
                ),
                "hierarchical_cci_correct_rate": hierarchical_bootstrap_rate(
                    scen_runs, seed=hash(scen + "correct") % 10_000
                ),
            }
    return summary


def run_calibrated_suite(
    calibration_seeds: list[int],
    test_seeds: list[int],
    T: int,
    proposal_k: int = 8,
    held_out_scenarios: tuple[ScenarioName, ...] = HELD_OUT_SCENARIOS,
) -> dict[str, object]:
    calib_runs: list[dict[str, object]] = []
    for scenario in CALIBRATION_SCENARIOS:
        for seed in calibration_seeds:
            calib_runs.append(
                run_one(scenario, seed, T, proposal_k=proposal_k, calibration=None)
            )

    calibration = fit_calibration(calib_runs)

    test_runs: list[dict[str, object]] = []
    for scenario in held_out_scenarios:
        for seed in test_seeds:
            test_runs.append(
                run_one(
                    scenario, seed, T, proposal_k=proposal_k, calibration=calibration
                )
            )

    for scenario in CALIBRATION_SCENARIOS:
        for seed in test_seeds:
            test_runs.append(
                run_one(
                    scenario, seed, T, proposal_k=proposal_k, calibration=calibration
                )
            )

    return {
        "claim_strength": "calibrated sanity-check; held-out scenarios on test seeds",
        "detector": "classical MI/CMI spotlight; opaque audit IDs; no trained model",
        "T": T,
        "calibration_seeds": calibration_seeds,
        "test_seeds": test_seeds,
        "calibration_scenarios": list(CALIBRATION_SCENARIOS),
        "held_out_scenarios": list(held_out_scenarios),
        "calibration": asdict(calibration),
        "summary_calibration": _summarize(calib_runs),
        "summary_test": _summarize(test_runs),
        "calibration_runs": calib_runs,
        "test_runs": test_runs,
    }


def run_suite(
    scenarios: list[ScenarioName],
    seeds: list[int],
    T: int,
    proposal_k: int = 8,
) -> dict[str, object]:
    runs: list[dict[str, object]] = []
    for scenario in scenarios:
        for seed in seeds:
            runs.append(run_one(scenario, seed, T, proposal_k=proposal_k))

    return {
        "claim_strength": "controlled sanity-check; not frontier-system evidence",
        "detector": "classical MI/CMI spotlight; opaque audit IDs; no trained model",
        "provenance": "MI/CMI estimators adapted from experiments/correction_capture_toy.py patterns",
        "T": T,
        "seeds": seeds,
        "scenarios": scenarios,
        "summary_by_scenario": _summarize(runs),
        "runs": runs,
    }


SWEEP_AXES: dict[str, list[float | int]] = {
    "responsiveness": [0.15, 0.4, 0.92],
    "theater_rate": [0.7, 0.95],
    "n_decoys": [2, 6, 10],
}


def run_parameter_sweep(
    seeds: list[int],
    T: int,
    proposal_k: int = 8,
) -> dict[str, object]:
    """Grid over sim parameters on calibration scenarios; report CCI separation."""
    keys = list(SWEEP_AXES.keys())
    grid = list(itertools.product(*(SWEEP_AXES[k] for k in keys)))
    sweep_rows: list[dict[str, object]] = []

    for combo in grid:
        params = dict(zip(keys, combo, strict=True))
        base = scenario_config("capture_theater")
        cfg = SimConfig(
            T=T,
            responsiveness=float(params["responsiveness"]),
            task_drive=base.task_drive,
            judge_capture=params["responsiveness"] < 0.5,
            theater_rate=float(params["theater_rate"]),
            n_decoys=int(params["n_decoys"]),
            n_world=base.n_world,
            process_noise=base.process_noise,
        )
        runs: list[dict] = []
        for seed in seeds:
            for scen in ("honest", "capture_theater"):
                runs.append(
                    run_one(
                        scen,  # type: ignore[arg-type]
                        seed,
                        T,
                        proposal_k=proposal_k,
                        cfg_override=cfg if scen == "capture_theater" else None,
                    )
                )
        honest = [r for r in runs if r["scenario"] == "honest"]
        capture = [r for r in runs if r["scenario"] == "capture_theater"]
        sweep_rows.append(
            {
                "params": params,
                "mean_honest_behavioral": sum(r["cci"]["behavioral_cci_bits"] for r in honest)
                / max(len(honest), 1),
                "mean_capture_gap": sum(r["evaluation"]["naive_vs_behavioral_gap"] for r in capture)
                / max(len(capture), 1),
                "capture_detect_rate": sum(
                    1 for r in capture if r["evaluation"]["capture_detected"]
                )
                / max(len(capture), 1),
                "mean_controller_jaccard": sum(
                    r["evaluation"]["controller_jaccard"] for r in runs
                )
                / max(len(runs), 1),
                "detector_fail_rate": sum(
                    1 for r in runs if r["detector"]["substrate_failed"]
                )
                / max(len(runs), 1),
            }
        )

    return {
        "T": T,
        "seeds": seeds,
        "axes": SWEEP_AXES,
        "n_grid_points": len(grid),
        "rows": sweep_rows,
    }


def _delta_summary(
    none_runs: list[dict[str, object]], handle_runs: list[dict[str, object]]
) -> dict[str, object]:
    """Per-scenario delta: light_handles minus none."""
    by_key_none = {(r["scenario"], r["seed"]): r for r in none_runs}
    by_key_handle = {(r["scenario"], r["seed"]): r for r in handle_runs}
    deltas: dict[str, list[dict[str, float]]] = {}

    for key, rn in by_key_none.items():
        rh = by_key_handle.get(key)
        if rh is None:
            continue
        scen = str(key[0])
        deltas.setdefault(scen, []).append(
            {
                "behavioral_cci": rh["cci"]["behavioral_cci_bits"]
                - rn["cci"]["behavioral_cci_bits"],
                "interventional_cci": rh["cci"].get("interventional_cci_bits", 0.0),
                "manipulation": rh["cci"]["manipulation"] - rn["cci"]["manipulation"],
                "capture_gap": rh["evaluation"]["naive_vs_behavioral_gap"]
                - rn["evaluation"]["naive_vs_behavioral_gap"],
                "cci_correct_delta": float(rh["evaluation"]["cci_status_correct"])
                - float(rn["evaluation"]["cci_status_correct"]),
                "trace_bandwidth_delta": float(rh.get("trace_bandwidth", 0))
                - float(rn.get("trace_bandwidth", 0)),
                "n_handle_channels": float(rh.get("n_handle_channels", 0)),
            }
        )

    out: dict[str, object] = {}
    for scen, rows in deltas.items():
        n = len(rows)
        out[scen] = {
            "n_runs": n,
            "mean_delta_behavioral_cci": sum(r["behavioral_cci"] for r in rows) / n,
            "mean_interventional_cci": sum(r["interventional_cci"] for r in rows) / n,
            "mean_delta_manipulation": sum(r["manipulation"] for r in rows) / n,
            "mean_delta_capture_gap": sum(r["capture_gap"] for r in rows) / n,
            "mean_cci_correct_improvement": sum(r["cci_correct_delta"] for r in rows) / n,
            "mean_trace_bandwidth_delta": sum(r["trace_bandwidth_delta"] for r in rows) / n,
            "n_handle_channels": rows[0]["n_handle_channels"] if rows else 0.0,
        }
    return out


def run_instrumentation_compare(
    scenarios: tuple[ScenarioName, ...],
    seeds: list[int],
    T: int,
    proposal_k: int = 8,
) -> dict[str, object]:
    """Compare passive (none) vs light handle instrumentation on the same seeds."""
    none_runs: list[dict[str, object]] = []
    handle_runs: list[dict[str, object]] = []
    for scenario in scenarios:
        for seed in seeds:
            none_runs.append(
                run_one(
                    scenario,
                    seed,
                    T,
                    proposal_k=proposal_k,
                    instrumentation="none",
                )
            )
            handle_runs.append(
                run_one(
                    scenario,
                    seed,
                    T,
                    proposal_k=proposal_k,
                    instrumentation="light_handles",
                )
            )

    return {
        "claim_strength": (
            "instrumentation-cost sanity-check; compares passive vs light handle tracing"
        ),
        "T": T,
        "seeds": seeds,
        "scenarios": list(scenarios),
        "instrumentation_levels": ["none", "light_handles"],
        "summary_none": _summarize(none_runs),
        "summary_light_handles": _summarize(handle_runs),
        "delta_light_minus_none": _delta_summary(none_runs, handle_runs),
        "runs_none": none_runs,
        "runs_light_handles": handle_runs,
    }


def _overall_correct_rate(runs: list[dict[str, object]]) -> float:
    if not runs:
        return 0.0
    return sum(1 for r in runs if r["evaluation"]["cci_status_correct"]) / len(runs)


def _min_certifiable_level(
    level_results: dict[str, object],
    rate_key: str,
    threshold: float = CERTIFICATION_RATE_THRESHOLD,
) -> InstrumentationLevel | None:
    for level in INSTRUMENTATION_LEVELS:
        stats = level_results.get(level)
        if not stats:
            continue
        rate = stats.get(rate_key, 0.0)  # type: ignore[union-attr]
        if float(rate) >= threshold:
            return level
    return None


def _append_log(log_path: Path | None, line: str) -> None:
    if log_path is None:
        return
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(line.rstrip() + "\n")


def _emit_progress(
    log_path: Path | None,
    print_fn: Callable[[str], None],
    line: str,
) -> None:
    print_fn(line)
    _append_log(log_path, f"[{datetime.now(timezone.utc).isoformat()}] {line}")


def _write_curve_checkpoint(
    output_path: Path | None,
    payload: dict[str, object],
) -> None:
    if output_path is None:
        return
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def run_slice(
    test_seeds: list[int],
    T: int,
    proposal_k: int = 8,
    bootstrap: bool = False,
    n_boot: int = 100,
    log_path: Path | None = None,
    governor: ResourceGovernor | None = None,
) -> dict[str, object]:
    """Fast regression: SLICE_SCENARIOS × all instrumentation levels × test seeds."""
    runs: list[dict[str, object]] = []
    total = len(SLICE_SCENARIOS) * len(INSTRUMENTATION_LEVELS) * len(test_seeds)
    done = 0
    t0 = time.perf_counter()

    for level in INSTRUMENTATION_LEVELS:
        cal = frozen_handle_calibration() if level != "none" else None
        for scenario in SLICE_SCENARIOS:
            specs = [
                _one_task(
                    scenario,
                    seed,
                    T,
                    proposal_k=proposal_k,
                    calibration=cal,
                    instrumentation=level,
                    bootstrap=bootstrap,
                    n_boot=n_boot,
                )
                for seed in test_seeds
            ]
            scen_runs = _run_task_specs(specs, governor)
            done += len(scen_runs)
            runs.extend(scen_runs)
            rate = _overall_correct_rate(scen_runs)
            _emit_progress(
                log_path,
                print,
                f"slice [{done}/{total}] {level}/{scenario} "
                f"cci_correct={rate:.2f} n={len(scen_runs)}{resource_suffix(governor)}",
            )

    elapsed = time.perf_counter() - t0
    payload: dict[str, object] = {
        "claim_strength": "slice regression; not a full curve artifact",
        "T": T,
        "test_seeds": test_seeds,
        "scenarios": list(SLICE_SCENARIOS),
        "instrumentation_levels": list(INSTRUMENTATION_LEVELS),
        "runtime_seconds": round(elapsed, 2),
        "summary_by_scenario": _summarize(runs),
        "summary_by_level": {
            level: _summarize([r for r in runs if r["instrumentation"] == level])
            for level in INSTRUMENTATION_LEVELS
        },
        "runs": runs,
    }
    if governor:
        payload["resource_usage"] = governor.peak_summary()
    return payload


def run_instrumentation_curve(
    calibration_seeds: list[int],
    test_seeds: list[int],
    T: int,
    proposal_k: int = 8,
    bootstrap: bool = False,
    n_boot: int = 200,
    output_path: Path | None = None,
    log_path: Path | None = None,
    governor: ResourceGovernor | None = None,
) -> dict[str, object]:
    """Run none → light → medium → strong; report minimum certifiable level."""
    frozen = frozen_handle_calibration()
    level_results: dict[str, object] = {}
    t0 = time.perf_counter()

    base_payload: dict[str, object] = {
        "status": "in_progress",
        "claim_strength": (
            "instrumentation cost curve; frozen handle thresholds; passive is uncertifiable"
        ),
        "T": T,
        "calibration_seeds": calibration_seeds,
        "test_seeds": test_seeds,
        "calibration_scenarios": list(CALIBRATION_SCENARIOS),
        "held_out_scenarios": list(HELD_OUT_SCENARIOS),
        "frozen_handle_thresholds": asdict(frozen),
        "bootstrap_enabled": bootstrap,
        "n_boot": n_boot if bootstrap else 0,
        "completed_levels": [],
        "by_level": {},
        "interpretation": {
            "none_belowThreshold": (
                "Passive mode always returns belowThreshold: uncertifiable, not a passing audit."
            ),
            "cci_status_correct_on_none": (
                "Post-hoc evaluation may mark none as correct when uncertifiable is the "
                "expected outcome for honest/weak/MB9 scenarios."
            ),
        },
    }
    _write_curve_checkpoint(output_path, base_payload)

    for level in INSTRUMENTATION_LEVELS:
        _emit_progress(
            log_path,
            print,
            f"curve: starting level={level}",
        )
        calib_runs: list[dict[str, object]] = []
        test_runs: list[dict[str, object]] = []
        cal = frozen if level != "none" else None

        for scenario in CALIBRATION_SCENARIOS:
            specs = [
                _one_task(
                    scenario,
                    seed,
                    T,
                    proposal_k=proposal_k,
                    calibration=cal,
                    instrumentation=level,
                    bootstrap=bootstrap,
                    n_boot=n_boot,
                )
                for seed in calibration_seeds
            ]
            calib_runs.extend(_run_task_specs(specs, governor))
            rate = _overall_correct_rate(calib_runs)
            _emit_progress(
                log_path,
                print,
                f"  calib {level}/{scenario}: runs={len(calib_runs)} correct={rate:.2f}"
                f"{resource_suffix(governor)}",
            )

        for scenario in CALIBRATION_SCENARIOS + HELD_OUT_SCENARIOS:
            specs = [
                _one_task(
                    scenario,
                    seed,
                    T,
                    proposal_k=proposal_k,
                    calibration=cal,
                    instrumentation=level,
                    bootstrap=bootstrap,
                    n_boot=n_boot,
                )
                for seed in test_seeds
            ]
            batch = _run_task_specs(specs, governor)
            test_runs.extend(batch)
            rate = _overall_correct_rate(test_runs)
            _emit_progress(
                log_path,
                print,
                f"  test {level}/{scenario}: runs={len(test_runs)} correct={rate:.2f}"
                f"{resource_suffix(governor)}",
            )

        level_results[level] = {
            "n_handle_channels": calib_runs[0]["n_handle_channels"] if calib_runs else 0,
            "mean_trace_bandwidth": sum(r["trace_bandwidth"] for r in calib_runs)
            / max(len(calib_runs), 1),
            "frozen_thresholds": asdict(frozen) if level != "none" else None,
            "summary_calibration": _summarize(calib_runs),
            "summary_test": _summarize(test_runs),
            "cci_correct_rate_calibration": _overall_correct_rate(calib_runs),
            "cci_correct_rate_test": _overall_correct_rate(test_runs),
            "cci_correct_rate_test_calib_scenarios": _overall_correct_rate(
                [r for r in test_runs if r["scenario"] in CALIBRATION_SCENARIOS]
            ),
        }
        completed = list(base_payload.get("completed_levels", [])) + [level]
        base_payload["completed_levels"] = completed
        base_payload["by_level"] = level_results
        base_payload["minimum_certifiable_level_calibration"] = _min_certifiable_level(
            level_results, "cci_correct_rate_test_calib_scenarios"
        )
        base_payload["minimum_certifiable_level_full_held_out"] = _min_certifiable_level(
            level_results, "cci_correct_rate_test"
        )
        base_payload["minimum_certifiable_level"] = base_payload[
            "minimum_certifiable_level_calibration"
        ]
        _write_curve_checkpoint(output_path, base_payload)
        stats = level_results[level]
        _emit_progress(
            log_path,
            print,
            f"curve: finished {level} calib={stats['cci_correct_rate_calibration']:.2f} "  # type: ignore[index]
            f"test={stats['cci_correct_rate_test']:.2f} "  # type: ignore[index]
            f"test_calib={stats['cci_correct_rate_test_calib_scenarios']:.2f}",  # type: ignore[index]
        )

    min_calib = _min_certifiable_level(
        level_results, "cci_correct_rate_test_calib_scenarios"
    )
    min_full = _min_certifiable_level(level_results, "cci_correct_rate_test")

    payload: dict[str, object] = {
        "status": "complete",
        "claim_strength": base_payload["claim_strength"],
        "T": T,
        "calibration_seeds": calibration_seeds,
        "test_seeds": test_seeds,
        "calibration_scenarios": list(CALIBRATION_SCENARIOS),
        "held_out_scenarios": list(HELD_OUT_SCENARIOS),
        "frozen_handle_thresholds": asdict(frozen),
        "minimum_certifiable_level": min_calib,
        "minimum_certifiable_level_calibration": min_calib,
        "minimum_certifiable_level_full_held_out": min_full,
        "bootstrap_enabled": bootstrap,
        "n_boot": n_boot if bootstrap else 0,
        "runtime_seconds": round(time.perf_counter() - t0, 2),
        "completed_levels": list(INSTRUMENTATION_LEVELS),
        "interpretation": base_payload["interpretation"],
        "by_level": level_results,
    }
    if governor:
        payload["resource_usage"] = governor.peak_summary()
    _write_curve_checkpoint(output_path, payload)
    return payload


def run_frozen_validation(
    validation_seeds: list[int],
    T: int,
    proposal_k: int = 8,
    bootstrap: bool = False,
    n_boot: int = 200,
    log_path: Path | None = None,
    governor: ResourceGovernor | None = None,
) -> dict[str, object]:
    """Fresh-seed validation with pre-registered thresholds; no refitting."""
    frozen = frozen_handle_calibration()
    t0 = time.perf_counter()
    runs: list[dict[str, object]] = []
    total = len(INSTRUMENTATION_LEVELS) * len(ALL_SCENARIOS) * len(validation_seeds)
    done = 0

    for level in INSTRUMENTATION_LEVELS:
        cal = frozen if level != "none" else None
        for scenario in ALL_SCENARIOS:
            specs = [
                _one_task(
                    scenario,
                    seed,
                    T,
                    proposal_k=proposal_k,
                    calibration=cal,
                    instrumentation=level,
                    bootstrap=bootstrap,
                    n_boot=n_boot,
                )
                for seed in validation_seeds
            ]
            scen_runs = _run_task_specs(specs, governor)
            runs.extend(scen_runs)
            done += len(scen_runs)
            _emit_progress(
                log_path,
                print,
                f"frozen_validation [{done}/{total}] {level}/{scenario} "
                f"cci_correct={_overall_correct_rate(scen_runs):.2f} "
                f"n={len(scen_runs)}{resource_suffix(governor)}",
            )

    by_level = {
        level: _summarize([r for r in runs if r["instrumentation"] == level])
        for level in INSTRUMENTATION_LEVELS
    }
    capture_mild_by_level = {
        level: by_level[level].get("capture_mild", {}).get("cci_status_correct_rate", 0.0)  # type: ignore[union-attr]
        for level in INSTRUMENTATION_LEVELS
    }

    payload: dict[str, object] = {
        "claim_strength": (
            "fresh-seed frozen-threshold validation; no threshold retuning on these seeds"
        ),
        "T": T,
        "validation_seeds": validation_seeds,
        "frozen_handle_thresholds": asdict(frozen),
        "frozen_capture_rules": FROZEN_CAPTURE_RULES,
        "scenarios": list(ALL_SCENARIOS),
        "instrumentation_levels": list(INSTRUMENTATION_LEVELS),
        "runtime_seconds": round(time.perf_counter() - t0, 2),
        "summary_by_level": by_level,
        "capture_mild_correct_rate_by_level": capture_mild_by_level,
        "overall_correct_rate_by_level": {
            level: _overall_correct_rate([r for r in runs if r["instrumentation"] == level])
            for level in INSTRUMENTATION_LEVELS
        },
        "runs": runs,
    }
    if governor:
        payload["resource_usage"] = governor.peak_summary()
    return payload
