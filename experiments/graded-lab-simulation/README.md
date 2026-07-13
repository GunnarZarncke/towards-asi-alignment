# Graded Lab Simulation

Fifth in-repo experiment line (successor substrate to `lab-simulation/`).
Spawned by G-41: boolean ecology limits; ambiguity must **emerge** from a
blinded resource/population substrate, not from dialed parameters.

**Status: Phases 0–7a done (incl. Phase 7a-blind scenario battery); Phase
7b–7c not started (2026-07-13)**
`CODE_VERSION` `graded-lab-0.9.0` — see `DESIGN.md` for frozen constants.

## Quick start

```bash
cd experiments/graded-lab-simulation
python3 -m pytest tests/              # full suite + speed limits (see below)
python3 -m pytest tests/ --fast       # dev loop: skip @pytest.mark.slow gates
python3 verify_isolate_equivalence.py 5
python3 report_isolate_cost.py
```

### Speed limits

- **Per-test hard cap** (`default_test_max_seconds`, overrides in
  `tests/speed_limits.json`): catches new unexpectedly slow tests.
- **Suite ceiling** (`suite_max_seconds`): fails when the whole run regresses.
- **Per-test regression** (`tests/speed_baseline.json` + slack): catches
  slowdowns on existing tests.
- Refresh baselines after intentional changes:
  `python3 -m pytest tests/ --update-speed-baseline --no-speed-check`

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
| 3 Optimizer agents + isolates | **done** (softmax policy, full four-role affordable-set API, resource-bounded admin access queue, episode loop, Mock/Subprocess isolates + equivalence script; Phase 3 gate tests — see `results/FINDINGS.md` G-3/G-7) |
| 3b Embedded carrier viability | **done** (resource-derived load/integrity; deterministic degrade, skip, terminate, or declared fresh-instance replacement; `carrier_load_scale=0` preserves Phase 3; 55 tests green) |
| 4 Trace/counterfactual instrumentation + EAI | **done** (boundary streams, same-seed noop/random controls, resource/failure diagnostics, corrected Tier-I EAI load; this is **not** BIQ) |
| 5 Referee port + freeze | **done** (tier projections, five detector families, twins, escalation, Tier-I-aligned misreporting; see `results/FINDINGS.md` G-8) |
| 6 Blind behavior features | **done** (`generated_behavior_features_v1.json`, `feature:*` programs, validator; see G-9) |
| 7a UAD + intervention validation | **done** (primitive traces, passive + standalone-dependency intervention discovery, full-partition ecology battery, blind scenario-designer battery; see G-10–G-12) |
| 7b–7c UAD-backed BIQ + calibration | not started |
| 8 Multi-episode / selection | not started |

## Rules

- `graded_lab` must **not** import `lab_sim` (enforced by `tests/test_no_lab_sim_imports.py`)
- Selection / D3 deferred to Phase 8 behind measured-EAI sweet-spot gate
