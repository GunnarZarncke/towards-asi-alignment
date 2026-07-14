#!/usr/bin/env python3
"""Run embedded simulation batch: curve, frozen, sweep, battery, reports, LLM."""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from embedded_sim.progress import configure_progress_logging, progress, suite_phase  # noqa: E402
from embedded_sim.batch import (  # noqa: E402
    run_access_tier_curve,
    run_certification_capacity_curve,
    run_frozen_validation,
    run_instrumentation_curve,
    run_instrumentation_matrix,
    run_main_report,
    run_parameter_sweep,
    run_redteam_battery,
)
from embedded_sim.intervention_benchmark import (  # noqa: E402
    md_intervention_curve,
    run_intervention_curve,
)
from embedded_sim.handle_calibration import (  # noqa: E402
    fit_handle_calibration,
    get_handle_calibration,
    md_handle_calibration,
    save_handle_calibration,
)
from embedded_sim.intervention_config import set_intervention_level  # noqa: E402
from embedded_sim.js_isolate import summarize_isolate_runs  # noqa: E402
from embedded_sim.lab_ecology import LabEcologyConfig, set_lab_ecology  # noqa: E402
from embedded_sim.uad_config import UADMode, set_uad_mode, uad_artifact_suffix  # noqa: E402
from run import _write_report  # noqa: E402

RESULTS = ROOT / "results"
LOGS = ROOT / "logs"


def _write_json_md(payload: dict, stem: str, md_builder, *, suffix: str = "") -> tuple[Path, Path]:
    RESULTS.mkdir(parents=True, exist_ok=True)
    full_stem = f"{stem}{suffix}"
    json_path = RESULTS / f"{full_stem}.json"
    md_path = RESULTS / f"{full_stem}.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_path.write_text(md_builder(payload), encoding="utf-8")
    return json_path, md_path


def _md_curve(payload: dict) -> str:
    lines = [
        "# Embedded instrumentation curve",
        "",
        f"T={payload['T']} threshold={payload['certification_rate_threshold']}",
        f"Min certifiable (calib): **{payload['minimum_certifiable_level_calibration']}**",
        f"Min certifiable (full held-out): **{payload['minimum_certifiable_level_full_held_out']}**",
        "",
        "## By level",
        "",
        "| Level | calib | test | test (calib scenarios only) |",
        "| --- | --- | --- | --- |",
    ]
    for level, stats in payload["by_level"].items():
        lines.append(
            f"| {level} | {stats['cci_correct_rate_calibration']:.2%} | "
            f"{stats['cci_correct_rate_test']:.2%} | "
            f"{stats['cci_correct_rate_test_calib_scenarios']:.2%} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            f"- {payload['interpretation']['none_belowThreshold']}",
        ]
    )
    if note := payload.get("monotonicity_note"):
        lines.append(f"- ⚠ {note}")
    lines.extend(["", f"Runtime: {payload['runtime_seconds']}s"])
    return "\n".join(lines) + "\n"


def _md_matrix(payload: dict) -> str:
    lines = [
        "# Embedded instrumentation matrix",
        "",
        f"T={payload['T']} seed={payload['seed']} redteam={payload['redteam_strategy']}",
        f"Min certifiable level: **{payload['minimum_certifiable_level']}**",
        "",
        "## Correct rate by level",
        "",
    ]
    for level, rate in payload["correct_rate_by_level"].items():
        lines.append(f"- {level}: {rate:.2%}")
    lines.extend(["", "## Bridge × level", "", "| Bridge | " + " | ".join(payload["correct_rate_by_level"]) + " |", "| --- | " + " | ".join(["---"] * len(payload["correct_rate_by_level"])) + " |"])
    for bridge, levels in payload["bridge_level_correct"].items():
        cells = " | ".join("✓" if levels.get(l, 0) else "✗" for l in payload["correct_rate_by_level"])
        lines.append(f"| {bridge} | {cells} |")
    if note := payload.get("monotonicity_note"):
        lines.extend(["", f"⚠ {note}"])
    lines.extend(
        [
            "",
            f"Overall in_sim_correct: {payload['in_sim_correct_rate']:.2%}",
            f"Runtime: {payload['runtime_seconds']}s",
        ]
    )
    return "\n".join(lines) + "\n"


def _md_frozen(payload: dict) -> str:
    lines = [
        "# Embedded frozen validation",
        "",
        f"Seeds: {payload['validation_seeds']} T={payload['T']}",
        f"Levels: {payload.get('instrumentation_levels', payload.get('instrumentation'))}",
        "",
        "## Overall correct rate by level",
        "",
    ]
    for level, rate in payload.get("overall_correct_rate_by_level", {}).items():
        lines.append(f"- {level}: {rate:.2%}")
    if mild := payload.get("capture_mild_correct_rate_by_level"):
        lines.extend(["", "## capture_mild by level", ""])
        for level, rate in mild.items():
            lines.append(f"- {level}: {rate:.2%}")
    if note := payload.get("monotonicity_note"):
        lines.extend(["", f"⚠ {note}"])
    lines.append(f"\nOverall in-sim correct: {payload.get('in_sim_correct_rate', 0):.2%}")
    lines.append(f"Runtime: {payload['runtime_seconds']}s")
    return "\n".join(lines) + "\n"


