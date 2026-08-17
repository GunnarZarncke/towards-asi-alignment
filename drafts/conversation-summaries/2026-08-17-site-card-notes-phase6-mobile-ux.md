# Site card notes Phase 6 — mobile UX + illustration caching

**Date:** 2026-08-17  
**Scope:** `PageNotes.astro`, `sync-chapter-illustrations.mjs`, `tex-convert.mjs`, `site/public/figures/illustrations/web/`, book resync.

## Done

- **A7:** Chapter-opening JPEGs copied to `site/public/figures/illustrations/web/`; `illustrationPublicSrc()` in tex-convert; illustration prompt pages use same-origin URLs; SW cache v11 (same-origin figures cache with pages).
- **A8:** Page-notes trigger and panel actions use inline SVG icons (save, copy, export, download, select, highlight, expand/collapse, close).
- **A9:** Mobile layout moves action buttons below textarea (no overlap with keyboard); visual-viewport sync retained.
- **A10:** Tap/click on `mark.page-notes-highlight` opens notes panel and loads that note.
- **A11:** Expanded panel uses ~88% of visual viewport height on mobile; explicit `height` when expanded.

## Pipeline

`npm run sync:chapter-illustrations` added before `sync:chapters` in root `sync` script.

## Site card notes triage

Phases 0–6 complete. Deferred items remain in `metadata/TODO.md` § Site (A3, A4, A6, A14, exercises/quiz, etc.).
