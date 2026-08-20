# 2026-08-02 — Site offline PWA cache fix

## Trigger
Locally served companion site pages did not show the latest content on refresh; adding a query string (e.g. `?a=1`) was required, suggesting the service worker was serving stale cache past its intended TTL.

## Done
- Restored opt-in offline behavior in `site/public/sw.js` (v8): network-first with `cache: 'no-store'` when offline mode is not enabled; cache used only after the footer button completes and only as fallback when the network fails.
- Removed 1-hour cache-first TTL and trimmed install pre-cache to shell URLs (`/`, `/offline/`, `/search-index.json`).
- `OfflineButton.astro`: register with `updateViaCache: 'none'` and call `registration.update()` on load.

## Decisions
- Normal browsing (offline not enabled) should always hit the network; offline bundle remains explicit opt-in via the footer control, matching the 2026-07-27 PWA design.
- No auto-reload on `controllerchange` — avoids surprise reloads during local dev; users can hard-refresh once to pick up v8.

## Open / next
- After deploy, verify on production HTTPS: refresh shows fresh content without query strings; offline button still populates full cache; airplane-mode fallback works.

## Key paths
- `site/public/sw.js`
- `site/src/components/OfflineButton.astro`

## Commits
- `bd359009` Fix offline PWA serving stale pages on refresh when online.
