#!/usr/bin/env python3
"""Run the ET-2a battery: CIL basin_stability episodes -> frozen passive UAD.

Must be run with the pinned CIL sibling checkout's venv, since episode
generation needs jax/jaxlib/cilib:

  cd experiments/graded-lab-simulation
  ./external/cil/.venv/bin/python3 scripts/run_et2_uad_battery.py \\
      --seeds-per-cell 10 --out results/et2a_uad_battery.json

Grid (PLAN_ET2.md ET2-0 freeze): mechanisms {pld, prd, pdd} x
adversarial_fraction {0.0, 0.1, 0.2, 0.3, 0.5} x 10 seeds/cell = 150 episodes
(+ 3 mechanisms x frac=0 already included above; 210 total per the plan's
"10/cell, 210 episodes" if a 7-fraction grid is used — see PLAN_ET2.md for
the exact frozen grid before a real run; this default grid is a placeholder
sized to match the plan's episode-count order of magnitude).

Prints per-cell progress as it runs (AGENTS.md long-running-task rule).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from graded_lab.external.cil_adapter import ET2_PROTOCOL_VERSION, run_basin_stability_episode  # noqa: E402
from graded_lab.external.cil_uad_score import evaluate_et2a_battery, score_episode  # noqa: E402

MECHANISMS = ("pld", "prd", "pdd")
ADVERSARIAL_FRACTIONS = (0.0, 0.1, 0.2, 0.3, 0.5)
N_AGENTS = 20
T_ROUNDS = 200


def _read_pin() -> str:
    pin_path = ROOT / "external" / "cil" / "PIN.txt"
    return pin_path.read_text(encoding="utf-8").strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds-per-cell", type=int, default=10)
    parser.add_argument("--mechanisms", nargs="*", default=list(MECHANISMS))
    parser.add_argument("--fractions", nargs="*", type=float, default=list(ADVERSARIAL_FRACTIONS))
    parser.add_argument("--n-agents", type=int, default=N_AGENTS)
    parser.add_argument("--rounds", type=int, default=T_ROUNDS)
    parser.add_argument("--out", type=Path, default=ROOT / "results" / "et2a_uad_battery.json")
    args = parser.parse_args()

    pin = _read_pin()
    cells = [(m, f) for m in args.mechanisms for f in args.fractions]
    total = len(cells) * args.seeds_per_cell
    print(f"[ET-2a] cil_pin={pin[:12]} cells={len(cells)} seeds/cell={args.seeds_per_cell} total_episodes={total}")

    scores = []
    done = 0
    start = time.time()
    for mechanism, frac in cells:
        n_adversarial = round(frac * args.n_agents)
        for seed_idx in range(args.seeds_per_cell):
            seed = seed_idx  # fixed per-cell seed range; re-pin bumps ET2_PROTOCOL_VERSION, not this
            episode = run_basin_stability_episode(
                mechanism=mechanism,
                n_agents=args.n_agents,
                n_adversarial=n_adversarial,
                seed=seed,
                T=args.rounds,
            )
            scores.append(score_episode(episode, adversarial_fraction=frac))
            done += 1
            elapsed = time.time() - start
            print(
                f"[{done}/{total}] mechanism={mechanism} frac={frac} seed={seed} "
                f"ari={scores[-1].ari_true:.3f} p95={scores[-1].permutation_null_p95:.3f} "
                f"exceeds={scores[-1].exceeds_null} elapsed={elapsed:.1f}s"
            )

    results = evaluate_et2a_battery(scores)
    results["et2_protocol_version"] = ET2_PROTOCOL_VERSION
    results["cil_pin"] = pin
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    preds = results["predictions"]
    print(f"ET-2a P1 holds={preds['P1']['holds']} cells={preds['P1']['cells_passing']}/{preds['P1']['cells_total']}")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
