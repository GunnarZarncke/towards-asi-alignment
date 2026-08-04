# 2026-07-06 — Lab-layer sim: open-findings follow-up (G-1a–G-8a)

## Trigger

User: work only on six open items from critic-priority list — analyze G-1,
G-3 field access, G-4 K sweep, G-5 build_params in red-team, G-6 admin
probe, G-8 server-side build_params enforcement — then end-of-session commit.

## Done

- **G-1a:** `run_g1_light_tier_analysis.py` (60 episodes) — light-tier
  anti-correlation is throughput confound, not detector bug; residual r
  +0.22 after controlling deploy count. Documented in FINDINGS G-1a.
- **G-3a:** Playbook selection logged as `playbook.selection` tool events
  (full tier: name, `feature_deltas`, `step_kinds`); new recorded extension
  `playbook_claim.playbook_claim_gap_score` (not in frozen composite).
- **G-4a:** `run_g4_escalation_sweep.py` — K∈{1,2,3,5,7,10} on 135
  episodes; K=3 precision 0.97/recall 0.87; K=7 recall 0.96.
- **G-5a:** `redteam._make_config` defaults to high-hazard `build_params`;
  reviewer weights now behaviorally live in search.
- **G-6a:** `eng_capability_probe` + `access:out_of_role` + `LabConfig.
  capability_probe_mode`; admin captured grants out-of-role `cap.sign_off`
  10/10 vs 0/10 uncaptured.
- **G-8a:** `world.run_episode` enforces `LabConfig.build_params` on
  engineer `submit_build` server-side.
- CODE_VERSION `lab-sim-0.6.0`; 211 tests green; regression digest re-pinned.

## Key paths

- `experiments/lab-simulation/lab_sim/playbook_claim.py`
- `experiments/lab-simulation/run_g{1,4,6}_*.py`
- `experiments/lab-simulation/results/FINDINGS.md` (G-1a–G-8a)
- `experiments/lab-simulation/results/g{1,4,6}_*.json`

## Open / next

- Re-run Phase 8 LLM spot-check under enforced high-hazard (G-8 fix).
- D3 ecology notes still untracked; `site/about/index.astro` unrelated edit.

## Commit

`0bfaf6c` — Close lab-simulation open findings G-1 through G-8 (follow-up tranche).
