# 2026-10-15 — Last Safety ending reachability (O-29)

kind: new-work
uptake: status

## Trigger
Implement full designated ending reachability as specced; keep slow suite off default `test:engine`.

Prompts: (session — game end reachability, not floorplan)

## Done
- content: `tests/ending-reachability.test.mjs` — witness path for each boundary-narrow `(arc, addOn)` (6 cells) plus suspend→technical_suspension; `npm run test:endings`.
- content: `spec/testing.md` layer 4b; `package.json` script.
- housekeeping: Clarified floorplan vs ending reachability in prior thread (no code).

## Decisions
- O-29 “every designated end-state reachable” = scripted witnesses, not state-space BFS (Lean/future for “from every state…”).

## Open / next
- Optional bounded BFS under fuel cap for partial O-29 second clause; playtest after door gates.

## Key paths
- `game/the-last-safety-review/tests/ending-reachability.test.mjs`

## Commits
- `334adeecb` Last Safety: O-29 ending reachability witness tests.
