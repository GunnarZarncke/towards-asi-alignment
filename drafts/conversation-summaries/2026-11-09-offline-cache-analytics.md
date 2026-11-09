# 2026-11-09 — Offline cache analytics flag

kind: new-work
uptake: local

## Trigger
Offline caching was inflating website analytics. Cache fills should be marked `cache=1` so they can be filtered, and a real visit to a cached page should still be recorded when the HTML is not fetched.
Prompts: (none recorded)

## Done
- content: `site/public/sw.js` — cache fills, shell install, sitemap fetch, and background refresh request `?cache=1`; Cache API keys stay on the clean URL.
- content: `site/src/components/PostHogAnalytics.astro`, `site/src/lib/page-visit.ts` — pageview on `pageshow`, including a service-worker cache hit and a back-forward restore. `?cache=1` is not a visit.
- bookkeeping: `scripts/check.sh` includes `site/src/lib/page-visit.test.ts`.
- bookkeeping: `node --test --experimental-strip-types site/src/lib/page-visit.test.ts` — 5 pass, 0 fail.
- bookkeeping: Local fixture: cache fill logged `/cached-page/?cache=1` and did not record a visit; opening that cached page logged `/recorded-visit?path=%2Fcached-page%2F` with no unflagged document fetch. Address bar stayed `/cached-page/`.

## Decisions
- `cache=1` is only on requests whose purpose is filling the cache. The document URL of a shown page stays clean, so PostHog and the Cloudflare beacon record that visit.
- Cloudflare Web Analytics does not store query strings, so the `cache=1` filter applies to PostHog and request logs. The beacon still runs in the shown document.

## Open / next
- Uncommitted. Deploy before the filter matches production traffic.

## Key paths
- `site/public/sw.js`
- `site/src/components/PostHogAnalytics.astro`
- `site/src/lib/page-visit.ts`

## Commits
- (pending this session)
