# Graded Lab Simulation

Fifth in-repo experiment line (successor substrate to `lab-simulation/`).
Spawned by GL-41: boolean ecology limits; ambiguity must **emerge** from a
blinded resource/population substrate, not from dialed parameters.

**Status: v1 program CLOSED (2026-07-15, GL-31); v2 program planned.**
The v1 arc and why it closed: [`results/TERMINAL_SUMMARY.md`](results/TERMINAL_SUMMARY.md).
Reproducing every v1 finding: [`REPRODUCING.md`](REPRODUCING.md).
The v2 program (blinded-grown ecology, variation operator, LLM
red-teaming): [`PLAN_v2.md`](PLAN_v2.md). v1 record below is kept as-is.

**v1 final state: Phases 0–7c done; Phase 8 scaffold + battery (GL-23), reviewed
(GL-24), and follow-up phases 8a/8b/8c run (GL-25/26/27, 2026-07-14).**
Phase 8 implements throughput-linked selection with campaign
grant/standing carryover on the GL-22 referee sweet-spot ecology;
first full run is a **clean null** on detector-evading emergence (mass
shifted to `weak_2step`, severity fell; GL-23). External review (GL-24)
raised four concerns; each has a follow-up result: **8a** (orthogonal
tagging) found the mass shift is *not* explained by a measurable
throughput difference between the tagged members — a selection-noise
finding, sharpening GL-23's causal claim (GL-25); **8b** (multi-handle
fitness) reproduces GL-23's direction under the pre-registered
audit-pass/latency-augmented fitness too — a proxy-insensitivity result
(GL-26); **8c** (carryover ablation) found carryover vs. reset *are*
statistically distinguishable, though the effect size on mass share is
small (GL-27). Concern 4 (gate-language) fixed in `PLAN.md`.
`CODE_VERSION` `graded-lab-0.17.0` — see `DESIGN.md` for frozen constants.

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
python3 run_phase7_calibration.py          # revised 5-cell carrier_load_scale battery, both vantages + 95% CIs (see GL-22)
python3 run_phase7_calibration.py --smoke  # 2-cell dev smoke
python3 run_phase7_calibration.py --legacy # original 16-cell compute×spread grid (diagnostic; see GL-16)
python3 run_referee_eai_check.py           # standalone referee- vs agent-vantage EAI entropy check (see GL-19/GL-20)
python3 run_phase8_selection.py            # Phase 8 throughput-linked selection (see GL-23)
python3 run_phase8_selection.py --smoke    # 4-member dev smoke
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

- `PLAN.md` — v1 phases 0–8, freeze gates (closed program record)
- `PLAN_v2.md` — v2 program plan (blinded-grown ecology, variation, red-teaming)
- `REPRODUCING.md` — per-finding reproduction map + final v1 commit hash
- `results/TERMINAL_SUMMARY.md` — v1 closure summary
- `DESIGN.md` — Phase 0 pre-registration (Tier K/I, BIQ, EAI, primitives)
- `generated_substrate_v1.json` — frozen blinded substrate (no delay/noise params)
- `pipeline_graded.json` — nine-step default topology
- `graded_lab/` — package (`world_visible`, `agent_visible`, `oracle_only`, `harness`)

## Phase status

| Phase | Status |
|-------|--------|
| 0 Scaffold + substrate | **done** |
| 1 Oracle + graded pipeline | **done** (unit tests; review pass fixed review/compliance polarity, per-model field-monitor sampling, `safety_effort` wiring — see `results/FINDINGS.md` GL-1) |
| 2 Resource/cost substrate | **done** (unit tests; ledger standing-recovery + scheduler contention now genuinely emergent, pay-to-observe projector added — see `results/FINDINGS.md` GL-2) |
| 3 Optimizer agents + isolates | **done** (softmax policy, full four-role affordable-set API, resource-bounded admin access queue, episode loop, Mock/Subprocess isolates + equivalence script; Phase 3 gate tests — see `results/FINDINGS.md` GL-3/GL-7) |
| 3b Embedded carrier viability | **done** (resource-derived load/integrity; deterministic degrade, skip, terminate, or declared fresh-instance replacement; `carrier_load_scale=0` preserves Phase 3; 55 tests green) |
| 4 Trace/counterfactual instrumentation + EAI | **done** (boundary streams, same-seed noop/random controls, resource/failure diagnostics, corrected Tier-I EAI load; this is **not** BIQ) |
| 5 Referee port + freeze | **done** (tier projections, five detector families, twins, escalation, Tier-I-aligned misreporting; see `results/FINDINGS.md` GL-8) |
| 6 Blind behavior features | **done** (`generated_behavior_features_v1.json`, `feature:*` programs, validator; see GL-9) |
| 7a UAD + intervention validation | **done** (primitive traces, passive + standalone-dependency intervention discovery, full-partition ecology battery, blind scenario-designer battery; see GL-10–GL-12) |
| 7b UAD-backed ecology-BIQ | **done** (`oracle_only/unit_biq.py`: held-out `I_pred`/`S_surp` bits, intervention-supported `I_ctrl` over a 4-component outcome state, declared `H_mem` proxy over UAD-inferred units; `I_ctrl`'s outcome vector was widened past task+harm alone to fix a resource-contention confound — see GL-13/GL-14) |
| 7c Calibration battery | **done** (`run_phase7_calibration.py`, `oracle_only/calibration.py`; results in `results/ecology_calibration.json` — see GL-15/GL-16/GL-22). Two backlog items resolved: a resource-sensitive agent program (`programmatic_budget_aware`, validated in a small separate battery, not the main criteria — GL-17) and an EAI-v2 logging/normalization fix (verified correct; measured effect on this substrate is a reported null — GL-18). Battery now reports both the oracle/agent vantage and a referee (light-tier) vantage from the same episodes with 95% CIs; neither passes (1/4 each, a different criterion each time — GL-22); next lever is roster scope, not another EAI reformulation |
| 8 Multi-episode / selection | **scaffold + first battery** (`run_phase8_selection.py`, `harness/selection.py`; results in `results/phase8_selection.json` — see GL-23). Clean null: throughput selection favors `weak_2step` over correction-preserving `strong_softmax`; weighted severity/detector fell, not rose. **Reviewed (GL-24):** confounded preservation tag, narrow proxy, and unvalidated carryover flagged before manuscript use; 8a/8b/8c pre-registered, not run |

## Rules

- `graded_lab` must **not** import `lab_sim` (enforced by `tests/test_no_lab_sim_imports.py`)
- Selection / D3 deferred to Phase 8 behind measured-EAI sweet-spot gate
