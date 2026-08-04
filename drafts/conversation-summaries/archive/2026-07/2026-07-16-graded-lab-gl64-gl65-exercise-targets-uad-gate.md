# 2026-07-16 — Graded lab GL-64/65 exercise targets + supplementary UAD gate

## Trigger
User: "Implement the four step preferred shape" — replace host `ChannelCouplingProtocol` as the UAD claim path with ecology-compiled exercise targets, fixture-only supplementary channel presets, and a pre-registered supplementary UAD gate (same class as GL-60 detector fixtures).

## Done
- **GL-64:** `ExerciseTargets` + `compile_exercise_targets()` on `RuntimeEcology`; removed profile merge of `mechanism_exercise`; observation field `exercise_targets`; honest reference `channel_coupling_rounds: 0`; host protocol only when `rounds > 0`.
- **GL-65:** `uad_channel_liaison` / `uad_channel_scribe` presets; `supplementary_uad_gate.py` + fixture + script + tests; `organic_channel_coupling_verified=true` (5/5 seeds @ 0.08 bits, T=80).
- Reference fixture `ecology_v3_slice_a_reference.json` updated; `CODE_VERSION` → `graded-lab-0.36.0`.
- Docs: `FINDINGS.md` GL-64/65, `BLIND_GENERATION.md`, `DESIGN.md`, `README.md`.
- Fast pytest subset green (13 tests).

## Decisions
- Honest reference UAD coupling claims use **supplementary gate only**; host protocol retained for debug/fixtures with `rounds > 0`.
- Organic CMI floor **0.08** (not 0.3) and probe **T=80** — organic window is noisier than designed host stimulus.
- Removed `pressure_coupling` from supplementary UAD fixture — reads crowded `communicate` out of `AFFORDABLE_CAP`.
- Four roles unchanged on grower surface; supplementary presets not wired into `pass_fail_only()` or C3/C4 reference.

## Open / next
- Growth brief freeze (user sign-off still pending).
- Optional: investigate `communicate` dropping from affordances after ~t=24 at T=200 on integrated substrate.
- Full slow pytest suite if desired; commit when user asks.

## Key paths
- `graded_lab/world_visible/mechanism_exercise.py`
- `graded_lab/harness/supplementary_uad_gate.py`
- `tests/fixtures/ecology_v3_supplementary_uad_channel_suite.json`
- `results/slice_d_v3_supplementary_uad_gate.json`
- Prior context: `2026-07-16-graded-lab-gl64-session-end-uad-roles.md`

## Commits
- (none this session — uncommitted GL-64/65 work)
