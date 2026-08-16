# 2026-08-07 — Page notes overlay

## Trigger
Add a site-wide notes panel (overlay button beside QR) with localStorage persistence, save/copy/export/download/select flows, and follow-up UX (mobile, page paths, highlight mode).

## Done
- Added `site/src/components/PageNotes.astro` — ✎ trigger; panel with 80ch textarea, action buttons, edit-with-buffer flow via `currentNoteId`, draft persistence.
- Wired into `site/src/layouts/SiteLayout.astro`; QR + notes grouped in `.page-corner-actions` (`PageQrCode.astro`, `global.css`).
- UX: right-aligned overlapping action buttons; ⤢ expand toggle (60vh); trailing newline on selection insert; `visualViewport` keyboard lift on mobile; safe-area insets on corner FABs.
- Each note stores `path` at save time; export/download prefix URLs with Chrome `#:~:text=` on first line.
- ▦ highlight toggle in panel action row — yellow `<mark>` for current-page notes (first-line match); hover shows full note; select list includes path link with text fragment.
- **Mobile fix:** teleport overlay to `document.body` (was clipped inside FAB cluster); visual-viewport positioning on mobile/keyboard; panel stays bottom-aligned; `overflow-x: clip` on `.shell` only.
- Site build verified (`npm run build`).

## Decisions
- Notes under `localStorage` key `site-page-notes`; expand `site-page-notes-expanded`; highlight mode `site-page-notes-highlight-mode`.
- Edit flow buffers draft; path preserved on edit (creation path only).
- Export format: `URL\nnote text` blocks separated by blank lines.
- Highlight matches first non-empty line (≥3 chars); longest matches first to reduce overlap issues.
- Highlight toggle lives in panel (not corner FAB cluster).

## Open / next
- Legacy notes without `path` won't highlight until re-saved from source page.
- Text fragments are Chrome-oriented; other browsers may ignore `#:~:text=`.

## Key paths
- `site/src/components/PageNotes.astro`
- `site/src/layouts/SiteLayout.astro`
- `site/src/styles/global.css`

## Commits
- `df0415ca` Add site-wide page notes overlay with localStorage persistence.
- `e598f675` Extend page notes with paths, highlights, and mobile layout fixes.
- `e6fc46cb` Fix page notes panel visibility on mobile and move highlight toggle into panel.
