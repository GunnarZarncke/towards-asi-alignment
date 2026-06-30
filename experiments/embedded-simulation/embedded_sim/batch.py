"""Batch runners: instrumentation curve, frozen validation, sweeps, red-team battery."""

from __future__ import annotations

import itertools
import time
from dataclasses import asdict
from typing import Any

from .audit_core.calibration import FROZEN_CAPTURE_RULES, frozen_handle_calibration
from .audit_core.schemas import (
    CALIBRATION_SCENARIOS,
    HANDLE_INSTRUMENTATION_LEVELS,
    HELD_OUT_SCENARIOS,
    INSTRUMENTATION_LEVELS,
    InstrumentationLevel,
)
from .methodology import (
    CERTIFICATION_RATE_THRESHOLD,
    CURVE_INTERPRETATION,
    DEFAULT_CALIBRATION_SEEDS,
    DEFAULT_TEST_SEEDS,
    FROZEN_VALIDATION_SEEDS,
    capture_mild_rate_by_level,
    frozen_payload_header,
    min_certifiable_level,
    overall_correct_rate,
    redteam_crux_metrics,
    scenario_to_bridge,
    summarize_runs,
)
from .pipeline import episode_to_dict, run_episode
from .redteam import STRATEGIES
from .scenarios import MB_SCENARIOS
from .stats import hierarchical_bootstrap_rate
REDTEAM_BATTERY_BRIDGES = (
    "MB1",
    "MB4",
    "MB6",
    "MB7",
    "MB9",
    "instrument_capture",
    "MB7d",
)
BATTERY_STRATEGIES = tuple(STRATEGIES.keys())
BATTERY_LEVELS: tuple[InstrumentationLevel, ...] = (
    "light_handles",
    "medium_handles",
    "strong_handles",
)


def _bridge_scenario(bridge: str) -> str:
    for b, sc, _ in MB_SCENARIOS:
        if b == bridge:
            return sc
    raise KeyError(bridge)


def _summarize_episodes(runs: list[dict[str, Any]]) -> dict[str, Any]:
    false_passes = [r for r in runs if r.get("outer", {}).get("false_pass")]
    by_key: dict[str, list[dict]] = {}
    for run in runs:
        key = f"{run.get('bridge')}|{run.get('redteam_strategy', 'none')}|{run.get('instrumentation')}"
        by_key.setdefault(key, []).append(run)

    return {
        "n_runs": len(runs),
        "false_pass_count": len(false_passes),
        "false_pass_rate": len(false_passes) / max(len(runs), 1),
        "outer_certifies_rate": sum(1 for r in runs if r.get("outer", {}).get("outer_certifies"))
        / max(len(runs), 1),
        "in_sim_correct_rate": sum(1 for r in runs if r.get("outer", {}).get("in_sim_correct"))
        / max(len(runs), 1),
        "summary_by_group": {
            key: {
                "n": len(group),
                "false_pass_rate": sum(1 for r in group if r.get("outer", {}).get("false_pass"))
                / max(len(group), 1),
                "in_sim_correct_rate": sum(
                    1 for r in group if r.get("outer", {}).get("in_sim_correct")
                )
                / max(len(group), 1),
            }
            for key, group in by_key.items()
        },
    }


def _run_scenario_episode(
    scenario: str,
    seed: int,
    *,
    T: int,
    instrumentation: InstrumentationLevel,
    redteam_strategy: str = "none",
    substrate: str = "python",
) -> dict[str, Any]:
    bridge = scenario_to_bridge(scenario)
    ep = run_episode(
        bridge,  # type: ignore[arg-type]
        scenario,
        seed=seed,
        T=T,
        instrumentation=instrumentation,
        redteam_strategy=redteam_strategy,
        substrate=substrate,  # type: ignore[arg-type]
    )
    return episode_to_dict(ep)


