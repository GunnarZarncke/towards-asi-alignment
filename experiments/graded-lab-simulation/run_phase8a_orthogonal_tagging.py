#!/usr/bin/env python3
"""Phase 8a — orthogonal preservation tagging (DESIGN.md, reviewer concern 1).

Reruns GL-23's selection protocol on a 2-member population where
`correction_preserving` is tagged by a named structural criterion
(does `rm1` send a status-report `communicate` to the reviewer) that is
independent of member identity — both members otherwise use the same
underlying agent type (WEAK_AGENT).

Outputs: ``results/phase8a_orthogonal_tagging.json``

Usage:
  python3 run_phase8a_orthogonal_tagging.py           # full protocol
  python3 run_phase8a_orthogonal_tagging.py --smoke   # 2 gens, 1 ep/member
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from graded_lab.harness.isolate import MockIsolate
from graded_lab.harness.selection import (
    D8_N_GENERATIONS,
    ORTHOGONAL_MEMBER_TEMPLATES,
    run_selection_loop,
    sample_initial_population,
    trajectory_to_dict,
)
from graded_lab.world_visible.config import CODE_VERSION

RESULTS_PATH = Path(__file__).resolve().parent / "results" / "phase8a_orthogonal_tagging.json"

# Same population size as GL-23 (8 members, alternating 4/4 over the 2
# orthogonal templates) so the battery shape is directly comparable.
POPULATION_SIZE = 8


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 8a orthogonal preservation tagging battery")
    parser.add_argument("--smoke", action="store_true", help="Small smoke run: 2 generations, 1 episode/member")
    args = parser.parse_args()

    n_generations = 2 if args.smoke else D8_N_GENERATIONS
    n_episodes = 1 if args.smoke else 2

    members = sample_initial_population(
        population_size=POPULATION_SIZE, templates=ORTHOGONAL_MEMBER_TEMPLATES,
    )
    print(
        f"[phase8a] starting orthogonal-tagging battery "
        f"(population={POPULATION_SIZE}, gens={n_generations}, "
        f"episodes/member={n_episodes}, CODE_VERSION={CODE_VERSION})"
    )
    t0 = time.perf_counter()
    trajectory = run_selection_loop(
        members,
        n_generations=n_generations,
        n_episodes_per_member=n_episodes,
        backend_factory=MockIsolate,
        progress=True,
        fitness_label="throughput_orthogonal",
    )
    wall = round(time.perf_counter() - t0, 2)

    payload = trajectory_to_dict(trajectory)
    payload["code_version"] = CODE_VERSION
    payload["smoke"] = args.smoke
    payload["wall_seconds"] = wall
    payload["member_templates"] = [dict(t) for t in ORTHOGONAL_MEMBER_TEMPLATES]

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"[phase8a] wrote {RESULTS_PATH}")
    print(f"[phase8a] wall {wall}s")

    gens = payload["generations"]
    if len(gens) >= 2:
        d_cp = gens[-1]["correction_preserving_mass_share"] - gens[0]["correction_preserving_mass_share"]
        d_thr = gens[-1]["weighted_mean_throughput"] - gens[0]["weighted_mean_throughput"]
        print(f"[phase8a] Δ correction-preserving mass (gen 0 → last): {d_cp:+.3f}")
        print(f"[phase8a] Δ weighted throughput (gen 0 → last): {d_thr:+.4f}")


if __name__ == "__main__":
    main()
