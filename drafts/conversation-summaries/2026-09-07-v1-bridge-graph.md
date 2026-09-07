# 2026-09-07 — Restore real v1 bridge graph

## Trigger
User noticed `/field/v1/` used an intermediate diagram where MB8 was already a gravestone. Asked to capture the real v1 graph, render it, and record the linked v1 commit on the field/v1 page.

## Done
- Restored `reference/field-agendas/graphs/mb-bridge-dependencies-v1.dot` from [`c15ad815`](https://github.com/GunnarZarncke/towards-asi-alignment/commit/c15ad8156ebeb5d3c852df5e69da6226262a594c) (`mb-bridge-dependencies.dot` as first shipped: live MB8 backup edges, no gravestone, no MB1→MB3).
- Re-ran `npm run sync:bridge-graph` so `bridge-dependencies-v1.svg` matches that DOT.
- `/field/v1/` hero + graph lede now link that commit; graphs README + sync-script comment updated.

## Decisions
- Freeze point is **graph introduction** (`c15ad815`, 2026-08-03), not the 2026-08-17 v2 cutover (`90161157`), which had copied the post-`c9a017f9` gravestone DOT.
- Last identical live-MB8 graph in git is `23293a24` (hours before gravestone); content equals `c15ad815`.

## Open / next
- None for this graph freeze.

## Key paths
- `reference/field-agendas/graphs/mb-bridge-dependencies-v1.dot`
- `site/src/pages/field/v1/index.astro`
- `site/scripts/sync-bridge-graph.mjs`

## Commits
- (this session's commit)

## Left unstaged
- Archive moves of Aug logs, attractor-season / funding drafts, `field.md` crux-map pointer, `experiments.json` / `chapter-reading-graph.json`, other summary edits.
