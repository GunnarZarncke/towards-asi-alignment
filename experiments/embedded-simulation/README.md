# Embedded audit simulation

V3 experiment: the auditor is an embedded process on simulated machines, reading mutable VFS artifacts via an isolate bridge. An outer evaluator compares in-sim certificates to omniscient `OuterTruthLedger` truth.

## Run

```bash
cd experiments/embedded-simulation
python3 run.py                    # all 13 MB scenarios, python substrate
python3 run.py --substrate js     # audit + red-team via Node isolates
python3 run.py --redteam full_redteam --substrate js
python3 smoke_all_mbs.py          # quick golden smoke (T=400)
python3 smoke_isolate_bridge.py   # JS bridge contract smoke
python3 smoke_oracle_separation.py
python3 -m pytest tests/ -q
```

Requires **Node.js** on `PATH` for `--substrate js`.

Use `--workers N` to run isolates in parallel across episodes at each pipeline timestep (red-team wave, audit wave, eval wave). Default is sequential (`--workers 1`).

## JS isolates

Node runs scripts under `isolate/` with a sync host-bridge RPC to Python:

- `isolate/runtime.js` — protocol + sandbox execution
- `isolate/lib/facade.js` — `fs`, `fetch`, `api`, `run`, `crypto`, `process`
- `isolate/scripts/redteam/*.js` — hard-coded red-team strategies
- `isolate/scripts/audit/read_logs.js` — auditor artifact reads

Every bridge call is logged as `SimToolCall` on `OuterTruthLedger`. CCI/safety still runs in Python on VFS-reconstructed traces.

Reports: `results/embedded_sim_report.{json,md}`.

## Architecture

- **Micro sim** (`embedded_sim/audit_core/`): copied toy dynamics → episode rows
- **Lab** (`lab.py`): deployment pipeline actors + workflow JSONL
- **VFS** (`world.py`): correction + workflow logs, audit config, attestation
- **Red-team** (`redteam.py`): hard-coded strategies patch logs via isolate bridge
- **Embedded audit** (`embedded_audit.py`): VFS reads → **UAD** → grounded handles → CCI + safety (pass requires grounded unit)
- **UAD** (`uad.py`): actor, machine, source_lineage, memory_namespace, coalition from workflow JSONL
- **Unit scope** (`unit_scope.py`): CCI interventional probes limited to unit workflow steps
- **Deploy gate** (`deploy_gate.py`): MB5 cert → `gate.local` → successor isolate artifacts
- **Referents** (`referents.py`): claimed referent map on VFS (`/etc/referents/claimed_map.json`)
- **Handles** (`handles.py`): correction probe/uptake/bearer/lineage anchors from `correction.jsonl`
- **Outer eval** (`outer_eval.py`): post-hoc compare to `TruthLedger` + referent drift

No LLMs. No sweeps. Audits may fail to certify (expected for some bridges).

## MB coverage

| Bridge | Scenario |
| --- | --- |
| none | honest |
| MB1 | boundary_alias |
| MB2 | bundle_goodhart |
| MB3 | bearer_mismap |
| MB4 | capture_theater |
| MB5 | successor_relabel |
| MB6 | selection_basin |
| MB6b | basin_lock_in |
| MB7 / MB7d | hidden_capability |
| MB8 | legitimacy_theater |
| MB9 / instrument_capture | grounding_silent_gap |
