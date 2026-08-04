#!/usr/bin/env python3
"""PLAN_v3 slice D GL-60: supplementary detector fixture gate."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from graded_lab.harness.supplementary_detector_gate import (  # noqa: E402
    evaluate_supplementary_detector_gate,
)

DEFAULT_FIXTURE = ROOT / "tests/fixtures/ecology_v3_supplementary_detector_suite.json"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "results/slice_d_v3_supplementary_detector_gate.json",
    )
    args = parser.parse_args()
    started = time.perf_counter()
    payload = evaluate_supplementary_detector_gate(args.fixture, progress=True)
    payload["wall_seconds"] = time.perf_counter() - started
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {args.out}", flush=True)
    print(
        f"machinery_transfer_verified={payload['machinery_transfer_verified']} "
        f"exercised={payload['families_exercised']} missing={payload['families_missing']}",
        flush=True,
    )
    for row in payload["probes"]:
        print(f"  {row['probe_id']}: passed={row['passed']}", flush=True)


if __name__ == "__main__":
    main()
