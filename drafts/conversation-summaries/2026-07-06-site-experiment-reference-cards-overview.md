# Session log — experiment & reference cards on overview

**Date:** 2026-07-06  
**Trigger:** User asked to create one card per experiment and reference on the overview page.

## Done

- Added `experiment` card type to `content.config.ts` and `badges.ts` (with optional `experimentLineId`).
- Extended `sync-experiments.mjs` to generate five line cards under `src/content/cards/experiments/` from `metadata/experiments.yml` (role, headline findings, how-to-read, repo links).
- Updated `/cards/` overview (`site/src/pages/cards/index.astro`):
  - New **Experiments** section (5 cards, build order).
  - **Reference cards** section now lists the reference index plus all 344 bibliography cards (was a single placeholder).
- Experiment card pages link to `/experiments/#{lineId}`.
- Gitignore: `src/content/cards/experiments/`.

## Verification

- `npm run sync:experiments` and `npm run sync:reference-cards` succeed.
- `ASTRO_BASE=/ npm run build` → 646 pages.

## Open / next

- None for this task.

## Key paths

- `site/scripts/sync-experiments.mjs`
- `site/src/pages/cards/index.astro`
- `site/src/content/cards/experiments/*.md` (generated)
