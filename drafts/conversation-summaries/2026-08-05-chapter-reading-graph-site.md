# 2026-08-05 — Chapter reading graph on site

## Trigger
Add companion-site card and interactive chapter reading DAG (clickable chapter links) from guided paths; fix serve/build failures and visible `\n` in node labels.

## Done
- **Site:** `/paths/chapter-reading-graph/` — clickable SVG (48 chapters → chapter cards); artifact card `chapter-reading-dependency`; callout on `/paths/`.
- **Sync:** `site/scripts/sync-chapter-reading-graph.mjs` + `ChapterReadingGraph.astro`; `dot-parse.mjs` quoted node IDs; wired into `npm run sync`.
- **Build fix:** `lean/index.astro` — LaTeX moved to `String.raw` (JS escape `\t`, `\r`, `\v`).
- **Label fix:** `build_chapter_symbol_dependency.py` — real newlines into `dot_label()` (was `\\n` → literal backslash-n in SVG).

## Decisions
- Graph page is canonical interactive view; card summarizes semantics + links to graph.
- Chapter hrefs root-relative (`/cards/chapters/chNN/`) for site-wide SVG links.

## Open / next
- Refine `chapter-informal-edges.yml` as editorial pass continues.
- C12 basin operationalization (symbol island) still open.

## Key paths
- `site/src/pages/paths/chapter-reading-graph.astro`
- `site/scripts/sync-chapter-reading-graph.mjs`
- `site/src/content/cards/chapter-reading-dependency.md`

## Commits
- `edaff449` Add clickable chapter reading graph to companion site.
