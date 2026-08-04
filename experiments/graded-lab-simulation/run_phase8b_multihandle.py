#!/usr/bin/env python3
"""Phase 8b — multi-handle selection fitness (DESIGN.md, reviewer concern 2).

Runs GL-23's exact population/ecology/seeds twice: once with the
single-handle throughput fitness (reproducing GL-23) and once with the
pre-registered multi-handle fitness (throughput + audit-pass +
review-speed), reported side by side.

Outputs: ``results/phase8b_multihandle.json``

Usage:
  python3 run_phase8b_multihandle.py           # full protocol
  python3 run_phase8b_multihandle.py --smoke   # 4 members, 2 gens, 1 ep/member
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
    multi_handle_fitness,
    run_selection_loop,
    sample_initial_population,
    throughput_fitness,
    trajectory_to_dict,
)
from graded_lab.world_visible.config import CODE_VERSION

RESULTS_PATH = Path(__file__).resolve().parent / "results" / "phase8b_multihandle.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 8b multi-handle selection fitness battery")
    parser.add_argument(
        "--smoke", action="store_true", help="Small smoke run: 4 members, 2 generations, 1 episode/member",
    )
    args = parser.parse_args()

    population_size = 4 if args.smoke else D8_POPULATION_SIZE
    n_generations = 2 if args.smoke else D8_N_GENERATIONS
    n_episodes = 1 if args.smoke else 2

    print(
        f"[phase8b] starting multi-handle battery "
        f"(population={population_size}, gens={n_generations}, "
        f"episodes/member={n_episodes}, CODE_VERSION={CODE_VERSION})"
    )

    payload: dict[str, object] = {
        "code_version": CODE_VERSION,
        "smoke": args.smoke,
    }
    t0 = time.perf_counter()
    for label, fitness_fn in (("throughput", throughput_fitness), ("multi_handle", multi_handle_fitness)):
        members = sample_initial_population(population_size=population_size)
        trajectory = run_selection_loop(
            members,
            n_generations=n_generations,
            n_episodes_per_member=n_episodes,
            backend_factory=MockIsolate,
            progress=True,
            fitness_fn=fitness_fn,
            fitness_label=label,
        )
        payload[label] = trajectory_to_dict(trajectory)
    wall = round(time.perf_counter() - t0, 2)
    payload["wall_seconds"] = wall

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"[phase8b] wrote {RESULTS_PATH}")
    print(f"[phase8b] wall {wall}s")

    for label in ("throughput", "multi_handle"):
        gens = payload[label]["generations"]
        if len(gens) >= 2:
            d_cp = gens[-1]["correction_preserving_mass_share"] - gens[0]["correction_preserving_mass_share"]
            print(f"[phase8b] [{label}] Δ correction-preserving mass (gen 0 → last): {d_cp:+.3f}")


if __name__ == "__main__":
    main()
