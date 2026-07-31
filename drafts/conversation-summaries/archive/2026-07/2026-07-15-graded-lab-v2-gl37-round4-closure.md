# Graded lab v2: GL-37 standing fix, round 4, V2-2 closure (C3 failure)

**Date:** 2026-07-15
**Trigger:** User approved combined plan: fix engine to honor `standing_mechanics.initial` for v2-shaped substrates, re-score rounds 1–3, spend round 4 only if C3 alone still fails (pass/fail only, physical isolation, no anchors).

## What was done

### GL-37 — engine completes pre-registered standing schema

- `standing_stock_for_role()` / `is_v2_shaped_ecology()` in `substrate.py`: v2 JSONs use `standing_mechanics.initial` as stock/cap; v1 path unchanged (preserves int vs float for digest pins).
- `CODE_VERSION` → **0.18.1**; `tests/test_config.py` updated.
- Re-scored clean rounds 1, 2', 3': **C1/C2/C4/C5 pass**, C3 fail (0.0 contention). C4 deploy 0.65 on all three.

### Round 4 (final clean round)

- Physical isolation (files stashed to `/tmp/graded_lab_blind_stash_*`, restored after grower).
- Feedback: `{C1: true, C2: true, C3: false, C4: true, C5: true}`.
- Grower (clean blinding) misread C3 as Part B structural (resource-flow completeness); left Part A unchanged (`shared_compute_slots: 3`). Part B: io/standing baseline flows + split `governed_capability_grant`.
- **Checker:** same as rounds 1–3' — C3 fail 0.0, C4 pass 0.65.

### V2-2 closure (GL-38)

- 4-round stopping rule: **no** `generated_ecology_v2.json` freeze; V2-3+ gated.
- Best partial ecology: round 3 Part A + structure (C4 interior after GL-37).

## Non-obvious decisions

- Did not add engine-interface anchors to round-4 brief (user-approved).
- Did not freeze round 4 as official ecology — Part A identical to round 3, C3 still fails.
- Contaminated rounds 2–3 remain archived and voided from budget.

## Open / next steps

- Program decision: V2-2b with brief/coherence iteration vs. accept C3 failure as Q1 gate result.
- Optional: contention-boundary investigation (`slots=2` + overlap knobs) for implementer diagnostics only.
- Q2/Q3 remain blocked on C1–C5-passing ecology per `PLAN_v2.md`.

## Key paths

- `results/FINDINGS.md` GL-37, GL-38
- `generated_ecology_v2_round4.*`
- `graded_lab/world_visible/substrate.py`

No commits this session.
