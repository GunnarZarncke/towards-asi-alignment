# 2026-06-25 — Assumptions appendix E + ledger verification

## Trigger
Verify chapter assumptions against ledger; add assumptions appendix with chapter refs; remove Executive Overview Assumptions section; point frontmatter to chapters + appendix.

## Done
- Verified chapter assumption sources; added **A-011** (ch02 civilizational minimum), **A-012** (ch14 co-scaling hinge).
- Restructured `metadata/assumptions-ledger.md` with verification table + `## Appendix index` tables (23 entries).
- Added `scripts/generate_assumptions_appendix.py` → `metadata/assumptions-index.tex`.
- Added `appendices/appE-assumptions.tex`; wired into `book.tex` and `build.sh`.
- Removed EO `\section*{Assumptions}` stubs; added appendix pointer after Thesis.
- Updated `check_structure.py` (10 appendices), `init_scaffold.py`, `tables/assumptions-table.tex`, README, INSTRUCTIONS.
- `./build.sh` passes.

## Decisions
- Appendix E = collated index (like A); full maintainer detail stays in markdown only.
- ch31 safety-case *example* assumptions are instance-level, not book-wide A-rows.
- ch21 non-presupposition of agency is methodological, not a ledger assumption.

## Open / next
- Link U-06 explicitly to A-012 in uncertainty ledger if revising that file.

## Key paths
- `metadata/assumptions-ledger.md`, `appendices/appE-assumptions.tex`, `frontmatter/executive-overview.tex`

## Commits
- none (not requested)
