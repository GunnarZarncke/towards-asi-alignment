# 2026-08-15 — zaman2014 site citation fix

## Trigger
Site chapter sync failed CI: unresolved citation `zaman2014`.

## Done
- Added `zaman2014` (Zaman et al. 2014, PLoS Biology / Avida coevolution) to `references/manuscript-citations.bib` and a matching `\bibsummary`.
- Chapter 34 already cited the key; the entry lived only in `papers/alignment-under-selection/alignment-under-selection.bib`.

## Decisions
- Copy the paper bib entry into the book bibliography rather than dropping the ch34 cite. Site sync indexes `references/*.bib` only.

## Open / next
- `scripts/check_citations.py` also loads `papers/**/*.bib`, so `make check` did not catch a manuscript cite missing from `references/`. Tighten that checker if this class of miss recurs.

## Key paths
- `chapters/ch34-selection-environment.tex` (cite site)
- `references/manuscript-citations.bib`
- `references/bibliography-summaries.tex`

## Verification
- `python3 scripts/check_bibliography_summaries.py` — pass.
- `python3 scripts/check_citations.py` — pass.
- `node site/scripts/sync-chapters.mjs` — pass.

## Commits
- none (not requested)
