# 2026-07-27 — Site offline PWA support

## Trigger
Add a bottom-of-site control that makes the companion site available offline, caching the app shell while excluding PDFs and demos.

## Done
- Added `site/public/manifest.webmanifest` and `site/public/sw.js`.
- Added `site/src/components/OfflineButton.astro` and placed it in `SiteLayout.astro`'s footer.
- The service worker precaches core routes, caches sitemap-listed site pages on request, and skips PDF and demo routes.
- Verified `npm run build` succeeds and lint reports no errors in the edited source files.

## Decisions
- Offline caching is opt-in through the footer button rather than automatically downloading the whole site.
- The generated sitemap supplies the page list, avoiding a manually maintained list of every card and chapter.
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
