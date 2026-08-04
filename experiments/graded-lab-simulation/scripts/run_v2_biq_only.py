#!/usr/bin/env python3
"""BIQ-only re-run on a grown ecology (GL-77).

Runs reference episodes + passive UAD (no intervention matrix), then
ecology-BIQ including singleton inferred units. Optionally patches
``ecology_biq`` into an existing ``v2_transfer.json``.

Usage:
  cd experiments/graded-lab-simulation
  .venv/bin/python scripts/run_v2_biq_only.py --workers 4
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

from graded_lab.harness.isolate import MockIsolate  # noqa: E402
from graded_lab.harness.machinery_transfer import (  # noqa: E402
    BIQ_MAX_SEEDS,
    BIQ_MAX_UNITS_PER_SEED,
    DEFAULT_ECOLOGY_PATH,
    reference_bundle,
    score_ecology_biq_on_passive_units,
)
from graded_lab.oracle_only.uad_discovery import discovered_units_uad  # noqa: E402
from graded_lab.world_visible.config import CODE_VERSION  # noqa: E402
from graded_lab.world_visible.world import run_episode  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_ECOLOGY_PATH)
    parser.add_argument("--out", type=Path, default=Path("results/v2_transfer_biq.json"))
    parser.add_argument(
        "--patch-transfer",
        type=Path,
        default=Path("results/v2_transfer.json"),
        help="If present, patch ecology_biq into this transfer JSON",
    )
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--max-seeds", type=int, default=BIQ_MAX_SEEDS)
    parser.add_argument("--max-units", type=int, default=BIQ_MAX_UNITS_PER_SEED)
    args = parser.parse_args()

    seeds = tuple(range(args.max_seeds))
    started = time.perf_counter()
    ecology_data, roster, cfg, programs, profiles = reference_bundle(args.fixture)
    del ecology_data, roster
    backend = MockIsolate()

    print(
        f"[biq-only] ecology={args.fixture.name} seeds={list(seeds)} "
        f"max_units={args.max_units} workers={args.workers} T={cfg.T}",
        flush=True,
    )

    results_by_seed = {}
    uad_rows = []
    for i, seed in enumerate(seeds):
        print(f"[biq-only episode {i + 1}/{len(seeds)}] seed={seed}", flush=True)
        result = run_episode(
            cfg, seed, backend, programs=programs, behavior_profiles=profiles
        )
        results_by_seed[seed] = result
        passive = discovered_units_uad(result=result, rng_seed=seed)
        units = sorted(set(passive.values()), key=lambda m: (-len(m), m))
        print(
            f"  deploy_count={result.deploy_count} "
            f"partition={[list(u) for u in units]}",
            flush=True,
        )
        uad_rows.append(
            {
                "seed": seed,
                "passive_partition": [list(u) for u in units],
                "passive_nonsingletons": [list(u) for u in units if len(u) > 1],
            }
        )

    uad = {"per_seed": uad_rows, "n_seeds": len(seeds)}
    biq = score_ecology_biq_on_passive_units(
        cfg,
        programs,
        uad,
        results_by_seed,
        max_seeds=args.max_seeds,
        max_units_per_seed=args.max_units,
        backend=backend,
        progress=True,
        workers=args.workers,
    )

    wall = time.perf_counter() - started
    payload = {
        "code_version": CODE_VERSION,
        "battery": "V2-3_ecology_biq_only_GL77",
        "ecology_path": str(args.fixture),
        "ecology_version": "v3_grown",
        "wall_seconds": wall,
        "workers": args.workers,
        "uad_passive": uad,
        "ecology_biq": biq,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {args.out} ({wall:.1f}s wall)", flush=True)
    for row in biq["per_seed"]:
        print(f"  seed={row['seed']} n_units={len(row['units'])}", flush=True)
        for unit in row["units"]:
            print(
                f"    members={unit['members']} i_pred_total={unit['i_pred_total']} "
                f"i_ctrl={unit['i_ctrl']} composite={unit['composite_bits']}",
                flush=True,
            )

    if args.patch_transfer and args.patch_transfer.exists():
        transfer = json.loads(args.patch_transfer.read_text(encoding="utf-8"))
        transfer["ecology_biq"] = biq
        transfer["ecology_biq_rerun"] = {
            "code_version": CODE_VERSION,
            "note": (
                "GL-77 BIQ-only re-run after singleton-unit harness fix. "
                "UAD/EAI/P1–P4 from GL-76 unchanged."
            ),
            "artifact": str(args.out),
            "wall_seconds": wall,
        }
        args.patch_transfer.write_text(json.dumps(transfer, indent=2), encoding="utf-8")
        print(f"Patched ecology_biq into {args.patch_transfer}", flush=True)


if __name__ == "__main__":
    main()
