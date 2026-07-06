# 2026-07-06 — Site reading guides unified steps

## Trigger
User reported guided tour / reading paths were incomplete and not well tuned to audience — each path should include a coherent ordered list of material (concept cards, chapter toys, experiment lines, book chapters).

## Done
- Replaced path schema `cards: string[]` with structured `steps[]` (`kind`: card | demo | experiment | book | lean; `ref`; optional `note`) in `site/src/content.config.ts`.
- Rewrote all six path files under `site/src/content/paths/` with audience-curated ordered steps mixing cards, demos, experiments, and book chapters.
- Updated `site/src/pages/paths/[slug].astro` to render a unified numbered "Read in this order" list with kind badges and cross-links to demos/experiments index.
- Updated guided tour index lede in `site/src/pages/paths/index.astro`.
- Added `id={line.id}` anchors on experiment line sections in `site/src/pages/experiments/index.astro` for path deep links.
- `npm run build` in `site/` succeeds.

## Decisions
- Unified `steps` array (not separate per-kind lists) so reading order is explicit and audience-tuned.
- Kept `featuredWorkedExample` / `featuredLean` callouts for paths that benefit from prominent BioShield or Lean entry points.
- Generalist/funder paths stay lighter on experiments; engineer/researcher paths include multiple experiment lines; philosopher path emphasizes value/bearer demos and synthesis chapters.

## Open / next
- Add more chapter demos to paths as the demo inventory grows.
- Consider showing step count / estimated time on path index cards.
- User may want to tune individual step notes after reading each path end-to-end.

## Key paths
- `site/src/content/paths/*.md`
- `site/src/pages/paths/[slug].astro`
- `site/src/content.config.ts`

## Commits
- None (user did not request commit).
