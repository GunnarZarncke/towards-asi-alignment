# 2026-07-17 — Site releases/updates page

## Trigger
User asked to add a releases/updates page to `site/` with one card shown newest-first, plus one card for each release; then end of session and commit.

## Done
- Added card type `release` (+ optional `releasedAt` / `version`) in `content.config.ts` and `badges.ts`.
- Cards: hub `releases-updates`, `release-v1-1-0`, `release-v1-0-0`.
- Page `/updates/` with `CardSection` `initialCount={1}`, versions sorted newest first.
- Nav link **Updates**; Cards index section; card detail badges/links; README row.
- `npm run build` green (`/updates/` + release card routes).
- Committed this task’s site files + session log only.

## Decisions
- Hub card is separate from the version list on `/updates/` (hero links to hub; list is version cards only).
- Source of truth for long changelog remains `RELEASE_NOTES.md`; cards compress highlights.

## Open / next
- Add a card when cutting the next tagged release.
- Optional: sync script from `RELEASE_NOTES.md` if release cadence grows.
- Left uncommitted: graded-lab `experiments.json` role text, salon slides, hostile-review, other drafts.

## Key paths
- `site/src/pages/updates/index.astro`
- `site/src/content/cards/releases-updates.md`
- `site/src/content/cards/release-v1-1-0.md`
- `site/src/content/cards/release-v1-0-0.md`

## Commits
- `16aacf7` Add companion-site releases page with newest-first release cards.
