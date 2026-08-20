# 2026-08-16 — Resumable offline caching (asset-first)

## Trigger
User reported offline mode unreliable: interrupted runs restarted from zero; CSS and other critical assets should cache before pages.

## Done
- `site/public/sw.js` (v9): two-phase cache (styles/assets then pages); skip already-cached URLs on resume; enable offline after asset phase; persist progress in cache; migrate legacy cache buckets on SW update; dedupe concurrent `cache-site` runs.
- `site/src/components/OfflineButton.astro`: phase-aware progress text; query status on load; “Continue offline caching” for partial runs.

## Decisions
- Offline mode turns on after the asset phase so styled pages work while page caching continues.
- SW cache version bumped to v9; older `asi-alignment-site-*` entries migrate instead of being wiped.

## Open / next
- After deploy, users may need one hard refresh to pick up v9 SW.
- PDFs and demos remain excluded by design.

## Key paths
- `site/public/sw.js`
- `site/src/components/OfflineButton.astro`

## Commits
- `e1d36683` — Make offline caching resumable with asset-first priority.
