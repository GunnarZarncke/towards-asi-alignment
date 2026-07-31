# 2026-07-13 — Graded lab Phase 7c: ecology calibration battery

## Trigger

User asked to continue implementation after Phase 7b commit (`d8ab097`).
Next phase per `PLAN.md`: Phase 7c ecology calibration battery.

## Done

- Pre-registered Phase 7c in `DESIGN.md` ("Phase 7c ecology calibration
  battery") before code: 16-cell substrate grid, 10 seeds, two agent types,
  four pass criteria, dose-response throttle factors, sweet-spot rule.
- Implemented `graded_lab/oracle_only/calibration.py`:
  - `programs_for`, `substrate_grid`, `eai_band`, `evaluate_pass_criteria`
  - `run_calibration_episode`, `run_dose_response`, `run_calibration_battery`
  - `select_mid_band_cell` for sweet-spot selection
- Implemented `run_phase7_calibration.py` (full battery + `--smoke` dev mode).
- Added `tests/test_phase7_calibration.py` (7 tests; slow smoke uses
  `compute_i_ctrl=False` for CI speed — full `I_ctrl` path is the runner).
- Smoke run (`--smoke`): criterion 1 passed, 2–4 failed (expected for
  2-cell corner grid — documented in G-15).
- Started full 16-cell battery in background (`run_phase7_calibration.py`);
  was at ~106/320 episodes when session ended (~26 min elapsed, ~80 min
  estimated total).
- Updated `PLAN.md`, `README.md`, `FINDINGS.md` G-15, speed limits/baseline.
- `CODE_VERSION` `0.11.0 → 0.12.0`.

## Decisions

- `programmatic_2step` = walk_pipeline engineer + reviewer_peer_review +
  honest_twin for rm/admin (deterministic weak agent).
- Pytest smoke integration skips `I_ctrl` (`compute_i_ctrl=False`) to keep
  suite ~200s; full battery runner always computes `I_ctrl` in mid band.
- Smoke battery failures on criteria 2–4 are **not** substrate failures —
  the 2-cell grid cannot span pre-registered EAI bands.

## Open / next

- Wait for full `run_phase7_calibration.py` to finish; read
  `results/ecology_calibration.json` and update G-15 with honest full-battery
  pass/fail (may require substrate allowance adjustment per PLAN if fail).
- Phase 8 multi-episode/selection only if Phase 7c sweet-spot gate passes.

## Key paths

- `experiments/graded-lab-simulation/graded_lab/oracle_only/calibration.py`
- `experiments/graded-lab-simulation/run_phase7_calibration.py`
- `experiments/graded-lab-simulation/results/ecology_calibration.json`
- `experiments/graded-lab-simulation/tests/test_phase7_calibration.py`

## Commits

- None yet this session.
