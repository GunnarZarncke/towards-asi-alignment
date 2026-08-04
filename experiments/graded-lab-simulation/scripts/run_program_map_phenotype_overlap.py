#!/usr/bin/env python3
"""PLAN_v3 slice D item 7: ProgramMap phenotype overlap battery."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from graded_lab.harness.ecology_complexity import V3_REFERENCE_T  # noqa: E402
from graded_lab.harness.phenotype_overlap import run_phenotype_overlap_battery  # noqa: E402

DEFAULT_FIXTURE = ROOT / "tests/fixtures/ecology_v3_slice_a_reference.json"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--T", type=int, default=V3_REFERENCE_T)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--variants-per-actor", type=int, default=12)
    parser.add_argument("--rng-seed", type=int, default=0)
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "results/slice_d_program_map_phenotype_overlap.json",
    )
    args = parser.parse_args()
    started = time.perf_counter()
    payload = run_phenotype_overlap_battery(
        args.fixture,
        T=args.T,
        seed=args.seed,
        variants_per_actor=args.variants_per_actor,
        rng_seed=args.rng_seed,
        progress=True,
    )
    payload["wall_seconds"] = time.perf_counter() - started
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {args.out}", flush=True)
    for row in payload["actors"]:
        print(
            f"  {row['actor_id']}: overlap={row['overlap_fraction']:.2f} "
            f"diversity={row['effective_diversity_fraction']:.2f} "
            f"deploy_diff={row['n_deploy_differs']}/{row['n_variants_sampled']}",
            flush=True,
        )


if __name__ == "__main__":
    main()
