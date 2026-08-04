# 2026-07-16 — Graded lab slice D criteria freeze (GL-53)

## Trigger
User: run reference battery to improve estimates; then document and apply
frozen values with confidence tiers; end of session and commit.

## Done
- Ran n=50 calibration battery at T=200 (~9 min); snapshot at
  `experiments/graded-lab-simulation/results/slice_d_reference_battery_T200_n50.json`.
- Applied `V3_REFERENCE_T=200` in `ecology_complexity._reference_episode_config`
  (v2 stays T=100).
- Added `DESIGN.md` § PLAN_v3 slice D with confidence table; GL-53 in
  `FINDINGS.md`; README/PLAN_v3 status updates.
- Added `scripts/run_slice_d_reference_battery.py` (repro runner).
- Updated tests: C1-v3 reference battery now asserts pass at frozen horizon;
  speed limits raised for T=200 reference batteries.
- `CODE_VERSION` → `graded-lab-0.27.0`.

## Decisions
- **T=200** frozen for v3 reference checker (not 160): interior C4 with margin
  (deploy 0.68) and stable C1-v3 at n=50.
- **Checker seeds stay n=20**; n=50 used for point-estimate CI only.
- **Confidence:** structural constants (slots=1, coupling rounds=8,
  min_effect_bits=0.3, C3 bands) high; C4/C1-v3 high at T=200; seed count
  medium for significance claims.

## Open / next
- Slice D remainder: growth protocol FINDINGS entry, detector coverage
  battery, `ProgramMap` overlap report, load-bearing Part B for default agents.
- Re-baseline calibration `uad_partition_match` / ecology-BIQ under GL-51.

## Key paths
- `experiments/graded-lab-simulation/graded_lab/harness/ecology_complexity.py`
- `experiments/graded-lab-simulation/DESIGN.md` (slice D section)
- `experiments/graded-lab-simulation/results/slice_d_reference_battery_T200_n50.json`

## Commits
- `043de0f` Freeze v3 reference battery at T=200 after slice D calibration (GL-53).
