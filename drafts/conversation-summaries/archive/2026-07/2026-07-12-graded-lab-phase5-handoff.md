# 2026-07-12 — Graded lab Phase 5 freeze complete

## Trigger

Continue implementation after review-correction pass: complete Phase 5 referee
port (events, detectors, twins, escalation, programs) and freeze gate.

## Done

- **Phase 5 referee port:** `events.py`, `detectors.py` (five families),
  `twins.py`, `escalation.py`; agent programs `walk_pipeline`,
  `inflate_pipeline`, `honest_twin`; `INFLATE_HAZARD_DELTA` in
  `agent_visible/ontology.py`.
- **Pipeline program fix:** `walk_pipeline` / `inflate_pipeline` now request
  capabilities via the published affordable set and accept enriched
  `draft_report` args (`world.py` `_pipeline_trigger_compatible`).
- **Freeze gate:** `CODE_VERSION` `graded-lab-0.6.0`; Phase 5 constants in
  `DESIGN.md`; `results/FINDINGS.md` G-8; `README.md` / `PLAN.md` status
  updated to Phases 0–5 done.
- **Tests:** 18 new Phase 5 tests; **78 tests green**; 5-seed mock/subprocess
  isolate equivalence green.

## Decisions

- Escalation screen stays full-tier-only (misreporting blind below deep); test
  uses **seed 4** where `access_integrity` friction lands in the
  `(SCREEN_LOW_GATE, SCREEN_HIGH_GATE)` band.
- Detectors/escalation tests use deceptive engineer + honest other roles so
  pipeline completes while inflate still diverges at deep tier.

## Open / next

1. **Phase 6** blind behavior features.
2. **Phase 3b** carrier calibration battery.
3. **Phase 7a–7c** UAD-backed BIQ + calibration.

## Key paths

- `experiments/graded-lab-simulation/graded_lab/oracle_only/{events,detectors,twins,escalation}.py`
- `experiments/graded-lab-simulation/graded_lab/agent_visible/{programs,policy,ontology}.py`
- `experiments/graded-lab-simulation/graded_lab/world_visible/world.py`
- `experiments/graded-lab-simulation/tests/test_{events,detectors,twins,escalation}.py`
- `experiments/graded-lab-simulation/results/FINDINGS.md` (G-8)

## Commits

- None (user did not request).
