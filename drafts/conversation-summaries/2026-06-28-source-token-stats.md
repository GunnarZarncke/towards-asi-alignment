# 2026-06-28 — Source token stats

## Trigger

The user asked whether the complete source material could be token-counted easily, and if so to add it to the stats.

## Done

- Updated `scripts/book_stats.py`:
  - added approximate LLM-token counting using `ceil(UTF-8 bytes / 4)`;
  - added `SourceExtractStats` for `context/extracts/*.md`;
  - added summary totals with and without context material:
    - book text sources without `context/`;
    - context extracts only;
    - combined book text sources + context extracts;
  - added a per-extract table to the generated book stats.
- Regenerated `metadata/book-stats.md`.
- Recorded chapter split preferences in `review/chapter-split-preferences-2026-06-28.md`.
- Added detailed ch25 split plan in `review/ch25-split-plan-2026-06-28.md`, recommending a certificate-vs-stress-test split and listing content allocation, chapter connections, cross-reference consequences, appendix options, metadata/book-map updates, and implementation order.
- Added a `metadata/TODO.md` pointer for the split preference pass.

## Decisions

- Counted the book-local readable source extracts in `context/extracts/*.md`, not binary PDFs.
- Counted no-context book text sources as TeX + `.bib` + Lean source files, excluding binary figures.
- Used a documented approximate token heuristic rather than adding a tokenizer dependency.

## Open / next

- If exact model-specific counts are needed later, add optional `tiktoken` / tokenizer support behind a graceful fallback.
- If doing a chapter split pass, start with ch19 and ch35. Treat ch36 as optional/noncritical, and keep ch25 together unless a stronger reason emerges.
- If splitting ch25, use the certificate-vs-stress-test plan rather than a simple theory/application split.

## Verification

- `python3 scripts/book_stats.py` passed.
- `ReadLints` reported no diagnostics for `scripts/book_stats.py`.

## Key paths

- `scripts/book_stats.py`
- `metadata/book-stats.md`
- `review/chapter-split-preferences-2026-06-28.md`
- `review/ch25-split-plan-2026-06-28.md`
- `metadata/TODO.md`

## Commits

- None.
