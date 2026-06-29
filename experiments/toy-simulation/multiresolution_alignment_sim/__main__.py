#!/usr/bin/env python3
"""Multi-resolution correction-capture simulation (v1).

Controlled sequential simulation with micro ground truth, audit-only
measurement, classical MI/CMI boundary detection, and vector CCI capture audit.

Scope: MB4 correction legitimacy/capture under blind audit. Not frontier evidence.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from .pipeline import (
    run_calibrated_suite,
    run_frozen_validation,
    run_instrumentation_compare,
    run_instrumentation_curve,
    run_parameter_sweep,
    run_slice,
    run_suite,
)
from .resources import ResourceGovernor
from .calibration import FROZEN_VALIDATION_SEEDS
from .schemas import ALL_SCENARIOS, CALIBRATION_SCENARIOS, ScenarioName

ROOT = Path(__file__).resolve().parent.parent
RESULT_DIR = ROOT / "results"
LOG_DIR = ROOT / "logs"

HONEST_CCI_DIAGNOSIS = """
## Why behavioral CCI is low even in honest mode

Behavioral CCI measures **I(correction; future_action | sensor, internal)** — not
whether corrections are *reported* as accepted. In honest runs we still observe
low behavioral bits (~0.05–0.12) because:

1. **Conditioning absorbs signal**: sensor and internal already predict action via
   task optimization; correction adds little *incremental* information at lag k=3.
2. **Sparse correction episodes** (~8–12% of steps): most timesteps have corr=0,
   so the marginal entropy of correction is low and episode-conditioned MI is noisy.
3. **Coarse 4-bin quantiles**: EMA-smoothed continuous traces are binned; temporal
   coupling at k=3 is partially lost.
4. **Honest ≠ perfectly obedient**: task_drive competes with correction uptake;
   action_cause is often `task_optimization` even when corr>0.
5. **Naive CCI uses reporting**: I(correction; reported_acceptance) stays high in
   honest mode because reporting tracks uptake — hence the naive–behavioral gap is
   *not* by itself evidence of capture.

