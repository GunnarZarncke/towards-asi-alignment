# 2026-07-25 — Concept card logos (draft + site)

## Trigger
User asked for minimalist square SVG logos for each site concept card, iterated on designs through visual review, then wired the finished set into the companion site.

## Done
- Added `scripts/generate_concept_logos.py` and 41 SVGs under `drafts/illustrations/concept-logos/` (excludes `subsumption-*` field-projection cards).
- Iterated icons from user feedback (arrowhead size, attractor-control, institutional cases, Goodhart broken target, artificial-civilization round-robin vs temple misassignment, etc.).
- Site integration: `site/scripts/sync-concept-logos.mjs` copies drafts → `site/public/concept-logos/`; `ConceptLogo.astro` inlines SVGs; logos on concept card pages and `CardSection` indexes; manifest at `site/src/data/concept-logos.json`.
- `npm run sync:concept-logos` added to site sync/check chain.

## Decisions
- Logos keyed by card slug (no per-card frontmatter) — only concepts with a matching SVG get an icon.
- Source of truth for art remains `drafts/illustrations/concept-logos/`; site copies via sync (same pattern as other generated assets).
- `institutional-entrenchment-corrigibility` uses broken-foundation temple; `artificial-civilization` restored to outer round-robin loop around central model.

## Open / next
- Subsumption (`subsumption-*`) cards still have no logos if desired later.
- Optional: badge index pages (`/badges/type/concept/`) could show logos too.
- `drafts/illustrations/concept-logos/preview.html` is local review only (not synced).

## Key paths
- `scripts/generate_concept_logos.py`
- `drafts/illustrations/concept-logos/*.svg`
- `site/scripts/sync-concept-logos.mjs`
- `site/src/components/ConceptLogo.astro`
- `site/src/lib/concept-logos.ts`

## Commits
- `fc7b73f7` Wire concept card logos into the companion site.
