#!/usr/bin/env python3
"""PLAN_v4 V4-2: run one decoupled per-bridge rig on a shared fixture.

Usage:
  cd experiments/graded-lab-simulation
  .venv/bin/python scripts/run_v4_rig.py --rig r-mb1 --out results/v4_r_mb1.json
  .venv/bin/python scripts/run_v4_rig.py --rig r-mb4 --out results/v4_r_mb4.json
  .venv/bin/python scripts/run_v4_rig.py --rig r-mb1 --smoke   # fast dev check
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from graded_lab.harness.ecology_complexity import C3_SEEDS  # noqa: E402
from graded_lab.harness.fixtures import build_reference_fixture  # noqa: E402
from graded_lab.harness.rigs import r_mb1_unit_discovery, r_mb4_detector_transfer  # noqa: E402
from graded_lab.world_visible.config import CODE_VERSION  # noqa: E402
from graded_lab.world_visible.substrate import V3_GROWN_ECOLOGY_PATH  # noqa: E402

RIGS = {
    "r-mb1": r_mb1_unit_discovery,
    "r-mb4": r_mb4_detector_transfer,
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rig", required=True, choices=sorted(RIGS))
    parser.add_argument(
        "--fixture",
        type=Path,
        default=V3_GROWN_ECOLOGY_PATH,
        help="Ecology JSON (default: frozen v3 grown, S-inherited)",
    )
    parser.add_argument(
        "--substrate-class",
        default="S-inherited",
        choices=("S-inherited", "S-blind", "S-fixture"),
    )
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--smoke", action="store_true", help="2 seeds only, fast dev check")
    args = parser.parse_args()

    module = RIGS[args.rig]
    seeds = (0, 1) if args.smoke else C3_SEEDS
    started = time.perf_counter()

    fixture = build_reference_fixture(
        args.fixture,
        seeds=seeds,
        workers=args.workers,
        progress=True,
        label=f"v4-{args.rig}-fixture",
    )
    rig_kwargs: dict = {"substrate_class": args.substrate_class, "progress": True}
    if args.rig == "r-mb1":
        rig_kwargs["workers"] = args.workers
    result = module.run_rig(fixture, **rig_kwargs)

    payload = {
        "code_version": CODE_VERSION,
        "battery": f"v4_{args.rig}",
        "ecology_path": str(args.fixture),
        "seeds": list(seeds),
        "wall_seconds": time.perf_counter() - started,
        **result.to_dict(),
    }
    out = args.out or Path(f"results/v4_{args.rig.replace('-', '_')}.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    print(f"\n[{args.rig}] outcome={result.outcome} substrate={result.substrate_class}", flush=True)
    print(f"[{args.rig}] precondition satisfied={result.precondition.satisfied}", flush=True)
    print(f"Wrote {out} ({payload['wall_seconds']:.1f}s wall)", flush=True)


if __name__ == "__main__":
    main()
