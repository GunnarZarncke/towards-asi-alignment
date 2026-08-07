# 2026-08-07 — Page notes overlay

## Trigger
Add a site-wide notes panel (overlay button beside QR) with localStorage persistence, save/copy/export/download/select flows, and follow-up UX tweaks.

## Done
- Added `site/src/components/PageNotes.astro` — ✎ trigger bottom-right; panel with 80ch textarea, action buttons (save, copy selection, export all, download all, select saved note), edit-with-buffer flow via `currentNoteId`, draft persistence.
- Wired into `site/src/layouts/SiteLayout.astro`; shifted QR trigger left in `PageQrCode.astro`.
- Right-aligned action buttons; top-center ⤢/⤡ expand toggle (60vh panel, persisted); trailing newline on selection insert (open + copy).
- Site build verified (`npm run build`).

## Decisions
- Notes stored under `localStorage` key `site-page-notes`; expand preference under `site-page-notes-expanded`.
- Selecting a saved note buffers the current draft; cancel/close restores buffer without mutating the list; save updates the note then restores buffered draft.
- Page selection prefilled on open only when draft is empty; copy button inserts at cursor with trailing newline.

## Open / next
- None for this feature unless user wants note timestamps, per-page tagging, or sync/export format changes.

## Key paths
- `site/src/components/PageNotes.astro`
- `site/src/layouts/SiteLayout.astro`
- `site/src/components/PageQrCode.astro`

## Commits
- (this session)
