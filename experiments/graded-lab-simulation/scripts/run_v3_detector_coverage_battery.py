#!/usr/bin/env python3
"""PLAN_v3 slice D item 6: frozen-detector coverage on v3 reference battery."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from graded_lab.harness.detector_coverage import run_detector_coverage_battery  # noqa: E402
from graded_lab.harness.ecology_complexity import C3_SEEDS  # noqa: E402

DEFAULT_FIXTURE = ROOT / "tests/fixtures/ecology_v3_slice_a_reference.json"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--seeds", type=int, default=len(C3_SEEDS))
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "results/slice_d_v3_detector_coverage_T200_n20.json",
    )
    args = parser.parse_args()
    seeds = tuple(range(args.seeds))
    started = time.perf_counter()
    payload = run_detector_coverage_battery(args.fixture, seeds=seeds, progress=True)
    payload["wall_seconds"] = time.perf_counter() - started
    # Drop per-episode raw scores from default JSON (summary only).
    payload.pop("episodes", None)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {args.out}", flush=True)
    for name, summary in payload["families"].items():
        print(
            f"  {name}: mean={summary['mean']:.3f} "
            f"unique={summary['n_unique_rounded']} "
            f"zero_var={summary['zero_variance']} "
            f"flag_rate={summary['flag_rate']:.2f}",
            flush=True,
        )
    print(
        f"transfer_failure_risk={payload['transfer_failure_risk']} "
        f"({payload['n_families_zero_variance']} zero-variance, "
        f"{payload['n_families_always_zero']} always-zero)",
        flush=True,
    )


if __name__ == "__main__":
    main()
