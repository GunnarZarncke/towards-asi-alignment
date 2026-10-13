# 2026-10-13 — Last Safety grammar, think, incident tables

kind: new-work
uptake: rule

## Trigger
Gunnar asked to join the grammar to the NPC model (interventions, tell = assert, commit), replace analyze with think, add the missing client fields, extend fuel, and to propose a day timeline, a parse-to-fact map, goal predicates, boundary-narrow tables, and Act III arcs. Provenance and when the model may choose a move needed a rule.
Prompts: (none in the message; paraphrase)

## Done
- content: Grammar kinds `think` and `commit`, relations `suspend` / `revoke` / `rerun` / `stop`. `assert` is tell. Note channel has no NORA. Specs: `spec/grammar.md`, `spec/contract.md`, `spec/engine.md`, `spec/npcs.md`, `spec/incident.md`, `spec/world.md`, `spec/documents.md`, `spec/meta.md`, `spec/terminal.md`, `spec/graphics-ui.md`, `spec/ranking.md`, `spec/playtest.md`, `PLAN.md`, `spec/testing.md`.
- content: Boundary-narrow tables name three scored explanations, six observables, four interventions, and five strategy pairs. Justine is on the Gate 1 handset.
- content: Visit is Friday 19 November 2027. Thursday 18 stays the incident. Meeting placeholder moved off 16:40 Thursday.
- content: Prototype openings in `public/grammar.js` and the demo parser in `lib/llm.mjs`. Think is hidden while someone is in the room.
- bookkeeping: `npm test` in `game/last-safety-autocomplete-prototype` — 34 pass, 0 fail.

## Decisions
- Think returns authored marks within a hop limit. Fuel for it is that hop count. The first prompt is Leila, and that mark is one hop.
- Reading a document adds only its `readsAs` checklist facts. A comparison the prose does not state is a think mark. `leanKnowledge` stays false.
- Hypotheses are typed assertions (asked, thought, written, heard, asserted), not a separate English inventory.
- The model may pick among moves that do not change disclose / withhold / share / act. Otherwise the engine forces the top effect. Every pick is logged.
- Provenance is `recorded_before`, `staff_action`, or `player_prompted`. Only the first two can rule an explanation out.
- `player_prompted` is why “tell Jun and follow NORA” scores the same as reading and stopping. That shared pair is the rule, not a hole in the tables.

## Open / next
- O-09 still owns the numbers: fuel budget, `minutesPerFuel`, reply delays.
- O-22 concealment lists. O-27 the release-despite-objections arc is sketched and not built.
- Engine does not store fuel, assertions, or marks yet. `exposedNpcFacts` still passes `oracleKnows`; the spec forbids that in the move implementation.
- Next implementation step is the boundary-narrow move loop, headless, before more rooms.

## Key paths
- `game/last-safety-autocomplete-prototype/spec/incident.md`
- `game/last-safety-autocomplete-prototype/spec/grammar.md`
- `game/last-safety-autocomplete-prototype/spec/engine.md`
- `game/last-safety-autocomplete-prototype/spec/world.md`

## Commits
- none
