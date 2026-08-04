# 2026-07-17 — Site header search UI

## Trigger

User noticed search was missing after content-sync plumbing (index existed but no UI). Implemented header search, refined layout/results, then improved matching (type field + multi-word fallback).

## Done

- Added `site/src/components/SiteSearch.astro`: lazy-fetches `public/search-index.json`, compact input inline at end of primary nav (after PDF).
- Wired into `site/src/layouts/SiteLayout.astro`.
- Results: one line per hit (title + type badge right), ellipsis overflow, up to 20 results.
- Search fields: `title`, `type`, `summary` (tiered scoring: title < type < summary).
- Multi-word fallback when full phrase has zero hits: score each word, sum scores (+500 penalty per missing word), rank by words matched then total score.

## Decisions

- No Fuse.js / server — keep static substring match on the prebuilt index from `build-search-index.mjs`.
- Type in search fixes `experiment` → all six experiment line cards; `chapter` → chapter cards by badge.
- Multi-word fallback only when phrase match is empty (not merged with partial phrase hits).

## Open / next

- Optional `keywords` / aliases on index entries (e.g. "unsupervised agent discovery" → agency-detect) if substring search still misses canonical names.
- Wire `npm run check:concepts` into CI as a separate fast-fail step (site build already regenerates on deploy).

## Key paths

- `site/src/components/SiteSearch.astro`
- `site/scripts/build-search-index.mjs`
- `site/public/search-index.json` (generated, gitignored)

## Commits

- `1116c5c` Add header search with type-aware and multi-word matching.
