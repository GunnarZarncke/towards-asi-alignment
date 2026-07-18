# Graded-capability lab simulation

Fifth in-repo experiment line. Successor **substrate** to
[`lab-simulation/`](../lab-simulation/) (which stays frozen at its referee/detector
freezes). Spawned by LS **GL-41**: the prior line's boolean ecology bottlenecks on
**ambiguity itself**, not on more detector engineering — so ambiguity must
**emerge** from a blinded resource/population substrate, not from dialed noise or
delay parameters.

**Active program:** PLAN **v4** — decoupled per-bridge rigs (`PLAN_v4.md`).
**Closed programs:** v1 (Phases 0–8, GL-31), v2/V2-2b (GL-43), v3 institutional
runtime (slices through GL-73; growth brief frozen GL-69). Version history:
[`CHANGELOG.md`](CHANGELOG.md).

---

## What this simulation is

A **graded deployment lab** where models, hazards, and harm are **continuous**
(not pass/fail), agents are **softmax optimizers** over affordable primitives inside
**OS subprocess isolates**, and resource contention, carrier viability, and
coordination cost **emerge** from scheduler mechanics rather than scenario knobs.

Each **episode** runs for `T` ticks (default 100; v3 reference batteries use
`V3_REFERENCE_T=200`). Four lab roles — engineer, reviewer, release manager,
admin — act through a nine-step **graded pipeline** (`pipeline_graded.json`).
A blinded substrate JSON (`generated_substrate_v1.json`) fixes primitive costs,
contention rules, and user-population parameters without letting experimenters dial
"ambiguity noise."

The line's distinctive measurements are **UAD-backed boundary discovery** (proper
rest-conditioned CMI + access-UAD as of GL-51), **ecology-BIQ** over *inferred*
units (not a labeled roster), and the **Emergent-Ambiguity-Index (EAI)** scored
from both the acting agent's full context and a **referee's limited-observation**
tier projection — the axis where GL-18–GL-22 landed.

Three planes (enforced by import tests; no imports from `lab_sim`):

| Plane | Package | Who uses it |
|-------|---------|-------------|
| **World** | `graded_lab/world_visible/` | Episode engine, graded pipeline, resource ledger, substrate loader, ecology runtime |
| **Agent** | `graded_lab/agent_visible/` | Isolate entrypoints, softmax policy, tool surface seen by subprocess agents |
| **Oracle / referee** | `graded_lab/oracle_only/` | Tier projections, five frozen detector families, twins, escalation, UAD/BIQ/EAI, calibration stats |
| **Harness** | `graded_lab/harness/` | Mock/Subprocess isolates, batteries, selection loops, v3 complexity gates, **v4 per-bridge rigs** |

An **outer referee** (oracle-only code) grades audit projections against Tier-K
generative truth. Agents and tier-`light` auditors never read oracle-only fields.

---

## Repository layout

```
graded_lab/
  world_visible/     config, substrate, pipeline, world.run_episode, ecology runtime
  agent_visible/     agent_main.py, policy, programs
  oracle_only/       referee, UAD, BIQ, EAI, calibration, stats
  harness/           isolates, selection, complexity gates, rigs/
PLAN.md              v1 closed program (Phases 0–8)
PLAN_v2.md           v2 blinded-grown ecology (closed)
PLAN_v3.md           v3 institutional Part B → live runtime (closed)
PLAN_v4.md           v4 decoupled per-bridge rigs (active)
DESIGN.md            frozen pre-registration constants
REPRODUCING.md       v1 per-finding reproduction
REPRODUCTION.md      deferred engineering (larger-team items)
results/FINDINGS.md  GL-0 … ledger (negatives first-class)
```

---

## Quick start

```bash
cd experiments/graded-lab-simulation
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

python3 -m pytest tests/ --profile smoke   # ~30s invariant gate
python3 -m pytest tests/ --profile fast    # ~120s dev loop
python3 -m pytest tests/ --profile slow    # full suite (default)

python3 verify_isolate_equivalence.py 5
python3 report_isolate_cost.py
```

### Test profiles

Three profiles in `tests/profiles.py`: **smoke** (~30s), **fast** (~120s, skips
`@slow`), **slow** (~380s, default). Refresh speed baselines after intentional
changes:

