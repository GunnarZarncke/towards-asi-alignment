#!/usr/bin/env python3
"""Phase 8 — throughput-linked selection battery (MB6 / DESIGN.md).

Runs the pre-registered population-over-program-maps loop on the GL-22
referee sweet-spot ecology (`carrier_load_scale=1.5`), with multi-episode
campaigns that carry grants and standing forward within each member.

Outputs: ``results/phase8_selection.json``

Usage:
  python3 run_phase8_selection.py           # full protocol (MockIsolate)
  python3 run_phase8_selection.py --smoke   # 4 members, 2 gens, 1 ep/member
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from graded_lab.harness.isolate import MockIsolate
from graded_lab.harness.selection import (
    D8_N_GENERATIONS,
    D8_POPULATION_SIZE,
    run_selection_loop,
    sample_initial_population,
    trajectory_to_dict,
)
from graded_lab.world_visible.config import CODE_VERSION

RESULTS_PATH = Path(__file__).resolve().parent / "results" / "phase8_selection.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 8 selection battery (MB6)")
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Small smoke run: 4 members, 2 generations, 1 episode/member",
    )
    args = parser.parse_args()

    population_size = 4 if args.smoke else D8_POPULATION_SIZE
    n_generations = 2 if args.smoke else D8_N_GENERATIONS
    n_episodes = 1 if args.smoke else 2

    members = sample_initial_population(population_size=population_size)
    print(
        f"[phase8] starting selection battery "
        f"(population={population_size}, gens={n_generations}, "
        f"episodes/member={n_episodes}, CODE_VERSION={CODE_VERSION})"
    )
    t0 = time.perf_counter()
    trajectory = run_selection_loop(
        members,
        n_generations=n_generations,
        n_episodes_per_member=n_episodes,
        backend_factory=MockIsolate,
        progress=True,
    )
    wall = round(time.perf_counter() - t0, 2)

    payload = trajectory_to_dict(trajectory)
    payload["code_version"] = CODE_VERSION
    payload["smoke"] = args.smoke
    payload["wall_seconds"] = wall

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"[phase8] wrote {RESULTS_PATH}")
    print(f"[phase8] wall {wall}s")

    gens = payload["generations"]
    if len(gens) >= 2:
        d_cp = gens[-1]["correction_preserving_mass_share"] - gens[0]["correction_preserving_mass_share"]
        d_sev = gens[-1]["weighted_mean_severity"] - gens[0]["weighted_mean_severity"]
        print(f"[phase8] Δ correction-preserving mass (gen 0 → last): {d_cp:+.3f}")
        print(f"[phase8] Δ weighted severity (gen 0 → last): {d_sev:+.4f}")


if __name__ == "__main__":
    main()
