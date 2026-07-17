# 2026-07-17 — Graded lab GL-75c: V2-3 battery process parallelism

## Trigger
User has 4 spare CPUs; requested parallelism to speed up the V2-3 transfer battery.

## Done
- `graded_lab/harness/machinery_transfer.py`: `workers` param on battery + BIQ;
  `ProcessPoolExecutor` runs UAD seeds and EAI cells in one shared pool; BIQ units
  parallelized in a second pool after UAD completes.
- `scripts/run_v2_transfer_battery.py`: `--workers` (default 4).
- `REPRODUCTION.md` §10.1: updated wall-time estimate with `--workers 4`.
- Test: `test_machinery_transfer_battery_parallel_smoke_on_reference_fixture`.
- `CODE_VERSION` → `graded-lab-0.39.2`.

## Decisions
- API/tests default `workers=1` (serial); CLI default `4` for full runs.
- UAD + EAI concurrent in one pool (70 independent jobs on full run) for load balancing.
- No change to frozen protocol constants or scoring.

## Open / next
- Full V2-3 run with `--workers 4` when ready.

## Key paths
- `experiments/graded-lab-simulation/graded_lab/harness/machinery_transfer.py`
- `experiments/graded-lab-simulation/scripts/run_v2_transfer_battery.py`

## Commits
- None