def run_instrumentation_curve(
    *,
    calibration_seeds: list[int] | None = None,
    test_seeds: list[int] | None = None,
    T: int = 800,
    substrate: str = "python",
    redteam_strategy: str = "none",
    bootstrap: bool = False,
    n_boot: int = 200,
) -> dict[str, Any]:
    """Toy-parity none → light → medium → strong curve with cal/test seed split."""
    t0 = time.perf_counter()
    calibration_seeds = list(calibration_seeds or DEFAULT_CALIBRATION_SEEDS)
    test_seeds = list(test_seeds or DEFAULT_TEST_SEEDS)
    frozen = frozen_handle_calibration()
    level_results: dict[str, object] = {}

    for level in INSTRUMENTATION_LEVELS:
        calib_runs: list[dict[str, Any]] = []
        test_runs: list[dict[str, Any]] = []
        print(f"instrumentation_curve: starting level={level}")

        for scenario in CALIBRATION_SCENARIOS:
            for seed in calibration_seeds:
                calib_runs.append(
                    _run_scenario_episode(
                        scenario,
                        seed,
                        T=T,
                        instrumentation=level,
                        redteam_strategy=redteam_strategy,
                        substrate=substrate,
                    )
                )
            print(
                f"  calib {level}/{scenario}: runs={len(calib_runs)} "
                f"correct={overall_correct_rate(calib_runs):.2f}"
            )

        for scenario in CALIBRATION_SCENARIOS + HELD_OUT_SCENARIOS:
            for seed in test_seeds:
                test_runs.append(
                    _run_scenario_episode(
                        scenario,
                        seed,
                        T=T,
                        instrumentation=level,
                        redteam_strategy=redteam_strategy,
                        substrate=substrate,
                    )
                )
            print(
                f"  test {level}/{scenario}: runs={len(test_runs)} "
                f"correct={overall_correct_rate(test_runs):.2f}"
            )

        level_summary_calib = summarize_runs(calib_runs, bootstrap=bootstrap, n_boot=n_boot)
        level_summary_test = summarize_runs(test_runs, bootstrap=bootstrap, n_boot=n_boot)
        test_calib_only = [
            r for r in test_runs if r.get("scenario") in CALIBRATION_SCENARIOS
        ]
        level_results[level] = {
            "frozen_thresholds": asdict(frozen) if level != "none" else None,
            "summary_calibration": level_summary_calib,
            "summary_test": level_summary_test,
            "cci_correct_rate_calibration": overall_correct_rate(calib_runs),
            "cci_correct_rate_test": overall_correct_rate(test_runs),
            "cci_correct_rate_test_calib_scenarios": overall_correct_rate(test_calib_only),
        }
        if bootstrap:
            level_results[level]["cci_correct_bootstrap_test"] = hierarchical_bootstrap_rate(  # type: ignore[index]
                test_runs, field="cci_status_correct", n_boot=n_boot
            )
        stats = level_results[level]
        print(
            f"instrumentation_curve: finished {level} "
            f"calib={stats['cci_correct_rate_calibration']:.2f} "  # type: ignore[index]
            f"test={stats['cci_correct_rate_test']:.2f} "  # type: ignore[index]
            f"test_calib={stats['cci_correct_rate_test_calib_scenarios']:.2f}"  # type: ignore[index]
        )

    min_calib = min_certifiable_level(
        level_results, "cci_correct_rate_test_calib_scenarios"
    )
    min_full = min_certifiable_level(level_results, "cci_correct_rate_test")

    return {
        "mode": "instrumentation_curve",
        "status": "complete",
        "claim_strength": (
            "instrumentation cost curve; frozen handle thresholds; passive is uncertifiable"
        ),
        "T": T,
        "calibration_seeds": calibration_seeds,
        "test_seeds": test_seeds,
        "calibration_scenarios": list(CALIBRATION_SCENARIOS),
        "held_out_scenarios": list(HELD_OUT_SCENARIOS),
        "frozen_handle_thresholds": asdict(frozen),
        "frozen_capture_rules": FROZEN_CAPTURE_RULES,
        "certification_rate_threshold": CERTIFICATION_RATE_THRESHOLD,
        "bootstrap_enabled": bootstrap,
        "n_boot": n_boot if bootstrap else 0,
        "substrate": substrate,
        "redteam_strategy": redteam_strategy,
        "runtime_seconds": round(time.perf_counter() - t0, 2),
        "interpretation": CURVE_INTERPRETATION,
        "by_level": level_results,
        "minimum_certifiable_level": min_calib,
        "minimum_certifiable_level_calibration": min_calib,
        "minimum_certifiable_level_full_held_out": min_full,
        "completed_levels": list(INSTRUMENTATION_LEVELS),
    }


