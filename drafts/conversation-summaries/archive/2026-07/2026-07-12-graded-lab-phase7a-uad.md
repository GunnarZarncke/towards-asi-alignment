# 2026-07-12 — Graded lab Phase 7a UAD over primitive traces

## Trigger

Continue implementation after Phase 6 blind behavior features (uncommitted
0.7.0 work verified green at session start).

## Done

- **Phase 7a UAD port:** `primitive_trace.py`, `uad_passive.py`,
  `uad_partition.py`, `intervention_probes.py`, `intervention_diff.py`,
  `uad_intervention.py`.
- **Golden ecologies:** `harness/ecology.py` — `committee_config`,
  `communicator_pair_config`, `serial_pipeline_config` with oracle `units`
  on `EpisodeConfig`.
- **Programs:** `committee_reviewer`, `lab_communicator`; extended
  `_STEP_CAPABILITIES` for reviewer/release pipeline steps.
- **Freeze gate:** `CODE_VERSION` `graded-lab-0.8.0`; DESIGN §Phase 7a;
  `results/FINDINGS.md` G-10; README/PLAN status updated.
- **Tests:** 11 new UAD tests; **102 tests green**; suite ~96s (limit 120s);
  speed baselines refreshed.

## Decisions

- Graded UAD uses **affordable-primitive discipline** in test programs (custom
  communicate channels denied by host — not a discovery bug).
- Committee unit signal: shared **lab-channel co-activity** + optional
  `peer_review` (pipeline allows only one reviewer step completion).
- Intervention probes are **episode-level** `program_freeze` triples (no
  mid-tick overseer yet); `min_compensation=0.15` pre-registered.
- Phase 6 (0.7.0) changes remain in working tree alongside 7a (not committed).

## Open / next

1. **Phase 7b** UAD-backed ecology-BIQ (MI/CMI, retained-state proxy).
2. **Phase 7c** calibration battery + `run_phase7_calibration.py`.
3. **Commit** Phase 6 + 7a + session logs when requested.

## Key paths

- `experiments/graded-lab-simulation/graded_lab/oracle_only/{primitive_trace,uad_passive,uad_intervention,intervention_*}.py`
- `experiments/graded-lab-simulation/graded_lab/harness/ecology.py`
- `experiments/graded-lab-simulation/tests/test_{primitive_trace,uad_passive,uad_intervention}.py`
- `experiments/graded-lab-simulation/results/FINDINGS.md` (G-10)

## Commits

- None (user did not request).
