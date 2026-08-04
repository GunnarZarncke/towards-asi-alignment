# 2026-07-18 — Site page QR button

## Trigger
Add a small fixed **QR** button on every companion-site page; clicking opens a full-viewport modal with a QR code for the page’s canonical URL; any click (or Escape) closes it. User then asked to scale the QR to fill most of the viewport.

## Done
- Added `site/src/components/PageQrCode.astro`: build-time SVG via `qrcode`, fixed bottom-right trigger, full-screen overlay modal, click-to-dismiss.
- Wired into `site/src/layouts/SiteLayout.astro` using existing `canonicalUrl`.
- Added `qrcode` dependency in `site/package.json` / lockfile.
- Modal panel ~96vmin; QR ~88vmin; 512px SVG source for sharp scaling.
- Verified `npm run build` (716 pages).

## Decisions
- QR generated at build time (no runtime API); canonical URL from `absoluteSiteUrl` matches SEO/sitemap.
- Component lives outside `.shell` so overlay covers header/footer.
- Scoped styles in component; no global CSS churn.

## Open / next
- None for this feature. Optional: push commit when ready.

## Key paths
- `site/src/components/PageQrCode.astro`
- `site/src/layouts/SiteLayout.astro`

## Commits
- `d7c521b` Add viewport-filling QR modal on every companion-site page.
