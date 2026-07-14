# Graded Lab Simulation

Fifth in-repo experiment line (successor substrate to `lab-simulation/`).
Spawned by G-41: boolean ecology limits; ambiguity must **emerge** from a
blinded resource/population substrate, not from dialed parameters.

**Status: Phases 0–7c done (incl. Phase 7c-revised calibration battery,
two backlog items from FINDINGS G-16 — a resource-sensitive agent
program, G-17, and an EAI-v2 logging/normalization fix, G-18 — a
referee-vantage EAI reframe and measurement, G-19/G-20, and the full
both-vantage battery with 95% CIs, G-22); Phase 8 not started
(2026-07-14)**
`CODE_VERSION` `graded-lab-0.14.0` — see `DESIGN.md` for frozen constants.

## Quick start

```bash
cd experiments/graded-lab-simulation
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
python3 -m pytest tests/ --profile smoke   # ~30s invariant gate
python3 -m pytest tests/ --profile fast    # ~120s dev loop (no @slow)
python3 -m pytest tests/ --profile slow    # ~290s full suite (default)
python3 -m pytest tests/ --fast             # alias for --profile fast
python3 verify_isolate_equivalence.py 5
python3 report_isolate_cost.py
python3 run_phase7_calibration.py          # revised 5-cell carrier_load_scale battery, both vantages + 95% CIs (see G-22)
python3 run_phase7_calibration.py --smoke  # 2-cell dev smoke
python3 run_phase7_calibration.py --legacy # original 16-cell compute×spread grid (diagnostic; see G-16)
python3 run_referee_eai_check.py           # standalone referee- vs agent-vantage EAI entropy check (see G-19/G-20)
```

### Test profiles and speed limits

Three profiles (`tests/profiles.py`):

- **smoke** — structural/unit invariants + one episode smoke (~30s cap)
- **fast** — everything except `@pytest.mark.slow` multi-seed gates (~120s cap)
- **slow** — full suite including slow integration tests (~270s cap); default

Per-test hard caps and regression baselines apply on the **slow** profile.
Refresh baselines after intentional changes:

```bash
python3 -m pytest tests/ --profile slow --update-speed-baseline --no-speed-check
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
| 3 Optimizer agents + isolates | **done** (softmax policy, full four-role affordable-set API, resource-bounded admin access queue, episode loop, Mock/Subprocess isolates + equivalence script; Phase 3 gate tests — see `results/FINDINGS.md` G-3/G-7) |
| 3b Embedded carrier viability | **done** (resource-derived load/integrity; deterministic degrade, skip, terminate, or declared fresh-instance replacement; `carrier_load_scale=0` preserves Phase 3; 55 tests green) |
| 4 Trace/counterfactual instrumentation + EAI | **done** (boundary streams, same-seed noop/random controls, resource/failure diagnostics, corrected Tier-I EAI load; this is **not** BIQ) |
| 5 Referee port + freeze | **done** (tier projections, five detector families, twins, escalation, Tier-I-aligned misreporting; see `results/FINDINGS.md` G-8) |
| 6 Blind behavior features | **done** (`generated_behavior_features_v1.json`, `feature:*` programs, validator; see G-9) |
| 7a UAD + intervention validation | **done** (primitive traces, passive + standalone-dependency intervention discovery, full-partition ecology battery, blind scenario-designer battery; see G-10–G-12) |
| 7b UAD-backed ecology-BIQ | **done** (`oracle_only/unit_biq.py`: held-out `I_pred`/`S_surp` bits, intervention-supported `I_ctrl` over a 4-component outcome state, declared `H_mem` proxy over UAD-inferred units; `I_ctrl`'s outcome vector was widened past task+harm alone to fix a resource-contention confound — see G-13/G-14) |
| 7c Calibration battery | **done** (`run_phase7_calibration.py`, `oracle_only/calibration.py`; results in `results/ecology_calibration.json` — see G-15/G-16/G-22). Two backlog items resolved: a resource-sensitive agent program (`programmatic_budget_aware`, validated in a small separate battery, not the main criteria — G-17) and an EAI-v2 logging/normalization fix (verified correct; measured effect on this substrate is a reported null — G-18). Battery now reports both the oracle/agent vantage and a referee (light-tier) vantage from the same episodes with 95% CIs; neither passes (1/4 each, a different criterion each time — G-22); next lever is roster scope, not another EAI reformulation |
| 8 Multi-episode / selection | not started (see PLAN.md "Manuscript integration backlog" item 4 for the registered go/no-go framing) |

## Rules

- `graded_lab` must **not** import `lab_sim` (enforced by `tests/test_no_lab_sim_imports.py`)
- Selection / D3 deferred to Phase 8 behind measured-EAI sweet-spot gate
