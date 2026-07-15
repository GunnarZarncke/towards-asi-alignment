#!/usr/bin/env python3
"""Phase 8d — budget-aware member on frozen Phase 8 ecology (DESIGN.md).

Runs GL-23 control population and budget-aware treatment population on the
same protocol, then compares deploy rates and endpoints per the pre-registered
decision rule.

Outputs: ``results/phase8d_budget_aware.json``

Usage:
  python3 run_phase8d_budget_aware.py           # full protocol
  python3 run_phase8d_budget_aware.py --smoke   # 4 members, 2 gens, 1 ep/member
"""

from __future__ import annotations

import argparse
import json
import statistics
import time
from pathlib import Path

from graded_lab.harness.isolate import MockIsolate
from graded_lab.harness.selection import (
    D8_N_GENERATIONS,
    D8_POPULATION_SIZE,
    run_selection_loop,
    sample_budget_aware_population,
    sample_initial_population,
    trajectory_to_dict,
)
from graded_lab.world_visible.config import CODE_VERSION

RESULTS_PATH = Path(__file__).resolve().parent / "results" / "phase8d_budget_aware.json"


def _mean_deploy_for_tag(trajectory_dict: dict, tag: str) -> float:
    deploys: list[int] = []
    for gen in trajectory_dict["generations"]:
        for member in gen["members"]:
            if member["member_tag"] == tag:
                for ep in member["episode_metrics"]:
                    deploys.append(ep["deploy_count"])
    if not deploys:
        raise ValueError(f"no episodes for member_tag={tag}")
    return statistics.mean(deploys)


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 8d budget-aware member battery")
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Small smoke run: 4 members, 2 generations, 1 episode/member",
    )
    args = parser.parse_args()

    population_size = 4 if args.smoke else D8_POPULATION_SIZE
    n_generations = 2 if args.smoke else D8_N_GENERATIONS
    n_episodes = 1 if args.smoke else 2

    print(
        f"[phase8d] starting budget-aware battery "
        f"(population={population_size}, gens={n_generations}, "
        f"episodes/member={n_episodes}, CODE_VERSION={CODE_VERSION})"
    )
    t0 = time.perf_counter()
    payloads: dict[str, object] = {"code_version": CODE_VERSION, "smoke": args.smoke}

    for label, sampler in (
        ("gl23_control", sample_initial_population),
        ("budget_aware_treatment", sample_budget_aware_population),
    ):
        members = sampler(population_size=population_size)
        trajectory = run_selection_loop(
            members,
            n_generations=n_generations,
            n_episodes_per_member=n_episodes,
            backend_factory=MockIsolate,
            progress=True,
            fitness_label=label,
        )
        payloads[label] = trajectory_to_dict(trajectory)

    wall = round(time.perf_counter() - t0, 2)
    payloads["wall_seconds"] = wall

    control = payloads["gl23_control"]
    treatment = payloads["budget_aware_treatment"]
    weak_deploy = _mean_deploy_for_tag(control, "weak_2step")
    budget_deploy = _mean_deploy_for_tag(treatment, "weak_budget_aware")
    deploy_delta = budget_deploy - weak_deploy
    w_thr_control = control["generations"][-1]["weighted_mean_throughput"]
    w_thr_treatment = treatment["generations"][-1]["weighted_mean_throughput"]
    w_thr_delta = w_thr_treatment - w_thr_control

    null_deploy = abs(deploy_delta) <= 0.05
    null_endpoint = abs(w_thr_delta) < 0.02
    verdict = "null" if (null_deploy and null_endpoint) else "non_null"

    payloads["comparison"] = {
        "weak_2step_mean_deploy": weak_deploy,
        "weak_budget_aware_mean_deploy": budget_deploy,
        "deploy_delta": deploy_delta,
        "final_w_thr_control": w_thr_control,
        "final_w_thr_treatment": w_thr_treatment,
        "w_thr_delta": w_thr_delta,
        "null_deploy_within_0_05": null_deploy,
        "null_endpoint_within_0_02": null_endpoint,
        "verdict": verdict,
    }

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(payloads, indent=2, sort_keys=True) + "\n")
    print(
        f"[phase8d] deploy delta={deploy_delta:+.3f} "
        f"w_thr delta={w_thr_delta:+.3f} verdict={verdict} wall={wall}s"
    )
    print(f"[phase8d] wrote {RESULTS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
