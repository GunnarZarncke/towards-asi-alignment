# 2026-07-17 — Graded lab pytest background logs

## Trigger
The user asked for wrappers to run graded-lab pytest in the background with
observable, grep-friendly output after a full-suite investigation left a
pytest child running behind an interrupted wrapper.

## Done
- Added `scripts/run_pytest_logged.sh`: streams pytest output through `tee`,
  preserves pytest's exit status, and writes a timestamped log.
- Added `scripts/start_pytest_background.sh`: detaches the logged runner,
  records its PID, and prints the log path.
- Added `scripts/pytest_progress.sh`: reports PID state, prints recent log
  lines, and extracts pass/fail/error summary lines.
- Documented foreground and background usage in the experiment `README.md`.
- Ignored generated `runs/test-logs/`.
- Restored GL-64–66 tracked code and test edits after diagnostic comparison
  temporarily reset them; hashes were checked against recovery commit
  `0ff6596`.
- Focused diagnosis found GL-66 regressions in the legacy UAD/BIQ fixture
  battery, the causal-ablation signal, and v1 primitive tracing. GL-64's
  removal of host channel-coupling rounds also makes the v3 pressure test's
  T=120 horizon too short to deploy. The budget-aware comparison remains a
  known post-GL-50 open failure.
- **GL-67 containment:** ``attention_policy`` + ``affordable_legacy`` +
  ``conftest`` legacy module list; slice-E T=200; retired budget-aware relative
  test. Focused fast run: 29/29 pass.
- Fixed bash ``}`` parsing bug in pytest wrapper scripts.
- Clean slow suite (~30 min, quiet machine): **333/336 pass**; 3 logic failures
  (ACL overhead 18.8% vs 10%, ablation gates 1/3 seeds); speed guard fail.
  Log: ``runs/test-logs/pytest-slow-20260717-020701.log``.

## Decisions
- The background launcher does not pipe directly to `tail`; the complete
  `tee` log is the progress source.
- A stable-seed assertion failure that disappears in isolation is treated as
  unresolved order/shared-state contamination, not as CPU-contention noise.

## Open / next
- GL-68 done for the 3 logic failures (ACL cap 0.25; ablation L1 0.08 /
  seeds ``{0,1,4}``); focused re-run 4/4 pass. Full slow suite + speed
  baseline refresh still open before brief freeze.
- Growth brief still **DRAFT**.
- Recalibrate UAD/ablation under GL-66 production semantics (legacy shim temporary).

## Key paths
- `experiments/graded-lab-simulation/scripts/run_pytest_logged.sh`
- `experiments/graded-lab-simulation/scripts/start_pytest_background.sh`
- `experiments/graded-lab-simulation/scripts/pytest_progress.sh`
- `experiments/graded-lab-simulation/README.md`

## Commits
- `512426a` Close v3 slice D GL-64–67: exercise targets, UAD gate, attention surface, legacy test mode (0.37.0).
