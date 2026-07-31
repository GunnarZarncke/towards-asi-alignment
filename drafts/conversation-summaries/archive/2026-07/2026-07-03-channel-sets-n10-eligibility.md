# 2026-07-03 — Channel-set registry + N-10 eligibility gating (Part B)

## Trigger
User asked to continue the finer-handles plan after Part A/D memory work; Part B (channel-sets / N-10 root fix) was next. Session ended with powered evaluation and commit.

## Done
- **`embedded_sim/audit_core/channel_sets.py`:** telemetry channel bundles per level; per-detector `required_channels`; `certification_pass_eligible`.
- **`InstrumentationLevel` extended:** `light_plus_handles`, `medium_minus_handles` in `audit_core/schemas.py` and `schemas_embedded.py`.
- **`observation.py`:** handle emission driven by channel-set registry (both `build_audit_trace` and `build_audit_trace_from_rows`).
- **`structural_signals.py`:** replaced `GROUNDING_INSTRUMENTATION` with `detector_channels_available`.
- **`calibration.py`:** `passes` requires full medium channel bundle (N-10 eligibility fix).
- **Tests:** `tests/unit/test_channel_sets.py`, `tests/contract/test_channel_eligibility.py` — 195 passed, 1 skipped.
- **Powered eval:** `eval_channel_eligibility.py` → `results/channel_eligibility_eval.json` (384 episodes, 8 seeds; ~16 min). Partial levels: 0/48 capture false-passes; medium/strong honest pass 0.875.
- **N-10 postscript** in `results/NEGATIVE_RESULTS.md` (root cause, fix, eval numbers).

## Decisions
- Eligibility rule: partial handle levels never receive `passes`; priced cost is honest agents also uncertifiable until medium bundle.
- `light_plus`/`medium_minus` are verdict-identical to `light` under current gate — flag-level detection differs (contract tests) but not graded certification yet.
- Full six-level frozen validation / instrumentation curve deferred (~40–80 min).

## Open / next
1. Re-run frozen validation + instrumentation curve across six levels.
2. Part C: writer attestation on `handle.hardware_tag` (N-9).
3. Remaining Part D handles + persistence probe.

## Key paths
- `experiments/embedded-simulation/embedded_sim/audit_core/channel_sets.py`
- `experiments/embedded-simulation/results/channel_eligibility_eval.json`
- `experiments/embedded-simulation/eval_channel_eligibility.py`

## Commits
- `2c64569` — Fix N-10 blind passes with channel-set eligibility gating.
