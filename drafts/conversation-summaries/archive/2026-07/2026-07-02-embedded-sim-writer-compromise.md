# 2026-07-02 — Embedded sim: writer-compromise + cross-stream checks

## Trigger
User: **Catch writer-compromise as discussed above** — deceptive emission at
write time (chained garbage in) needs cross-stream checks, not more integrity tech.

## Done
- **`cross_stream.py`** — compares correction `visible_action` to bearer
  `clinician_final_action` / `recommended_action` per step; mismatch ⇒
  `invalid_certificate` in `embedded_audit.py`.
- **`trace_emit.py`** — shared `commit_deploy_streams` / `build_workflow_rows`
  for trusted emitter and compromised re-emission (valid hash chain + manifest).
- **`redteam.py`** — strategies `writer_compromise` (sloppy: forged correction,
  stale bearers) and `writer_compromise_coordinated` (all streams aligned).
- **`bearer_trace.py`** — `project_bearer_rows_from_correction` for coordinated path.
- **`world.py`** — refactored to use `trace_emit.commit_deploy_streams`.
- **Tests** — `tests/contract/test_writer_compromise.py`; updated N-4 test in
  `test_audit_projection.py` to use coordinated emitter for residual unsigned pass.
- **`TODO.md`**, **`NEGATIVE_RESULTS.md`** — writer-compromise closed; N-4 boundary updated.

## Decisions
- **Single cross-stream check** (correction vs bearer action alignment) — uplift/harm
  and workflow-capacity checks false-positive on honest capture/MB6 ecology.
- **Sloppy vs coordinated** — `consistent_forge` and `writer_compromise` now fail
  cross-stream even unsigned; residual false pass requires `writer_compromise_coordinated`.
- **Coordinated signed pass** — valid chain + aligned streams still in-sim passes on
  capture_theater (outer oracle only) — documented as residual attack surface.

## Open / next
- Regenerate suite artifacts with new red-team strategies in battery.
- External trust anchor / out-of-band interventional evidence for coordinated emitter.

## Key paths
- `experiments/embedded-simulation/embedded_sim/{cross_stream,trace_emit}.py`
- `experiments/embedded-simulation/tests/contract/test_writer_compromise.py`

## Commits
- (none this session)
