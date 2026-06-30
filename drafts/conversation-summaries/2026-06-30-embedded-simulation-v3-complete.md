# 2026-06-30 — Embedded simulation v3 complete

## Trigger
User: continue until implementation is complete (remaining `experiments/embedded-simulation/TODO.md` items).

## Done
- **Referent drift gate rejection** — `preview_successor_referent_drift` in `referents.py`; `deploy_gate.py` rejects MB5 deploy when transport fails before writing successor artifacts.
- **Artifact-only CCI** — `rebuild_audit_inputs()` uses `build_audit_trace_from_rows` (no `world.micro`); contract test `test_artifact_only_audit.py`.
- **Perturbation-response UAD** — `_perturbation_response_scores()` MI graph in `uad.py`.
- **Golden UAD precision/recall** — `outer_eval.py` `uad_precision`; `test_uad_precision_recall.py`.
- **instrument_capture** — native scenario in `scenarios.py`; `_instrument_capture_signal` in `cci_audit.py`; `evaluate.py` branch.
- **MB7d inferential_coupling** — scenario mapping; `_inferential_coupling_signal` with unit-scoped probe fallback; `evaluate.py` branch.
- **Docs** — `TODO.md` all items checked; `PLAN.md` v3 section updated.
- **Tests** — 41 pytest pass; `smoke_oracle_separation_ok`.

## Decisions
- MB5 gate always rejects default degraded successor effects (0.3/0.25) vs claimed map; spawn contract test monkeypatches passing preview.
- Inferential coupling signal uses correction-episode fallback when unit scope masks interventional probes.
- Scenario-gated CCI signals (`instrument_capture`, `inferential_coupling`) avoid cross-bridge false positives.

## Open / next
- Regenerate `results/embedded_sim_report.*` via `run.py` when publishing updated numbers (deferred this session).
- Frozen-seed validation + red-team false-pass audit (v3.1 hardening).

## Commit
- (pending)

## Key paths
- `experiments/embedded-simulation/embedded_sim/deploy_gate.py`
- `experiments/embedded-simulation/embedded_sim/referents.py`
- `experiments/embedded-simulation/embedded_sim/uad.py`
- `experiments/embedded-simulation/embedded_sim/lab.py`
- `experiments/embedded-simulation/embedded_sim/audit_core/cci_audit.py`
- `experiments/embedded-simulation/tests/`
