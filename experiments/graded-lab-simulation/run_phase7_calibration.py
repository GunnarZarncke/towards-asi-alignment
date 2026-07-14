#!/usr/bin/env python3
"""Phase 7c-revised — ecology calibration battery (`PLAN.md` / `DESIGN.md`
"Phase 7c-revised ecology calibration battery"; FINDINGS G-16).

Sweeps `carrier_load_scale` (the only knob shown to have a demonstrated
causal path to measured EAI for this ecology/agent roster — FINDINGS
G-16) × agent types × seeds on `default_lab_config`, classifies each
cell's EAI band via the reference agent, scores UAD-backed `I_ctrl` in
mid-band cells, runs a graded carrier-load dose-response, and writes
`results/ecology_calibration.json`.

Usage:
  python3 run_phase7_calibration.py            # full revised 5-cell battery
  python3 run_phase7_calibration.py --smoke    # 2-cell, 2-seed dev grid
  python3 run_phase7_calibration.py --legacy   # original 16-cell compute×spread
                                                # grid (FINDINGS G-15/G-16
                                                # diagnostic fixture, not the
                                                # battery default)
  python3 run_phase7_calibration.py --skip-mechanism-check  # for --legacy reruns
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from graded_lab.harness.isolate import MockIsolate
from graded_lab.oracle_only.calibration import (
    CARRIER_SCALES,
    GRID_SCALES,
    NOMINAL_COMPUTE_SCALE,
    NOMINAL_SPREAD_SCALE,
    carrier_grid,
    check_mechanism_sensitivity,
    run_calibration_battery,
    substrate_grid,
)
from graded_lab.world_visible.config import CODE_VERSION, SubstrateSettings

RESULTS_PATH = Path(__file__).resolve().parent / "results" / "ecology_calibration.json"


def _revised_smoke_grid() -> list[SubstrateSettings]:
    return [
        SubstrateSettings(
            compute_scale=NOMINAL_COMPUTE_SCALE,
            population_spread_scale=NOMINAL_SPREAD_SCALE,
            carrier_load_scale=CARRIER_SCALES[0],
        ),
        SubstrateSettings(
            compute_scale=NOMINAL_COMPUTE_SCALE,
            population_spread_scale=NOMINAL_SPREAD_SCALE,
            carrier_load_scale=CARRIER_SCALES[-1],
        ),
    ]


def _legacy_smoke_grid() -> list[SubstrateSettings]:
    return [
        SubstrateSettings(compute_scale=0.5, population_spread_scale=0.5),
        SubstrateSettings(compute_scale=2.0, population_spread_scale=2.0),
    ]


def _run_mechanism_check_or_abort(*, allow_abort: bool) -> None:
    """PLAN.md "Battery design checklist" item 1 / item 5: don't spend a
    multi-hour blind run on a grid whose knobs demonstrably do nothing.
    Prints the report either way; aborts a `--full` (non-smoke, non-
    `--skip-mechanism-check`) revised run only if *every* knob is dead."""
    print("[phase7c] running mechanism-sensitivity pre-check (see DESIGN.md 'Phase 7c-revised')...")
    reports = check_mechanism_sensitivity(
        knob_values={
            "compute_scale": (GRID_SCALES[0], GRID_SCALES[-1]),
            "population_spread_scale": (GRID_SCALES[0], GRID_SCALES[-1]),
            "carrier_load_scale": (CARRIER_SCALES[0], CARRIER_SCALES[-1]),
        },
        seeds=(0, 1, 2, 3, 4),
        backend=MockIsolate(),
        progress=False,
    )
    any_demonstrated = False
    for r in reports:
        status = "demonstrated_effect" if r.demonstrated_effect else "no_demonstrated_effect"
        print(f"[phase7c]   knob={r.knob!r} eai_range={r.eai_range:.4f} deploy_range={r.deploy_range:.4f} -> {status}")
        any_demonstrated = any_demonstrated or r.demonstrated_effect
    if not any_demonstrated and allow_abort:
        print(
            "[phase7c] ABORT: every swept knob shows no_demonstrated_effect. "
            "Per PLAN.md checklist item 5, this is not a signal to try more "
            "cells within the same ranges — rerun with --smoke to inspect, "
            "or register a different pre-registered dimension / agent "
            "roster change before spending compute on a full battery."
        )
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 7c-revised ecology calibration battery")
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Run a 2-cell smoke grid with 2 seeds instead of the full battery",
    )
    parser.add_argument(
        "--legacy",
        action="store_true",
        help="Run the original 16-cell compute×spread grid (FINDINGS G-15/G-16 "
        "diagnostic fixture) with the corrected evaluator, instead of the "
        "revised carrier_load_scale grid",
    )
    parser.add_argument(
        "--skip-mechanism-check",
        action="store_true",
        help="Skip the pre-battery mechanism-sensitivity dry run (not recommended)",
    )
    args = parser.parse_args()

    if not args.skip_mechanism_check:
        _run_mechanism_check_or_abort(allow_abort=not args.smoke)

    if args.legacy:
        settings_list = _legacy_smoke_grid() if args.smoke else substrate_grid()
    else:
        settings_list = _revised_smoke_grid() if args.smoke else carrier_grid()
    seeds = (0, 1) if args.smoke else tuple(range(10))
    n_cells = len(settings_list)
    n_seeds = len(seeds)
    print(
        f"[phase7c] starting calibration ({'legacy' if args.legacy else 'revised'} grid, "
        f"{n_cells} cells × {n_seeds} seeds, CODE_VERSION={CODE_VERSION})"
    )
    t0 = time.perf_counter()
    payload = run_calibration_battery(
        backend=MockIsolate(),
        settings_list=settings_list,
        seeds=seeds,
        progress=True,
    )
    payload["code_version"] = CODE_VERSION
    payload["smoke"] = args.smoke
    payload["grid_mode"] = "legacy" if args.legacy else "revised"
    payload["wall_seconds"] = round(time.perf_counter() - t0, 2)

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"[phase7c] wrote {RESULTS_PATH}")
    print(f"[phase7c] wall {payload['wall_seconds']}s")

    def _print_report(label: str, report: dict) -> None:
        print(
            f"[phase7c][{label}] criterion 1 (deploy vs EAI slope < 0, within agent type): "
            f"{report['criterion_1_deploy_eai_negative_slope']}"
            f"{' [inconclusive]' if report['criterion_1_inconclusive'] else ''}"
        )
        print(f"[phase7c][{label}] criterion 2 (mid-band I_ctrl strong > weak): {report['criterion_2_mid_band_ctrl_separation']}")
        print(
            f"[phase7c][{label}] criterion 3 (high-band deploy collapse): "
            f"{report['criterion_3_high_band_deploy_collapse']}"
            f"{' [inconclusive]' if report['criterion_3_inconclusive'] else ''}"
        )
        print(
            f"[phase7c][{label}] criterion 4 (graded dose-response): "
            f"{report['criterion_4_graded_dose_response']}"
            f"{' [inconclusive]' if report['criterion_4_inconclusive'] else ''}"
        )
        print(f"[phase7c][{label}] ALL PASSED: {report['all_passed']}")

    # DESIGN.md "Phase 7c full battery, both vantages, with confidence
    # intervals" (FINDINGS G-19/G-20/G-22): report the oracle/agent
    # vantage (as before) and the referee vantage side by side, from the
    # same episodes — neither replaces the other.
    _print_report("oracle", payload["pass_criteria"])
    if payload.get("sweet_spot_candidate"):
        print(f"[phase7c][oracle] sweet-spot candidate: {payload['sweet_spot_candidate']}")
    _print_report("referee", payload["pass_criteria_referee"])
    if payload.get("sweet_spot_candidate_referee"):
        print(f"[phase7c][referee] sweet-spot candidate: {payload['sweet_spot_candidate_referee']}")


if __name__ == "__main__":
    main()
