# 2026-09-19 — Interactive Field Crux Map UI polish

## Trigger
User feedback on the App B spring crux map: consistent naming, bridge short labels, bigger nodes with 2× pop, desktop hover panel + click-to-navigate, mobile overlay flow, caption links, and narrow-desktop mouse interaction fixes.

## Done
- Renamed demo to **Interactive Field Crux Map** (`index.html`, header, `demos/index.html`, README).
- Bridge nodes: short labels (`Boundary`, `Value`, `Ref.`, …), radius 34, 2× pop on focus; `BRIDGE_SHORT_LABELS` in `weights.ts`.
- **Wide desktop:** side panel on hover; click opens org site or bridge concept card.
- **Compact + touch:** tap to select/highlight; second tap opens bottom-sheet overlay.
- **Compact + mouse (narrow desktop):** hover highlights unchanged; click opens overlay (not navigate); click empty canvas closes overlay.
- Split `compactLayout()` vs `touchInteraction()` so narrow windows with a mouse are not treated as touch-only.
- Caption: AISafety.com → map; **listed evidence** → `/field/coverage/#coverage-evidence-catalog`; removed `max-width: 70ch` wrap bug.
- Rebuilt `app.js` via `npm run build` in `demos/`.

## Decisions
- MB9 (Grounding Drift) labeled **Ground.** — user list had 11 abbreviations for 12 live bridges.
- Wide vs compact click: navigate only when side panel is visible; compact uses overlay for details (links inside overlay still navigate).

## Open / next
- None for this thread. Optional: embed title on companion site if App B card still says old name.

## Files
- `demos/appB-field-spring-map/{app.ts,app.js,weights.ts,physics.ts,index.html,README.md}`
- `demos/index.html`
