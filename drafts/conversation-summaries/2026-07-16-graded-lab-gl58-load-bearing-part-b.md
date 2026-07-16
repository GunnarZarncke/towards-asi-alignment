# 2026-07-16 — Graded lab GL-58 load-bearing Part B

## Trigger
User approved dependency plan and asked to start load-bearing Part B (slice D blocking gate).

## Done
- **GL-58 (`graded-lab-0.32.0`):** auto-merge `mechanism_exercise` targets for all v3 ecologies with Part B `mechanisms` via `mechanism_exercise_profile_for_ecology`; `reference_mechanism_exercise` is optional override only.
- **Strict affordances:** `part_b_strict` on `build_affordable_set` omits unbound `lab` channel + `notes/status` scratch writes when load-bearing Part B is active.
- **C5-v3 gate:** `run_complexity_check` runs C5-v3 whenever `v3_has_part_b_mechanisms` (not only when ecology declares `reference_mechanism_exercise`).
- **Tests:** `test_c5_v3_load_bearing_without_reference_opt_in`, strict affordance unit test, updated battery tests.
- **Docs:** FINDINGS GL-58, README/PLAN_v3/DESIGN version bumps.

## Decisions
- Chose **retarget + scoped strict affordances** over global v3 strict mode — preserves v1/v2 digest-pinned behavior; frozen presets already call `_try_governed_mechanism` first.
- **0.32.1 scope correction:** docs reverted "Part B closed"; renamed to `omit_unbound_lab_affordances`; added exercise-disabled negative control; explicit `reference_mechanism_exercise: false` disables auto-merge.

## Open / next
1. Causal C2-v3 gate (ablation, ≥2 fixtures)
2. Supplementary detector fixtures (blocking for Q1 transfer claims)
3. Revise & freeze growth brief
4. First v3 growth round (mitigation 1) after 1–3
5. Generic walker-step interpreter (before mitigation-2 round)

## Key paths
- `graded_lab/world_visible/mechanism_exercise.py`
- `graded_lab/world_visible/affordable.py`
- `graded_lab/world_visible/ecology_agents.py`
- `tests/test_slice_b_completion.py`
- `results/FINDINGS.md` (GL-58)

## Commits
Not committed (user did not request).