def run_instrumentation_matrix(
    *,
    seed: int = 42,
    T: int = 800,
    substrate: str = "python",
    redteam_strategy: str = "none",
    progress_every: int = 10,
) -> dict[str, Any]:
    t0 = time.perf_counter()
    runs: list[dict[str, Any]] = []
    matrix: dict[str, dict[str, float]] = {}

    total = len(MB_SCENARIOS) * len(INSTRUMENTATION_LEVELS)
    n = 0
    for bridge, scenario, _desc in MB_SCENARIOS:
        matrix[bridge] = {}
        for level in INSTRUMENTATION_LEVELS:
            ep = run_episode(
                bridge,  # type: ignore[arg-type]
                scenario,
                seed=seed,
                T=T,
                instrumentation=level,
                redteam_strategy=redteam_strategy,
                substrate=substrate,  # type: ignore[arg-type]
            )
            row = episode_to_dict(ep)
            runs.append(row)
            matrix[bridge][level] = 1.0 if row["outer"]["in_sim_correct"] else 0.0
            n += 1
            if n % progress_every == 0 or n == total:
                print(f"instrumentation_matrix: [{n}/{total}] bridge={bridge} level={level}")

    level_rates: dict[str, float] = {}
    for level in INSTRUMENTATION_LEVELS:
        subset = [r for r in runs if r["instrumentation"] == level]
        level_rates[level] = overall_correct_rate(subset)

    min_certifiable = min_certifiable_level(
        {
            level: {"cci_correct_rate_test_calib_scenarios": rate}
            for level, rate in level_rates.items()
            if level in HANDLE_INSTRUMENTATION_LEVELS
        },
        "cci_correct_rate_test_calib_scenarios",
    )

    return {
        "mode": "instrumentation_matrix",
        "seed": seed,
        "T": T,
        "substrate": substrate,
        "redteam_strategy": redteam_strategy,
        "certification_rate_threshold": CERTIFICATION_RATE_THRESHOLD,
        "runtime_seconds": round(time.perf_counter() - t0, 2),
        "bridge_level_correct": matrix,
        "correct_rate_by_level": level_rates,
        "minimum_certifiable_level": min_certifiable,
        "interpretation": CURVE_INTERPRETATION,
        **_summarize_episodes(runs),
        "runs": runs,
    }


