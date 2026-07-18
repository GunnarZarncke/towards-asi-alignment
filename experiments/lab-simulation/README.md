# Lab-layer simulation

Fourth in-repo experiment line (after toy, embedded, and goal-agent). Goal-driven
**playbook agents** (engineer, reviewer, release manager, access admin) act inside
a lab with **real mechanics**: a deployment pipeline as an infrastructure-as-code
JSON step-DAG, an on-disk workspace, service-managed access control, and **real OS
subprocess isolates** speaking JSON-RPC to a host that mediates every tool call.

Referee frozen **2026-07-06** (`lab-sim-0.3.0`); detector layer frozen **2026-07-07**
(S6/S7). Version history: [`CHANGELOG.md`](CHANGELOG.md).

---

## What this simulation is

Each **episode** wires four (or more) persistent Python subprocess agents through a
host **tool dispatch** boundary. Agents choose tactics from a **playbook repertoire**
(goal weights × step sequences), not from oracle scenario knobs. The **pipeline engine**
is the only mutator of deploy state: a declarative DAG in `pipeline_default.json`
with versioned spec history for referent-drift experiments.

Hidden **model capability and hazard** live in oracle-only state; filed reports and
monitoring signals are audit-visible and may diverge (the deception surface). A
frozen **referee** (`oracle_only/`) projects four instrumentation tiers
(`none` → `light` → `full` → `deep`), runs five detector families + honest twins +
escalation, and scores continuous severity against oracle truth.

Three planes:

| Plane | Package | Contents |
|-------|---------|----------|
| **Agent-visible** | `lab_sim/agent_visible/` | Subprocess entrypoints, playbooks, LLM adapter (Phase 8 exploratory) |
| **World-visible** | `lab_sim/world_visible/` | Pipeline engine, access control, comms, workspace, episode loop |
| **Oracle-only** | `lab_sim/oracle_only/` | Oracle models, severity, detectors, UAD/intervention stack, handles |
| **Harness** | `lab_sim/harness/` | Mock/Subprocess isolates, batteries, cache, D3 selection loops |

`MockIsolate` is for fast tests only; pre-registered batteries use **`SubprocessIsolate`**
(proven byte-identical via `verify_isolate_equivalence.py`).

Lean **leak-proof** certificates (`leak-proof/`) complement runtime plane tests.

---

## Quick start

```bash
cd experiments/lab-simulation
python3 -m pytest                    # full suite (~467 tests)
python3 verify_isolate_equivalence.py 5
python3 report_isolate_cost.py
```

---

## Entry points

### Pre-registered batteries

| Script | Output | Notes |
|--------|--------|-------|
| `run_phase6.py` | `results/phase6_battery.*` | Blind playbooks; SubprocessIsolate (LS-1) |
| `run_phase7.py` | `results/phase7_battery.*` | Escalation, redteam, capture grid (LS-4–6) |
| `run_phase9.py` | `results/phase9_battery.*` | D1/D4/D2 equivalence + ecology batteries (LS-14–16) |
| `run_d3_population.py` | `results/d3_population.*` | D3.1 population selection (LS-36); `--mock` for smoke |
| `run_d3_spec_evolution.py` | `results/d3_spec_evolution.*` | D3.2 spec-weakening mutation (LS-37) |

### UAD / detector line (S5–S7, LS-24–33)

| Script | Backend | Finding |
|--------|---------|---------|
| `run_s6_intervention_uad.py` | MockIsolate | LS-28 |
| `run_s7_blind_battery.py` | SubprocessIsolate | LS-30 |
| `run_llm_detector_stress_test.py` | Real `gpt-4o-mini` (API spend) | LS-32 |
| `run_llm_detector_stats_validation.py` | Real API | LS-33 |

Also: `run_s5_uad_core_port.py`, `run_s5_deep_trace_sweep.py`, `run_s6_cmi_detector.py`,
`run_d2_adversarial_lineage.py`, `run_llm_detector_root_cause_probe.py`,
`run_llm_detector_committee_stress_test.py`.

### Exploratory (not batteries)

| Script | Purpose |
|--------|---------|
| `run_phase8_llm_spotcheck.py` | LLM engineer spot-check (LS-7) |
| `run_phase8_llm_redteam.py` | LLM red-team prompt variant (LS-8) |
| `run_s1_build_loop_prototype.py` … `run_s4_shared_slot_prototype.py` | S1–S4 scenario prototypes (LS-17–20) |
| `run_llm_discovery_*.py` | Phase 10 LLM coordination discovery (LS-21–23) |
| `run_handle_calibration_battery.py` | Handle dose calibration (LS-39) |

Requires `OPENAI_API_KEY` in repo-root `.env` for LLM scripts.

---

## Layout

```
lab_sim/
  agent_visible/    playbooks, programs, LLM adapter
  world_visible/    pipeline, access, world.run_episode, config (CODE_VERSION)
  oracle_only/      referee, UAD/intervention, handles, attic/ (retired detectors)
  harness/          isolates, batteries, D3 loops, redteam
leak-proof/         Lean 4 plane-separation certificates
tests/              mirrors four tiers + plane/regression tests
results/FINDINGS.md LS-1 … ledger
```

Tier rationale: [`ACCESS_TIERS.md`](ACCESS_TIERS.md). Design freeze: [`DESIGN.md`](DESIGN.md).
Full plan: [`PLAN.md`](PLAN.md).

---

## Claim strength

Methodology-building sanity checks only. Negative results (light-tier
anti-correlation, admin capture null, `shared_slot` blind spot, LLM non-determinism
miss) are load-bearing — see [`results/FINDINGS.md`](results/FINDINGS.md) before citing
headline accuracies.

Narrative map: [`docs/EXPERIMENTS.md`](../../docs/EXPERIMENTS.md) §4.
