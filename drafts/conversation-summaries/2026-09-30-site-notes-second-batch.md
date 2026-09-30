# 2026-09-30 — Site notes second batch

kind: new-work
uptake: status

## Trigger
Implement site-notes batch two: consolidate field tiles, notes panel save placement, card preview images, graphics instruction docs, offline service-worker fix.

## Done
- content: **Field tiles** — trimmed `site/src/content/field/intro.md`; removed Bridge assumptions tile from `FieldPreviewHub.astro`; user tightened agenda badge copy (`badges.ts`) and bearer-admission-adjacent concept body.
- content: **Notes panel** — save button moved into `page-notes-input-row` beside textarea in `PageNotes.astro` + CSS.
- content: **Card previews** — shared `site/scripts/lib/preview-image.mjs`; wired into `sync-field-news.mjs`, `sync-chapter-cards.mjs` (chapter JPEG `previewImage`), and build-time fallback in `cards/[...slug].astro`.
- content: **Offline SW** — `site/public/sw.js` v12: cache-first when offline enabled, `navigator.onLine` gate, 2.5s network timeout, stale-while-revalidate background refresh.
- content: **Graphics instruction** — card-graphics checklist in root `AGENTS.md` and `site/README.md`.
- bookkeeping: Ran `npm run sync:chapter-cards`, `sync:field-news`, `npm run build` in `site/` — **1155 pages, build Complete**.

## Decisions
- Preview resolution order: explicit `previewImage` → first in-body image on disk → chapter opening JPEG → field-news meme basename; site default `/og-image.png` unchanged when none resolve.
- Offline: serve cached immediately when offline mode is on; revalidate in background only when online (avoids hanging on dead network).

## Open / next
- Decision-block plain-language pass (YAML `decision` fields).
- Ch.15 overlapping-environments paragraph.

## Key paths
- `site/scripts/lib/preview-image.mjs`
- `site/public/sw.js`
- `site/src/components/PageNotes.astro`, `FieldPreviewHub.astro`
- `AGENTS.md` (Companion site — Card graphics)

## Commits
- (filled in at session end)
