#!/usr/bin/env python3
"""Phase 8c — carryover ablation (DESIGN.md, reviewer concern 3).

Runs GL-23's exact population/ecology/seeds twice: once with campaign
carryover as implemented (reproducing GL-23) and once with
`campaign_state` forced to `None` every episode (reset baseline), then
compares the two conditions' per-generation series via paired 95% CIs.

Outputs: ``results/phase8c_carryover_ablation.json``

Usage:
  python3 run_phase8c_carryover_ablation.py           # full protocol
  python3 run_phase8c_carryover_ablation.py --smoke   # 4 members, 2 gens, 1 ep/member
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
    paired_generation_comparison,
    run_selection_loop,
    sample_initial_population,
    trajectory_to_dict,
)
from graded_lab.world_visible.config import CODE_VERSION

RESULTS_PATH = Path(__file__).resolve().parent / "results" / "phase8c_carryover_ablation.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 8c carryover ablation battery")
    parser.add_argument(
        "--smoke", action="store_true", help="Small smoke run: 4 members, 2 generations, 1 episode/member",
    )
    args = parser.parse_args()

    population_size = 4 if args.smoke else D8_POPULATION_SIZE
    n_generations = 2 if args.smoke else D8_N_GENERATIONS
    n_episodes = 1 if args.smoke else 2

    print(
        f"[phase8c] starting carryover-ablation battery "
        f"(population={population_size}, gens={n_generations}, "
        f"episodes/member={n_episodes}, CODE_VERSION={CODE_VERSION})"
    )

    payload: dict[str, object] = {"code_version": CODE_VERSION, "smoke": args.smoke}
    t0 = time.perf_counter()
    trajectories = {}
    for label, carryover in (("carryover", True), ("reset", False)):
        members = sample_initial_population(population_size=population_size)
        trajectory = run_selection_loop(
            members,
            n_generations=n_generations,
            n_episodes_per_member=n_episodes,
            backend_factory=MockIsolate,
            progress=True,
            carryover=carryover,
            fitness_label=label,
        )
        trajectories[label] = trajectory
        payload[label] = trajectory_to_dict(trajectory)
    wall = round(time.perf_counter() - t0, 2)
    payload["wall_seconds"] = wall

    comparisons = {
        field: paired_generation_comparison(trajectories["carryover"], trajectories["reset"], field=field)
        for field in ("weighted_mean_throughput", "correction_preserving_mass_share")
    }
    payload["paired_comparison"] = comparisons

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"[phase8c] wrote {RESULTS_PATH}")
    print(f"[phase8c] wall {wall}s")

    for field, comp in comparisons.items():
        print(
            f"[phase8c] {field}: paired diff mean={comp['mean']:.4f} "
            f"ci95=({comp['ci95_low']:.4f}, {comp['ci95_high']:.4f}) "
            f"zero_in_ci95={comp['zero_in_ci95']}"
        )


if __name__ == "__main__":
    main()