def run_frozen_validation(
    *,
    seeds: list[int] | None = None,
    T: int = 800,
    instrumentation: InstrumentationLevel | None = None,
    all_levels: bool = True,
    substrate: str = "python",
    redteam_strategy: str = "none",
    bootstrap: bool = False,
    n_boot: int = 200,
) -> dict[str, Any]:
    t0 = time.perf_counter()
    seeds = list(seeds or FROZEN_VALIDATION_SEEDS)
    runs: list[dict[str, Any]] = []
    levels = list(INSTRUMENTATION_LEVELS) if all_levels else [instrumentation or "medium_handles"]

    scenarios = list(CALIBRATION_SCENARIOS) + list(HELD_OUT_SCENARIOS)
    total = len(levels) * len(scenarios) * len(seeds)
    done = 0

    for level in levels:
        for scenario in scenarios:
            for seed in seeds:
                runs.append(
                    _run_scenario_episode(
                        scenario,
                        seed,
                        T=T,
                        instrumentation=level,
                        redteam_strategy=redteam_strategy,
                        substrate=substrate,
                    )
                )
                done += 1
            print(
                f"frozen_validation [{done}/{total}] {level}/{scenario} "
                f"correct={overall_correct_rate([r for r in runs if r['instrumentation']==level and r['scenario']==scenario]):.2f}"
            )

    by_level = {
        level: summarize_runs(
            [r for r in runs if r["instrumentation"] == level],
            bootstrap=bootstrap,
            n_boot=n_boot,
        )
        for level in levels
    }
    capture_mild_by_level = {
        level: capture_mild_rate_by_level(runs, level) for level in levels
    }

    payload: dict[str, Any] = {
        "mode": "frozen_validation",
        **frozen_payload_header(T=T, validation_seeds=seeds),
        "instrumentation_levels": levels,
        "scenarios": scenarios,
        "substrate": substrate,
        "redteam_strategy": redteam_strategy,
        "bootstrap_enabled": bootstrap,
        "n_boot": n_boot if bootstrap else 0,
        "runtime_seconds": round(time.perf_counter() - t0, 2),
        "summary_by_level": by_level,
        "capture_mild_correct_rate_by_level": capture_mild_by_level,
        "overall_correct_rate_by_level": {
            level: overall_correct_rate([r for r in runs if r["instrumentation"] == level])
            for level in levels
        },
        **_summarize_episodes(runs),
        "runs": runs,
    }
    if not all_levels and instrumentation is not None:
        payload["instrumentation"] = instrumentation
    return payload


SWEEP_AXES: dict[str, list[int]] = {
    "T": [400, 800, 1200],
}


def run_parameter_sweep(
    *,
    bridges: tuple[str, ...] | None = None,
    seed: int = 42,
    instrumentation: InstrumentationLevel = "medium_handles",
    substrate: str = "python",
) -> dict[str, Any]:
    t0 = time.perf_counter()
    bridges = bridges or ("none", "MB5", "MB6", "MB7d", "instrument_capture")
    keys = list(SWEEP_AXES.keys())
    grid = list(itertools.product(*(SWEEP_AXES[k] for k in keys)))
    runs: list[dict[str, Any]] = []

    for combo in grid:
        params = dict(zip(keys, combo, strict=True))
        T = int(params["T"])
        for bridge in bridges:
            scenario = _bridge_scenario(bridge)
            ep = run_episode(
                bridge,  # type: ignore[arg-type]
                scenario,
                seed=seed,
                T=T,
                instrumentation=instrumentation,
                substrate=substrate,  # type: ignore[arg-type]
            )
            row = episode_to_dict(ep)
            row["sweep_params"] = params
            runs.append(row)
        print(f"sweep: T={T} done")

    return {
        "mode": "parameter_sweep",
        "axes": SWEEP_AXES,
        "bridges": list(bridges),
        "seed": seed,
        "instrumentation": instrumentation,
        "runtime_seconds": round(time.perf_counter() - t0, 2),
        **_summarize_episodes(runs),
        "runs": runs,
    }


