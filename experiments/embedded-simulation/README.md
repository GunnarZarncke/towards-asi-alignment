# Embedded audit simulation

Second in-repo experiment line (June 2026). The **auditor is an embedded process**
on simulated machines: it reads mutable virtual-filesystem artifacts through a
Python/Node **isolate bridge**, discovers a unit of attribution with **UAD**, runs
**scoped CCI** on grounded handles, and may trip an **MB5 deploy gate** before a
successor isolate may write artifacts. An **outer evaluator** grades certificates
against omniscient truth the isolates cannot see.

Version milestones: [`CHANGELOG.md`](CHANGELOG.md).

---

## What this simulation is

Each **episode** rolls out micro-dynamics on the host, projects a lossy subset into
a **VirtualFS** the in-sim auditor can read, runs optional **red-team** patches via
isolates, then runs the **embedded audit** path (VFS → UAD → handles → CCI +
safety). Finally **`outer_eval.py`** compares the certificate to host-side truth
rows — the only code that sees both sides.

Three planes (full mental model in [`embedded_sim/__init__.py`](embedded_sim/__init__.py)):

| Plane | Location | Role |
|-------|----------|------|
| **World / oracle** | Host `episode_meta`, `TruthLedger` | Omniscient truth rows |
| **Auditor (in-sim)** | `embedded_audit.py`, isolate bridge, VFS | Sensor-limited measurement |
| **Outer referee** | `outer_eval.py` | False-pass / referent-drift grading |

The **projection** (`audit_projection.py`) enforces what a real instrument could
report; `ORACLE_ONLY_FIELDS` stay host-side. Trace integrity uses hash-chained anchors
and a recomputable correction schema.

---

## Package layout

```
embedded_sim/
  audit_core/       Micro simulator → truth rows
  audit_projection.py   Plane boundary (KEEP/RENAME/DROP)
  world.py          VirtualFS + episode wiring
  bridge.py         Python/Node isolate RPC
  embedded_audit.py VFS → UAD → CCI path
  uad.py            Unit discovery from workflow JSONL
  handles.py        Correction / bearer / lineage handle kernels
  deploy_gate.py    MB5 successor gate
  outer_eval.py     Referee
  redteam.py        Hard-coded adversarial strategies
isolate/            Node runtime + red-team/audit scripts
results/NEGATIVE_RESULTS.md   ES-* ledger (read before citing positives)
```

---

## Quick start

```bash
cd experiments/embedded-simulation
python3 run.py                    # all 13 MB scenarios, Python substrate
python3 run.py --substrate js     # audit + red-team via Node isolates
python3 smoke_all_mbs.py          # golden smoke (T=400)
python3 -m pytest tests/ -q
```

Requires **Node.js** on `PATH` for `--substrate js`. Use `--workers N` for parallel
isolate waves.

---

## Entry points

| Command | Purpose |
|---------|---------|
| `python3 run.py [--substrate js] [--redteam …]` | Full scenario battery → `results/embedded_sim_report.*` |
| `python3 smoke_all_mbs.py` | Quick MB smoke |
| `python3 smoke_isolate_bridge.py` | JS bridge contract |
| `python3 smoke_oracle_separation.py` | Plane separation smoke |
| `python3 run_suite.py` | Batch sweeps; `--llm-live` for LLM red-team (`embedded_llm/`) |

---

## MB scenario map

| Bridge | Scenario |
|--------|----------|
| none | honest |
| MB1 | boundary_alias |
| MB2 | bundle_goodhart |
| MB3 | bearer_mismap |
| MB4 | capture_theater |
| MB5 | successor_relabel |
| MB6 / MB6b | selection_basin / basin_lock_in |
| MB7 / MB7d | hidden_capability |
| MB8 | legitimacy_theater |
| MB9 | grounding_silent_gap |

No LLMs in the core pipeline.

Narrative map: [`docs/EXPERIMENTS.md`](../../docs/EXPERIMENTS.md) §2.
