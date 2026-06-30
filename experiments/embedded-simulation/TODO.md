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
- [ ] MB1: boundary unit from source/machine lineage + hidden-route correlates in workflow
- [ ] Perturbation-response scoring + lagged dependence graph (replace heuristic ranks)
- [ ] Golden: UAD precision/recall per bridge before CCI assertions
- [ ] MB5 false-pass: align successor_shift witness with toy held-out behavior

## Next (plan order)

- [ ] Referent maps: outer-only `TrueReferentMap` vs audit `ClaimedReferentMap` drift scoring in-sim
- [ ] Semantic drift scenario beyond MB5 effect proxy
- [ ] LLM red-team via isolate tools (no direct patch API)
- [ ] MB5 false-pass: align successor_shift witness with toy held-out behavior
- [ ] `instrument_capture` native micro scenario (not relabeled grounding gap)
- [ ] MB7d `inferential_coupling` in audit_core
- [ ] Audit path: rebuild CCI trace without `world.micro` (artifact-only)

## Run

```bash
cd experiments/embedded-simulation
python3 -m pytest tests/unit tests/contract -q
python3 -m pytest tests/golden -q
python3 smoke_isolate_bridge.py
python3 smoke_oracle_separation.py
python3 run.py --substrate js --workers 4
```