def run_redteam_battery(
    *,
    bridges: list[str] | None = None,
    seeds: list[int] | None = None,
    T: int = 800,
    strategies: list[str] | None = None,
    instrumentation_levels: list[InstrumentationLevel] | None = None,
    substrate: str = "python",
    progress_every: int = 25,
) -> dict[str, Any]:
    """Phase-1-style battery over embedded pipeline (hand-written strategies)."""
    t0 = time.perf_counter()
    bridges = bridges or list(REDTEAM_BATTERY_BRIDGES)
    seeds = seeds or list(range(11, 21))
    strategies = strategies or list(BATTERY_STRATEGIES)
    levels = instrumentation_levels or list(BATTERY_LEVELS)

    total = len(bridges) * len(seeds) * len(strategies) * len(levels)
    runs: list[dict[str, Any]] = []
    false_pass_count = 0
    n = 0

    print(
        f"redteam_battery: starting {total} runs "
        f"(T={T}, {len(bridges)} bridges, {len(strategies)} strategies, {len(levels)} levels)"
    )

    for level in levels:
        for strategy in strategies:
            for bridge in bridges:
                scenario = _bridge_scenario(bridge)
                for seed in seeds:
                    ep = run_episode(
                        bridge,  # type: ignore[arg-type]
                        scenario,
                        seed=seed,
                        T=T,
                        instrumentation=level,
                        redteam_strategy=strategy,
                        substrate=substrate,  # type: ignore[arg-type]
                    )
                    row = episode_to_dict(ep)
                    runs.append(row)
                    if row["outer"]["false_pass"]:
                        false_pass_count += 1
                    n += 1
                    if n == 1 or n == total or n % progress_every == 0:
                        elapsed = time.perf_counter() - t0
                        print(
                            f"redteam_battery: [{n}/{total}] "
                            f"{level}/{strategy}/{bridge}/seed{seed} "
                            f"false_pass={false_pass_count} elapsed={elapsed:.0f}s"
                        )

    by_strategy: dict[str, dict[str, float]] = {}
    for strategy in strategies:
        subset = [r for r in runs if r["redteam_strategy"] == strategy]
        by_strategy[strategy] = {
            "n_runs": len(subset),
            "false_pass_rate": sum(1 for r in subset if r["outer"]["false_pass"])
            / max(len(subset), 1),
            "in_sim_correct_rate": sum(1 for r in subset if r["outer"]["in_sim_correct"])
            / max(len(subset), 1),
        }

    by_level: dict[str, dict[str, float]] = {}
    for level in levels:
        subset = [r for r in runs if r["instrumentation"] == level]
        by_level[level] = {
            "n_runs": len(subset),
            "false_pass_rate": sum(1 for r in subset if r["outer"]["false_pass"])
            / max(len(subset), 1),
            "in_sim_correct_rate": sum(1 for r in subset if r["outer"]["in_sim_correct"])
            / max(len(subset), 1),
        }

    elapsed = time.perf_counter() - t0
    print(
        f"redteam_battery: finished {total} runs in {elapsed:.1f}s, "
        f"false_passes={false_pass_count}"
    )

    crux = redteam_crux_metrics(runs)

    return {
        "mode": "redteam_battery",
        "claim_strength": "hand-written red-team on embedded pipeline; not frontier LLM evidence",
        "T": T,
        "bridges": bridges,
        "seeds": seeds,
        "strategy_names": strategies,
        "instrumentation_levels": levels,
        "substrate": substrate,
        "runtime_seconds": round(elapsed, 2),
        "n_runs": len(runs),
        "false_pass_count": false_pass_count,
        "false_pass_rate": false_pass_count / max(len(runs), 1),
        "crux_metrics": crux,
        "summary_by_strategy": by_strategy,
        "summary_by_instrumentation": by_level,
        "runs": runs,
    }


def run_main_report(
    *,
    seed: int = 42,
    T: int = 800,
    instrumentation: InstrumentationLevel = "medium_handles",
    redteam_strategy: str = "full_redteam",
    substrate: str = "python",
) -> dict[str, Any]:
    """All MB scenarios with chosen red-team (default full_redteam)."""
    t0 = time.perf_counter()
    runs: list[dict[str, Any]] = []
    for bridge, scenario, _desc in MB_SCENARIOS:
        ep = run_episode(
            bridge,  # type: ignore[arg-type]
            scenario,
            seed=seed,
            T=T,
            instrumentation=instrumentation,
            redteam_strategy=redteam_strategy,
            substrate=substrate,  # type: ignore[arg-type]
        )
        runs.append(episode_to_dict(ep))
    summary = _summarize_episodes(runs)
    return {
        "mode": "main_report",
        "seed": seed,
        "T": T,
        "instrumentation": instrumentation,
        "redteam_strategy": redteam_strategy,
        "substrate": substrate,
        "runtime_seconds": round(time.perf_counter() - t0, 2),
        **summary,
        "runs": runs,
    }
