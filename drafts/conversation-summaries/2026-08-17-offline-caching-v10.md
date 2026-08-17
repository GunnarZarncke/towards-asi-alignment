# 2026-08-17 — Offline caching v10 (partial enable + URL fix)

## Trigger
Offline mode still unreliable: partial caches were not always usable; status was missing when idle; caching aborted with `Failed to construct 'URL'`.

## Done
- `site/public/sw.js` v10: resolve relative URLs against site origin (the abort was `new URL("/manifest…")` with no base); skip bad hrefs; persist durable `offline-state`; enable offline after home + CSS (or after the asset phase); serve cache on network failure once caching has started; parse CSS `url(...)` for fonts.
- `site/src/components/OfflineButton.astro`: always show status (checking / idle / caching / partial / interrupted / complete).

## Decisions
- Enable threshold is home page plus at least one CSS file, not the full site.
- Interrupted runs keep counts and say whether partial offline is already usable.

## Open / next
- After deploy, hard-refresh once so v10 replaces v9.
- PDFs and demos remain excluded.

## Key paths
- `site/public/sw.js`
- `site/src/components/OfflineButton.astro`

## Commits
- `eee6d7a8` — Fix offline caching abort and enable partial caches sooner.
