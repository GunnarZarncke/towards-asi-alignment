# 2026-06-30 — Embedded hardening (structural tests + trace ingest)

## Trigger
User: implement hardening (ontology decoupling next steps from methodology session).

## Done
- `structural_fixtures.py` — synthesize correction rows from profiles with probe-lag semantics.
- `trace_ingest.py` + `trace_audit_cli.py` — audit external `correction.jsonl` without micro oracle.
- `knob_world.py` — held-out `WorldKnobs` grid; episodes use bridge `none`.
- `outer_rules.py` — unified `outer_certifies` / `false_pass` from evaluation rubric.
- `lab.py` / `pipeline.py` — optional `cfg_override` on `build_world` / `run_episode`.
- Tests: `test_structural_cci.py`, `test_trace_ingest.py`, `test_knob_world.py`, `test_outer_rules.py`.
- `PLAN.md`, `TODO.md` updated.
- **64 pytest pass**.

## Decisions
- Structural fixtures set `visible_action` at `t+lag` from probe intent (matches CCI interventional metrics).
- Knob worlds pick micro scenario via `WorldKnobs.structural_scenario`; bridge label stays `none`.
- `outer_certifies = ev.cci_status_correct`; failure-bridge false-pass = any `pass` decision.

## Open / next
- Run `python trace_audit_cli.py` on real logged LLM/tool traces when available.
- Optional: `run_knob_validation` batch artifact for held-out knob grid.

## Key paths
- `embedded_sim/structural_fixtures.py`
- `embedded_sim/trace_ingest.py`
- `embedded_sim/knob_world.py`
- `embedded_sim/outer_rules.py`
- `trace_audit_cli.py`

## Commits
- (pending)
