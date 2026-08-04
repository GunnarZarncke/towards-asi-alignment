# 2026-07-16 — Graded lab GL-62 Part B preset retarget

## Trigger
User: continue GL-61 path (a) — implement Part B preset retargeting until
freeze-ready, but **do not** freeze growth brief yet.

## Done
- `ecology_governed_affordance_targets` + gating in `world.py` (only when
  `mechanism_exercise_disabled` and no host profile targets).
- `programs.py`: `_try_v3_part_b_governed`, `_try_governed_presets` on frozen
  presets; one-shot kinds before minimal channel credit (budget 2 when coupling
  rounds 0).
- `v3_omit_unbound_lab_affordances` whenever v3 Part B mechanisms declared.
- Fixture `tests/fixtures/ecology_v3_part_b_retarget_alt_ids.json`.
- Tests `tests/test_v3_part_b_retarget.py`; flipped
  `test_c5_v3_negative_control_exercise_disabled`.
- FINDINGS GL-62; `CODE_VERSION` **`graded-lab-0.35.0`**.

## Decisions
- Ecology preset path activates **only** when host merge is explicitly disabled
  (`reference_mechanism_exercise: false` / `enabled: false`) — preserves
  slice E and other episodes that run without injected profiles.
- Preset channel actions must match governed affordance message shape
  (`mechanism_exercise`, not ad-hoc `part_b_preset`).
- Brief **not** frozen (per user).

## Open / next
- Revise growth brief with honest Part B language; then freeze
  `BLIND_GENERATION.md` § V3 when satisfied.
- C3/C4 @ T=200 re-run post GL-62: **pass** (n=20, deploy_rate=0.70).
- `transfer_failure_risk` scope unchanged; supplementary probes (GL-60) stand.
- Commit when user asks (GL-60 + GL-61 docs + GL-62 likely separate commits).

## Key paths
- `graded_lab/world_visible/world.py`
- `graded_lab/agent_visible/programs.py`
- `graded_lab/world_visible/mechanism_exercise.py`
- `tests/test_v3_part_b_retarget.py`
- `results/FINDINGS.md` (GL-62)

## Commits
- (none this session)
