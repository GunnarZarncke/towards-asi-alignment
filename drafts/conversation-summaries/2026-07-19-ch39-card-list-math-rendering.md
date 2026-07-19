# 2026-07-19 — ch39 card list math rendering

## Trigger
Formulas in `/cards/chapters/ch39/` broke from **Decision Triggers** onward: raw `$$`, visible `</li>` tags, and garbled prose through Summary.

## Done
- Root cause: `tex-convert.mjs` emitted LaTeX `enumerate`/`itemize` as HTML `<ol>/<li>`. CommonMark does not run remark-math inside HTML blocks, so display math in list items was not KaTeX-rendered and broke the rest of the page.
- Fixed `convertList()` to emit markdown lists with indented block content and `convertDocument()` per item (not inline-only conversion).
- Ran `npm run sync:chapters` and `npm run build`; verified KaTeX in `dist/cards/chapters/ch39/` for Stop Triggers and Summary.

## Open / next
- Deploy site (push to `main` or gh-pages build) for live fix.

## Key paths
- `site/scripts/lib/tex-convert.mjs`

## Commits
- (none — user did not request commit)
