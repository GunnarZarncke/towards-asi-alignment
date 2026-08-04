#!/usr/bin/env python3
"""Small handle-UAD smoke run on CIL's basin_stability (ET-2 follow-up).

Not a scored battery — a first look at whether freeze-probe dependency
scores are (a) nonzero at all, unlike GL-87's flat passive-UAD zero, and
(b) diffuse (every agent affects every other, consistent with the shared
resource channel) or structured (some pairs stand out). See
REPRODUCTION.md §14 item 1 and graded_lab/external/cil_handle_uad.py.

Run with the CIL venv's interpreter:
    external/cil/.venv/bin/python3 scripts/run_et2_handle_uad_smoke.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from graded_lab.external.cil_handle_uad import (  # noqa: E402
    cross_seed_null_rate,
    dependency_matrix_from_episode,
    run_baseline_and_freeze_episodes,
)

N_AGENTS = 6
N_ADVERSARIAL = 1
MECHANISM = "pdd"
T = 200
SEEDS = [0, 1, 2]


def main() -> None:
    t0 = time.time()
    episodes = []
    for i, seed in enumerate(SEEDS):
        print(f"[{i + 1}/{len(SEEDS)}] running baseline + {N_AGENTS} freeze probes at seed={seed}...", flush=True)
        ep = run_baseline_and_freeze_episodes(
            mechanism=MECHANISM,
            n_agents=N_AGENTS,
            n_adversarial=N_ADVERSARIAL,
            seed=seed,
            T=T,
        )
        episodes.append(ep)
        print(f"    done ({time.time() - t0:.1f}s elapsed)", flush=True)

    null_rate = cross_seed_null_rate(episodes)
    print(f"\ncross-seed baseline-vs-baseline action-diff rate (null): {null_rate:.4f}")

    matrices = [dependency_matrix_from_episode(ep) for ep in episodes]
    n = N_AGENTS
    mean_matrix: dict[tuple[int, int], float] = {}
    for source in range(n):
        for target in range(n):
            if source == target:
                continue
            vals = [m[(source, target)] for m in matrices]
            mean_matrix[(source, target)] = sum(vals) / len(vals)

    all_vals = list(mean_matrix.values())
    print(f"mean freeze-induced action-diff rate over all ordered pairs: "
          f"{sum(all_vals) / len(all_vals):.4f} (min={min(all_vals):.4f}, max={max(all_vals):.4f})")
    print(f"(for comparison, cross-seed null was {null_rate:.4f})")

    print("\nper-source mean effect on all other agents (source -> mean_target_diff_rate):")
    for source in range(n):
        row = [mean_matrix[(source, t)] for t in range(n) if t != source]
        print(f"  agent_{source}: {sum(row) / len(row):.4f}  (min={min(row):.4f}, max={max(row):.4f})")

    out = {
        "mechanism": MECHANISM,
        "n_agents": N_AGENTS,
        "n_adversarial": N_ADVERSARIAL,
        "T": T,
        "seeds": SEEDS,
        "cross_seed_null_rate": null_rate,
        "mean_dependency_matrix": {f"{s}->{t}": v for (s, t), v in mean_matrix.items()},
        "per_seed_dependency_matrices": [
            {f"{s}->{t}": v for (s, t), v in m.items()} for m in matrices
        ],
    }
    out_path = Path(__file__).resolve().parents[1] / "results" / "et2_handle_uad_smoke.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(f"\nwrote {out_path}")
    print(f"total wall time: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
