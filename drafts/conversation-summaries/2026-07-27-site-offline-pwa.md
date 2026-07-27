# 2026-07-27 — Site offline PWA support

## Trigger
Add a bottom-of-site control that makes the companion site available offline, caching the app shell while excluding PDFs and demos.

## Done
- Added `site/public/manifest.webmanifest` and `site/public/sw.js`.
- Added `site/src/components/OfflineButton.astro` and placed it in `SiteLayout.astro`'s footer.
- The service worker precaches only the home/offline fallback and search index until the footer control is selected. It then caches sitemap-listed pages plus their same-origin dependencies, while skipping PDF and demo routes.
- Missing offline navigations use a built-in fallback response, so the notice remains available even if the cached fallback page is absent.
- The footer control now reports service-worker caching failures instead of remaining disabled indefinitely.
- Fixed service-worker registration on nested routes by registering the root/base-path `sw.js`, rather than resolving it relative to the current page URL.
- Verified `npm run build` succeeds and lint reports no errors in the edited source files.

## Decisions
- Offline caching is opt-in through the footer button rather than automatically downloading the whole site.
- The cache uses Astro's generated sitemap to enumerate pages, then includes each page's same-origin linked dependencies. `serve-site.sh` now builds and copies the generated sitemap into `site/public/` before starting the local dev server, where Astro otherwise does not emit it.
- PDF and demo exclusions apply both to the explicit offline bundle and runtime caching.

## Open / next
- Test the install and offline flow on the deployed HTTPS site in Chrome/Safari.
- Consider adding dedicated 192px and 512px PWA icons if stronger install prompts are needed.

## Key paths
- `site/src/layouts/SiteLayout.astro`
- `site/src/components/OfflineButton.astro`
- `site/public/sw.js`
- `site/public/manifest.webmanifest`

## Commits
- None.