def _md_sweep(payload: dict) -> str:
    lines = ["# Embedded parameter sweep", "", f"Axes: {payload['axes']}", ""]
    for run in payload["runs"]:
        p = run.get("sweep_params", {})
        lines.append(
            f"- T={p.get('T')} bridge={run['bridge']} "
            f"correct={run['outer']['in_sim_correct']} false_pass={run['outer']['false_pass']}"
        )
    lines.append(f"\nRuntime: {payload['runtime_seconds']}s")
    return "\n".join(lines) + "\n"


def _md_battery(payload: dict) -> str:
    lines = [
        "# Embedded red-team battery",
        "",
        f"T={payload['T']} runs={payload['n_runs']}",
        f"**Raw false-pass rate: {payload['false_pass_rate']:.2%}** "
        f"({payload['false_pass_count']}) — includes unattacked auditor error; "
        "see baseline-adjusted section below for attack-attributable rate",
        "",
        "## By strategy",
        "",
    ]
    for name, stats in payload["summary_by_strategy"].items():
        lines.append(
            f"- {name}: false_pass={stats['false_pass_rate']:.2%} "
            f"correct={stats['in_sim_correct_rate']:.2%} n={stats['n_runs']}"
        )
    lines.extend(["", "## By instrumentation", ""])
    for level, stats in payload["summary_by_instrumentation"].items():
        lines.append(
            f"- {level}: false_pass={stats['false_pass_rate']:.2%} "
            f"correct={stats['in_sim_correct_rate']:.2%} n={stats['n_runs']}"
        )
    if crux := payload.get("crux_metrics"):
        bd = crux["boundary_decouple"]
        lines.extend(
            [
                "",
                "## Crux metrics",
                "",
                f"- Pass attempt rate: {crux['pass_attempt_rate']:.2%}",
                f"- False pass (conditional on pass): {crux['false_pass_conditional_on_pass']:.2%}",
                f"- boundary_decouple false-pass: {bd['false_pass_rate']:.2%} "
                f"(conditional on pass: {bd['false_pass_conditional_on_pass']:.2%})",
            ]
        )
        if crux.get("capture_only_scenarios"):
            lines.append(f"- ⚠ {crux['capture_only_scenarios_note']}")
    if ba := payload.get("baseline_adjusted"):
        lines.extend(
            [
                "",
                "## Baseline-adjusted false-pass (honest attribution)",
                "",
                f"_{ba['note']}_",
                "",
            ]
        )
        for level, rate in ba["baseline_false_pass_rate_by_level"].items():
            lines.append(f"- baseline (`{ba['baseline_strategy']}`) @ {level}: {rate:.2%}")
        lines.append("")
        lines.append(
            f"**Attack-attributable false-pass rate (baseline-subtracted, overall): "
            f"{ba['attack_attributable_false_pass_rate_overall']:.2%}**"
        )
        lines.append("")
        for strategy, stats in sorted(
            ba["attack_attributable_by_strategy"].items(),
            key=lambda kv: kv[1]["attack_attributable_false_pass_rate"],
            reverse=True,
        ):
            lines.append(
                f"- {strategy}: attack-attributable="
                f"{stats['attack_attributable_false_pass_rate']:.2%}"
            )
    if matrix := payload.get("summary_by_strategy_handle"):
        lines.extend(["", "## Strategy × Handle Type", ""])
        for _key, stats in matrix.items():
            lines.append(
                f"- {stats['strategy']} @ {stats['target_handle_type']}: "
                f"false_pass={stats['false_pass_rate']:.2%} "
                f"pass_attempt={stats['pass_attempt_rate']:.2%} n={stats['n_runs']}"
            )
    lines.append(f"\nRuntime: {payload['runtime_seconds']}s")
    return "\n".join(lines) + "\n"


