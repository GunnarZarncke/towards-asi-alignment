# 2026-07-08 — Site longtable / Appendix B crosswalk fix

## Trigger
Appendix B crosswalk table on the companion site showed raw LaTeX/markdown pipe text instead of a rendered table (`{@{}p{0.13}...}` column spec as first row).

## Done
- Fixed `site/scripts/lib/tex-convert.mjs`: skip mandatory `{...}` args on `longtable`/`tabular`/`tabularx`; strip longtable preamble (`\endfirsthead`/`\endhead` repeat block, rules, caption); emit HTML `<table class="book-table">` instead of broken GFM pipes.
- Verified appB converts to 10 rows (header + MB1–MB10); site build green.
- **Site PDF de-emphasis** (user policy: PDF/book links only in top nav, overview-hub footer, and end of full rendered card pages):
  - Removed footer, home hero, book map hero, guided-tour path footer, and paths-index “Book index” PDF/book CTAs.
  - Overview hubs: removed top and sidebar PDF buttons; kept footer row (“Read full appendix in PDF”) and added “Read in PDF” at end of full synced chapter/appendix pages.
  - `tex-convert.mjs`: unresolved cross-refs without a web page render as plain text (no inline PDF links in synced body).
- Added presentation TODOs to `metadata/TODO.md`; lab-sim detector pivot plan in `experiments/lab-simulation/PLAN.md`.

## Decisions
- HTML tables in synced book markdown rather than GFM pipes — more reliable when LaTeX cells contain `|` or column counts were mismatched.
- Nested `\begin{...}` inside tables also skips column-spec args via shared `skipBeginArgs`.

## Open / next
- Push `main` (1 commit ahead of `origin/main` as of session end: `3dd5b37`).
- v1.1.0 tag still points at `baf7d1c` (before site CI fix `66d005f`); consider `v1.1.1` or retagging if publishing.
- Other unstaged/untracked drafts from prior sessions remain outside this commit (demos, experiment cards, generated `.tex` fragments, etc.).
- Presentation & legibility TODOs in `metadata/TODO.md` (per-part renumbering, real worked example, bridge/assumption separation) still open.

## Key paths
- `site/scripts/lib/tex-convert.mjs`
- `appendices/appB-bridge-crosswalk.tex`
- `site/src/components/BridgeCrosswalkTable.astro` (linked table on appB card — was already fine)

## Commits
- `3dd5b37` Fix site longtable rendering and continue the v1.1 legibility pass.
