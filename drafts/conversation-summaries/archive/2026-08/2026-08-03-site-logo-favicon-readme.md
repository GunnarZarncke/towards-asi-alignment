# 2026-08-03 — Site logo, favicon, README trim

## Trigger
Convert `TSA.png` to SVG; crop surplus background; add circular transparent variant; wire logo and favicons on the companion site; size header logo to navbar height; end-of-session commit including user README edits.

## Done
- Traced logo from `TSA.png` → `site/public/logo.svg` (square dark fill) and `site/public/logo-circle.svg` (circular `#161E2B` fill, transparent outside; r=440 after edge ring tuning).
- Added favicon bundle: `favicon.svg`, `favicon.ico`, `apple-touch-icon.png`, `icon-192.png`, `icon-512.png` (PNG raster via `rsvg-convert` for transparency).
- Updated `SiteLayout.astro`: brand logo + favicon links; theme color `#161E2B`.
- Updated `global.css`: `--header-bar-height: 3.5rem`; logo fills navbar height.
- Updated `manifest.webmanifest` with PWA icon entries.
- Committed user README changes (removed standalone-claims block; revised “What this is” and companion-site row).

## Decisions
- **`logo-circle.svg` is canonical** for header and favicons (transparent outside circle); `logo.svg` kept as square-background variant.
- Root `TSA.png` / `TSA.svg` left untracked (source artifacts; ~1.1 MB PNG).

## Open / next
- Optional: fix README typos (“empiricallly”, “The include Lean”) if author wants a follow-up prose pass.
- Optional: add `logo.svg` / `logo-circle.svg` to a documented brand assets note if reused off-site.

## Verification
- `npm run build` in `site/` succeeded.