def _md_access_tier_curve(payload: dict) -> str:
    lines = [
        "# Embedded access-tier curve",
        "",
        f"T={payload['T']} redteam={payload['redteam_strategy']}",
        "",
        "| Tier | Instrumentation | Operation handles | UAD recall | False pass | CCI pass |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in payload["tiers"]:
        recall = row["uad_recall_mean"]
        recall_s = "n/a" if recall is None else f"{recall:.2%}"
        lines.append(
            f"| {row['access_tier']} | {row['instrumentation']} | "
            f"{len(row['operation_handles'])} | {recall_s} | "
            f"{row['false_pass_rate']:.2%} | {row['cci_pass_rate']:.2%} |"
        )
    if payload.get("capture_only_scenarios"):
        lines.extend(["", f"⚠ {payload['scenario_class_note']}"])
    lines.append(f"\nRuntime: {payload['runtime_seconds']}s")
    return "\n".join(lines) + "\n"


def _md_certification_capacity_curve(payload: dict) -> str:
    lines = [
        "# Embedded certification-capacity curve",
        "",
        f"Delta={payload['delta']} seeds={payload['seeds']}",
        "",
        "| Tier | Probe budget | CCI bits | Control | Max certifiable control | Numeric pass |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in payload["points"]:
        lines.append(
            f"| {row['access_tier']} | {row['probe_budget']} | "
            f"{row['cci_bits_mean']:.3f} | {row['control_mean']:.3f} | "
            f"{row['max_certifiable_control_mean']:.3f} | "
            f"{row['satisfies_numeric_leaf_rate']:.2%} |"
        )
    if note := payload.get("small_n_note"):
        lines.extend(["", f"⚠ {note}"])
    for plateau in payload.get("tier_plateau_notes") or []:
        lines.append(f"⚠ {plateau}")
    lines.append(f"\nRuntime: {payload['runtime_seconds']}s")
    return "\n".join(lines) + "\n"


def _md_llm(payload: dict) -> str:
    lines = [
        "# Embedded LLM red-team",
        "",
        f"Planner: {payload.get('planner')} T={payload.get('T')}",
        f"**False pass rate: {payload.get('llm_false_pass_rate', 0):.2%}**",
        f"In-sim correct: {payload.get('llm_mean_in_sim_correct', 0):.2%}",
    ]
    if note := payload.get("planner_note"):
        lines.append(f"⚠ {note}")
    lines.append("")
    lines.extend(
        [
            "| Bridge | Seed | False pass | Decision | CCI |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for run in payload.get("runs", []):
        lines.append(
            f"| {run['bridge']} | {run['seed']} | {run['false_pass']} | "
            f"{run['safety_decision']} | {run['cci_status']} |"
        )
    lines.append(f"\nRuntime: {payload.get('runtime_seconds')}s")
    return "\n".join(lines) + "\n"


def _uad_summary_from_runs(runs: list[dict]) -> dict:
    """UAD recall/precision over runs where the metric is *defined*.

    Recall/precision are None on episodes without a hidden-coalition target;
    averaging filler zeros over all bridges produced the misleading 3.8%
    headline (review finding 5). Report the defined subset plus per-bridge
    values.
    """
    defined = [r for r in runs if r.get("outer", {}).get("uad_recall") is not None]
    per_bridge: dict[str, dict[str, float]] = {}
    for r in defined:
        bridge = str(r.get("bridge", "?"))
        cell = per_bridge.setdefault(bridge, {"n": 0, "recall_sum": 0.0, "precision_sum": 0.0})
        cell["n"] += 1
        cell["recall_sum"] += float(r["outer"]["uad_recall"])
        cell["precision_sum"] += float(r["outer"].get("uad_precision") or 0.0)
    return {
        "n_uad_defined": len(defined),
        "n_runs_total": len(runs),
        "mean_uad_recall": (
            sum(float(r["outer"]["uad_recall"]) for r in defined) / len(defined)
            if defined
            else None
        ),
        "mean_uad_precision": (
            sum(float(r["outer"].get("uad_precision") or 0.0) for r in defined) / len(defined)
            if defined
            else None
        ),
        "uad_by_bridge": {
            bridge: {
                "n": int(cell["n"]),
                "mean_recall": cell["recall_sum"] / cell["n"],
                "mean_precision": cell["precision_sum"] / cell["n"],
            }
            for bridge, cell in sorted(per_bridge.items())
        },
        "mi_primary_count": sum(
            1
            for r in runs
            if "unit.mi." in str(r.get("in_sim", {}).get("unit_id") or "")
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Embedded simulation batch runner")
    parser.add_argument("--T", type=int, default=800)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--substrate", default="python", choices=("python", "js"))
    parser.add_argument("--instrumentation", default="medium_handles")
    parser.add_argument("--smoke", action="store_true", help="Short runs for CI")
    parser.add_argument("--all", action="store_true", help="Run full parity suite")
    parser.add_argument("--instrumentation-matrix", action="store_true")
    parser.add_argument("--curve", action="store_true", help="Toy-parity instrumentation curve")
    parser.add_argument("--access-tier-curve", action="store_true", help="Milestone v4 access-tier curve")
    parser.add_argument("--certification-curve", action="store_true", help="Milestone v4 certification-capacity curve")
    parser.add_argument("--frozen", action="store_true")
    parser.add_argument("--full-frozen", action="store_true", help="All levels × all scenarios (slow)")
    parser.add_argument("--sweep", action="store_true")
    parser.add_argument("--battery", action="store_true")
    parser.add_argument("--report", action="store_true", help="Main MB report with full_redteam")
    parser.add_argument("--llm", action="store_true", help="Run LLM red-team (mock unless --llm-live)")
    parser.add_argument("--llm-live", action="store_true", help="Use OpenAI API for LLM red-team")
    parser.add_argument("--llm-model", default="gpt-4o-mini")
    parser.add_argument(
        "--uad-mode",
        choices=("full", "fake"),
        default="full",
        help="full=agency-detect MI UAD; fake=heuristic-only (no uad_core clustering)",
    )
    parser.add_argument(
        "--uad-compare",
        action="store_true",
        help="Run suite twice (full + fake UAD) and write embedded_uad_compare.md",
    )
    parser.add_argument("--n-adversarial-candidates", type=int, default=0)
    parser.add_argument("--common-legitimate-lab-agents", action="store_true")
    parser.add_argument("--auditor-agent", action="store_true")
    parser.add_argument("--alignment-target-agent", action="store_true")
    parser.add_argument("--n-decoys", type=int, default=0)
    parser.add_argument(
        "--coactive-offender",
        action="store_true",
        help="Overlay a benign co-actor at every offending step (defeats window scoping)",
    )
    parser.add_argument(
        "--intervention-level",
        choices=("pipeline", "window", "actor"),
        default="window",
        help="Auditor intervention granularity (action-side handle strength)",
    )
    parser.add_argument(
        "--intervention-curve",
        action="store_true",
        help="Sweep intervention levels × UAD modes; write embedded_intervention_curve.*",
    )
    parser.add_argument(
        "--calibrate-handles",
        action="store_true",
        help="Fit UAD coordination + scoped blind-auditor policy; write handle_calibration.*",
    )
    args = parser.parse_args()

    ecology = LabEcologyConfig(
        n_adversarial_candidates=args.n_adversarial_candidates,
        common_legitimate_lab_agents=args.common_legitimate_lab_agents,
        auditor_agent=args.auditor_agent,
        alignment_target_agent=args.alignment_target_agent,
        n_decoys=args.n_decoys,
        coactive_offender=args.coactive_offender,
    )
    set_lab_ecology(ecology)
    set_intervention_level(args.intervention_level)

    if args.calibrate_handles:
        calib_seeds = (101, 102, 103) if args.smoke else tuple(range(101, 111))
        T = 400 if args.smoke else args.T
        print(f"Calibrating handle policy on seeds {list(calib_seeds)} T={T} ...")
        cal = fit_handle_calibration(seeds=calib_seeds, T=T)
        json_path = save_handle_calibration(cal)
        md_path = json_path.with_suffix(".md")
        md_path.write_text(md_handle_calibration(cal), encoding="utf-8")
        print(f"Wrote {json_path}\nWrote {md_path}")
        print(
            f"  coord_ref={cal.uad.coord_ref:.4f} "
            f"coord_strong_min={cal.uad.coord_strong_min:.4f} "
            f"coord_weight={cal.uad.coord_weight:.1f}"
        )
        print(
            f"  blind_retained_max={cal.scope.blind_retained_max} "
            f"blind_pass_status={cal.scope.blind_pass_status}"
        )
        return

    if args.intervention_curve:
        get_handle_calibration()
        seeds = [11] if args.smoke else [11, 12, 13]
        T = 400 if args.smoke else args.T
        payload = run_intervention_curve(
            seeds=seeds,
            T=T,
            instrumentation=args.instrumentation,
            coactive=True,
        )
        j, m = _write_json_md(payload, "embedded_intervention_curve", md_intervention_curve)
        print(f"Wrote {j}\nWrote {m}")
        for level in payload["levels"]:
            sep = payload["by_level"][level]["false_pass_separation"]
            print(f"  {level}: fake−full false-pass separation = {sep:+.1%}")
        return

    if args.smoke:
        args.T = 400
        args.all = True

    if args.all:
        args.curve = True
        args.instrumentation_matrix = True
        args.frozen = True
        args.sweep = True
        args.battery = True
        args.access_tier_curve = True
        args.certification_curve = True
        args.report = True
        args.llm = True

    if not any(
        (
            args.instrumentation_matrix,
            args.curve,
            args.access_tier_curve,
            args.certification_curve,
            args.frozen,
            args.sweep,
            args.battery,
            args.report,
            args.llm,
        )
    ):
        args.report = True

    LOGS.mkdir(parents=True, exist_ok=True)
    configure_progress_logging(LOGS)
    stamp = datetime.now(timezone.utc).isoformat()
    progress(
        f"run_suite start stamp={stamp} T={args.T} substrate={args.substrate} "
        f"uad_mode={args.uad_mode} smoke={args.smoke} full_frozen={args.full_frozen}"
    )

    if args.uad_compare:
        all_metrics: dict[str, dict] = {}
        for mode in ("full", "fake"):
            progress(f"=== UAD mode: {mode} ===")
            set_uad_mode(mode)  # type: ignore[arg-type]
            suffix = uad_artifact_suffix(mode)  # type: ignore[arg-type]
            artifacts, metrics = _execute_suite(args, stamp, artifact_suffix=suffix, uad_mode=mode)
            all_metrics[mode] = metrics
            summary_name = "OVERALL_SUMMARY.md" if mode == "full" else f"OVERALL_SUMMARY{suffix}.md"
            summary_path = RESULTS / summary_name
            summary_path.write_text(
                _build_overall_summary(artifacts, stamp, args, metrics, uad_mode=mode),
                encoding="utf-8",
            )
            progress(f"wrote {summary_path}")
        compare_path = RESULTS / "embedded_uad_compare.md"
        compare_path.write_text(_build_uad_compare(stamp, args, all_metrics), encoding="utf-8")
        progress(f"wrote {compare_path}")
        return

    set_uad_mode(args.uad_mode)  # type: ignore[arg-type]
    suffix = uad_artifact_suffix(args.uad_mode)  # type: ignore[arg-type]
    artifacts, metrics = _execute_suite(args, stamp, artifact_suffix=suffix, uad_mode=args.uad_mode)
    summary_name = "OVERALL_SUMMARY.md" if args.uad_mode == "full" else f"OVERALL_SUMMARY{suffix}.md"
    summary_path = RESULTS / summary_name
    summary_path.write_text(
        _build_overall_summary(artifacts, stamp, args, metrics, uad_mode=args.uad_mode),
        encoding="utf-8",
    )
    progress(f"wrote {summary_path}")
    progress("artifacts:\n  " + "\n  ".join(artifacts))


def _execute_suite(
    args,
    stamp: str,
    *,
    artifact_suffix: str,
    uad_mode: str,
) -> tuple[list[str], dict[str, dict]]:
    artifacts: list[str] = []
    metrics: dict[str, dict] = {}
    planned = [
        name
        for flag, name in (
            (args.curve, "instrumentation_curve"),
            (args.access_tier_curve, "access_tier_curve"),
            (args.certification_curve, "certification_capacity_curve"),
            (args.instrumentation_matrix, "instrumentation_matrix"),
            (args.frozen, "frozen_validation"),
            (args.sweep, "parameter_sweep"),
            (args.battery, "redteam_battery"),
            (args.report, "main_report"),
            (args.llm, "llm_redteam"),
        )
        if flag
    ]
    progress(f"suite plan ({len(planned)} stages): {', '.join(planned)}")

    if args.curve:
        with suite_phase("instrumentation_curve"):
            calib = [1] if args.smoke else list(range(1, 9))
            test = [11] if args.smoke else list(range(11, 21))
            payload = run_instrumentation_curve(
                calibration_seeds=calib,
                test_seeds=test,
                T=args.T,
                substrate=args.substrate,
                bootstrap=not args.smoke,
                n_boot=50 if args.smoke else 200,
            )
        payload["uad_mode"] = uad_mode
        metrics["instrumentation_curve"] = {
            "min_certifiable": payload["minimum_certifiable_level"],
            "min_certifiable_full": payload["minimum_certifiable_level_full_held_out"],
            "runtime_seconds": payload["runtime_seconds"],
            "monotonicity_note": payload.get("monotonicity_note"),
        }
        j, m = _write_json_md(
            payload, "embedded_instrumentation_curve", _md_curve, suffix=artifact_suffix
        )
        artifacts.extend([str(j), str(m)])
        progress(
            f"wrote {j.name} min_certifiable={payload['minimum_certifiable_level']} "
            f"full={payload['minimum_certifiable_level_full_held_out']}"
        )

    if args.access_tier_curve:
        with suite_phase("access_tier_curve"):
            seeds = [11] if args.smoke else [11, 12, 13]
            payload = run_access_tier_curve(
                seeds=seeds,
                T=args.T,
                substrate=args.substrate,
                redteam_strategy="full_redteam",
            )
        payload["uad_mode"] = uad_mode
        metrics["access_tier_curve"] = {
            "runtime_seconds": payload["runtime_seconds"],
            "tiers": payload["tiers"],
            "capture_only_scenarios": payload.get("capture_only_scenarios"),
            "scenario_class_note": payload.get("scenario_class_note"),
        }
        j, m = _write_json_md(
            payload, "embedded_access_tier_curve", _md_access_tier_curve, suffix=artifact_suffix
        )
        artifacts.extend([str(j), str(m)])
        progress(f"wrote {j.name}")

    if args.certification_curve:
        with suite_phase("certification_capacity_curve"):
            seeds = [11] if args.smoke else [11, 12]
            payload = run_certification_capacity_curve(
                seeds=seeds,
                substrate=args.substrate,
            )
        payload["uad_mode"] = uad_mode
        metrics["certification_capacity_curve"] = {
            "runtime_seconds": payload["runtime_seconds"],
            "points": payload["points"],
            "tier_plateau_notes": payload.get("tier_plateau_notes") or [],
            "small_n_note": payload.get("small_n_note"),
        }
        j, m = _write_json_md(
            payload,
            "embedded_certification_capacity_curve",
            _md_certification_capacity_curve,
            suffix=artifact_suffix,
        )
        artifacts.extend([str(j), str(m)])
        progress(f"wrote {j.name}")

    if args.instrumentation_matrix:
        with suite_phase("instrumentation_matrix"):
            payload = run_instrumentation_matrix(seed=args.seed, T=args.T, substrate=args.substrate)
        payload["uad_mode"] = uad_mode
        metrics["instrumentation_matrix"] = {
            "min_certifiable": payload["minimum_certifiable_level"],
            "in_sim_correct_rate": payload["in_sim_correct_rate"],
            "runtime_seconds": payload["runtime_seconds"],
            "monotonicity_note": payload.get("monotonicity_note"),
        }
        j, m = _write_json_md(
            payload, "embedded_instrumentation_matrix", _md_matrix, suffix=artifact_suffix
        )
        artifacts.extend([str(j), str(m)])
        progress(
            f"wrote {j.name} min_certifiable={payload['minimum_certifiable_level']}"
        )

    if args.frozen:
        with suite_phase("frozen_validation"):
            seeds = [21, 22] if args.smoke else list(range(21, 31))
            payload = run_frozen_validation(
                seeds=seeds,
                T=args.T,
                instrumentation=args.instrumentation,  # type: ignore[arg-type]
                all_levels=args.full_frozen,
                substrate=args.substrate,
                bootstrap=not args.smoke,
                n_boot=50 if args.smoke else 200,
            )
        payload["uad_mode"] = uad_mode
        metrics["frozen_validation"] = {
            "seeds": seeds,
            "in_sim_correct_rate": payload["in_sim_correct_rate"],
            "runtime_seconds": payload["runtime_seconds"],
            "all_levels": args.full_frozen,
            "monotonicity_note": payload.get("monotonicity_note"),
        }
        j, m = _write_json_md(
            payload, "embedded_frozen_validation", _md_frozen, suffix=artifact_suffix
        )
        artifacts.extend([str(j), str(m)])
        progress(f"wrote {j.name}")

    if args.sweep:
        with suite_phase("parameter_sweep"):
            payload = run_parameter_sweep(
                seed=args.seed, instrumentation=args.instrumentation, substrate=args.substrate
            )
        payload["uad_mode"] = uad_mode
        metrics["parameter_sweep"] = {
            "n_runs": payload["n_runs"],
            "false_pass_rate": payload["false_pass_rate"],
            "runtime_seconds": payload["runtime_seconds"],
        }
        j, m = _write_json_md(
            payload, "embedded_parameter_sweep", _md_sweep, suffix=artifact_suffix
        )
        artifacts.extend([str(j), str(m)])
        progress(f"wrote {j.name}")

    if args.battery:
        with suite_phase("redteam_battery"):
            seeds = [11] if args.smoke else list(range(11, 21))
            bridges = ["MB4", "MB1", "MB9"] if args.smoke else None
            strategies = ["none", "full_redteam"] if args.smoke else None
            levels = ["medium_handles"] if args.smoke else None
            payload = run_redteam_battery(
                bridges=bridges,
                seeds=seeds,
                T=args.T,
                strategies=strategies,
                instrumentation_levels=levels,
                substrate=args.substrate,
            )
        payload["uad_mode"] = uad_mode
        uad_summary = _uad_summary_from_runs(payload["runs"])
        metrics["redteam_battery"] = {
            "false_pass_rate": payload["false_pass_rate"],
            "false_pass_count": payload["false_pass_count"],
            "in_sim_correct_rate": sum(
                1 for r in payload["runs"] if r.get("outer", {}).get("in_sim_correct")
            )
            / max(payload["n_runs"], 1),
            "n_runs": payload["n_runs"],
            "runtime_seconds": payload["runtime_seconds"],
            "by_strategy": payload["summary_by_strategy"],
            "baseline_adjusted": payload.get("baseline_adjusted"),
            "capture_only_scenarios": payload.get("crux_metrics", {}).get(
                "capture_only_scenarios"
            ),
            **uad_summary,
        }
        j, m = _write_json_md(
            payload, "embedded_redteam_battery", _md_battery, suffix=artifact_suffix
        )
        artifacts.extend([str(j), str(m)])
        progress(
            f"wrote {j.name} false_pass_rate={payload['false_pass_rate']:.1%} "
            f"n_runs={payload['n_runs']}"
        )

    if args.report:
        from embedded_sim.pipeline import run_all_mbs

        with suite_phase("main_report"):
            t_report = time.perf_counter()
            results = run_all_mbs(
                seed=args.seed,
                T=args.T,
                instrumentation=args.instrumentation,  # type: ignore[arg-type]
                redteam_strategy="full_redteam",
                substrate=args.substrate,  # type: ignore[arg-type]
            )
            wall = time.perf_counter() - t_report
        report_json = RESULTS / f"embedded_sim_report{artifact_suffix}.json"
        report_md = RESULTS / f"embedded_sim_report{artifact_suffix}.md"
        _write_report(
            results,
            report_json,
            report_md,
            wall_seconds=wall,
        )
        result_rows = [
            {
                "bridge": r.bridge,
                "in_sim": {
                    "unit_id": r.in_sim.unit.candidate_id if r.in_sim.unit else None,
                },
                "outer": {
                    "uad_recall": r.outer.uad_recall,
                    "uad_precision": r.outer.uad_precision,
                },
            }
            for r in results
        ]
        uad_summary = _uad_summary_from_runs(result_rows)
        artifacts.extend([str(report_json), str(report_md)])
        metrics["main_report"] = {
            "false_pass_count": sum(1 for r in results if r.outer.false_pass),
            "n_episodes": len(results),
            "runtime_seconds": round(wall, 2),
            **uad_summary,
        }
        progress(f"wrote {report_json.name} false_pass={metrics['main_report']['false_pass_count']}")

    if args.llm:
        from embedded_llm.llm_runner import run_llm_suite

        bridges = ["MB4", "MB9"] if args.smoke else None
        seeds = [11] if args.smoke else [11, 12, 13]
        with suite_phase("llm_redteam"):
            payload = run_llm_suite(
                bridges=bridges,
                seeds=seeds,
                T=args.T,
                instrumentation=args.instrumentation,  # type: ignore[arg-type]
                use_mock=not args.llm_live,
                model=args.llm_model,
            )
        metrics["llm_redteam"] = {
            "planner": payload["planner"],
            "false_pass_rate": payload["llm_false_pass_rate"],
            "in_sim_correct_rate": payload["llm_mean_in_sim_correct"],
            "runtime_seconds": payload["runtime_seconds"],
            "live": args.llm_live,
            "planner_note": payload.get("planner_note"),
        }
        suffix = "live" if args.llm_live else "mock"
        j, m = _write_json_md(
            payload,
            f"embedded_llm_redteam_{suffix}",
            _md_llm,
            suffix=artifact_suffix,
        )
        artifacts.extend([str(j), str(m)])
        progress(f"wrote {j.name} llm_false_pass_rate={payload['llm_false_pass_rate']:.1%}")

    return artifacts, metrics


def _uad_headline(m: dict) -> str:
    """UAD recall/precision headline restricted to coalition-target episodes."""
    recall = m.get("mean_uad_recall")
    if recall is None:
        return "UAD recall undefined (no coalition-target episodes)"
    return (
        f"UAD recall {recall:.1%}, precision {m.get('mean_uad_precision') or 0.0:.1%} "
        f"over {m.get('n_uad_defined', 0)}/{m.get('n_runs_total', m.get('n_episodes', 0))} "
        "coalition-target episodes"
    )


def _build_uad_compare(stamp: str, args, all_metrics: dict[str, dict]) -> str:
    lines = [
        "# Embedded UAD comparison — full vs fake",
        "",
        f"Generated: {stamp}",
        "",
        f"T={args.T} seed={args.seed} substrate={args.substrate}",
        "",
        "| Metric | Full UAD (MI) | Fake UAD (heuristic) |",
        "| --- | --- | --- |",
    ]

    def _cell(mode: str, key: str, subkey: str, *, pct: bool = False) -> str:
        m = all_metrics.get(mode, {}).get(key, {})
        val = m.get(subkey)
        if val is None:
            return "—"
        if pct:
            return f"{val:.1%}"
        if isinstance(val, float):
            return f"{val:.2f}"
        return str(val)

    rows = [
        ("Red-team battery false-pass", "redteam_battery", "false_pass_rate", True),
        ("Red-team battery in-sim correct", "redteam_battery", "in_sim_correct_rate", True),
        ("Red-team battery UAD recall (coalition targets only)", "redteam_battery", "mean_uad_recall", True),
        ("Red-team battery UAD precision (coalition targets only)", "redteam_battery", "mean_uad_precision", True),
        ("Red-team battery coalition-target runs", "redteam_battery", "n_uad_defined", False),
        ("Main report false passes", "main_report", "false_pass_count", False),
        ("Main report MI-primary units", "main_report", "mi_primary_count", False),
        ("Main report UAD recall (coalition targets only)", "main_report", "mean_uad_recall", True),
        ("Main report UAD precision (coalition targets only)", "main_report", "mean_uad_precision", True),
        ("Main report coalition-target episodes", "main_report", "n_uad_defined", False),
        ("Instrumentation matrix correct", "instrumentation_matrix", "in_sim_correct_rate", True),
        ("Frozen validation correct", "frozen_validation", "in_sim_correct_rate", True),
        ("Parameter sweep false-pass", "parameter_sweep", "false_pass_rate", True),
    ]
    for label, key, subkey, pct in rows:
        lines.append(
            f"| {label} | {_cell('full', key, subkey, pct=pct)} | {_cell('fake', key, subkey, pct=pct)} |"
        )

    lines.extend(
        [
            "",
            "## Artifacts",
            "",
            "- Full: default `embedded_*` names",
            "- Fake: `embedded_*_fake_uad.*` and `OVERALL_SUMMARY_fake_uad.md`",
            "",
        ]
    )
    return "\n".join(lines)


def _build_overall_summary(
    artifacts: list[str],
    stamp: str,
    args,
    metrics: dict,
    *,
    uad_mode: str = "full",
) -> str:
    lines = [
        "# Embedded simulation — overall summary",
        "",
        f"Generated: {stamp}",
        "",
        "## Claim strength",
        "",
        "Controlled falsification harness for the embedded audit pipeline (VFS + UAD + scoped CCI + outer eval). "
        "Not frontier-system evidence. Hand-written and LLM red-team agents patch deployment-visible logs only.",
        "",
        "## Run configuration",
        "",
        f"- T={args.T} seed={args.seed} substrate={args.substrate} instrumentation={args.instrumentation}",
        f"- uad_mode={uad_mode} smoke={args.smoke} llm_live={args.llm_live}",
        (
            "- lab_ecology="
            f"adv_candidates={args.n_adversarial_candidates}, "
            f"common_legit={args.common_legitimate_lab_agents}, "
            f"auditor={args.auditor_agent}, "
            f"alignment_target={args.alignment_target_agent}, "
            f"decoys={args.n_decoys}"
        ),
        "",
        "## Artifacts",
        "",
    ]
    for path in artifacts:
        lines.append(f"- `{Path(path).name}`")

    if metrics:
        lines.extend(["", "## Key results", ""])
        if m := metrics.get("instrumentation_curve"):
            lines.append(
                f"- **Instrumentation curve:** min certifiable `{m['min_certifiable']}` "
                f"(full held-out `{m['min_certifiable_full']}`); {m['runtime_seconds']}s"
            )
            if note := m.get("monotonicity_note"):
                lines.append(f"  - ⚠ {note}")
        if m := metrics.get("instrumentation_matrix"):
            lines.append(
                f"- **Instrumentation matrix:** min certifiable `{m['min_certifiable']}`; "
                f"in-sim correct {m['in_sim_correct_rate']:.1%} ({m['runtime_seconds']}s)"
            )
            if note := m.get("monotonicity_note"):
                lines.append(f"  - ⚠ {note}")
        if m := metrics.get("frozen_validation"):
            lines.append(
                f"- **Frozen validation** (seeds {m['seeds']}): "
                f"in-sim correct {m['in_sim_correct_rate']:.1%} ({m['runtime_seconds']}s)"
            )
            if note := m.get("monotonicity_note"):
                lines.append(f"  - ⚠ {note}")
        if m := metrics.get("parameter_sweep"):
            lines.append(
                f"- **Parameter sweep:** {m['n_runs']} runs; false-pass {m['false_pass_rate']:.1%}"
            )
        if m := metrics.get("redteam_battery"):
            lines.append(
                f"- **Red-team battery:** raw false-pass {m['false_pass_rate']:.1%} "
                f"({m['false_pass_count']}/{m['n_runs']}) in {m['runtime_seconds']}s"
            )
            if ba := m.get("baseline_adjusted"):
                base_str = ", ".join(
                    f"{lvl} {rate:.1%}"
                    for lvl, rate in ba["baseline_false_pass_rate_by_level"].items()
                )
                lines.append(
                    f"  - Unattacked-auditor baseline (`{ba['baseline_strategy']}`) "
                    f"false-pass by level: {base_str}"
                )
                lines.append(
                    "  - **Attack-attributable false-pass (baseline-subtracted): "
                    f"{ba['attack_attributable_false_pass_rate_overall']:.1%}**"
                )
                worst = max(
                    ba["attack_attributable_by_strategy"].items(),
                    key=lambda x: x[1]["attack_attributable_false_pass_rate"],
                )
                lines.append(
                    f"  - Worst attack-attributable strategy: `{worst[0]}` at "
                    f"{worst[1]['attack_attributable_false_pass_rate']:.1%}"
                )
            else:
                worst = max(m["by_strategy"].items(), key=lambda x: x[1]["false_pass_rate"])
                lines.append(
                    f"  - Worst strategy: `{worst[0]}` at {worst[1]['false_pass_rate']:.1%} false-pass"
                )
            if m.get("capture_only_scenarios"):
                lines.append(
                    "  - ⚠ battery bridges are all violation/capture scenarios; "
                    "false-pass-conditional-on-pass is structurally near 100% "
                    "and not independently informative (see NEGATIVE_RESULTS.md ES-11)"
                )
        if m := metrics.get("access_tier_curve"):
            lines.append(f"- **Access-tier curve:** {m['runtime_seconds']}s")
            if m.get("capture_only_scenarios"):
                lines.append(f"  - ⚠ {m['scenario_class_note']}")
        if m := metrics.get("certification_capacity_curve"):
            lines.append(f"- **Certification-capacity curve:** {m['runtime_seconds']}s")
            if note := m.get("small_n_note"):
                lines.append(f"  - ⚠ {note}")
            for plateau in m.get("tier_plateau_notes") or []:
                lines.append(f"  - ⚠ {plateau}")
        if m := metrics.get("main_report"):
            lines.append(
                f"- **Main report** (full_redteam, {m['n_episodes']} episodes): "
                f"{m['false_pass_count']}/{m['n_episodes']} false passes; "
                + _uad_headline(m)
            )
            for bridge, cell in (m.get("uad_by_bridge") or {}).items():
                lines.append(
                    f"  - UAD {bridge}: recall {cell['mean_recall']:.1%}, "
                    f"precision {cell['mean_precision']:.1%} (n={cell['n']})"
                )
        if m := metrics.get("llm_redteam"):
            mode = "live API" if m["live"] else "mock"
            lines.append(
                f"- **LLM red-team** ({mode}, `{m['planner']}`): false-pass "
                f"{m['false_pass_rate']:.1%}; in-sim correct {m['in_sim_correct_rate']:.1%}"
            )
            if note := m.get("planner_note"):
                lines.append(f"  - ⚠ {note}")

    lines.extend(
        [
            "",
            "## Parity with toy-simulation",
            "",
            "| Toy-sim artifact | Embedded artifact |",
            "| --- | --- |",
            "| instrumentation curve | `embedded_instrumentation_curve.*` |",
            "| instrumentation matrix (single seed) | `embedded_instrumentation_matrix.*` |",
            "| frozen validation | `embedded_frozen_validation.*` |",
            "| parameter sweep | `embedded_parameter_sweep.*` |",
            "| llm_redteam_battery | `embedded_redteam_battery.*` |",
            "| llm episodic | `embedded_llm_redteam_*.`* |",
            "| main report | `embedded_sim_report.*` |",
            "",
            "## Open decisions (postponed)",
            "",
            "- MB5 gate always rejects default degraded successor referent transport.",
            "- Unit-scoped CCI vs global signals for MB7d inferential coupling.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    main()
