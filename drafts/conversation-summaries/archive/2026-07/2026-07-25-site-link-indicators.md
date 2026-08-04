# 2026-07-25 — Site link-type indicators

## Trigger

User: many links on `site/` point to different kinds of content (cards, PDFs, GitHub, demos, other external sites), indicated inconsistently. Standardize: (a) internal site cards/pages — no indicator, (b) PDFs — small "(PDF)", (c) GitHub content — small git icon, (d) demos etc. — open-in-new-tab indication, (e) other external content — external-link symbol.

## Done

- Added `site/src/components/LinkIndicator.astro`: renders `(PDF)` text or a small inline SVG (github / new-tab / external-arrow) after link text, given a `kind` prop.
- Added `.link-indicator*` CSS classes to `site/src/styles/global.css`.
- Added `classifyLinkKind(url)` helper to `site/src/lib/site-urls.ts` (pdf / github / external by URL shape) for data-driven links (author profile, reference cards) where the destination isn't known statically.
- Applied `LinkIndicator` + (where missing) `target="_blank" rel="noopener noreferrer"` across every raw external/demo/GitHub link found in `site/src`:
  - `layouts/SiteLayout.astro` (footer GitHub links)
  - `pages/cards/[...slug].astro` (reference publication links, Lean spine node links, evidence "results" links, demo block, generic external-links list)
  - `pages/demos/index.astro` (all demo launch/standalone/source/live links)
  - `pages/faq.astro`, `pages/book/index.astro`, `pages/about/index.astro` (GitHub, aintelope, LessWrong/preprint, publication PDFs via `classifyLinkKind`)
  - `pages/lean/index.astro`, `pages/lean/node/[id].astro`, `components/LeanCodeBlock.astro`, `components/LeanSpineSource.astro`, `components/LeanTryIt.astro` (GitHub source + Lean 4 Web external tool)
  - `pages/updates/index.astro`, `pages/experiments/index.astro`, `pages/experiments/findings/[id].astro` (GitHub release notes / ledgers / EXPERIMENTS.md)
  - `components/ReferencesByChapter.astro` (DOI/URL publication links via `classifyLinkKind`)
  - `pages/paths/[slug].astro`, `pages/paths/index.astro` (demo-kind reading-path steps and spotlights get the new-tab indicator + `target="_blank"`)
  - `content/reading-paths/philosopher.md` (one inline external link, hand-written with raw HTML + inline SVG since it's inside markdown body copy)
- Verified with `npm run build` (site) — 729 pages built clean; spot-checked generated HTML on `/demos/`, `/about/`, and a card page for indicator classes.

## Decisions

- Internal `cardHref`/`bookHref`/etc. links get no indicator (category a), matching the "no indicator" instruction.
- Self-labeled PDF links (button text already says "PDF", e.g. nav "PDF", "Download PDF") were left as-is rather than double-labeled with `(PDF)`.
- Demo launch links (site's own `/chapter-demos/...` pages) were changed to `target="_blank"` plus the new-tab icon, since the user's category (d) implies opening in a new tab, not just labeling.
- GitHub-hosted `.pdf` files (e.g. author's papers in sibling repos) are classified as `pdf`, not `github`, since the content itself is a PDF — content type wins over host.
- Removed the redundant literal "(GitHub)" text suffixes on ledger/experiment links now that the icon conveys the same thing (erasure of duplicate signal).

## Open / next

- Did not touch `site/src/content/cards/*.md` or `site/src/content/book/*.md` prose bodies (rendered manuscript/card content) — those may contain inline external links too, but weren't in scope of the "site" chrome audit and would need a markdown-aware pass if desired.
- Did not audit `site/src/content/reading-paths/*.md` beyond the one external link found; other reading-path files had no raw external links at audit time.

## Key paths

- `site/src/components/LinkIndicator.astro`
- `site/src/lib/site-urls.ts` (`classifyLinkKind`)
- `site/src/styles/global.css` (`.link-indicator*`)

## Commits

- (none yet — uncommitted at end of session)
