# 2026-10-10 — Last Safety Review: graphics lane, live 3D rooms

kind: new-work
uptake: status

## Trigger
Gunnar: "Start implementing UI & graphics" (PLAN.md graphics lane), then "build proper 3D scenes with the furniture and person objects. Allow the persons to move in the scene by clicking."
Prompts: none resolvable (paraphrase only).

## Done
- content: Graphics solo harness `npm run dev:ui` (`scripts/dev-ui.mjs`, port 3001) on `fixtures/client-state.json` + `fixtures/scene-platform-doubt.json`; no engine, no model.
- content: `public/render/scene-view.mjs` — `buildSceneView` (pure over `ClientState`) plus the CSS room, now only the fallback when WebGL or `three` is missing.
- content: Live Three.js renderer `public/render/three-scene.mjs` with `room.mjs` (cutaway walls, windows, doors), `kit.mjs` (procedural furniture: desks, racks, glass partition, NORA wall, bench, screens, plants, …), `person.mjs` (procedural bodies, walk/idle), `nav.mjs` (grid A*), `layouts.mjs` (three rooms as data), `lighting.mjs` (act presets).
- content: Interaction — click floor walks the selected person; click a person or name tag selects them; doors / records / workstation walk the player there, then act. Surveillance view: grayscale + annotation boxes that track their target. Act I/II/III lighting switch in the harness.
- content: `three@0.186.1` added to `package.json`; `server.mjs` and `dev-ui.mjs` serve `node_modules/three/build/` at `/vendor/three/` (import map in `index.html`).
- bookkeeping: `spec/meta.md` records O-33 closed; `spec/graphics-ui.md` renderer section and third-person walking (working); `spec/contract.md` scene-view shape and vendor route; `PLAN.md`, `README.md` updated.
- content: Follow-up lighting — brighter welcome/doubt; ceiling as invisible overhead lights (no fixture meshes); act III softer wide desk pools (linear falloff, main+fill), higher room fill/exposure; walk speed 2× (`person.mjs` 3 m/s).

Verification: `npm test` → `ℹ pass 6` / `ℹ fail 0`. Browser check on `dev:ui` (screenshots this session): Platform Operations in acts I–III, Evaluation Suite, People Operations, phone width 390 px; floor walk, NPC move, walk-then-inspect (marker flipped to `examined`), door transition to Evaluation Suite, surveillance boxes. `curl` on `npm start` (DEMO_MODE): `/vendor/three/three.module.js 200`, `/vendor/three/../package.json 404`.

## Decisions
- O-33 closed as live Three.js because Gunnar asked for 3D scenes. Asset kit stays open; nothing downloaded.
- The player has a third-person body (new, on request). Positions are presentation-only; not engine state.
- Screen textures are abstract (no incident facts) so nothing leaks before evidence is examined.
- `server.mjs` (composition lane) touched only to serve `/vendor/three/`.

## Open / next
- Engine does not emit act or scene view; act fixed at `doubt` in `npm start` (O-08).
- Annotations come from fixtures; the engine should own them when surveillance becomes evidence.
- Asset kit choice; O-34 character style, O-35 animation depth still open.
- Terminal hotspot only posts a notice until the terminal lane ships `/api/terminal`.

## Key paths
- `game/last-safety-autocomplete-prototype/public/render/`
- `game/last-safety-autocomplete-prototype/spec/graphics-ui.md`

## Commits
- none
