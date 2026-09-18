# 2026-09-18 — Field crux spring-map demo

## Trigger

Build the alignment map prototype: ingest AISafety.com map listings, assign MB bridge crux weights, spring-layout with modes A/B/C.

## Done

- Added [`demos/ch05-field-spring-map/`](../../demos/ch05-field-spring-map/) — canvas force sim, filters, inspect panel
- `scripts/build_snapshot.py` — fetch organizations API, clustering match, matrix/evidence inherit, heuristic fallback
- Frozen `data/snapshot.json` (369 listings, CC-BY-4.0)
- Modules: `weights.ts`, `physics.ts`, `layout.ts`, `app.test.ts`
- Plan: [`drafts/plans/field-spring-map.md`](../plans/field-spring-map.md)
- Updated `demos/index.html`, `demos/README.md`

## Decisions

- Demo folder `ch05-*` for `serve.py` / esbuild discovery; README states field-hub toy, not ch05 prose
- Snapshot uses heuristics for unmatched listings; `--llm` optional for refresh
- Live bridges exclude MB8 gravestone; no MB6a/b or MB7a–c split in inherit path

## Open / next

- Optional: `--llm` batch classify + calibration report vs inherited rows
- Optional: weak tether to AISafety.com category-map x,y as overlay
- Site picks up demo on next `npm run sync:demos` in `site/`

## Key paths

- [`demos/ch05-field-spring-map/README.md`](../../demos/ch05-field-spring-map/README.md)
- [`reference/field-agendas/data/clustering.yml`](../../reference/field-agendas/data/clustering.yml)

## Commits

- (none yet)
