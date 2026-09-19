# 2026-09-19 — Field spring-map polish

## Trigger
Follow-up on the ch05 field crux spring-map demo: connect remaining research orgs, layout/physics tuning, simplified UI, and session commit.

## Done
- **Listing weights:** agenda overrides (Hadfield-Menell→chai-russell, Arbital→miri) + manual weights for AIXI, Dovetail, MAISI, Paradigm 3, CARMA, GCRI, Forethought, Narrow Path, PAI, GPAI; snapshot regenerated.
- **Layout:** per-geometry anchor scales (`DEPENDENCY_ANCHOR_SCALE`, `CIRCLE_ANCHOR_SCALE`); MB4 aligned to MB4a y in `bridge-layout.json`; circle bridge order DP (co-occurrence ring).
- **Physics:** seeded ±5% weight jitter on crux springs (breaks multi-bridge center equilibria); geometry-aware spawn/rest lengths.
- **UI:** controls reduced to category selector + dependency/circle toggle; fixed mode A; active listings + research categories only; unified default zoom (dependency scale).
- **Rendering:** bridge dependency edges 2× line width.

## Decisions
- Skip field-building / forecasting orgs (Iliad, Epoch, etc.) unless explicitly curated.
- Display weights stay canonical; jitter applies to simulation edges only.
- Default view scale uses dependency anchor scale for both geometries so toggling layout does not jump zoom.

## Open / next
- Optional: wire Apart, Epoch, Quri with curated weights if desired on map.
- Optional: person-level Hadfield-Menell weights (trim CHAI cluster MB7 baggage).
- Re-run `build_snapshot.py` after further clustering/matrix edits.

## Key paths
- `demos/ch05-field-spring-map/app.ts`, `layout.ts`, `physics.ts`, `weights.ts`
- `demos/ch05-field-spring-map/scripts/build_snapshot.py`
- `demos/ch05-field-spring-map/data/snapshot.json`, `bridge-layout.json`

## Commits
- `83a08679` Polish field spring-map demo: weights, layout, and simplified UI.
