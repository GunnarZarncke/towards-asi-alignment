# 2026-07-02 — Site: chapters as rendered web pages

## Trigger
Implement the approved plan to convert LaTeX chapters (and selected front matter / appendices) into standalone Astro pages with build-time math rendering, resolving internal cross-references and citations to site links (preferring curated cards when `bookLabels` match).

## Done
- Added `book` content collection and `bookLabels` field on cards in [`site/src/content.config.ts`](site/src/content.config.ts).
- Gitignored generated [`site/src/content/book/`](site/src/content/book/) and [`site/src/data/references.json`](site/src/data/references.json).
- Built LaTeX→Markdown pipeline:
  - [`site/scripts/lib/tex-convert.mjs`](site/scripts/lib/tex-convert.mjs) — parser for chapters, math, tables, theorem boxes, lean spine, epigraphs, figures.
  - [`site/scripts/lib/bib-index.mjs`](site/scripts/lib/bib-index.mjs) — bib + bibliography-summary index.
  - [`site/scripts/lib/card-index.mjs`](site/scripts/lib/card-index.mjs) — card label → slug mapping.
  - [`site/scripts/sync-chapters.mjs`](site/scripts/sync-chapters.mjs) — generates 53 pages (48 chapters + front matter + appB/C/D/F) and 376 references; fails build on unresolved refs/cites.
  - [`site/scripts/check-book-links.mjs`](site/scripts/check-book-links.mjs) — wrapper for link validation.
- Wired sync into `npm run sync` / `prebuild`; added `@astrojs/markdown-remark`, `remark-math`, `rehype-katex` with book macros (`\MI`, `\Correctable`, `\DL`).
- Added [`site/src/pages/book/[id].astro`](site/src/pages/book/[id].astro) and [`site/src/pages/references/index.astro`](site/src/pages/references/index.astro).
- Updated book map, card side-panel chapter links, and nav (References).
- Backfilled `bookLabels` on ~25 concept cards (Parts I–II spine + correction-channel card).
- Fixed critical bug: `refsection` environments were stripped instead of passing body content through.
- Verified: `npm run build` → 104 pages.

## Decisions
- **KaTeX at build time** (not client MathJax): faster static pages, consistent with existing card formula rendering.
- **Generated book markdown is gitignored** — LaTeX remains source of truth; sync runs on every build.
- **PDF-only fallback** for labels in excluded appendices (appA/E/G etc.): link text + GitHub Releases PDF URL.
- **Two-tier ref resolution**: `bookLabels` / `formulas[].id` → card page; otherwise in-chapter anchor on `/book/<id>/`.

## Open / next
- Improve card `bookSections` to carry LaTeX label ids for direct section anchors (currently links to chapter top only).
- Extend `bookLabels` backfill to Parts III–X cards as those are authored.
- Spot-check math edge cases in long chapters (nested align, unusual macros) during reading passes.
- Optional: copy `figures/` into `site/public/` for local offline figure viewing instead of GitHub raw URLs.

## Key paths
- [`site/scripts/sync-chapters.mjs`](site/scripts/sync-chapters.mjs)
- [`site/scripts/lib/tex-convert.mjs`](site/scripts/lib/tex-convert.mjs)
- [`site/src/pages/book/[id].astro`](site/src/pages/book/[id].astro)
- [`site/src/content/book/ch01.md`](site/src/content/book/ch01.md) (generated, gitignored)

## Commits
- (none — user did not request commit)