```bash
python3 -m pytest tests/ --profile slow --update-speed-baseline --no-speed-check
```

Logged background runs (avoid piping pytest to `tail`):

```bash
scripts/start_pytest_background.sh slow
scripts/pytest_progress.sh runs/test-logs/pytest-slow-YYYYMMDD-HHMMSS.log
scripts/run_pytest_logged.sh fast
```

---

## Entry points

### v1 batteries (closed program; still runnable)

| Script | Purpose |
|--------|---------|
| `run_phase7_calibration.py` | Phase 7c calibration grid, both vantages + 95% CIs (GL-22) |
| `run_referee_eai_check.py` | Referee- vs agent-vantage EAI entropy check (GL-19/20) |
| `run_phase8_selection.py` | Throughput-linked selection battery (GL-23) |
| `run_phase8a_orthogonal_tagging.py` | Phase 8a follow-up (GL-25) |
| `run_phase8b_multihandle.py` | Phase 8b follow-up (GL-26) |
| `run_phase8c_carryover_ablation.py` | Phase 8c follow-up (GL-27) |
| `run_phase8d_budget_aware.py` | Budget-aware relative-claim probe |

Add `--smoke` where supported for dev checks.

### v3 slice D / V2-3 harness (`scripts/`)

| Script | Purpose |
|--------|---------|
| `scripts/run_slice_d_reference_battery.py` | Integrated reference fixture @ `V3_REFERENCE_T=200` |
| `scripts/run_v3_detector_coverage_battery.py` | Detector coverage on honest reference (GL-54) |
| `scripts/run_program_map_phenotype_overlap.py` | ProgramMap phenotype overlap (GL-55) |
| `scripts/run_v3_supplementary_uad_gate.py` | Supplementary UAD gate |
| `scripts/run_v3_supplementary_detector_gate.py` | Supplementary detector fixtures |
| `scripts/run_v2_transfer_battery.py` | V2-3 transfer battery (GL-76) |
| `scripts/run_v2_biq_only.py` | BIQ-only re-run (GL-77) |
| `scripts/run_eai_precondition_probe.py` | EAI precondition probe v1 vs v3_grown (GL-83) |

### v4 per-bridge rigs (active)

```bash
.venv/bin/python scripts/run_v4_rig.py --rig r-mb1 --out results/v4_r_mb1.json
.venv/bin/python scripts/run_v4_rig.py --rig r-mb4 --out results/v4_r_mb4.json
.venv/bin/python scripts/run_v4_rig.py --rig r-mb9 --out results/v4_r_mb9.json
.venv/bin/python scripts/run_v4_rig.py --rig r-mb7d --out results/v4_r_mb7d.json
.venv/bin/python scripts/run_v4_rig.py --rig r-mb6a --out results/v4_r_mb6a.json
.venv/bin/python scripts/run_v4_rig.py --rig r-mb2 --out results/v4_r_mb2.json
.venv/bin/python scripts/run_v4_rig.py --rig r-mb1 --smoke
```

Rigs: precondition check → machinery test → pass / null / **SKIP** (independent per
bridge). Scored artifacts under `results/v4_r_*.json`. Growth / ambiguity
orchestration: `scripts/build_v4_ambiguity_candidate.py`,
`scripts/score_v4_ambiguity_growth_round.sh`.

---

## Rules

- `graded_lab` must **not** import `lab_sim` (`tests/test_no_lab_sim_imports.py`).
- No injected delay/noise parameters to manufacture ambiguity (founding constraint).
- Pre-registered constants live in `DESIGN.md`; do not tune thresholds against outcomes.
- Claim strength: methodology-building sanity checks only — see
  [`docs/EXPERIMENTS.md`](../../docs/EXPERIMENTS.md).

## Further reading

- Narrative map: [`docs/EXPERIMENTS.md`](../../docs/EXPERIMENTS.md) §5
- v1 closure: [`results/TERMINAL_SUMMARY.md`](results/TERMINAL_SUMMARY.md)
- Collaboration on `REPRODUCTION.md` items: [`COLLABORATION.md`](COLLABORATION.md)
