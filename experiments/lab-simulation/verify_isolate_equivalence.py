#!/usr/bin/env python3
"""Verify MockIsolate and SubprocessIsolate agree byte-for-byte across a
seed sweep, and record a timing benchmark to the isolate cost ledger
(read by report_isolate_cost.py; summarized in DESIGN.md).

Usage: python3 verify_isolate_equivalence.py [n_seeds]
"""

from __future__ import annotations

import sys

from lab_sim.isolate import MockIsolate, SubprocessIsolate
from lab_sim.isolate_cost import append_ledger
from lab_sim.isolate_smoke import run_isolate_episode


def main() -> int:
    n_seeds = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    mock_timings = []
    sub_timings = []
    all_ok = True
    for seed in range(n_seeds):
        mock_digest, mock_timing = run_isolate_episode(MockIsolate(), seed=seed)
        sub_digest, sub_timing = run_isolate_episode(SubprocessIsolate(), seed=seed)
        mock_timings.append(mock_timing)
        sub_timings.append(sub_timing)
        status = "PASS" if mock_digest == sub_digest else "FAIL"
        if status == "FAIL":
            all_ok = False
        print(f"seed={seed}: {status} (combined={mock_digest['combined'][:12]}...)")

    append_ledger(mock_timings, label="verify_isolate_equivalence:mock")
    append_ledger(sub_timings, label="verify_isolate_equivalence:subprocess")

    mock_total = sum(t.total_seconds for t in mock_timings)
    sub_total = sum(t.total_seconds for t in sub_timings)
    print(f"\nmock backend:       {mock_total:.4f}s total over {n_seeds} episodes ({mock_total / n_seeds:.5f}s/ep)")
    print(f"subprocess backend: {sub_total:.4f}s total over {n_seeds} episodes ({sub_total / n_seeds:.5f}s/ep)")
    print(f"\noverall: {'PASS' if all_ok else 'FAIL'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
