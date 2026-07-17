# Voided — v3 grower round 2 (blinding leak, GL-71)

**Do not use** for harvest sentences, ecology freeze, or successive-round
continuity. This is a **dead branch**, not round 2 of the active ≤4-round chain.

## What happened

Round 2 (2026-07-17) passed the full checker after the grower read
orchestrator-only file `runs/grower-v3-round1/check_result_round1.json`,
which contained `details_summary` (failing conflict pairs and metrics) —
**not** authorized grower feedback (`pass_fail_only()` only).

Implementer decision: void the round; successive rounds continue from
round 1 artifacts only. A clean round 2 was re-run after moving orchestrator
snapshots to `growth-orchestrator/` and stashing that directory during grower
launches (GL-72).

## Archived artifacts

- `generated_ecology_v3_round2.json` (+ rationale + knowledge base) — checker
  all-pass on 20 seeds, but **invalid** for protocol claims due to leak.
- Orchestrator snapshot preserved at
  `growth-orchestrator/v3/check_result_round2_voided.json` (gitignored).

See `REPRODUCTION.md` §3.1 and `results/FINDINGS.md` GL-71/GL-72.
