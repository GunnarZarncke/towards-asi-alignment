# 2026-06-30 — Red-team battery + logging

## Trigger
Continue Phase 1 battery; improve progress/completion logging; end-of-session commit.

## Done
- **Logging:** `harness.py` progress every 25 runs (ETA, false-pass count); `format_battery_completion()` banner; expanded session log in `__main__.py`.
- **Phase 1 battery completed:** 1080 runs, T=2000, ~3261s (~54 min); overall false-pass **35%**.
- **Bridge roadmap** added to `experiments/toy-simulation/TODO.md` (MB3/MB8/MB5/MB6b/MB7d scenarios).
- Aborted silent first battery run; restarted with logging.

## Decisions
- Commit experiments only (exclude `drafts/`).
- Phase 1 battery marked done in `experiments/toy-simulation/TODO.md`.

## Open / next
- MB3 `bearer_mismap` (first new bridge scenario).
- Live LLM red-team smoke (Phase 3); Phase 4–5 held off.
- Optional: commit conversation logs separately if user wants.

## Key paths
- `experiments/toy-simulation/results/llm_redteam_battery.json`
- `experiments/toy-simulation/results/llm_redteam_report.md`
- `experiments/toy-simulation/logs/battery-2026-06-30-001014.log`

## Commits
- `66f8b7e` Complete Phase 1 red-team battery and add progress logging.
