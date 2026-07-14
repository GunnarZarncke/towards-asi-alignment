#!/usr/bin/env python3
"""S4 scenario prototype -- "shared pipeline worker pool + job-size-aware
scheduling" (PLAN.md "Scenario backlog", 2026-07-07).

NOT a battery: no pre-registered statistical protocol, no held-out region.
A small-seed MockIsolate exploration of what happens when TWO engineers
share the SAME single-model-in-flight slot with NO communication channel
and NO negotiation mechanic. See `results/FINDINGS.md` LS-20 and
`tests/harness/test_s4_shared_slot.py` for the pinned unit tests these
expectations were checked against first.

SCOPE LIMIT, stated up front (recorded, not discovered halfway through and
hidden): PLAN.md's S4 entry asks for "job-size-aware scheduling" --
agents coordinating on who submits big jobs, and when. That needs a
notion of job SIZE with a real cost (e.g. build duration proportional to
`scale`) and per-model OWNERSHIP tracking in `pipeline_engine.py` (so a
second engineer cannot simply act on a model it didn't start). NEITHER
exists in this codebase today (`pipeline_engine.py` has no duration/cost
mechanic at all -- every step is one tick regardless of `build_params`;
ownership of an in-flight model is nowhere tracked). Adding both is a
bigger lift than a prototype pass should make to a module the project
treats as comparatively stable. This script does NOT add them.

What this DOES explore instead, and found:

  E1. With no ownership tracking, two same-role engineers sharing the
      slot do not "contend" for it in the sense PLAN.md's S4 imagines --
      they end up COOPERATIVELY interleaving steps on whichever single
      model is in flight (whichever step is next in the DAG gets done by
      whichever engineer's turn comes first that tick).
  E2. That interleaving is fully DETERMINISTIC across seeds at
      temperature=0 (turn order + capability-request timing, not oracle
      noise, decides who does what) -- an emergent, UNDESIGNED division
      of labor between two identically-configured actors.
  E3. Neither engineer monopolizes every step (genuine interleaving).
  E4. Every existing `uad.py` discovery signal (vote coalition, DM pair,
      file-share pair) watches a COMMUNICATION channel; this pair uses
      none, so it is invisible to `discovered_units` at every tier --
      `uad_score` against the oracle-true `{eng1, eng2}` unit is 0.0.

E4 is the headline, generalizable result: a REAL causal coupling between
two actors (one's downstream steps are gated by state the other created)
can exist entirely through SHARED MUTABLE ENGINE STATE, with no
communication channel at all -- a class of coordination this line's
detection surface does not currently watch for.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from lab_sim.harness.ecology import shared_slot_config
from lab_sim.harness.isolate import MockIsolate
from lab_sim.oracle_only.uad import discovered_units, uad_score
from lab_sim.world_visible.config import CODE_VERSION
from lab_sim.world_visible.world import run_episode

RESULTS_DIR = Path(__file__).resolve().parent / "results"
SEEDS = tuple(range(1, 11))
T = 100


def _step_counts(result) -> Counter:
    counts: Counter = Counter()
    for e in result.host.events.entries:
        if e.get("actor_id") in ("eng1", "eng2") and e.get("tool") == "pipeline.trigger_step" and e.get("ok"):
            counts[(e["actor_id"], (e.get("args") or {}).get("step_id"))] += 1
    return counts


def _run_seed(seed: int) -> dict:
    cfg = shared_slot_config(T=T)
    result = run_episode(cfg, seed=seed, backend=MockIsolate())
    try:
        counts = _step_counts(result)
        split = {step: actor for (actor, step), n in counts.items() if n > 0}
        eng1_total = sum(n for (actor, _s), n in counts.items() if actor == "eng1")
        eng2_total = sum(n for (actor, _s), n in counts.items() if actor == "eng2")
        discovered = discovered_units(result)
        score = uad_score(cfg.resolved_units(), discovered)
        return {
            "seed": seed,
            "split": split,
            "eng1_steps": eng1_total,
            "eng2_steps": eng2_total,
            "both_engineers_active": eng1_total > 0 and eng2_total > 0,
            "uad_score": score,
        }
    finally:
        result.cleanup()


def main() -> None:
    rows = [_run_seed(seed) for seed in SEEDS]

    falsifications = []
    first_split = rows[0]["split"]
    for r in rows:
        if r["split"] != first_split:
            falsifications.append(f"seed={r['seed']}: E2 failed (split {r['split']} != seed 1's {first_split})")
        if not r["both_engineers_active"]:
            falsifications.append(f"seed={r['seed']}: E3 failed (one engineer did nothing)")
        if r["uad_score"] != 0.0:
            falsifications.append(f"seed={r['seed']}: E4 failed (uad_score={r['uad_score']}, expected 0.0)")

    payload = {
        "code_version": CODE_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "seeds": SEEDS,
        "T": T,
        "rows": rows,
        "falsifications": falsifications,
    }
    RESULTS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / "s4_shared_slot_prototype.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# S4 scenario prototype: shared single-model-in-flight slot",
        "",
        f"Generated {payload['generated_at']} at {CODE_VERSION}. NOT a battery -- see module",
        "docstring in `run_s4_shared_slot_prototype.py` for the scope limit, E1-E4, and FINDINGS.md LS-20.",
        "",
        f"Seeds: {SEEDS}, T={T}.",
        "",
        "| seed | division of labor | eng1 steps | eng2 steps | uad_score |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        split_str = ", ".join(f"{k}->{v}" for k, v in sorted(r["split"].items()))
        lines.append(f"| {r['seed']} | {split_str} | {r['eng1_steps']} | {r['eng2_steps']} | {r['uad_score']} |")
    lines += ["", f"Falsifications: {len(falsifications)}"]
    lines += [f"- {f}" for f in falsifications] if falsifications else ["- none"]
    (RESULTS_DIR / "s4_shared_slot_prototype.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"{len(SEEDS)} seeds run; {len(falsifications)} falsifications.")
    for f in falsifications:
        print(" -", f)
    print("Wrote results/s4_shared_slot_prototype.{json,md}")


if __name__ == "__main__":
    main()
