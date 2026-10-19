# 2026-10-09 — Last Safety Review plan split

kind: new-work
uptake: local

## Trigger
User asked for a development plan without the design detail, and for the consolidated game doc to be split into component and meta specs so agents can work in parallel and a person can test one lane or all of them.
Prompts: paraphrase (no prompt id)

## Done
- content: `game/the-last-safety-review/PLAN.md` — lanes, file ownership, solo versus combined checks, gates.
- content: `spec/terminal.md` — player computer as an isolate UI (files, delayed messages including NORA, access requests). Pipeline and overseer handles excluded.
- content: `spec/incident.md` — shutdown incident as a causal model (hypotheses, facts, interventions) that gates dialogue and rooms. Epistemic success and control success stay separate. Disclosure is an action. NORA-channel completions may omit evidence. Transfer study marked later.
- bookkeeping: PLAN lanes, contract `TerminalState`, meta O-43 and O-44, short pointers in engine, graphics, and world specs.

## Decisions
- Specs are the working copy for implementation. The consolidated markdown stays the source and is not edited by lane work.
- Grammar, graphics/UI, terminal, and engine each own a file set. `server.mjs` and `lib/llm.mjs` are composition. World content is engine-owned and read by graphics.
- The player computer matches the lab-sim isolate tool list. Player tools are file read/write/share, DM read/send, and access.request. `pipeline.trigger_step` and `handle.invoke` are not on that screen. The game does not import the Python sim.
- Contract changes are not a single-lane edit.
- Open questions stay open. The shutdown tables in `spec/incident.md` are the next content; they are not filled in. A post-game transfer scenario is out of scope.
- `dev:ui`, `dev:terminal`, and `test:engine` are named and not implemented.

## Open / next
- Authoritative incident history: fill `spec/incident.md` (three explanations, six facts, four interventions) and run the headless strategies before more dialogue or rooms.
- Harness scripts so graphics, terminal, and engine can be run without each other.
- Phone overlay UI (homescreen, four apps, viewers) specified; not built.

## Key paths
- `game/the-last-safety-review/PLAN.md`
- `game/the-last-safety-review/spec/README.md`

## Commits
- none
