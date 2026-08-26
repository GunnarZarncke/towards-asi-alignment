# 2026-08-26 — Book contents and experiment coverage

## Trigger
User asked for the Book page to match PDF structure and to restore appendices (A/E/G had no chapter cards). End-of-session commit.

## Done
- `/book/` is a full contents map: front matter (incl. TOC / lists), ten parts with numbered chapters, appendices in `book.tex` order (A, B, C, M, D, E, F, G, N), back matter (bibliography + index).
- Appendices without cards link to site homes: A → `/notation/`, E → `/glossary/`, G → `/lean/`; others use chapter cards via shared `chapterCardFor`.
- `/book/map/` 301s to `/book/`.
- `/experiments/coverage/` slimmed to six jump cards + folded sections; coverage matrix gets `#coverage-matrix` anchor.
- Chapter-reading dependency graph synced (ch06→ch10 informal; ch07→ch35 ε; ch08→ch31 informal; layer reorder; ch04 fillcolor).

## Decisions
- Front-matter prose items share the frontmatter card link; TOC / figure / table lists are plain text (no site pages).
- Index listed in back matter but not linked (PDF-only today).

## Open / next
- Site nav landing pass mostly done; Field hub simplification and copy pass on lower-traffic landings remain in TODO if desired.

## Key paths
- `site/src/pages/book/index.astro`
- `site/src/pages/experiments/coverage/index.astro`
- `metadata/concept-graph/chapter-reading-dependency.md`

## Commits
- (pending)
