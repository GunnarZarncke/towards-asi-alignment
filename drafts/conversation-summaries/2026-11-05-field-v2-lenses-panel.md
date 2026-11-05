# 2026-11-05 — Field v2 lenses preview panel

kind: new-work
uptake: local

## Trigger
Add a fourth preview panel on the field overview v2 linking to the lenses overview page.

## Done
- content: Fourth hub panel on `/field/v2/` — clipped alignment-frames graph preview, links to `/cards/lens/lenses-and-frameworks/` (`FieldPreviewHub.astro`).

## Decisions
- Panel sits after “The research programs,” reusing `FieldBridgeGraph` + `alignment-frames-relations.svg` like the bridge panel.

## Open / next
- None.

## Key paths
- `site/src/components/FieldPreviewHub.astro`
- `site/src/pages/field/v2/index.astro`

## Verification
- `cd site && npm run build` → `1211 page(s) built` (exit 0).

## Commits
- (this session)
