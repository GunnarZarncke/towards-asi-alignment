# 2026-08-03 — Site full-width layout toggle

## Trigger
Add a fixed overlay button (left side, like the QR button on the right) that toggles between the standard constrained layout and full viewport width, using a `<->` icon.

## Done
- `site/src/components/PageWidthToggle.astro` — bottom-left fixed button; toggles `layout-full-width` on `<html>`; persists via `localStorage` (`site-layout-full-width`).
- `site/src/layouts/SiteLayout.astro` — mounts toggle; inline head script restores preference before paint.
- `site/src/styles/global.css` — full-width mode sets `--max-wide: 100%`, clears `.hero` / `.lede` / `.readable` max-width caps.
- Site build verified (`npm run build`).

## Decisions
- Mirror QR button styling (fixed pill, bottom corner) rather than a nav item — keeps layout control ambient without cluttering header.
- Class on `html` + CSS variables reuse existing width system instead of per-page overrides.

## Open / next
- Page-scoped max-width rules (e.g. Field intro `48rem`) still apply in full-width mode; expand if users want truly edge-to-edge prose everywhere.
- Other unstaged drafts in working tree (LW debate section, TSA assets, etc.) — not part of this commit.

## Key paths
- `site/src/components/PageWidthToggle.astro`
- `site/src/layouts/SiteLayout.astro`
- `site/src/styles/global.css`

## Commits
- `4e7658de` Add full-width layout toggle to companion site.
