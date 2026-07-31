# 2026-06-30 — Embedded audit simulation v1

## Trigger
Implement the embedded audit experiment fully: run all planned MB scenarios with hard-coded red-team (no LLM, no sweeps), in-sim and outer evaluation functioning.

## Done
- Built `experiments/embedded-simulation/` package: world/VFS, isolate bridge, lab, UAD, embedded audit, red-team, outer eval, pipeline, `run.py`.
- Copied `audit_core` from toy-simulation; episodes materialize to `/var/log/deploy/*.jsonl`.
- 13 MB scenarios run end-to-end (`none` + MB1–MB9 + MB6b + MB7d + `instrument_capture`).
- Reports: `results/embedded_sim_report.{json,md}`; smoke script `smoke_all_mbs.py`; pytest stubs under `tests/`.
- README and index entry in `experiments/TODO.md`.

## Decisions
- Audit reads full episode rows from VFS JSONL (not truncated fields) so `build_audit_trace` matches toy semantics.
- MB7d and `instrument_capture` reuse `hidden_capability` / `grounding_silent_gap` micro scenarios with bridge-specific outer-truth flags.
- Baseline run uses `redteam=none`; `full_redteam` intentionally produces many false passes (outer eval tracks them).

## Open / next
- Install pytest in env to run `tests/` (not in default python3.13 here).
- MB5 successor false-pass under baseline (in-sim passes, outer expects refusal) — known gap vs toy held-out behavior.
- LLM red-team via isolate tools; successor deploy gate; JS isolate stubs under `isolate/`.

## Key paths
- `experiments/embedded-simulation/run.py`
- `experiments/embedded-simulation/embedded_sim/pipeline.py`
- `experiments/embedded-simulation/results/embedded_sim_report.md`

## Commits
- (none — user did not request commit)
