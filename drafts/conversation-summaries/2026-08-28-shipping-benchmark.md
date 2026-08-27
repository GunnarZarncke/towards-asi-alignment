# 2026-08-28 — TSA shipping benchmark

## Trigger

User asked for a benchmark of how quickly TSA content ships: investigate GitHub history, cross-index with conversation logs, estimate work days (8h/day, weekends included), account for parallel lanes, save in `drafts/`.

## Done

- Added [`drafts/tsa-shipping-benchmark.md`](../tsa-shipping-benchmark.md): 73-day window (2026-06-17 → 2026-08-28), 662 commits, 633 session logs, 62 estimated work days (496h), release velocity table (v1.0.0 at +13d through v1.5.0 at +66d), 54-row deliverable table with conversation log cross-refs, parallel burst calendar, lane index, planning throughput notes.
- Method: work day = ≥1 session log or ≥3 commits; per-deliverable days from tagged sessions; global budget not summed (lanes overlap).

## Decisions

- **8h effective day** reflects Berlin 10:00–03:00 interrupted schedule, not agent wall time.
- Pre-repo draft import (2026-06-17) excluded from work-day totals.
- Housekeeping-only commits excluded from deliverable rows but included in intensity stats.

## Open / next

- Optional: script under `scripts/` to regenerate tables from `git log` + session filenames after future releases.
- Unrelated working-tree changes (manuscript A-* boxes, alignment crux map, etc.) left unstaged for other sessions.

## Key paths

- [`drafts/tsa-shipping-benchmark.md`](../tsa-shipping-benchmark.md)
- `drafts/conversation-summaries/archive/2026-{06,07,08}-INDEX.md`
- `RELEASE_NOTES.md`

## Commits

- `1554b311` Add a shipping benchmark cross-indexing git history and session logs.
