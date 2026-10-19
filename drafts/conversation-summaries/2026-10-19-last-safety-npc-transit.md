# 2026-10-19 — Last Safety NPC transit and 3D continuity

kind: new-work
uptake: status

## Trigger
NPCs should arrive one-by-one during Welcome, walk to desks and meetings through floorplan rooms (one hop per fuel tick), and the 3D view should show door-correct departures without re-walking from the door on every re-enter. Text console enter/leave lines stay as present-set diffs (confirmed, no change needed).

Prompts: paraphrase only (no prompt id)

## Done
- content: `room-path.mjs` — BFS paths, `transitStep`, staff entry at commons.
- content: `npcs.mjs` — welcome arrival schedule, Ian at 9:30 to review, `placementWithTransit`, `lastNpcMoves` / `settleNpcs` test helper, meeting goals via transit.
- content: `game.mjs` — expose `npcMoves` on client state per fuel step.
- content: `three-scene.mjs`, `npc-travel.mjs`, `app.js`, `scene-view.mjs` — deferred room load, door departures, saved positions, entrance only when move listed.
- content: `config.mjs`, specs (`npcs`, `world`, `graphics-ui`); `person.mjs` import fix; welcome face order in `view.mjs`.
- content: tests — `room-path.test.mjs`, engine/access/glue/helpers adjustments.
- housekeeping: session log, HANDOFF, INDEX.

## Decisions
- Transit is engine-side one edge per `placeNpcs` tick; client animates only moves in `npcMoves` for that response.
- Text UI does not narrate corridor hops; graphical 3D walks; text prints “is here now” / “heads to …” when presence in the player room changes between commands.

## Open / next
- Manual playtest: Daniel commons→collab while player shuttles; same-fuel Ian departure vs player door cross.
- Institutional add-on gate (earlier handoff) still open.
- Optional explicit commons waypoints if design wants every arrival to visibly pass commons even when pathing already routes through it.

## Key paths
- `game/the-last-safety-review/lib/world/room-path.mjs`
- `game/the-last-safety-review/lib/world/npcs.mjs`
- `game/the-last-safety-review/public/render/three-scene.mjs`
- `game/the-last-safety-review/lib/text/console.mjs` (movement lines unchanged)

## Verification
- `cd game/the-last-safety-review && npm test` → `ℹ pass 143`, `ℹ fail 0`

## Commits
- (this session)
