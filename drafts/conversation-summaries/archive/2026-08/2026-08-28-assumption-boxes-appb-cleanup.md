# 2026-08-28 — Assumption key-only boxes and App B cleanup

## Trigger
Continue A-* assumption work: Option 1 (key-only box headings, no chapter counter); App B MIRI/field-index meta prose was inaccurate; landscape crosswalk table; companion-site URLs only in frontmatter; end-of-session commit.

## Done
- **`metadata/preamble.tex`:** `bookassumption` environment (heading **Assumption A-011** only); numbered `assumption` kept for App G MB bridges.
- **14 chapter boxes:** `\begin{bookassumption}[A-…]`; `\akey` cross-refs in ch14, ch43, App G.
- **Frontmatter:** “keyed Assumption boxes” wording (intro, preface, executive overview, ch02 footnote).
- **`appendices/appB-bridge-crosswalk.tex`:** Removed `\paragraph{Field agenda index}` (matrix/Field hub out of PDF) and `\paragraph{MIRI writeups}`; folded sourcing + typed-cut notes into opener and “Why a crosswalk”; MB4a/MB5 split sentences; crosswalk table only in `\begin{landscape}…\end{landscape}` with `L{…\linewidth}` columns.
- **`chapters/ch42-safety-case.tex`:** Dropped `/news/` companion-site footnote.
- **PDF:** Rebuilt `dist/pdf/towards-superintelligence-alignment.pdf`.

## Decisions
- Field agenda matrix stays in `reference/field-agendas/` and on the site, not in App B opener.
- `towards-alignment.com` URLs in the book: frontmatter only (`current-status`, preface glossary).

## Open / next
- Optional: `\akey` pass for plain `A-00x` strings still in App B note paragraphs.
- Uncommitted: `drafts/plans/construct.md`, `site/src/data/chapter-reading-graph.json`, `drafts/alignment-crux-map.md`.

## Commit
`8912c222` — Use key-only assumption headings and slim App B crosswalk opener.
