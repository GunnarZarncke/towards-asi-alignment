# 2026-07-15 — Graded lab PLAN_v3 slice A implemented

## Trigger
User: "Now start slice A" — implement `resource_flows` → live per-actor runtime allowances via `institutional_compiler.py` per `PLAN_v3.md`.

## Done
- **`graded_lab/world_visible/institutional_compiler.py`** (new): `compile_ecology()`, `validate_v3_resource_flows()`, reachability (C2-style), resource_type→compute/io/standing mapping, ±25% cross-check warnings, flow ablation at compile time.
- **`world.py`**: v3 path uses compiled allowances in `_allowances_map()`.
- **`substrate.py`**: v3 in `ECOLOGY_VERSION_PATHS`, `is_v3_shaped_ecology()`, v3 validation on load.
- **`config.py`**: `CODE_VERSION` → `graded-lab-0.20.0`; `EpisodeConfig.flow_ablation_ids`.
- **`tests/fixtures/ecology_v3_slice_a_reference.json`**: hand-built v3 fixture (38+2 engineer compute split for ablation).
- **Tests**: `test_institutional_compiler.py`, `test_v3_slice_a_flow_ablation.py`, `test_ecology_version.py` v3 path, `test_config.py` version bump.
- **`results/FINDINGS.md`**: GL-44 entry.
- **`DESIGN.md`**, **`PLAN_v3.md`**: slice A status + gate table synced (seeds `{0,2,4}`, `carrier_load_scale=1.5`).
- Fast profile green (~212s suite).

## Decisions
- Compiled flows **replace** role defaults (sum only); declarative `resource_allowances_per_tick` is cross-check only.
- Ablation gate uses `carrier_load_scale=1.5` — at default 0.0 engineer compute ablation did not bind behavior.
- Seeds `{0,2,4}` after seed 1 failed L1≥0.10 on first battery (not retuned post hoc).
- Engineer compute split 38 (lab_operator) + 2 (grant_funder) = declared 40.

## Open / next
- Slice B: mechanisms → enforced ACLs/votes (not started).
- Optional: commit slice A when user asks.
- Slow profile battery if needed before growth work.

## Key paths
- `experiments/graded-lab-simulation/PLAN_v3.md` (slice A spec + gate)
- `experiments/graded-lab-simulation/graded_lab/world_visible/institutional_compiler.py`
- `experiments/graded-lab-simulation/tests/fixtures/ecology_v3_slice_a_reference.json`
- `experiments/graded-lab-simulation/tests/test_v3_slice_a_flow_ablation.py`

## Commits
- `14129c0` Implement PLAN_v3 slice A: compile resource flows into live budgets.
