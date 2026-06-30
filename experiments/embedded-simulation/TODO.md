# Embedded simulation — TODO

Plan: `PLAN.md` (handoff) · `.cursor/plans/embedded_audit_experiment_8fbb03ff.plan.md` (full)

## Done (v1)

- [x] Package under `experiments/embedded-simulation/`
- [x] VFS + isolate bridge (Python + Node JS)
- [x] Lab workflow + 13 MB scenarios
- [x] UAD → embedded audit → outer eval pipeline
- [x] Hard-coded red-team (Python + JS)
- [x] Isolate runtime timing + parallel timestep workers
- [x] UAD reads workflow from VFS JSONL (not `hidden_group`)
- [x] Oracle separation guard + smoke
- [x] pytest unit / contract / golden subset
- [x] **UAD before CCI** — reordered pipeline + contract test
- [x] **Heterogeneous UAD** — actor, machine, source_lineage, memory_namespace, coalition
- [x] **Grounded handles** — `handles.py` from correction.jsonl + workflow
- [x] **UAD pass gate** — no grounded unit ⇒ `invalid_certificate`
- [x] `PLAN.md` with UAD spec + MB grounding table

## UAD gaps (plan v2)

- [x] Scope CCI interventional probes to selected `UADCandidate` workflow steps
- [x] Successor deploy gate + claimed referent map on VFS (MB5)
- [x] MB5 false-pass: interventional CCI witness (not surface uptake) in `cci_audit.py`
- [x] MB1: `boundary_route` UAD + lab workflow signals under bypass perturbations
- [x] In-sim referent drift scoring from claimed map vs deploy artifacts
- [x] Perturbation-response scoring + lagged dependence graph (`uad.py` MI boost)
- [x] Golden: UAD precision/recall per bridge before CCI assertions
- [x] Real UAD: vendored agency-detect lagged-MI clustering (`uad_core/`) merged into `discover_units`

## Next (plan order) — complete

- [x] Referent drift: gate rejection when in-sim transport fails (not just outer oracle)
- [x] `instrument_capture` native micro scenario (not relabeled grounding gap)
- [x] MB7d `inferential_coupling` in audit_core
- [x] Audit path: rebuild CCI trace without `world.micro` (artifact-only)

## Hardening (ontology decoupling)

- [x] Structural property tests (`tests/contract/test_structural_cci.py`) — blind scenario label
- [x] Trace ingest hook (`trace_ingest.py`, `trace_audit_cli.py`)
- [x] Knob-held-out worlds (`knob_world.py`, `tests/contract/test_knob_world.py`)
- [x] Unified outer eval rules (`outer_rules.py`)

## Run

```bash
cd experiments/embedded-simulation
python3 -m pytest tests/ -q
python3 smoke_oracle_separation.py
python3 run.py --redteam full_redteam          # main 13-bridge report
python3 run_suite.py --all --llm-live          # full parity suite + live LLM
python3 trace_audit_cli.py tests/fixtures/sample_capture_theater.jsonl
python3 write_overall_summary.py             # regenerate OVERALL_SUMMARY.md
```

Parity artifacts live under `results/` — see `OVERALL_SUMMARY.md`.