Use **capture theater** (high reported acceptance + low behavioral uptake + high
manipulation on episodes) to interpret gaps, not honest-mode absolute behavioral CCI.
"""


def write_markdown(payload: dict[str, object], path: Path) -> None:
    lines = [
        "# Multiresolution alignment simulation (v1)",
        "",
        "Controlled sanity-check artifact. Not evidence about frontier systems.",
        "",
    ]
    if "calibration" in payload:
        lines.extend(
            [
                f"- Horizon `T`: {payload.get('T')}",
                f"- Calibration seeds: {payload.get('calibration_seeds')}",
                f"- Test seeds: {payload.get('test_seeds')}",
                f"- Calibration scenarios: {payload.get('calibration_scenarios')}",
                f"- Held-out scenarios: {payload.get('held_out_scenarios')}",
                f"- Fitted thresholds: {payload.get('calibration')}",
                "",
                "## Summary — calibration split",
                "",
            ]
        )
        for scen, stats in payload.get("summary_calibration", {}).items():
            lines.append(f"### {scen}")
            for key, val in stats.items():
                if isinstance(val, float):
                    lines.append(f"- {key}: {val:.4f}")
                else:
                    lines.append(f"- {key}: {val}")
            lines.append("")
        lines.append("## Summary — test split (held-out scenarios + test seeds)")
        lines.append("")
        for scen, stats in payload.get("summary_test", {}).items():
            lines.append(f"### {scen}")
            for key, val in stats.items():
                if isinstance(val, float):
                    lines.append(f"- {key}: {val:.4f}")
                else:
                    lines.append(f"- {key}: {val}")
            lines.append("")
        lines.append(HONEST_CCI_DIAGNOSIS.strip())
        lines.append("")
        return path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    lines.extend(
        [
            f"- Horizon `T`: {payload.get('T')}",
            f"- Seeds: {payload.get('seeds')}",
            f"- Scenarios: {payload.get('scenarios')}",
            f"- Detector: {payload.get('detector')}",
            "",
            "## Summary by scenario",
            "",
        ]
    )
    summary = payload.get("summary_by_scenario", {})
    for scen, stats in summary.items():
        lines.append(f"### {scen}")
        for key, val in stats.items():
            if isinstance(val, float):
                lines.append(f"- {key}: {val:.4f}")
            else:
                lines.append(f"- {key}: {val}")
        lines.append("")

    lines.append(HONEST_CCI_DIAGNOSIS.strip())
    lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_instrumentation_markdown(payload: dict[str, object], path: Path) -> None:
    lines = [
        "# Instrumentation cost comparison — multiresolution alignment sim",
        "",
        "Compares passive tracing (`none`) vs light handle instrumentation (`light_handles`).",
        "",
        f"- Horizon `T`: {payload.get('T')}",
        f"- Seeds: {payload.get('seeds')}",
        f"- Scenarios: {payload.get('scenarios')}",
        "",
        "## Delta (light_handles − none) by scenario",
        "",
        "| scenario | Δ behavioral CCI | interventional CCI | Δ manipulation | Δ gap | Δ cci correct | Δ bandwidth | handles |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for scen, stats in payload.get("delta_light_minus_none", {}).items():
        lines.append(
            f"| {scen} | {stats['mean_delta_behavioral_cci']:.3f} | "
            f"{stats['mean_interventional_cci']:.3f} | {stats['mean_delta_manipulation']:.3f} | "
            f"{stats['mean_delta_capture_gap']:.3f} | {stats['mean_cci_correct_improvement']:.2f} | "
            f"{stats['mean_trace_bandwidth_delta']:.0f} | {int(stats['n_handle_channels'])} |"
        )
    lines.extend(["", "## Summary — none", ""])
    for scen, stats in payload.get("summary_none", {}).items():
        lines.append(f"### {scen}")
        lines.append(f"- cci_correct: {stats['cci_status_correct_rate']:.2f}")
        lines.append(f"- behavioral_cci: {stats['mean_behavioral_cci']:.3f}")
        lines.append(f"- capture_gap: {stats['mean_capture_gap']:.3f}")
        lines.append(f"- manipulation (via gap proxy): see per-run")
        lines.append("")
    lines.extend(["## Summary — light_handles", ""])
    for scen, stats in payload.get("summary_light_handles", {}).items():
        lines.append(f"### {scen}")
        lines.append(f"- cci_correct: {stats['cci_status_correct_rate']:.2f}")
        lines.append(f"- behavioral_cci: {stats['mean_behavioral_cci']:.3f}")
        lines.append(f"- interventional_cci: {stats['mean_interventional_cci']:.3f}")
        lines.append(f"- capture_gap: {stats['mean_capture_gap']:.3f}")
        lines.append(f"- trace_bandwidth: {stats['mean_trace_bandwidth']:.0f}")
        lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_instrumentation_curve_markdown(payload: dict[str, object], path: Path) -> None:
    interp = payload.get("interpretation", {})
    lines = [
        "# Instrumentation cost curve — multiresolution alignment sim",
        "",
        "Passive (`none`) is **uncertifiable**: audit status is always `belowThreshold`.",
        "That is not a passing certificate. Post-hoc evaluation may still mark `none` as",
        "`cci_status_correct` when uncertifiable is the expected outcome (honest, weak, MB9).",
        "",
        "Handle levels use frozen thresholds and intervention-probe CCI.",
        "",
        f"- Horizon `T`: {payload.get('T')}",
        f"- Calibration seeds: {payload.get('calibration_seeds')}",
        f"- Test seeds: {payload.get('test_seeds')}",
        f"- Status: {payload.get('status', 'complete')}",
        f"- Runtime: {payload.get('runtime_seconds', 'n/a')}s",
        f"- Frozen handle thresholds: {payload.get('frozen_handle_thresholds')}",
        f"- **Minimum certifiable (calibration scenarios):** "
        f"`{payload.get('minimum_certifiable_level_calibration', payload.get('minimum_certifiable_level'))}`",
        f"- **Minimum certifiable (full held-out):** "
        f"`{payload.get('minimum_certifiable_level_full_held_out')}`",
        "",
    ]
    if interp:
        lines.append("## Interpretation")
        lines.append("")
        for key, text in interp.items():
            lines.append(f"- **{key}:** {text}")
        lines.append("")
    lines.extend([
        "| level | handles | bandwidth | calib correct | test correct | test (calib scen) |",
        "|---|---:|---:|---:|---:|---:|",
    ])
    for level, stats in payload.get("by_level", {}).items():
        lines.append(
            f"| {level} | {stats['n_handle_channels']} | {stats['mean_trace_bandwidth']:.0f} | "
            f"{stats['cci_correct_rate_calibration']:.2f} | {stats['cci_correct_rate_test']:.2f} | "
            f"{stats['cci_correct_rate_test_calib_scenarios']:.2f} |"
        )
    lines.append("")
    for level, stats in payload.get("by_level", {}).items():
        lines.append(f"## {level} — test split by scenario")
        lines.append("")
        for scen, scen_stats in stats.get("summary_test", {}).items():
            line = (
                f"- **{scen}**: cci_correct={scen_stats['cci_status_correct_rate']:.2f} "
                f"behavioral={scen_stats['mean_behavioral_cci']:.3f} "
                f"interventional={scen_stats['mean_interventional_cci']:.3f} "
                f"gap={scen_stats['mean_capture_gap']:.3f}"
            )
            if scen_stats.get("mean_hidden_probe_uptake", 0.0) > 0.0:
                line += (
                    f" visible_probe={scen_stats['mean_visible_probe_uptake']:.2f}"
                    f" hidden_probe={scen_stats['mean_hidden_probe_uptake']:.2f}"
                )
            boot = scen_stats.get("bootstrap")
            if boot:
                line += (
                    f" boot_uptake=[{boot['uptake_lo']:.2f},{boot['uptake_hi']:.2f}]"
                    f" boot_ivl=[{boot['interventional_cci_lo']:.3f},"
                    f"{boot['interventional_cci_hi']:.3f}]"
                )
                across = boot.get("across_seed_uptake")
                if across:
                    line += (
                        f" seed_uptake=[{across['lo']:.2f},{across['hi']:.2f}]"
                    )
                h_uptake = boot.get("hierarchical_uptake")
                if h_uptake:
                    line += (
                        f" hier_uptake=[{h_uptake['lo']:.2f},{h_uptake['hi']:.2f}]"
                    )
                h_correct = boot.get("hierarchical_cci_correct_rate")
                if h_correct:
                    line += (
                        f" hier_correct=[{h_correct['lo']:.2f},{h_correct['hi']:.2f}]"
                    )
            lines.append(line)
        lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_frozen_validation_markdown(payload: dict[str, object], path: Path) -> None:
    lines = [
        "# Frozen-threshold validation — multiresolution alignment sim",
        "",
        "Fresh held-out seeds with **pre-registered** capture rules; no refitting.",
        "",
        f"- Horizon `T`: {payload.get('T')}",
        f"- Validation seeds: {payload.get('validation_seeds')}",
        f"- Frozen thresholds: {payload.get('frozen_handle_thresholds')}",
        f"- Frozen capture rules: {payload.get('frozen_capture_rules')}",
        f"- Runtime: {payload.get('runtime_seconds')}s",
        "",
        "## Overall cci_status_correct by level",
        "",
        "| level | overall correct | capture_mild correct |",
        "|---|---:|---:|",
    ]
    overall = payload.get("overall_correct_rate_by_level", {})
    mild = payload.get("capture_mild_correct_rate_by_level", {})
    for level in overall:
        lines.append(
            f"| {level} | {overall[level]:.2f} | {mild.get(level, 0.0):.2f} |"
        )
    lines.append("")
    for level, by_scen in payload.get("summary_by_level", {}).items():
        lines.append(f"## {level}")
        lines.append("")
        for scen, stats in by_scen.items():
            lines.append(
                f"- **{scen}**: cci_correct={stats['cci_status_correct_rate']:.2f} "
                f"n={stats['n_runs']}"
            )
        lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_slice_markdown(payload: dict[str, object], path: Path) -> None:
    lines = [
        "# Slice regression — multiresolution alignment sim",
        "",
        "Fast check on honest, capture_theater, grounding_silent_gap, boundary_alias.",
        "",
        f"- T: {payload.get('T')}",
        f"- Test seeds: {payload.get('test_seeds')}",
        f"- Runtime: {payload.get('runtime_seconds')}s",
        "",
        "## By scenario (all levels pooled)",
        "",
    ]
    for scen, stats in payload.get("summary_by_scenario", {}).items():
        lines.append(
            f"- **{scen}**: cci_correct={stats['cci_status_correct_rate']:.2f} "
            f"n={stats['n_runs']}"
        )
    lines.extend(["", "## By level", ""])
    for level, by_scen in payload.get("summary_by_level", {}).items():
        total_r = sum(s["n_runs"] for s in by_scen.values())
        correct = sum(s["cci_status_correct_rate"] * s["n_runs"] for s in by_scen.values())
        lines.append(
            f"- **{level}**: cci_correct={correct / max(total_r, 1):.2f} n={int(total_r)}"
        )
    lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_sweep_markdown(payload: dict[str, object], path: Path) -> None:
    lines = [
        "# Parameter sweep — multiresolution alignment sim",
        "",
        f"- T: {payload.get('T')}",
        f"- Seeds: {payload.get('seeds')}",
        f"- Grid axes: {payload.get('axes')}",
        f"- Grid points: {payload.get('n_grid_points')}",
        "",
        "| responsiveness | theater_rate | n_decoys | honest_beh | capture_gap | detect_rate | jaccard | det_fail |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in payload.get("rows", []):
        p = row["params"]
        lines.append(
            f"| {p['responsiveness']} | {p['theater_rate']} | {p['n_decoys']} | "
            f"{row['mean_honest_behavioral']:.3f} | {row['mean_capture_gap']:.3f} | "
            f"{row['capture_detect_rate']:.2f} | {row['mean_controller_jaccard']:.2f} | "
            f"{row['detector_fail_rate']:.2f} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Multiresolution alignment sim v1")
    parser.add_argument("--T", type=int, default=2000, help="Horizon steps")
    parser.add_argument("--seeds", type=str, default="1,2,3", help="Comma-separated seeds")
    parser.add_argument(
        "--calibration-seeds",
        type=str,
        default="1-10",
        help="Seed range or list for calibration (e.g. 1-10 or 1,2,3)",
    )
    parser.add_argument(
        "--test-seeds",
        type=str,
        default="11-20",
        help="Seed range or list for test evaluation",
    )
    parser.add_argument(
        "--scenarios",
        type=str,
        default=",".join(ALL_SCENARIOS),
        help="Comma-separated scenario names",
    )
    parser.add_argument("--proposal-k", type=int, default=8, help="MI cluster proposal K")
    parser.add_argument(
        "--calibrated",
        action="store_true",
        help="Fit thresholds on calibration split; evaluate test seeds + held-out scenarios",
    )
    parser.add_argument(
        "--bootstrap",
        action="store_true",
        help="Compute bootstrap CIs on interventional metrics (handle modes)",
    )
    parser.add_argument("--n-boot", type=int, default=200, help="Bootstrap resamples")
    parser.add_argument(
        "--instrumentation-curve",
        action="store_true",
        help="Run none → light → medium → strong cost curve with frozen thresholds",
    )
    parser.add_argument(
        "--frozen-validation",
        action="store_true",
        help=(
            "Validate frozen capture rules on fresh seeds (default 21–30); "
            "no threshold retuning"
        ),
    )
    parser.add_argument(
        "--instrumentation-compare",
        action="store_true",
        help="Compare none vs light_handles instrumentation on calibration scenarios",
    )
    parser.add_argument(
        "--sweep",
        action="store_true",
        help="Run parameter sweep grid (writes sweep JSON/MD)",
    )
    parser.add_argument(
        "--slice",
        action="store_true",
        help="Fast regression: honest/capture/grounding/boundary × all levels (default T=1000)",
    )
    parser.add_argument(
        "--curve-log",
        type=str,
        default="",
        help="Append progress log path (default: experiments/toy-simulation/logs/curve-<timestamp>.md)",
    )
    parser.add_argument(
        "--workers",
        type=str,
        default="auto",
        help="Parallel workers: auto (adaptive), 1 (sequential), or integer",
    )
    parser.add_argument(
        "--cpu-target",
        type=float,
        default=0.80,
        help="Target max CPU utilization (0-1); waits and reduces workers above this",
    )
    parser.add_argument(
        "--gpu-target",
        type=float,
        default=0.80,
        help="Target max GPU utilization (0-1) when nvidia-smi is available",
    )
    parser.add_argument(
        "--no-throttle",
        action="store_true",
        help="Disable CPU/GPU wait-throttle (workers still apply if >1)",
    )
    parser.add_argument("--smoke", action="store_true", help="Short smoke run T=500 seed=1")
    args = parser.parse_args()

    def build_governor() -> ResourceGovernor | None:
        workers = ResourceGovernor.resolve_workers(args.workers)
        if args.no_throttle and workers == 1:
            return None
        gov = ResourceGovernor(
            cpu_target=args.cpu_target,
            gpu_target=args.gpu_target,
            workers=workers,
            throttle_enabled=not args.no_throttle,
        )
        snap = gov.snapshot()
        print(
            f"Resource governor: workers={gov.workers} cpu_target={args.cpu_target:.0%} "
            f"gpu_target={args.gpu_target:.0%} throttle={not args.no_throttle} "
            f"({snap.format_short()})"
        )
        return gov

    if args.slice and args.T == 2000:
        args.T = 1000

    if args.smoke:
        args.T = 500
        args.seeds = "1,2"
        args.calibration_seeds = "1"
        args.test_seeds = "2"
        args.scenarios = "honest,capture_theater"

    def parse_seeds(spec: str) -> list[int]:
        spec = spec.strip()
        if "-" in spec and "," not in spec:
            lo, hi = spec.split("-", 1)
            return list(range(int(lo), int(hi) + 1))
        return [int(s.strip()) for s in spec.split(",") if s.strip()]

    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    def curve_log_path() -> Path:
        if args.curve_log:
            return Path(args.curve_log)
        stamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        return LOG_DIR / f"curve-{stamp}.md"

    if args.slice:
        test_seeds = parse_seeds(args.test_seeds)
        if len(test_seeds) > 4:
            test_seeds = test_seeds[:4]
        log_path = curve_log_path()
        log_path.write_text(
            f"# Slice run {datetime.now().isoformat()}\n\n", encoding="utf-8"
        )
        payload = run_slice(
            test_seeds,
            args.T,
            proposal_k=args.proposal_k,
            bootstrap=args.bootstrap,
            n_boot=args.n_boot,
            log_path=log_path,
            governor=build_governor(),
        )
        json_path = RESULT_DIR / "multiresolution_slice.json"
        md_path = RESULT_DIR / "multiresolution_slice.md"
        json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        write_slice_markdown(payload, md_path)
        print(f"Wrote {json_path}")
        print(f"Wrote {md_path}")
        print(f"Log {log_path}")
        print(f"Runtime {payload['runtime_seconds']}s")
        for scen, stats in payload["summary_by_scenario"].items():
            print(f"  {scen}: cci_correct={stats['cci_status_correct_rate']:.2f}")
        return

    if args.frozen_validation:
        val_seeds = parse_seeds(args.test_seeds)
        if args.test_seeds == "11-20":
            val_seeds = list(FROZEN_VALIDATION_SEEDS)
        if args.smoke:
            val_seeds = parse_seeds("21,22")
        log_path = curve_log_path()
        log_path.write_text(
            f"# Frozen validation {datetime.now().isoformat()}\n\n", encoding="utf-8"
        )
        payload = run_frozen_validation(
            val_seeds,
            args.T,
            proposal_k=args.proposal_k,
            bootstrap=args.bootstrap,
            n_boot=args.n_boot,
            log_path=log_path,
            governor=build_governor(),
        )
        json_path = RESULT_DIR / "multiresolution_frozen_validation.json"
        md_path = RESULT_DIR / "multiresolution_frozen_validation.md"
        json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        write_frozen_validation_markdown(payload, md_path)
        print(f"Wrote {json_path}")
        print(f"Wrote {md_path}")
        print(f"Log {log_path}")
        print("capture_mild by level:", payload["capture_mild_correct_rate_by_level"])
        return

    if args.instrumentation_curve:
        calib_seeds = parse_seeds(args.calibration_seeds)
        test_seeds = parse_seeds(args.test_seeds)
        if args.smoke:
            calib_seeds = parse_seeds("1,2")
            test_seeds = parse_seeds("3,4")
        json_path = RESULT_DIR / "multiresolution_instrumentation_curve.json"
        md_path = RESULT_DIR / "multiresolution_instrumentation_curve.md"
        log_path = curve_log_path()
        log_path.write_text(
            f"# Instrumentation curve {datetime.now().isoformat()}\n\n", encoding="utf-8"
        )
        payload = run_instrumentation_curve(
            calib_seeds,
            test_seeds,
            args.T,
            proposal_k=args.proposal_k,
            bootstrap=args.bootstrap,
            n_boot=args.n_boot,
            output_path=json_path,
            log_path=log_path,
            governor=build_governor(),
        )
        write_instrumentation_curve_markdown(payload, md_path)
        print(f"Wrote {json_path}")
        print(f"Wrote {md_path}")
        print(f"Log {log_path}")
        print("Minimum certifiable (calib):", payload["minimum_certifiable_level_calibration"])
        print("Minimum certifiable (full held-out):", payload["minimum_certifiable_level_full_held_out"])
        if payload.get("resource_usage"):
            print("Resource usage:", payload["resource_usage"])
        for level, stats in payload["by_level"].items():
            print(
                f"  {level}: test_calib_correct="
                f"{stats['cci_correct_rate_test_calib_scenarios']:.2f} "
                f"test_all_correct={stats['cci_correct_rate_test']:.2f} "
                f"handles={stats['n_handle_channels']} bw={stats['mean_trace_bandwidth']:.0f}"
            )
        return

    if args.instrumentation_compare:
        compare_seeds = parse_seeds(args.calibration_seeds)
        if args.smoke:
            compare_seeds = parse_seeds("1,2")
        payload = run_instrumentation_compare(
            CALIBRATION_SCENARIOS, compare_seeds, args.T, proposal_k=args.proposal_k
        )
        json_path = RESULT_DIR / "multiresolution_instrumentation_compare.json"
        md_path = RESULT_DIR / "multiresolution_instrumentation_compare.md"
        json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        write_instrumentation_markdown(payload, md_path)
        print(f"Wrote {json_path}")
        print(f"Wrote {md_path}")
        for scen, stats in payload["delta_light_minus_none"].items():
            print(
                f"{scen}: Δbeh={stats['mean_delta_behavioral_cci']:.3f} "
                f"ivl={stats['mean_interventional_cci']:.3f} "
                f"Δcorrect={stats['mean_cci_correct_improvement']:.2f} "
                f"Δbw={stats['mean_trace_bandwidth_delta']:.0f}"
            )
        return

    if args.sweep:
        sweep_seeds = parse_seeds(args.calibration_seeds)
        payload = run_parameter_sweep(sweep_seeds, args.T, proposal_k=args.proposal_k)
        json_path = RESULT_DIR / "multiresolution_alignment_sim_sweep.json"
        md_path = RESULT_DIR / "multiresolution_alignment_sim_sweep.md"
        json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        write_sweep_markdown(payload, md_path)
        print(f"Wrote {json_path}")
        print(f"Wrote {md_path}")
        return

    if args.calibrated:
        calib_seeds = parse_seeds(args.calibration_seeds)
        test_seeds = parse_seeds(args.test_seeds)
        payload = run_calibrated_suite(
            calib_seeds, test_seeds, args.T, proposal_k=args.proposal_k
        )
        json_path = RESULT_DIR / "multiresolution_alignment_sim.json"
        md_path = RESULT_DIR / "multiresolution_alignment_sim.md"
        json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        write_markdown(payload, md_path)
        print(f"Wrote {json_path}")
        print(f"Wrote {md_path}")
        print("Calibration thresholds:", payload["calibration"])
        for split_name in ("summary_calibration", "summary_test"):
            print(f"\n{split_name}:")
            for scen, stats in payload[split_name].items():
                print(
                    f"  {scen}: cci_correct={stats['cci_status_correct_rate']:.2f} "
                    f"jaccard={stats['mean_controller_jaccard']:.2f} "
                    f"det_fail={stats['detector_substrate_fail_rate']:.2f}"
                )
        return

    seeds = parse_seeds(args.seeds)
    scenarios: list[ScenarioName] = [
        s.strip()  # type: ignore[misc]
        for s in args.scenarios.split(",")
        if s.strip()
    ]
    payload = run_suite(scenarios, seeds, args.T, proposal_k=args.proposal_k)

    json_path = RESULT_DIR / "multiresolution_alignment_sim.json"
    md_path = RESULT_DIR / "multiresolution_alignment_sim.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, md_path)

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    for scen, stats in payload["summary_by_scenario"].items():
        print(
            f"{scen}: cci_correct={stats['cci_status_correct_rate']:.2f} "
            f"capture_detected={stats['capture_detected_rate']:.2f} "
            f"jaccard={stats['mean_controller_jaccard']:.2f} "
            f"mean_gap={stats['mean_capture_gap']:.3f}"
        )


if __name__ == "__main__":
    main()
