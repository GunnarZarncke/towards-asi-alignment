# 2026-07-17 — Cloudflare Web Analytics (replace GA4)

## Trigger
User asked to undo GA4 integration and use cookieless Cloudflare Web Analytics instead; provided beacon token; requested Impressum disclosure and end-of-session commit.

## Done
- Removed GA4 (`GoogleAnalytics.astro`, `G-CSE38FJPXY` in `seo.ts`) — GA4 was never committed to `main`.
- Added `site/src/components/CloudflareWebAnalytics.astro` (production builds only; off in dev).
- Wired beacon before `</body>` in `SiteLayout.astro`; token in `seo.ts` with optional `PUBLIC_CF_WEB_ANALYTICS_TOKEN` override.
- CI build step accepts optional GitHub secret `PUBLIC_CF_WEB_ANALYTICS_TOKEN` (default token in repo suffices).
- Added `site/.env.example`.
- Impressum **Web-Analyse** section (German): cookieless Cloudflare, no cross-site tracking, link to Cloudflare privacy policy.

## Decisions
- Hardcode beacon token in `seo.ts` — public in page HTML; avoids requiring a GitHub secret for deploy.
- Match Cloudflare snippet (`type="module"`, `beacon.min.js`) rather than gtag/GA4 Consent Mode stack.
- Discussed GA4 vs cookieless analytics for EEA; chose Cloudflare for zero cost and no consent banner (with Impressum note).

## Open / next
- Push to `origin/main` so GitHub Pages redeploys with beacon.
- Verify live HTML contains `cloudflareinsights.com/beacon.min.js` and data appears in Cloudflare Web Analytics dashboard.
- Optional: delete unused GA4 property `G-CSE38FJPXY` in Google Analytics if created.

## Key paths
- `site/src/components/CloudflareWebAnalytics.astro`
- `site/src/lib/seo.ts`
- `site/src/layouts/SiteLayout.astro`
- `site/src/pages/impressum.astro`
- `.github/workflows/site.yml`

## Commits
- (pending) Replace GA4 with Cloudflare Web Analytics and Impressum note.
