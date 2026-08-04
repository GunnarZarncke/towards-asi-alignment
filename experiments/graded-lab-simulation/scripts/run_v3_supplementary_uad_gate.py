#!/usr/bin/env python3
"""PLAN_v3 slice D GL-65: supplementary in-ecology UAD channel fixture gate."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from graded_lab.harness.supplementary_uad_gate import (  # noqa: E402
    evaluate_supplementary_uad_gate,
)

DEFAULT_FIXTURE = ROOT / "tests/fixtures/ecology_v3_supplementary_uad_channel_suite.json"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "results/slice_d_v3_supplementary_uad_gate.json",
    )
    args = parser.parse_args()
    payload = evaluate_supplementary_uad_gate(args.fixture, progress=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {args.out}", flush=True)
    print(
        f"organic_channel_coupling_verified={payload['organic_channel_coupling_verified']}",
        flush=True,
    )


if __name__ == "__main__":
    main()
