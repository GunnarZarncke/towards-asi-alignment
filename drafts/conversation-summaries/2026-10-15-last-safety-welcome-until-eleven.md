# 2026-10-15 — Last Safety Welcome until 11:00

kind: new-work
uptake: local

## Trigger
Welcome ended on the first sentence to Ian, so simulated play spent almost all of its fuel in Doubt. Gunnar asked for a later, natural transition into Act II.
Prompts: paraphrase (no prompt id in this session)

## Done
- content: Act I now lasts until 11:00, when Ian leaves the commons for the investor update. Lab Access still opens on the first sentence and no longer changes the act. `CONFIG.DOUBT_AT`. Spec: `world.md`, `npcs.md`, `engine.md`, game `README.md`.
- content: Tests: Welcome stays after the handset line; Ian’s closing glue fires at the departure. `startedSession` walks the clock forward with logged moves so save/replay still matches.
- bookkeeping: `npm test` in `game/last-safety-autocomplete-prototype` — 99 pass, 0 fail.

## Decisions
- The transition is Ian leaving for the investor update, the next beat already on the Friday schedule. It is not the first discrepancy (`job_continued`), which the smoke player hits within a few actions and would leave Welcome short again.

## Open / next
- A player who reads the job log at 09:30 still has Welcome lighting until 11:00. If that should tip the act early, say so.
- Welcome is 4 minutes per fuel, so 11:00 is 30 fuel from 09:00. The review threshold is unchanged.

## Key paths
- `game/last-safety-autocomplete-prototype/lib/game.mjs`
- `game/last-safety-autocomplete-prototype/lib/world/config.mjs`
- `game/last-safety-autocomplete-prototype/spec/world.md`

## Commits
- none
