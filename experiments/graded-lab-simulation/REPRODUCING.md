# Reproducing the graded-lab v1 experiments (GL-0–GL-31)

This file is the closure-time reproduction record for the v1 program
(closed 2026-07-15; see `results/TERMINAL_SUMMARY.md`). Every battery
below is deterministic given its seed derivation; JSON outputs land in
`results/` and overwrite the checked-in copies, so run on a scratch
branch if you want to diff against the recorded results.

**Final v1 code commit:** `ed21adb` ("Graded lab optional directions:
parity, 8c diagnosis, Phase 8d.") — the last commit that changed
`graded_lab` code or batteries; check it out to reproduce against the
exact frozen code (`CODE_VERSION` `graded-lab-0.17.0`, asserted in
`graded_lab/world_visible/config.py`).

**v1 closure commit (these docs, no code changes):** `26e9638`
("Graded lab: close v1 program (GL-31), add terminal summary,
reproduction guide, and PLAN_v2.").

## Environment

```bash
cd experiments/graded-lab-simulation
python3 -m venv .venv                 # Python >= 3.12
.venv/bin/pip install -r requirements.txt   # pytest + scipy
source .venv/bin/activate                    # or prefix commands with .venv/bin/
```

No network, GPU, or API keys are needed; all agents are programmatic
(the LLM adapter was never built in v1). All wall times below are from a
2024-class laptop; everything totals well under 30 minutes.

## Determinism and frozen inputs

- `generated_substrate_v1.json` and
  `graded_lab/agent_visible/generated_behavior_features_v1.json` are the
  blinded frozen inputs (`BLIND_GENERATION.md`); do not regenerate them
  to reproduce v1.
- Seeds are derived inside each battery script from fixed base seeds;
  there are no CLI seed knobs to set.
- Mock vs subprocess isolates produce identical trajectories (GL-30);
  everything below uses the default `MockIsolate` unless noted.

## Test suite (structural gates for all phases)

```bash
python3 -m pytest tests/ --profile smoke   # ~30s structural invariants
python3 -m pytest tests/ --profile fast    # ~120s, skips @slow
python3 -m pytest tests/ --profile slow    # ~290s full suite incl. speed caps (default)
```

The slow profile enforces per-test speed caps against
`tests/speed_baseline.json`; a slow machine may trip caps without any
code being wrong (`--no-speed-check` disables them).

## Per-finding reproduction map

Findings are documented in `results/FINDINGS.md`; the table gives the
command that regenerates each finding's data.

| Findings | Command | Output | Wall |
|---|---|---|---|
| GL-1–GL-9 (phases 0–6: substrate, oracle, resources, agents, carrier, traces, referee, blind features) | `python3 -m pytest tests/ --profile slow` | test log only (these phases are gated by tests, not batteries) | ~290s |
| GL-3/GL-7 (isolate equivalence) | `python3 verify_isolate_equivalence.py 5` | stdout PASS/FAIL | ~1min |
| GL-7 (isolate cost) | `python3 report_isolate_cost.py` | `results/isolate_cost_ledger.json` (gitignored) | seconds |
| GL-10–GL-12 (UAD passive/intervention, ecology battery, blind scenarios) | `python3 -m pytest tests/test_uad_*.py --profile slow` | test log; blind scenario briefs in `graded_lab/harness/blind_scenarios_v1.md` | ~2min |
| GL-13/GL-14 (ecology-BIQ, `I_ctrl` outcome-vector fix) | `python3 -m pytest tests/test_unit_biq.py tests/test_ecology_biq.py --profile slow` | test log | ~1min |
| GL-15/GL-16/GL-22 (Phase 7c calibration, both vantages, 95% CIs) | `python3 run_phase7_calibration.py` | `results/ecology_calibration.json` | ~430s |
| — legacy 16-cell diagnostic grid (GL-16 context) | `python3 run_phase7_calibration.py --legacy` | same file, `legacy` block | ~10min |
| GL-17 (budget-aware agent, single-episode battery) | `python3 -m pytest tests/test_budget_aware_agent.py --profile slow` | test log | ~1min |
| GL-19/GL-20/GL-21 (referee-vantage EAI) | `python3 run_referee_eai_check.py` | `results/referee_eai_check.json` | ~2min |
| GL-23 (Phase 8 selection, first battery) | `python3 run_phase8_selection.py` | `results/phase8_selection.json` | ~32s |
| GL-25 (Phase 8a orthogonal tagging) | `python3 run_phase8a_orthogonal_tagging.py` | `results/phase8a_orthogonal_tagging.json` | ~40s |
| GL-26 (Phase 8b multi-handle fitness) | `python3 run_phase8b_multihandle.py` | `results/phase8b_multihandle.json` | ~79s |
| GL-27 (Phase 8c carryover ablation) | `python3 run_phase8c_carryover_ablation.py` | `results/phase8c_carryover_ablation.json` | ~75s |
| GL-28 (8c mechanism diagnosis; reads GL-27 output) | `python3 diagnose_phase8c_carryover.py` | `results/phase8c_diagnosis.json` | seconds |
| GL-29 (Phase 8d budget-aware member) | `python3 run_phase8d_budget_aware.py` | `results/phase8d_budget_aware.json` | ~75s |
| GL-30 (mock/subprocess parity) | `python3 verify_phase8_isolate_parity.py` | stdout PASS/FAIL | ~2min |

Smoke variants for the expensive scripts:
`run_phase7_calibration.py --smoke` (2 cells),
`run_phase8_selection.py --smoke` (4 members × 2 generations, add
`--subprocess` for the backend check).

## Verifying a reproduction

1. Batteries print progress per cell/generation/seed as they run.
2. Compare the regenerated JSON against the committed copy
   (`git diff results/`). Trajectory numbers should match exactly on the
   same platform; floating-point CI bounds may differ in the last digits
   across BLAS/scipy builds.
3. Headline numbers to check against `results/FINDINGS.md`:
   GL-22 — both `pass_criteria` blocks show `all_passed: false` with 1/4
   true each; GL-23 — final `weak_2step` mass ≈0.922, correction-
   preserving share gen 5 ≈0.007, weighted severity falls ≈0.048→0.004;
   GL-27 — paired diffs `(−0.0533, +0.0018)` with neither CI containing
   zero.

## Interpretation guardrails

Reproducing the numbers does not license stronger claims than
`results/FINDINGS.md` records: GL-25 forbids reading GL-23's mass shift
as preservation being selected against, GL-29's preservation endpoint is
an accounting confound, and nothing in v1 supports parasite (ch36) or
goal-laundering (ch40) claims. See `results/TERMINAL_SUMMARY.md`.
