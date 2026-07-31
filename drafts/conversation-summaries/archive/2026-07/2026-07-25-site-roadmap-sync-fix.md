# 2026-07-25 — Fix site sync after roadmap archival

## Trigger
`serve-site.sh` failed because `site/scripts/sync-chapters.mjs` still attempted to read the archived `frontmatter/roadmap.tex`.

## Done
- Updated `site/scripts/sync-chapters.mjs` to use live `frontmatter/current-status.tex` in the front-matter source list.
- Removed the deleted `appendices/appL-assumptions.tex` from the optional label-scan list.
- Verified `npm run sync:chapters` and the full `npm run sync` complete successfully.

## Decisions
- The site should follow the manuscript's live front-matter source rather than retain a compatibility copy of the superseded roadmap.
- Unrelated working-tree changes were not staged or modified.

## Open / next
- Run `./serve-site.sh` interactively if browser-level verification is needed.

## Key paths
- `site/scripts/sync-chapters.mjs`
- `frontmatter/current-status.tex`
- `drafts/repo-cleanup-plan.md`

## Commits
- Scoped site-sync fix commit for this session.
