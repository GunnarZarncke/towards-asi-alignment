# 2026-07-15 — Graded lab PLAN_v3 slice E (pressure coupling)

## Trigger
User: "continue slices" — resume dependency-ordered v3 build after slice F; implement slice E (feedback-coupled pressure + task injection).

## Done
- `graded_lab/world_visible/pressure_coupling.py`: driver vocabulary, channel parser, accumulator + injection engine, `compute_pressure_drivers()`, task completion helpers.
- `affordable.py`: injected `incident_review` write primitives for pending per-role tasks.
- `world.py`: v3-only pressure tick after `oracle.tick()`, `pressure_diagnostics` on `EpisodeResult`, injected-task logging/completion.
- `workspace.py`: `write_at_path` for deterministic injected artifact paths.
- `substrate.py`: optional v3 `pressure_coupling` validation.
- `tests/test_slice_e_pressure_coupling.py` (7 tests): unit + deploy-driver gate + expiry + v1 unchanged.
- `CODE_VERSION` → `graded-lab-0.23.0`; FINDINGS GL-47; PLAN_v3 + DESIGN.md slice E sections updated.

## Decisions
- On threshold crossing: reset accumulator to 0 (not carry overflow); default `decay_per_tick = 0.05`.
- v2 `exogenous_workload` unchanged for v2 ecologies; v3 uses `pressure_coupling` only.
- Optional v2 cost-multiplier on channel fire deferred (not in minimum viable slice E).
- Task completion: successful write to `artifacts/injected_responses/{task_id}.json` with matching `task_id` in content.

## Open / next
- Slice B completion checklist (ACL overhead, reference agent exercise of governed mechanism ids, C5-v3, UAD live-coupling).
- Slice C (principal scorecard + measured tension).
- Commit when user asks.

## Key paths
- `experiments/graded-lab-simulation/graded_lab/world_visible/pressure_coupling.py`
- `experiments/graded-lab-simulation/tests/test_slice_e_pressure_coupling.py`
- `experiments/graded-lab-simulation/PLAN_v3.md` § Slice E, build-order table
- `experiments/graded-lab-simulation/results/FINDINGS.md` GL-47

## Commits
- (none yet — uncommitted)
