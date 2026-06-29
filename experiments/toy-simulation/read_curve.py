#!/usr/bin/env python3
"""Summarize instrumentation curve JSON (in_progress or complete)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT = Path(__file__).resolve().parent / "results" / "multiresolution_instrumentation_curve.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Read instrumentation curve artifact")
    parser.add_argument("--json", type=Path, default=DEFAULT)
    args = parser.parse_args()

    payload = json.loads(args.json.read_text(encoding="utf-8"))
    status = payload.get("status", "?")
    completed = payload.get("completed_levels", [])
    print(f"status={status}  T={payload.get('T')}  completed={completed}")
    print(
        f"min_cert calib={payload.get('minimum_certifiable_level_calibration')} "
        f"full={payload.get('minimum_certifiable_level_full_held_out')}"
    )
    print()
    print("| level | calib correct | test correct | test calib | handles | bw |")
    print("|---|---:|---:|---:|---:|---:|")
    for level, stats in payload.get("by_level", {}).items():
        print(
            f"| {level} | {stats.get('cci_correct_rate_calibration', 0):.2f} | "
            f"{stats.get('cci_correct_rate_test', 0):.2f} | "
            f"{stats.get('cci_correct_rate_test_calib_scenarios', 0):.2f} | "
            f"{stats.get('n_handle_channels', 0)} | "
            f"{stats.get('mean_trace_bandwidth', 0):.0f} |"
        )
    print()
    stress = ("capture_mild", "bundle_goodhart", "hidden_capability", "grounding_silent_gap")
    for level, stats in payload.get("by_level", {}).items():
        test = stats.get("summary_test", {})
        if not test:
            continue
        print(f"## {level} — stress scenarios")
        for scen in stress:
            s = test.get(scen)
            if not s:
                continue
            line = f"  {scen}: cci_correct={s['cci_status_correct_rate']:.2f} n={s['n_runs']}"
            if s.get("mean_bundle_geometry_spread", 0) > 0:
                line += f" bundle_spread={s['mean_bundle_geometry_spread']:.3f}"
            if s.get("mean_hidden_memory_step_rate", 0) > 0:
                line += f" mem_shadow={s['mean_hidden_memory_step_rate']:.3f}"
            print(line)
        print()


if __name__ == "__main__":
    main()
