# Graded Lab Simulation

Fifth in-repo experiment line (successor substrate to `lab-simulation/`).
Spawned by G-41: boolean ecology limits; ambiguity must **emerge** from a
blinded resource/population substrate, not from dialed parameters.

**Status: Phase 0–3 done; Phase 3b designed (2026-07-11)**  
`CODE_VERSION` `graded-lab-0.3.0` — see `DESIGN.md` for frozen constants.

## Quick start

```bash
cd experiments/graded-lab-simulation
python3 -m pytest tests/ -q
```

## Layout

- `PLAN.md` — phases 0–8, freeze gates
- `DESIGN.md` — Phase 0 pre-registration (Tier K/I, BIQ, EAI, primitives)
- `generated_substrate_v1.json` — frozen blinded substrate (no delay/noise params)
- `pipeline_graded.json` — nine-step default topology
- `graded_lab/` — package (`world_visible`, `agent_visible`, `oracle_only`, `harness`)

## Phase status

| Phase | Status |
|-------|--------|
| 0 Scaffold + substrate | **done** |
| 1 Oracle + graded pipeline | **done** (unit tests; review pass fixed review/compliance polarity, per-model field-monitor sampling, `safety_effort` wiring — see `results/FINDINGS.md` G-1) |
| 2 Resource/cost substrate | **done** (unit tests; ledger standing-recovery + scheduler contention now genuinely emergent, pay-to-observe projector added — see `results/FINDINGS.md` G-2) |
| 3 Optimizer agents + isolates | **done** (softmax policy, affordable-set API, episode loop, Mock/Subprocess isolates + equivalence script; Phase 3 gate tests — see `results/FINDINGS.md` G-3) |
| 3b Embedded carrier viability | designed (resource-derived load/integrity; deterministic degrade, skip, terminate, or declared fresh-instance replacement; `carrier_load_scale=0` preserves Phase 3) |
| 4 Ecology-BIQ + EAI | partial (`eai.py` operational for gate; full BIQ deferred) |
| 5–8 | not started |

## Rules

- `graded_lab` must **not** import `lab_sim` (enforced by `tests/test_no_lab_sim_imports.py`)
- Selection / D3 deferred to Phase 8 behind measured-EAI sweet-spot gate
