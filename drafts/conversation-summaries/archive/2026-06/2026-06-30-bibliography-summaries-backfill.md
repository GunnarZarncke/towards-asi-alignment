# 2026-06-30 — Bibliography summaries backfill + maintenance

## Trigger
User asked to add missing one-line bibliography summaries and instructions to maintain them.

## Done
- Backfilled **30** missing `\bibsummary` lines (including restored `gordon2020`, `wall1999pain`, cited manuscript/governance/philosophy keys).
- Full coverage: **357** summaries for **357** `.bib` keys.
- Added `scripts/check_bibliography_summaries.py`; wired into `make check`.
- Added `references/README.md`; updated header in `bibliography-summaries.tex`, `AGENTS.md`, `INSTRUCTIONS.md` §7.

## Open
- Editorial tightening of auto-generated glosses (noted in 2026-06-26 log) remains optional.

## Key paths
- `references/bibliography-summaries.tex`
- `scripts/check_bibliography_summaries.py`
- `references/README.md`
