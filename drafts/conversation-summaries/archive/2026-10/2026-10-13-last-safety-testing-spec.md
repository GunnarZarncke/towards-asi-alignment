# 2026-10-13 — Last Safety testing spec

kind: new-work
uptake: rule

## Trigger
Gunnar asked for more specification of the game's testing parts and a small testing concept.
Prompts: paraphrase-only (no prompt id resolved)

## Done
- content: New `game/the-last-safety-review/spec/testing.md`. Concept: a test is an observer on the same planes as the game (oracle / engine vs player-visible). Seven layers with owners, commands, and stops. Lane-unit table for what exists (`grammar`, `documents`, `access`, `terminal`) and what is still missing (`engine*`, ranking, NPC enumerate, incident strategies). Graphics stays fixture-only. In-fiction O-16 handles are out of this file.
- bookkeeping: Pointers from `PLAN.md`, `spec/README.md`, `playtest.md`, `engine.md`, `incident.md`, `npcs.md`, `grammar.md`, game `README.md`.

## Decisions
- Player-plane tests may not import oracle, policies, or goals except as a fixture label. Engine-plane tests may read those fields to build state, then still assert on the payload with the player-visible list.
- No new open question. O-47 remains the playtest rate freeze. Graphics Node tests are not required.

## Open / next
- Implement `tests/engine*.mjs` and `npm run test:engine` when Gate 1 tables exist.
- Ranking unit test when the ranker lands.
- Do not run LLM playtest until layer 4 is green on the first pack.

## Key paths
- `game/the-last-safety-review/spec/testing.md`
- `game/the-last-safety-review/spec/playtest.md`
- `game/the-last-safety-review/PLAN.md`

## Commits
- (none)
