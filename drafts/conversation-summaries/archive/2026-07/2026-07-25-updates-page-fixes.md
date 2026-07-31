# 2026-07-25 — Updates page expand button and releases hub cleanup

## Trigger
User reported the “Show 3 more releases” button on `/updates/` did not work, and the “Releases hub card” link at the top was redundant with the updates page itself.

## Done
- Moved `CardSection` expand/collapse script from `cards/index.astro` into `CardSection.astro` so all pages using the component get working toggles.
- Removed “Releases hub card” primary button from `/updates/` hero; promoted RELEASE_NOTES link to primary.
- `/cards/releases-updates/` now 301-redirects to `/updates/`.
- Dropped hub card from Cards index releases section; removed “Releases hub” sidebar link on release cards.
- Site build verified (`npm run build` in `site/`).

## Decisions
- Keep generating the `releases-updates` hub card in sync-releases (still in release `related` arrays) but redirect its URL to `/updates/` rather than delete the card slug.
- Did not stage unrelated working-tree changes (Microsoft open-weights field news, RELEASE_NOTES commit-hash tweak, table-overflow log edit).

## Open / next
- Add INDEX row when committing or after merging other 2026-07-25 unstaged work.
- Deploy site so production `/updates/` picks up the toggle fix.

## Key paths
- `site/src/components/CardSection.astro`
- `site/src/pages/updates/index.astro`
- `site/src/pages/cards/[...slug].astro`
- `site/src/pages/cards/index.astro`

## Commits
- `d0f5e008` Fix /updates/ release expand toggle and retire redundant releases hub.
