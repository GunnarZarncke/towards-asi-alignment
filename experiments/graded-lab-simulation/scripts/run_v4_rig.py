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
from graded_lab.harness.rigs import (  # noqa: E402
    r_mb1_unit_discovery,
    r_mb4_detector_transfer,
    r_mb7d_channel_ablation,
    r_mb9_contradiction_surface,
)
from graded_lab.world_visible.config import CODE_VERSION  # noqa: E402
from graded_lab.world_visible.substrate import V3_GROWN_ECOLOGY_PATH  # noqa: E402

RIGS = {
    "r-mb1": r_mb1_unit_discovery,
    "r-mb4": r_mb4_detector_transfer,
    "r-mb9": r_mb9_contradiction_surface,
    "r-mb7d": r_mb7d_channel_ablation,
}
# r-mb7d/r-mb9 return a dict of per-arm RigResult (never a single merged
# RigResult, per DESIGN.md) — r-mb1/r-mb4 return one RigResult each.
MULTI_ARM_RIGS = {"r-mb7d", "r-mb9"}


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
        default=None,
        choices=("S-inherited", "S-blind", "S-fixture"),
        help="Default: each rig module's own default (S-fixture for r-mb7d, S-inherited otherwise)",
    )
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--smoke", action="store_true", help="2 seeds only, fast dev check")
    args = parser.parse_args()

    module = RIGS[args.rig]
    if args.rig == "r-mb7d":
        # needs >= n_dose_seeds distinct seeds regardless of --smoke.
        seeds = (0, 1, 2, 3) if args.smoke else C3_SEEDS
    else:
        seeds = (0, 1) if args.smoke else C3_SEEDS
    started = time.perf_counter()

    fixture = build_reference_fixture(
        args.fixture,
        seeds=seeds,
        workers=args.workers,
        progress=True,
        label=f"v4-{args.rig}-fixture",
    )
    rig_kwargs: dict = {"progress": True}
    if args.substrate_class is not None and args.rig != "r-mb9":
        # r-mb9's two arms have fixed, distinct substrate classes
        # (S-inherited specificity / S-fixture sensitivity) — no single
        # override makes sense; --substrate-class is a no-op for it.
        rig_kwargs["substrate_class"] = args.substrate_class
    if args.rig in ("r-mb1", "r-mb7d"):
        rig_kwargs["workers"] = args.workers
    if args.rig == "r-mb7d" and args.smoke:
        # Dev-speed override only — the frozen ONSET_FRACS/N_DOSE_SEEDS
        # constants are used for every real scored battery.
        rig_kwargs["onset_fracs"] = (0.5,)
        rig_kwargs["n_dose_seeds"] = 4

    outcome = module.run_rig(fixture, **rig_kwargs)

    if args.rig in MULTI_ARM_RIGS:
        results_by_arm: dict = outcome
        payload = {
            "code_version": CODE_VERSION,
            "battery": f"v4_{args.rig}",
            "ecology_path": str(args.fixture),
            "seeds": list(seeds),
            "wall_seconds": time.perf_counter() - started,
            "arms": {name: r.to_dict() for name, r in results_by_arm.items()},
        }
        for name, r in results_by_arm.items():
            print(f"\n[{args.rig}:{name}] outcome={r.outcome} substrate={r.substrate_class}", flush=True)
            print(f"[{args.rig}:{name}] precondition satisfied={r.precondition.satisfied}", flush=True)
    else:
        result = outcome
        payload = {
            "code_version": CODE_VERSION,
            "battery": f"v4_{args.rig}",
            "ecology_path": str(args.fixture),
            "seeds": list(seeds),
            "wall_seconds": time.perf_counter() - started,
            **result.to_dict(),
        }
        print(f"\n[{args.rig}] outcome={result.outcome} substrate={result.substrate_class}", flush=True)
        print(f"[{args.rig}] precondition satisfied={result.precondition.satisfied}", flush=True)

    out = args.out or Path(f"results/v4_{args.rig.replace('-', '_')}.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    print(f"Wrote {out} ({payload['wall_seconds']:.1f}s wall)", flush=True)


if __name__ == "__main__":
    main()
