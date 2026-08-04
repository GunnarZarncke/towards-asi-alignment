# 2026-06-17 — Source map references import

## Trigger
User asked to find references from the linked source map in `INSTRUCTIONS.md` §3.0 and incorporate them into the book's bibliography.

## Done
- Added `scripts/import_source_map_refs.py` to merge `.bib` files from sibling repos (`../agency-detect/docs/papers/`, `../brain-to-values/papers/`), plus manual `\begin{thebibliography}` entries from papers without `.bib` files.
- Populated all six categorized `references/*.bib` files with **235 deduplicated entries**:
  - `internal-project-sources.bib`: 23 (all source-map Zarncke papers + alias crossrefs)
  - `external-alignment.bib`: 44
  - `neuroscience-values.bib`: 58
  - `dynamical-systems.bib`: 70
  - `governance-institutions.bib`: 3
  - `philosophy.bib`: 37
- Updated `INSTRUCTIONS.md` §11 with regenerate command.
- Clean rebuild verified (`./clean.sh && ./build.sh` succeeds; biber loads all bib files).

## Decisions
- Canonical internal keys use `zarncke2025*` / `zarncke2026*` with source-path notes; legacy keys (`ZarnckeUAD`, `uad2025`, etc.) kept as BibLaTeX `crossref` aliases for compatibility with source papers.
- Categorization is keyword/heuristic-based; uncategorized technical refs default to `dynamical-systems.bib`.
- Context-only PDF (Units of Caring literature review) has no TeX/bib source; not imported as a separate entry.

## Open / next
- Chapters still need `\cite{}` keys wired in as they are drafted.
- Re-run `python3 scripts/import_source_map_refs.py` after sibling-repo bib updates (manual edit to categorized `.bib` files will be overwritten).
- Optional: tighten categorization rules if entries land in the wrong bucket.
- README.md refreshed (thesis frame, audience, repo map, bibliography, source canon, updated status).

## Key paths
- `scripts/import_source_map_refs.py`
- `references/*.bib`
- `INSTRUCTIONS.md` §3.0 (source map), §11 (reference system)

## Commits
- (none — user did not request commit)
