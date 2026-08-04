#!/usr/bin/env python3
"""Verify MockIsolate and SubprocessIsolate agree byte-for-byte across a
seed sweep, and record isolate + episode wall-time benchmarks to ledgers
(read by ``report_isolate_cost.py``; summarized in DESIGN.md).

Usage: python3 verify_isolate_equivalence.py [n_seeds]
"""

from __future__ import annotations

import sys

from graded_lab.harness.episode_cost import append_ledger as append_episode_ledger
from graded_lab.harness.isolate import MockIsolate, SubprocessIsolate
from graded_lab.harness.isolate_cost import append_ledger
from graded_lab.harness.isolate_smoke import run_isolate_episode


def main() -> int:
    n_seeds = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    mock_timings = []
    sub_timings = []
    mock_episodes = []
    sub_episodes = []
    all_ok = True
    for seed in range(n_seeds):
        mock_digest, mock_timing, mock_episode = run_isolate_episode(
            MockIsolate(), seed=seed
        )
        sub_digest, sub_timing, sub_episode = run_isolate_episode(
            SubprocessIsolate(), seed=seed
        )
        mock_timings.append(mock_timing)
        sub_timings.append(sub_timing)
        mock_episodes.append(mock_episode)
        sub_episodes.append(sub_episode)
        ok = mock_digest["combined"] == sub_digest["combined"]
        all_ok = all_ok and ok
        status = "PASS" if ok else "FAIL"
        print(f"seed={seed}: {status} (combined={mock_digest['combined'][:12]}...)")

    append_ledger(mock_timings, label="verify_isolate_equivalence:mock")
    append_ledger(sub_timings, label="verify_isolate_equivalence:subprocess")
    append_episode_ledger(mock_episodes, label="verify_isolate_equivalence:mock")
    append_episode_ledger(sub_episodes, label="verify_isolate_equivalence:subprocess")

    mock_iso = sum(t.total_seconds for t in mock_timings)
    sub_iso = sum(t.total_seconds for t in sub_timings)
    mock_wall = sum(t.wall_seconds for t in mock_episodes)
    sub_wall = sum(t.wall_seconds for t in sub_episodes)
    print(
        f"\nmock backend:       isolate {mock_iso:.4f}s, "
        f"episode wall {mock_wall:.4f}s over {n_seeds} episodes "
        f"({mock_wall / n_seeds:.5f}s/ep wall)"
    )
    print(
        f"subprocess backend: isolate {sub_iso:.4f}s, "
        f"episode wall {sub_wall:.4f}s over {n_seeds} episodes "
        f"({sub_wall / n_seeds:.5f}s/ep wall)"
    )
    print(f"\noverall: {'PASS' if all_ok else 'FAIL'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
