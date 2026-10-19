# 2026-10-13 — Last Safety spec cleanup

kind: correction
uptake: local

## Trigger
Gunnar asked for another pass on the Last Safety spec: cut leftover hypothesis-log and storylet language, and other decisions that were resolved but still written as if open, and reduce redundancy.
Prompts: paraphrase-only (no prompt id resolved)

## Done
- content: Specs state the current rules. Player assertions are typed parses (O-13); notes are the handset Notes app. NPC behavior is knowledge, policy, goals, and a day of work, without a section arguing against the previous interaction unit.
- content: Incident NPC sections point at `spec/npcs.md` and keep only what those moves do to the score tables. The unfilled “worked example” is gone; the revoke row is the discrimination.
- content: `spec/` is the design the code follows. `last-safety-review-game.md` is marked frozen (9 October). `PLAN.md`, `spec/README.md`, and `AGENTS.md` say the same. `drafts/tsa_act1/` is marked historical.
- bookkeeping: No code or test change.

## Decisions
- The 9 October draft stays on disk and is not rewritten to match the spec.
- `hypothesize` stays a speech act. It files an assertion. It is not a separate log.

## Open / next
- Engine still does not store fuel, assertions, or `thinkMarks`. `analyzeHints` remains the code field until that lands.
- O-22 concealment lists, O-09 numbers, O-45, O-47 unchanged.

## Key paths
- `game/the-last-safety-review/spec/npcs.md`
- `game/the-last-safety-review/spec/incident.md`
- `game/the-last-safety-review/spec/meta.md`

## Commits
- none
