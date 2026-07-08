# 2026-07-08 — Lab sim D3.1–D3.2 selection ecology

## Trigger
Implement D3.1; run full D3.1 battery in background while implementing D3.2; end session + commit; add TODO for toy demo.

## Done
- **D3.1:** `lab_sim/harness/d3_population.py`, `run_d3_population.py`, 5 tests. SubprocessIsolate battery (12×8, ~10s). **G-36:** correction-preserving mass 0.083→0.005; winners = captured-board/lenient-admin default-pipeline configs.
- **Bugfix:** aggregate mass shares use `deployment_mass_after` (post-selection).
- **D3.2:** `lab_sim/harness/d3_spec_evolution.py`, `run_d3_spec_evolution.py`, 5 tests. Battery (12×10, ~11s). **G-37:** preserving mass 1→0, shortcut fixation by gen 2, throughput collapse gen 3+ (shortcut×playbook mismatch).
- Docs: `PLAN.md`, `DESIGN.md`, `README.md`, `metadata/experiments.yml`, FINDINGS G-36/G-37.
- **TODO added:** `metadata/TODO.md` §Experiments / demos — D3 selection-ecology interactive demo candidate (`demos/ch08-selection-ecology/`).
- **442 tests green** (lab-simulation suite).

## Decisions
- D3.2 mutation = D2 `upgrade_spec` at ecology timescale (one weakening step), not in-episode `rm_spec_upgrade` pinning.
- No `CODE_VERSION` bump — harness orchestration only.

## Open / next
- D3.3 multi-lab shared world if warranted.
- Shortcut-aware playbooks or document limitation.
- Build D3 toy demo per TODO.

## Key paths
- `experiments/lab-simulation/lab_sim/harness/d3_population.py`
- `experiments/lab-simulation/lab_sim/harness/d3_spec_evolution.py`
- `experiments/lab-simulation/results/d3_population.{json,md}` (G-36)
- `experiments/lab-simulation/results/d3_spec_evolution.{json,md}` (G-37)
- `experiments/lab-simulation/results/FINDINGS.md` G-36, G-37

## Commits
- (pending this session)
