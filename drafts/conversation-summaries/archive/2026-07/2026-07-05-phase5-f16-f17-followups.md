# 2026-07-05 — Phase 5: F-16/F-17 follow-ups

## Trigger

User provided the pre-registered plan `f-16_f-17_follow-ups_79e7bf4e.plan.md`
(todos already created) and asked to implement it end-to-end in
`experiments/goal-agent-simulation/`, without editing the plan file, marking
todos in-progress as work proceeded, and not stopping until all were
complete. Motivation: Phase 4 (previous session) closed with two mixed/
negative findings — F-16 (light-tier honest-twin composite gap runs the
wrong direction in 3/4 repertoires) and F-17 (the escalation ladder's
query-and-disclose pathway was never once decisive) — both diagnosed from
mechanism reasoning but not directly tested.

## Done

- **Part A (F-16 diagnosis test)**: `light_deception_composite` — a new,
  additive function in `goal_sim/detectors.py` (equal-weight mean of
  `d1_score`/`d1b_score` only, `d2_score` excluded; `score_detectors` and
  every existing detector untouched). Per-detector honest-twin gap
  decomposition (`d1`, `d1b`, `d2`, `light_deception`) computed on the
  identical Phase 4b sampling (legacy, round1-3; 30 configs x 8 seeds).
- **Part B (F-17 fix)**: `select_query_steps_v2` in `goal_sim/escalation.py`
  — a fixed three-signal priority order (S1 = v1's own signal; S2 = `d2`'s
  overt probe-noncompliance signal; S3 = a claim with no active
  correction), filling the `k`-step budget from S1 before falling through
  to S2 then S3. `run_escalation` gained an explicit `query_selector`
  parameter defaulting to `select_query_steps` (v1), so no existing caller's
  behavior changes. A queryability diagnostic (fraction of episodes with
  >= 1 queryable step under v1 vs. v2, independent of the screen-score
  gate) computed per repertoire.
- **Runner**: `run_phase5_followups.py` — full pre-registration in its
  docstring (written before the first run), both batteries (Part A on
  legacy/round1-3, Part B on legacy/round1-4), v1's RNG stream identical to
  Phase 4c's (`f"{config_id}:{seed}"`) so its numbers double as a
  cross-check against the frozen `phase4_escalation.json`; v2 uses an
  independent stream. Artifacts: `results/phase5_followups.{json,md}`.
- **Tests**: `tests/test_phase5.py` (11 new unit tests) — v2 selector
  priority-order behavior on synthetic projections (S1 before S2 before S3,
  dedup across signals, the exact round-4-style probe-noncompliance case
  v1 misses but v2 catches); `light_deception_composite` arithmetic and its
  F-16-mechanism zero case; regression checks that `select_query_steps`
  (v1) and `score_detectors` (incl. `d2` in its light composite) are
  unchanged. Full suite: 87 tests, all green.
- **`results/FINDINGS.md`**: F-19 (positive — confirms F-16's diagnosis
  exactly: `d2`'s gap is negative and largest-magnitude in all four
  repertoires, `d1`/`d1b` gaps non-negative, `light_deception_composite`'s
  gap positive in all four) and F-20 (mixed — v2 fixes queryability
  everywhere, including round 4's 1.25% → 100%; 2 of 3 pre-registered
  round-4 predictions confirmed (nonzero queried steps; severity separates
  by verdict); the twin-false-positive prediction is FALSIFIED for round 4
  (twin verdict-true rate 0.0708 > agent's 0.0542) — diagnosed as the same
  F-16 mechanism recurring one layer up, since v2's S2 reuses `d2`'s exact
  signal and `twins.py`'s frozen rule does not transform `responses`).
  Also recorded a reproducibility footnote: re-running the unmodified,
  pre-existing `run_phase4_escalation.run_repertoire("round3")` today gives
  numbers close to but not identical to the frozen `phase4_escalation.json`
  snapshot (0.2333/2.9107 vs. the recorded 0.2833/2.9265) — reproducible
  and stable across repeated runs today, so not new nondeterminism, but not
  investigated further (out of this plan's scope; frozen artifacts are not
  touched). Legacy/round1/round2/round4 all reproduce exactly.
- **Docs**: `README.md` (new "Phase 5" section + run-instructions line),
  `../embedded-simulation/MILESTONE-v5-goal-agents.md` (new Phase 5
  paragraph after the Phase 4 one).

## Decisions

- **`select_query_steps` (v1) kept byte-identical, not replaced**:
  `run_escalation` takes the selector as an explicit parameter rather than
  branching internally, so every existing caller (including
  `run_phase4_escalation.py`, never re-run this session) is unaffected by
  construction, not by convention.
- **`d2` not "fixed"**: per the plan, F-16's finding is that `d2` does its
  documented job (visible probe noncompliance) correctly — the problem is
  reusing that exact signal as a proxy for honesty elsewhere (the light
  composite in F-16; `select_query_steps_v2`'s S2 in F-20). Nothing in `d2`
  itself, its threshold, or `score_detectors` was changed.
- **Twin false-positive falsification reported, not hidden or re-tuned**:
  prediction (c) failing for round 4 under v2 is the most interesting
  result in Part B — it shows F-17's fix inherits F-16's known limitation
  rather than sidestepping it, which is itself evidence about *why* a
  behavior-based query signal is not automatically a good proxy for
  honesty, even when it succeeds at its narrower stated goal (finding
  something to ask about).
- **Reproducibility drift on round3 recorded, not chased**: confirmed (by
  rerunning the original, unmodified Phase 4c code three times) that this
  is stable today, not caused by anything changed this session, and not
  something the plan authorized touching (`phase4_escalation.md` is a
  frozen snapshot) — noted transparently so a future session does not
  mistake it for a new Phase 5 bug.

## Open / next

- The `responses`-side twin transform F-20 point 4 identifies as a
  candidate fix (twins currently inherit the original action's unmodified
  response options) is explicitly left open — `twins.py`'s rule is frozen
  and schema-only by its own Phase 4b pre-registration; changing it is a
  new pre-registration decision, not a patch to make after seeing this
  result.
- An S2 variant reading something other than `d2`'s exact structural
  signal (to avoid inheriting its honesty/visible-compliance conflation)
  is a candidate follow-up, not attempted.
- The round3 `run_phase4_escalation.py` reproducibility drift (frozen
  artifact vs. current code, ~0.05 on `escalated_rate`) is unexplained;
  worth a dedicated look if a future session touches `run_phase4_escalation.py`
  or its dependencies again.

## Key paths

- `experiments/goal-agent-simulation/goal_sim/detectors.py` —
  `light_deception_composite` (bottom of file).
- `experiments/goal-agent-simulation/goal_sim/escalation.py` —
  `select_query_steps_v2`, the `query_selector` parameter on
  `run_escalation` (module docstring has the full priority-order
  pre-registration).
- `experiments/goal-agent-simulation/run_phase5_followups.py` — both
  batteries, pre-registration docstring.
- `experiments/goal-agent-simulation/results/FINDINGS.md` F-19/F-20.
- `experiments/goal-agent-simulation/tests/test_phase5.py`.

## Commits

- (none this session; changes left uncommitted per AGENTS.md — stage only
  what is explicitly authorized)
