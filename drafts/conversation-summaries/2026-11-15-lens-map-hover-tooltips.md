# 2026-11-15 — Lens map node hover summaries

kind: new-work
uptake: status

## Trigger
On the Lenses and frameworks card, show each criteria entity’s summary when hovering a node on the lens map. End-of-session commit. (Same session, read-only follow-up: where Florian Dietz’s SPT and DCA sit on the criteria map — no repo edits.)

Prompts: (no prompt id captured)

## Done
- content: **`FieldBridgeGraph.astro`** — optional `nodeTooltips`; fixed tooltip on hover/focus; scoped by graph id.
- content: **`FieldLensGraph.astro`** — `lensNodeTooltipMap()` from `lenses-data.mjs`; hint mentions hover.
- content: **`render-graphviz.mjs`** — `tooltipMap` on node links; `data-node-id`; native SVG `<title>` fallback.
- content: **`sync-lens-graph.mjs`** — builds tooltip map from lens summaries.
- content: **`lenses-data.mjs`** — `lensNodeTooltipMap()` export.
- bookkeeping: Regenerated `public/field-graphs/alignment-frames-relations.svg` locally (gitignored; run `cd site && npm run sync:lens-graph` on deploy).

## Decisions
- Tooltips are lens-map-only via `FieldLensGraph` prop; bridge dependency graphs unchanged.
- Field hub preview clip left without tooltips unless extended later.

## Open / next
- Optional: pass `nodeTooltips` on `FieldPreviewHub` lens graph clip.
- Optional: site card or agenda note placing Dietz SPT/DCA on criteria map (warrant/route attachments).

## Key paths
- `site/src/components/FieldLensGraph.astro`
- `site/src/components/FieldBridgeGraph.astro`
- `site/scripts/sync-lens-graph.mjs`

## Commits
- (this session)