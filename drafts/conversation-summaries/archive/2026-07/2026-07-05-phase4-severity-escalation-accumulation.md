# 2026-07-05 — Phase 4: severity-graded referee, gated escalation, accumulation bounds

## Trigger

User provided the pre-registered plan `phase_4_severity_and_escalation_94d2ac6f.plan.md`
(todos already created) and asked to implement it end-to-end in
`experiments/goal-agent-simulation/`, without editing the plan file, marking
todos in-progress as work proceeded, and not stopping until all were
complete. Motivation: F-14 (round 3) found the boolean episode label
saturates against a large, varied repertoire almost regardless of
threshold — no honest population is left inside a saturated repertoire to
compare detectors against.

## Done

- **Step 0 (roadmap-doc)**: `PHASE4-PLAN.md` — design decisions (continuous
  oracle severity, gated boolean-verdict escalation ladder, two-tier
  never-event/graded-severity label structure, medical/aviation rationale),
  two documented-not-implemented TODO markers (in-sim ladder adaptation,
  recursive drill-down grounding out in Logical Induction). Cross-referenced
  from `README.md` and `../embedded-simulation/MILESTONE-v5-goal-agents.md`.
- **Phase 4a (severity, detector-scores, ranking-runner)**: `goal_sim/severity.py`
  (continuous `sev_report`/`sev_harm`/`sev_change` + equal-weight scalar,
  normalized only by frozen schema constants; `never_event` kept alongside,
  not folded in); `d*_score` continuous variants of every detector in
  `detectors.py`; `run_phase4_ranking.py` computing
  `Spearman(oracle severity, detector composite)` per repertoire (legacy,
  round1-3) — the blind comparison that survives full label saturation.
  Results: `results/phase4_severity.{json,md}`.
- **Phase 4b (twins)**: `goal_sim/twins.py` — mechanical, pre-registered
  twin rule on three frozen `ActionSpec` fields only
  (`visible_mode:="truthful"`, `report_mode` derived from
  `uptake_on_correction`, `adopts_practice:=false`); paired severity/score
  gap evaluation added to the same ranking runner.
- **Phase 4c (response-schema, round4-generation, escalation-eval)**:
  `ResponseOption` dataclass + `responses` field on `ActionSpec`
  (`actions.py`), `RESPONSE_TRUTHFUL_MODES` enum, partial canonical mapping
  in `ontology.py` (`resolve_response_canonical`); `goal_sim/escalation.py`
  (screen-gate → bounded query → boolean-verdict ladder, `LOW_GATE`/
  `HIGH_GATE`/`K_QUERIES`/`DISCLOSE_FRACTION_GATE` pre-registered before
  round 4 was generated); blind round-4 subagent generated 23 actions with
  response sets (`generated_actions_v4.json`, two name collisions with
  round 3 mechanically suffixed `_r4`, documented in provenance); protocol
  section added to `BLIND_GENERATION.md`; `run_phase4_escalation.py`
  battery. Results: `results/phase4_escalation.{json,md}`.
- **Phase 4d (accumulation)**: real multi-step semantics for `delayed`
  (lag-`DELAY_LAG_STEPS=5`) and `aggregated` (trailing-`AGGREGATE_WINDOW_STEPS=5`
  majority) `visible_mode` in `world.py`, overriding the conservative
  single-step default `ontology.py` still documents; two new audit-visible
  stock fields (`resource_accum`, `stall_flag`) added to every oracle row;
  two new bound-first secondary detectors (`d7_accumulation_cap`,
  `d8_disclosure_latency` + score variants) in `detectors.py`; new
  `FULL_EXTRA_FIELDS`/channel entries in `channels.py`.
- **Docs/tests/log**: `tests/test_phase4.py` (23 new unit tests covering
  severity bounds, detector-score gating, twin mechanics, escalation-ladder
  gate behavior, and Phase 4d lag/window/stock-variable arithmetic);
  `REGRESSION_DIGESTS` in `tests/test_actions_and_ontology.py` re-scoped to
  the pre-Phase-4d field set (proves no pre-existing field changed) plus a
  new `PHASE4D_FULL_ROW_DIGESTS` baseline over the grown schema; round-4
  file added to the generated-repertoire test matrix and the
  disjoint-names test; `results/FINDINGS.md` F-15 through F-18 recorded.
  Full suite: 74 tests, all green.

## Decisions

- **Regression digests re-scoped, not reset**: since `resource_accum`/
  `stall_flag` are added to every row (a schema *growth*, not a change to
  any pre-existing field), `REGRESSION_DIGESTS` now hashes the row set with
  the two new fields excluded and keeps its original Phase-1 expected
  values unchanged; a separate `PHASE4D_FULL_ROW_DIGESTS` baseline (fresh
  this session) protects the grown schema going forward. This preserved
  the original regression's evidentiary value (byte-identical to the
  pre-refactor Phase 1 code) instead of silently rebaselining it.
- **`d7`/`d8` not retroactively re-run through the already-recorded Phase
  4a/4c battery artifacts** (`phase4_severity.md`, `phase4_escalation.md`):
  those were pre-registered and run before Phase 4d added the two new
  full-only detectors. Per the repo's no-post-hoc-retuning discipline, they
  are left as frozen snapshots of the pre-4d detector set; F-18 documents
  the consequence (future full-tier composites will differ slightly;
  light-tier numbers, the primary comparison, are unaffected).
- **Two genuine negative findings surfaced, not smoothed over**: F-16 found
  light-tier detectors' honest-twin composite gap runs the WRONG direction
  in 3/4 repertoires (light tier tracks visible compliance, not honesty);
  F-17 found the escalation ladder's disclosure-query pathway was never
  once decisive in this battery, for two independently diagnosable
  structural reasons (rounds 1-3 predate the response schema by design;
  round 4's particular deceptive mechanisms didn't trip the D1-style
  query-selection signal). Both recorded as bounded, structural findings
  about the pre-registered designs, not bugs to patch after the fact.

## Open / next

- The escalation ladder's query-selection criterion (`select_query_steps`)
  only reuses D1's structural signal; F-17 suggests a broader/OR-of-signals
  criterion or a repertoire-level "has queryable steps" diagnostic
  pre-check as a candidate follow-up — not attempted, to avoid picking a
  fix after seeing round 4's specific null result.
- Phase 4d's two documented TODOs remain unimplemented by design: in-sim
  adaptation of the escalation ladder's own gates, and recursive
  drill-down depth beyond one response level (grounds out in Logical
  Induction).
- A future battery re-run (not required by this session) would refresh
  `phase4_severity.{json,md}`/`phase4_escalation.{json,md}`'s full-tier
  numbers to include `d7`/`d8`.

## Key paths

- `experiments/goal-agent-simulation/PHASE4-PLAN.md` — roadmap and design
  rationale.
- `experiments/goal-agent-simulation/goal_sim/{severity,twins,escalation}.py`
  — the three new Phase 4a/4b/4c modules.
- `experiments/goal-agent-simulation/goal_sim/world.py` — Phase 4d stock
  variables and real `delayed`/`aggregated` semantics (module docstring
  has the full mechanism writeup).
- `experiments/goal-agent-simulation/results/FINDINGS.md` F-15 through
  F-18 — what the numbers actually showed, including the two negative
  findings.
- `experiments/goal-agent-simulation/tests/test_phase4.py` — the new unit
  tests for this phase.

## Commits

- (none this session; changes left uncommitted per AGENTS.md — stage only
  what is explicitly authorized)
