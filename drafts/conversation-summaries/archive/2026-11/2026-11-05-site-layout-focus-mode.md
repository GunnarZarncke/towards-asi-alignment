# 2026-11-05 — Site layout focus mode

kind: new-work
uptake: local

## Trigger
Add a third mode to the bottom-left full-width layout button, cycling standard → wide → focus; focus hides the right related panel and tightens outer page gutters.

## Done
- content: `site/src/lib/site-layout-mode.ts` — three modes, `site-layout-mode` storage, legacy `site-layout-full-width` → wide.
- content: `site/src/components/PageWidthToggle.astro` — cycle on click; title/aria-label per mode.
- content: `site/src/layouts/SiteLayout.astro` — inline restore before paint.
- content: `site/src/styles/global.css`, `tokens.css` — `--layout-inline-padding`, `html.layout-focus` (single column, hide `.side-panel`, 0.35rem gutters, full width).
- bookkeeping: `cd site && npm run build` — exit 0 (`1211 page(s) built`).

## Decisions
- **Wide** keeps the side panel; **focus** adds panel hide + minimal margin (not a separate “panel only” mode).
- One `layout-focus` class carries full-width prose rules plus focus-specific grid/gutter overrides.

## Open / next
- Unrelated working-tree changes (field agendas, conversation logs, papers draft, etc.) left unstaged.

## Key paths
- `site/src/lib/site-layout-mode.ts`
- `site/src/components/PageWidthToggle.astro`
- `site/src/styles/global.css`

## Commits
- `cdbb77a85d` Add focus layout mode to companion site width control.
