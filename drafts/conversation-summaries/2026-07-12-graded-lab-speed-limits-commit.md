# 2026-07-12 — Graded lab Phase 5 freeze + speed limits (commit)

## Trigger

Continue Phase 5 referee port; compare test runtimes to lab-sim; add per-test
and suite speed enforcement; end-of-session commit.

## Done

- **Phase 5 freeze** (`graded-lab-0.6.0`): `events.py`, `detectors.py`,
  `twins.py`, `escalation.py`; programs `walk_pipeline`, `inflate_pipeline`,
  `honest_twin`; pipeline affordable-set fixes; G-8 in `FINDINGS.md`.
- **Speed / cost parity with lab-sim:**
  - `pytest.ini` (`--durations=10`), `tests/speed_limits.json`,
    `tests/speed_baseline.json`, `graded_lab/harness/speed_limits.py`,
    conftest enforcement (hard cap, suite cap, regression slack).
  - `EpisodeResult.wall_seconds`, `episode_cost.py` ledger,
    `report_isolate_cost.py`, `verify_isolate_equivalence.py` timing summary.
  - `@pytest.mark.slow` on Phase 3 20-seed gates; `--fast` dev loop (~34s).
- **Verification:** 82 tests green; speed OK at ~75–79s suite; 5-seed
  isolate equivalence green.

## Decisions

- Default pytest runs full suite with speed enforcement; `--fast` skips slow
  gates and uses `fast_suite_max_seconds` (58s).
- Baselines refreshed with `--update-speed-baseline --no-speed-check`.
- Unrelated drafts (`ai-salon-uad-demo-slides.md`, `hostile-review.md`,
  embedded-value-formation logs) left unstaged.

## Open / next

1. Phase 6 blind behavior features.
2. Phase 3b carrier calibration battery.
3. Phase 7a–7c UAD-backed BIQ.

## Key paths

- `experiments/graded-lab-simulation/` (full package)
- `experiments/graded-lab-simulation/tests/speed_{limits,baseline}.json`
- `drafts/conversation-summaries/2026-07-12-graded-lab-speed-limits-commit.md`

## Commits

- `44edbd6` — Add graded-lab simulation through Phase 5 freeze and speed limits.
