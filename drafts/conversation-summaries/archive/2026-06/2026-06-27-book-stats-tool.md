# 2026-06-27 — Book stats tool

## Trigger
User asked for a small tool (if not already present) that generates a markdown report with chapter/frontmatter sizes (words, lines, pages), reference counts, formula counts, anchors per chapter, totals, and other usual stats.

## Done
- Added `scripts/book_stats.py` — writes `metadata/book-stats.md` by default (`-o` to override).
- Added `make bookstats` target in `Makefile`.
- Documented in `README.md` build commands section.
- Ran once against current build artifacts (`book.toc`, `book.log`).

## Decisions
- Reused approximate word-count stripping from existing `scripts/wordcount.py` rather than refactoring wordcount to import shared code (minimal scope).
- Page spans from `book.toc` when built; no build → pages show as `—`.
- Formulas count display-math environments only (not inline `$...$`).
- Citation stats match `check_citations.py` (132 cited keys vs 328 bib entries).

## Open / next
- Optional: wire `make bookstats` into `make check` or post-build hook if desired.
- Optional: count `\nocite` / printed-bibliography entries separately from inline cites.

## Key paths
- `scripts/book_stats.py`
- `metadata/book-stats.md`
- `Makefile` (`bookstats` target)

## Commits
- (none this session)
