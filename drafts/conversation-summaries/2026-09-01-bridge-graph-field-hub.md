# 2026-09-01 — Bridge graph field hub fix

## Trigger
User reported `/cards/concept/bridge-assumptions/` (field hub panel “Which problems depend on which”) showing “Graph SVG not found” on the live site.

## Done
- `FieldBridgeGraph.astro`: default SVG/dot paths updated from legacy `bridge-dependencies.*` to `bridge-dependencies-v2.*` (sync script only generates v1 + v2; production had v2 but not the legacy file).
- `FieldPreviewHub.astro`: panel link corrected from `/cards/concept/bridge-assumptions/` to `/cards/bridge/bridge-assumptions/`.
- `field/coverage/index.astro`, `experiments/coverage/index.astro`, `cards/[...slug].astro`: same canonical bridge-assumptions URL fix.

## Decisions
- Point all embeds at v2 (live graph) rather than reintroducing a legacy alias in `sync-bridge-graph.mjs`; `FieldBridgeGraphSection` already used v2.

## Open / next
- Deploy site build so `/field/` preview panel renders the graph on production.
- Unrelated working-tree changes (ch10, witness, intro, crux map, etc.) left unstaged.

## Key paths
- `site/src/components/FieldBridgeGraph.astro`
- `site/scripts/sync-bridge-graph.mjs`
- `site/public/field-graphs/` (gitignored; generated at build)

## Commits
- (this session)
