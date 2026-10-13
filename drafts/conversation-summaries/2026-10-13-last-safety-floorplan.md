# 2026-10-13 — Last Safety courtyard floorplan

kind: new-work
uptake: local

## Trigger
Integrate the verified courtyard floorplan into the Last Safety prototype.
Prompts: paraphrase

## Done
- content: The running game uses the 22 × 17 m courtyard plan. `lib/floorplan.mjs` holds the rooms and the sixteen doors; `public/floorplan.svg` is the drawing. The Floorplan button opens it. A click walks one door. The prototype badge is clearance 2, so the test bay and security control stay shut.
- content: Platform, Evaluation, and People keep their furnished rooms. Their doors now match the plan (they meet through the technical spine). The other rooms are generated from the plan’s metres.
- content: Specs updated: `spec/world.md` floorplan, `spec/engine.md` `go`, `spec/contract.md` `clearance`, `spec/graphics-ui.md`.
- bookkeeping: `npm test` in `game/last-safety-autocomplete-prototype` — 38 pass, 0 fail. Browser check: map opens on Platform Operations; Technical Circulation is the only door; the test bay returns “That door needs a higher clearance.”; People + Product shows Elena and doors to the spine, courtyard, and collaboration bay.

## Decisions
- Movement is one door at a time. The map does not teleport across the building.
- The three furnished rooms stay larger than their plan footprints. Neighbors match the plan; furniture was not rescaled.
- Clearance 2 is the prototype visitor badge, so the existing scene still starts in Platform Operations and can reach Leila and Elena.

## Open / next
- The other rooms have no cast yet. Jun, Mara, and the security room wait on the incident gate.
- The technical spine is a 22 × 1.6 m cutaway, so door labels sit close together.

## Key paths
- `game/last-safety-autocomplete-prototype/lib/floorplan.mjs`
- `game/last-safety-autocomplete-prototype/public/floorplan.svg`
- `game/last-safety-autocomplete-prototype/public/render/floorplan-view.mjs`
- `game/last-safety-autocomplete-prototype/spec/world.md`

## Commits
- none
