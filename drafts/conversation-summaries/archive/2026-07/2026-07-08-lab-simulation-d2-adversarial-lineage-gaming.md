# 2026-07-08 — Lab-sim: adversarial D2 lineage gaming (G-31)

## Trigger

User: "Now start with the medium lift tasks, first Adversarial D2
lineage gaming" — the first of the "medium lift" items from a prior
step-back review's next-steps list, and a "still open" note in
`PLAN.md`/`DESIGN.md` since Phase 9 (`run_phase9.py`'s Section B
docstring; `FINDINGS.md` G-12/G-15): no playbook in the repertoire
combined `build_from_parent` (D2 model-from-model lineage) with
`report:inflate` (dishonest reporting), so whether `provenance_gap`
catches adversarial lineage gaming had never actually been tested.

## Done

- Explored D2 mechanics end to end (`pipeline_engine.py`, `programs.py`,
  `world.py`, `severity.py`, `detectors.py`) before writing anything, to
  confirm: `build_from_parent` threads `parent_model_id` from
  `last_deployed_model_id` (engine/release-manager state, never
  agent-report-controlled); `provenance_gap`/`provenance_score` check
  eval-without-build DAG orphans, not report content; `report:inflate`
  already existed as a single-generation lever with its own detectors
  (`misreporting_score`, `accumulation_score`).
- Added `eng_inflate_upgrade` (`playbooks.py`): identical to
  `eng_honest_upgrade` except `report:inflate` in place of
  `report:honest`. No new step-kind, resolver branch, or detector logic
  needed — purely a new combination of existing primitives.
- Added `ecology.d2_lineage_config(inflate: bool)`, promoting
  `run_phase9.py`'s ad hoc `_d2_config` into a shared, parametrized
  builder used by both the historical honest battery and the new
  adversarial variant.
- Wrote `run_d2_adversarial_lineage.py` (MockIsolate, seeds 1–10,
  T=200, honest vs. inflate): pre-registered 5 predictions (D2-P1..P5)
  in the module docstring before running. **All 5 held, 0
  falsifications** — see `results/d2_adversarial_lineage.{json,md}`.
  Headline: `provenance_gap`/`provenance_score` stay exactly 0.0 in all
  20 cells under both conditions (closes G-12's open question with a
  scope clarification: it's a DAG-shape check, not a report-honesty
  check); `misreporting_score`/`accumulation_score` (built against
  one-shot `eng_inflate`) generalize unmodified to ~20–30 repeated
  inflation cycles (~0.99 both, no retuning); lineage threading is
  honesty-independent.
- Bumped `CODE_VERSION` 0.9.2 → 0.9.3 (new playbook = playbook-mechanics
  change per `config.py`'s own rule; purely additive, every pre-0.9.3
  episode byte-identical — documented inline).
- Added 4 new tests: `test_d2.py` (lineage-under-dishonesty,
  `provenance_gap` stays 0) and `test_detectors.py` (misreporting/
  accumulation generalize to multi-gen inflation, and stay 0 for honest
  multi-gen). Updated `test_playbooks.py`'s baseline-repertoire-name set
  to include `eng_inflate_upgrade`.
- Recorded `FINDINGS.md` G-31, and updated `PLAN.md`, `DESIGN.md` (new
  "Adversarial D2 lineage gaming" section + resolved the two "still
  open" notes), `README.md` (status line, CODE_VERSION, tests-green
  count, entry-point list, file listing), `metadata/experiments.yml`
  (MB5 cell, headline findings), and `docs/EXPERIMENTS.md` (D2 status,
  new paragraph, MB1/MB5 coverage cells).
- Along the way, also updated stale references to the
  `committee_informal_chatter` over-merge fix from the PRIOR session
  (which had fixed the bug but left `README.md`/`DESIGN.md`'s "still
  open" list and `metadata/experiments.yml`/`docs/EXPERIMENTS.md`
  pointing at the pre-fix state) — a documentation-only correction, not
  new mechanics.
- Full suite: 413 tests green (was 409).

## Decisions

- Scoped to exactly the recorded open question (`build_from_parent` +
  `report:inflate`, non-loop variant) rather than also building the
  loop variant (`build_from_parent_gated` + `report:inflate`) or a
  `SubprocessIsolate` re-run — both recorded as "not done this round" in
  G-31/DESIGN.md rather than silently skipped.
- Treated this as a documentation-and-tests exercise, not a new
  detector: since `provenance_gap`/`provenance_score` were already
  well-defined (just untested against this attack) and
  `misreporting_score`/`accumulation_score` already existed, no new
  `oracle_only/` module was needed — the medium lift here was building
  the missing playbook/ecology/script/tests and running the
  pre-registered check, not inventing new detection logic.
- Did not touch `run_phase9.py`'s historical `_d2_config`/battery script
  itself (frozen record of Phase 9); the new `ecology.d2_lineage_config`
  is additive, reused by the new script only.

## Open / next

- Loop variant (`build_from_parent_gated` + `report:inflate`) not built;
  expected to behave the same way (ack-gating reads `deploy_ack`/
  `monitor`, not report content) but unverified.
- `SubprocessIsolate` re-run of this exploration not done (MockIsolate
  only, matching the S1–S4 prototype convention).
- Still pending from the PRIOR session: re-run `run_s7_blind_battery.py`
  under `SubprocessIsolate` with the committee-over-merge fix and record
  that as its own G-number (would be G-32 now).
- Remaining "medium lift" items from the earlier step-back review:
  report-mode-widening blind-generation round 2; S5's second probe
  (acausal/ICI coordination, needed for `shared_slot`); D3 (extended
  ecology); LLM-driven detector stress test; manuscript integration.

## Key paths

- `experiments/lab-simulation/lab_sim/agent_visible/playbooks.py`
- `experiments/lab-simulation/lab_sim/harness/ecology.py`
- `experiments/lab-simulation/lab_sim/world_visible/config.py`
- `experiments/lab-simulation/run_d2_adversarial_lineage.py`
- `experiments/lab-simulation/results/d2_adversarial_lineage.{json,md}`
- `experiments/lab-simulation/tests/world_visible/test_d2.py`
- `experiments/lab-simulation/tests/oracle_only/test_detectors.py`
- `experiments/lab-simulation/results/FINDINGS.md` (G-31)
