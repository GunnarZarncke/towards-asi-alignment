# 2026-06-29 — MB3/MB8 bridge scenarios

## Trigger
User asked to implement MB3 (`bearer_mismap`) and MB8 (`legitimacy_theater`) while LLM model sweep runs; also asked whether medium_handles certification requires protected/value-grounded handles and if that is simulable.

## Done
- **MB3 `bearer_mismap`:** harm on `bearer.infra`, human passive trace flat; audit `bearer_mismatch_detected` uses passive infra drop vs MB9 (no infra drop).
- **MB8 `legitimacy_theater`:** pref theater + lineage stall under interventions, honest rule channel; audit `legitimacy_theater_detected` (lineage stall + inflated probe reports) overrides MB4 capture path to `belowThreshold`.
- Schemas, simulator, observation (`passive_infra_bearer_level`, `correction_lineage_series`), cci_audit, evaluate, safety `failed_bridge` tags.
- `experiments/toy-simulation/mb3_mb8_diagnostic.py` → `experiments/toy-simulation/results/mb3_mb8_diagnostic.json` (seeds 11–20, T=1000).
- `experiments/toy-simulation/TODO.md` updated; handle-protection / `instrument_capture` note added.

## Diagnostic (seeds 11–20)
| Scenario | none | light | medium | strong |
|----------|------|-------|--------|--------|
| bearer_mismap | 100% | 0% (false-pass demo) | 100% | 100% |
| legitimacy_theater | 100% | 80% | 100% | 100% |

## Handle protection (answer)
- **Partially simulable today:** handles are truthful logs from micro; attacks are in dynamics (wrong bearer, lineage theater), not instrument rewrite.
- **Not yet simulable:** adversary directly patching `handle.*` while micro diverges — planned as `instrument_capture` (MB4/MB9 commutation). Strong_handles cross-check vs passive reconstruction is the next step.

## Open / next
- `instrument_capture` scenario for handle-protection stress.
- Optional: re-run 4-level curve with new held-out scenarios.
- LLM model sweep (parallel).

## Key paths
- `experiments/toy-simulation/multiresolution_alignment_sim/simulator.py`
- `experiments/toy-simulation/multiresolution_alignment_sim/cci_audit.py`
- `experiments/toy-simulation/mb3_mb8_diagnostic.py`
- `experiments/toy-simulation/results/mb3_mb8_diagnostic.json`
