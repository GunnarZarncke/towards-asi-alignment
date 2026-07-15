#!/usr/bin/env python3
"""Verify MockIsolate and SubprocessIsolate agree on Phase 8 member episodes
and a small selection-loop trajectory (DESIGN.md isolate equivalence).

Usage:
  python3 verify_phase8_isolate_parity.py           # default checks
  python3 verify_phase8_isolate_parity.py --smoke   # member episodes only
"""

from __future__ import annotations

import argparse
import json
import sys

from graded_lab.harness.isolate import MockIsolate, SubprocessIsolate
from graded_lab.harness.selection import (
    MEMBER_TEMPLATES,
    ORTHOGONAL_MEMBER_TEMPLATES,
    member_programs,
    phase8_ecology_config,
    run_selection_loop,
    sample_initial_population,
    trajectory_to_dict,
)
from graded_lab.world_visible.world import run_episode

MEMBER_EPISODE_SEED = 4242
SELECTION_POPULATION = 4
SELECTION_GENERATIONS = 2
SELECTION_EPISODES = 1


def _all_member_templates() -> tuple[dict[str, object], ...]:
    return MEMBER_TEMPLATES + ORTHOGONAL_MEMBER_TEMPLATES


def verify_member_episodes() -> bool:
    cfg = phase8_ecology_config()
    ok = True
    for template in _all_member_templates():
        tag = str(template["member_tag"])
        agent_type = str(template["agent_type"])
        eng = template.get("eng_program")
        rm = template.get("rm_program")
        programs = member_programs(
            agent_type,
            eng_program=str(eng) if eng is not None else None,
            rm_program=str(rm) if rm is not None else None,
        )
        mock = run_episode(
            cfg, seed=MEMBER_EPISODE_SEED, backend=MockIsolate(), programs=programs,
        )
        sub = run_episode(
            cfg, seed=MEMBER_EPISODE_SEED, backend=SubprocessIsolate(), programs=programs,
        )
        match = (
            mock.digests["combined"] == sub.digests["combined"]
            and mock.deploy_count == sub.deploy_count
        )
        ok = ok and match
        status = "PASS" if match else "FAIL"
        print(
            f"member {tag}: {status} "
            f"(deploy={mock.deploy_count}, combined={mock.digests['combined'][:12]}...)"
        )
    return ok


def verify_selection_trajectory() -> bool:
    members = sample_initial_population(population_size=SELECTION_POPULATION)
    mock_traj = run_selection_loop(
        members,
        n_generations=SELECTION_GENERATIONS,
        n_episodes_per_member=SELECTION_EPISODES,
        backend_factory=MockIsolate,
        progress=False,
    )
    sub_traj = run_selection_loop(
        members,
        n_generations=SELECTION_GENERATIONS,
        n_episodes_per_member=SELECTION_EPISODES,
        backend_factory=SubprocessIsolate,
        progress=False,
    )
    mock_json = json.dumps(trajectory_to_dict(mock_traj), sort_keys=True)
    sub_json = json.dumps(trajectory_to_dict(sub_traj), sort_keys=True)
    ok = mock_json == sub_json
    print(
        f"selection loop ({SELECTION_POPULATION} members, "
        f"{SELECTION_GENERATIONS} gens): {'PASS' if ok else 'FAIL'}"
    )
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 8 mock/subprocess isolate parity")
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Member single-episode checks only (skip selection loop)",
    )
    args = parser.parse_args()

    members_ok = verify_member_episodes()
    traj_ok = True if args.smoke else verify_selection_trajectory()
    overall = members_ok and traj_ok
    print(f"\noverall: {'PASS' if overall else 'FAIL'}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
