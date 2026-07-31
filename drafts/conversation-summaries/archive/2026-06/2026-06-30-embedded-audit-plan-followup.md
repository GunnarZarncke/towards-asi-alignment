# 2026-06-30 — Embedded audit plan follow-up

## Trigger
Continue embedded-audit experiment plan: VFS-backed UAD, oracle separation guard, golden/contract tests, TODO doc.

## Done
- `load_workflow_from_vfs()` in `lab.py`; `embedded_audit.py` UAD + anchors use VFS workflow (not in-memory `hidden_group`).
- `oracle_guard.py` with split inference vs bridge checks; `smoke_oracle_separation.py`.
- Tests: `test_oracle_separation`, `test_bridge_logging`, `test_uad_vfs`, `test_episode_outcomes`.
- `experiments/embedded-simulation/TODO.md` with done/next checklist.
- Refined oracle guard: allow bridge `world.truth` logging; allow UAD `unit_type="coalition"` (workflow-derived, not oracle).
- **17 pytest tests pass**; oracle smoke OK.

## Decisions
- Oracle separation applies strictly to inference modules (`embedded_audit.py`, `uad.py`); bridge may append tool/patch logs but must not read oracle secret fields.
- VFS workflow JSONL intentionally omits `hidden_group`; UAD scores from public workflow fields only.

## Open / next
- Successor deploy gate (audit artifact → gate → spawn isolate).
- Referent maps on VFS; MB5 false-pass vs `successor_shift_witness`.
- Copy plan to `experiments/embedded-simulation/PLAN.md`.

## Key paths
- `experiments/embedded-simulation/embedded_sim/oracle_guard.py`
- `experiments/embedded-simulation/embedded_sim/lab.py` (`load_workflow_from_vfs`)
- `experiments/embedded-simulation/TODO.md`

## Commits
- (none — user did not request commit)
