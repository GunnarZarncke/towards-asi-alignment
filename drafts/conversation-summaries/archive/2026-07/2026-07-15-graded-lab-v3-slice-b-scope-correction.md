# 2026-07-15 — Slice B scope correction (GL-48b)

## Trigger
User review: C5 exercised only by parallel `V3_MECHANISM_REFERENCE`; no integrated A+F+E+B; parallel special paths; Part B not load-bearing for ordinary agents.

## Done
- Removed `V3_MECHANISM_REFERENCE`, `governed_*` programs, separate C5 battery.
- Added ecology field `reference_mechanism_exercise`; host merge in `programs_and_profiles_for_roster(..., ecology_data=)`.
- `_try_governed_mechanism` integrated into `walk_pipeline` / `reviewer_peer_review` / `honest_twin`.
- C5-v3 on same `run_reference_episodes` as C3/C4 when ecology opts in.
- Integrated fixture: `pressure_coupling` + `reference_mechanism_exercise` + metadata (A+E+B).
- Downgraded PLAN/DESIGN/FINDINGS claims: slice B partial; load-bearing Part B → slice D.
- `CODE_VERSION` → `graded-lab-0.24.1`.

## Open / next
- Slice C; slice D strict reference / ProgramMap must target governed ids.
- Refresh speed baselines if CI flags slower unified battery tests.

## Commits
- (none yet)
