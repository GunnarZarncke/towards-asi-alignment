# 2026-06-30 — Embedded toy methodology parity + ontology decoupling

## Trigger
User asked to bring embedded-simulation to toy-simulation methodology parity and how to avoid coding to the ontology.

## Done
- Added `embedded_sim/methodology.py` (0.95 cert threshold, cal/test seeds, min certifiable, crux metrics, scenario→bridge map).
- Added `embedded_sim/stats.py` (hierarchical bootstrap on `evaluation.cci_status_correct`).
- Added `run_instrumentation_curve()` in `batch.py` (toy-parity cal 1–8 / test 11–20, frozen rules in payload).
- Fixed `minimum_certifiable_level` (handle levels only; passive `none` never certifiable).
- Upgraded `run_frozen_validation` (FROZEN_CAPTURE_RULES, optional all-levels, bootstrap).
- Red-team battery now reports `crux_metrics` (pass attempts vs false passes; `boundary_decouple` conditional rates).
- `episode_to_dict` includes `evaluation.cci_status_correct`.
- Removed scenario-name guards from `_instrument_capture_signal` / `_inferential_coupling_signal` in `cci_audit.py`.
- `run_suite.py`: `--curve`, `--full-frozen`; updated MD summaries.
- `PLAN.md`: methodology parity table + ontology-avoidance contract.
- `tests/unit/test_methodology.py`; **43 pytest pass**.

## Decisions
- Frozen validation defaults to single instrumentation level (medium) unless `--full-frozen` — embedded episodes are heavier than toy micro runs.
- `capture_mild` / `weak_not_captured` map to bridge `none` (held-out stress, not MB labels on audit path).
- Ontology labels remain in outer eval and scenario registry; audit detectors use structural telemetry only.

## Open / next
- Run full `--curve` to regenerate `results/embedded_instrumentation_curve.*`.
- Property-based tests without scenario names; real trace ingest hook.
- Postponed: MB5 gate policy, unit-scope vs global CCI for MB7d.

## Key paths
- `experiments/embedded-simulation/embedded_sim/methodology.py`
- `experiments/embedded-simulation/embedded_sim/batch.py`
- `experiments/embedded-simulation/PLAN.md` (ontology section)
- `experiments/embedded-simulation/run_suite.py`
- `experiments/embedded-simulation/results/OVERALL_SUMMARY.md`

## Also in this commit (parity suite)
- `run_suite.py`, `embedded_llm/`, `write_overall_summary.py`, batch results artifacts.
- See [2026-06-30-embedded-parity-suite.md](2026-06-30-embedded-parity-suite.md).

## Commits
- (pending — user requested commit at session end)
