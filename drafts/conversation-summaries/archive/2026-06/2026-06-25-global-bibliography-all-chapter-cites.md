# 2026-06-25 — Global bibliography includes all chapter citations

## Trigger
User asked for the back-matter bibliography to include all references cited across chapters.

## Done
- Added `references/manuscript-citations.bib` with 45 cite keys that were in chapters but missing from category bibs.
- Added `scripts/generate_global_nocite.py` → `metadata/global-nocite.tex` (110 cited keys); wired into `build.sh`.
- Updated `book.tex`: load `manuscript-citations.bib`, `\input{metadata/global-nocite.tex}` before `\printbibliography[title={Bibliography}]`.
- Root cause: chapter `\begin{refsection}` isolates citations; refsection 0 had only glossary cites until `\nocite` registered all keys for the global list.
- `python3 scripts/check_citations.py` passes; `./build.sh` passes; refsection 0 bbl lists 110 entries.

## Decisions
- Keep per-chapter sub-bibliographies unchanged; global bib uses `\nocite` in refsection 0 rather than removing refsections.
- New missing keys live in `manuscript-citations.bib` until merged into category files via import script.

## Open / next
- Optional: run `scripts/import_source_map_refs.py` when sibling repos are available and fold `manuscript-citations.bib` into category files.
- Optional: deduplicate entries that appear in both global bib and chapter sub-bibs (intentional for now).

## Key paths
- `book.tex`, `build.sh`, `references/manuscript-citations.bib`, `scripts/generate_global_nocite.py`, `metadata/global-nocite.tex`

## Commits
- (none this session)
