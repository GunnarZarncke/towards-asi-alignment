# 2026-08-29 — Epistemic status site callout box

## Trigger
User asked to mark `\begin{epistemicstatus}` blocks on the companion site with a box similar to, but lighter than, the chapter-thesis callout.

## Done
- Added `epistemicstatus` handler in `site/scripts/lib/tex-convert.mjs` (was previously stripped to plain text).
- Added lighter `.epistemic-status` callout styling on book pages in `site/src/pages/cards/[...slug].astro` (neutral gray tint, 3px left border vs chapter thesis accent).
- Ran `node scripts/sync-chapters.mjs` locally to regenerate `src/content/book/` (gitignored; rebuild on deploy).

## Decisions
- Mirror LaTeX hierarchy: chapter thesis keeps accent-blue callout; epistemic status uses muted neutral box with thinner border.
- Scoped styles under `.book-page` alongside existing `.chapter-thesis` rules.

## Open / next
- Re-run `npm run sync:chapters` (or full site sync) in CI/deploy if book pages are not auto-synced there.

## Key paths
- `site/scripts/lib/tex-convert.mjs`
- `site/src/pages/cards/[...slug].astro`
- `metadata/preamble.tex` (PDF box colors for reference)

## Commits
- `6b6f7122` Style epistemic status blocks as lighter callouts on book pages.
