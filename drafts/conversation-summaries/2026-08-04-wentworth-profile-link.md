# 2026-08-04 — Wentworth profile link fix

## Trigger
User asked that the John Wentworth profile link on the Wentworth field agenda page point to `https://www.lesswrong.com/users/johnswentworth` instead of the Alignment Forum user URL.

## Done
- Updated profile URL in `reference/field-agendas/data/agendas/wentworth-natural-abstractions.yml` (`links`) and `reference/field-agendas/data/clustering.yml` (map listing).
- Ran `node site/scripts/sync-field-agendas.mjs` — regenerated agenda card, `field-agenda-index.md`, and `site/src/data/field-agendas.json`.

## Decisions
- Changed only explicit profile links (`links`, clustering listing). In-body term links for NAH / selection theorems / natural latents still use the AF user URL via `term-links.yml` (concept anchors, not the profile button).

## Open / next
- Optional: retarget NAH-related term-links to specific LW posts or tag pages if AF profile links feel wrong for concept terms.

## Key paths
- `reference/field-agendas/data/agendas/wentworth-natural-abstractions.yml`
- `site/src/content/cards/field-agendas/wentworth-natural-abstractions.md`

## Commits
- (pending) Point Wentworth agenda profile link at LessWrong user page.
