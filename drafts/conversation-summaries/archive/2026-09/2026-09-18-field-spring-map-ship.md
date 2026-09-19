# 2026-09-18 — Field spring-map ship

## Trigger

End-of-session commit for the field crux spring-map demo after layout/UI polish, TSA + curated listing weights, and bridge repositioning.

## Done

- **`demos/ch05-field-spring-map/`** — TypeScript demo (physics, layout, app), snapshot + logos, build/extract scripts, tests.
- **Layout** — Dependency geometry default; MB11 under MB1; MB9/MB7d/MB4a repositioned; project icons ×0.7; center pull 0.0005; reverted unconnected inward pull.
- **UI** — Bridge hover highlights crux + bridge-dep edges; full bridge title tooltips; TSA pinned in default filter.
- **Data** — TSA + Byrnes clustering; `LISTING_AGENDA_OVERRIDES` / `LISTING_WEIGHT_OVERRIDES` (ACS, CSER, Yampolskiy, Team Shard) with per-MB comments in `build_snapshot.py`.
- **Integration** — `demos/index.html`, `demos/build-demos.mjs`, `demos/README.md`.

## Decisions

- Unconnected projects use original spawn + uniform center pull (no orbit scale hack).
- Curated weights are manual scores with documented MB rationale, not matrix discharge.

## Open / next

- Tighten fuzzy inherit (`ARC` ⊂ `research`) per tune log.
- Optional site card linking to demo.
- More matrix rows vs manual overrides for unmatched research orgs.

## Key paths

- `demos/ch05-field-spring-map/`
- `reference/field-agendas/data/clustering.yml`
- `drafts/plans/field-spring-map.md`

## Commits

- `53e570b6` Add field crux spring-map demo for AISafety.com listings by bridge affinity.
