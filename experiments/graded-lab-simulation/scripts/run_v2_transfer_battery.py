#!/usr/bin/env python3
"""V2-3 Q1 machinery transfer battery (PLAN_v2.md V2-3).

Frozen v1 UAD, EAI, ecology-BIQ, and detector coverage on a blinded-grown
v3 ecology. Pre-registered output: ``results/v2_transfer.json``.

Usage:
  cd experiments/graded-lab-simulation
  .venv/bin/python scripts/run_v2_transfer_battery.py
  .venv/bin/python scripts/run_v2_transfer_battery.py --smoke   # fast dev check
  .venv/bin/python scripts/run_v2_transfer_battery.py --fixture generated_ecology_v3.json
  .venv/bin/python scripts/run_v2_transfer_battery.py --workers 4
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from graded_lab.harness.machinery_transfer import (  # noqa: E402
    DEFAULT_ECOLOGY_PATH,
    RESULTS_DEFAULT,
    run_machinery_transfer_battery,
    write_transfer_results,
)
from graded_lab.world_visible.substrate import V3_GROWN_ECOLOGY_PATH  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fixture",
        type=Path,
        default=DEFAULT_ECOLOGY_PATH,
        help="Ecology JSON (default: frozen v3 grown)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=RESULTS_DEFAULT,
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Minimal seeds/carriers for harness validation (~2–5 min)",
    )
    parser.add_argument(
        "--no-biq",
        action="store_true",
        help="Skip ecology-BIQ (slowest subsection)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Process pool size for UAD/EAI/BIQ episode work (default: 4; use 1 to disable)",
    )
    args = parser.parse_args()

    uad_seeds = (0, 1) if args.smoke else None
    eai_seeds = (0, 1) if args.smoke else None
    carrier_scales = (1.0,) if args.smoke else None

    kwargs: dict = {
        "ecology_path": args.fixture,
        "include_biq": not args.no_biq,
        "workers": args.workers,
        "progress": True,
    }
    if uad_seeds is not None:
        kwargs["uad_seeds"] = uad_seeds
    if eai_seeds is not None:
        kwargs["eai_seeds"] = eai_seeds
    if carrier_scales is not None:
        kwargs["carrier_scales"] = carrier_scales

    payload = run_machinery_transfer_battery(**kwargs)
    out = write_transfer_results(payload, args.out)
    print(f"\nWrote {out} ({payload['wall_seconds']:.1f}s wall)", flush=True)
    preds = payload["predictions"]
    for key in ("P1", "P2", "P3", "P4"):
        row = preds[key]
        holds = row.get("holds")
        print(f"  {key}: holds={holds}", flush=True)
    if payload.get("ecology_version") == "v3_grown" or args.fixture.resolve() == V3_GROWN_ECOLOGY_PATH.resolve():
        print(
            f"  go_gate (V2-5/V2-6, default load): {preds['P3'].get('go_gate_for_V2_5_V2_6')}",
            flush=True,
        )
        print(
            f"  P4 note: {preds['P4'].get('interpretation', '')[:120]}...",
            flush=True,
        )


if __name__ == "__main__":
    main()
