# 2026-10-10 — Last Safety Review O-31–O-41

kind: new-work
uptake: status

## Trigger
Gunnar decided O-31 through O-41: save format, input limits, renderer and character detail, recordings, music, mobile, audience language, how a gap gets noticed, and optional TSA links.
Prompts: none resolvable (paraphrase only).

## Done
- content: `spec/meta.md` decision rows O-31–O-41. Still open: O-06, O-12, O-19, O-22, O-24, O-27, O-28 (whether the copy is needed), O-37, O-42, O-43, O-44. The 100-character cap is tentative.
- content: `spec/engine.md` — local storage, versioned JSON with a scenario name, movement events on the fuel clock, three ways to notice a report gap, no learning score.
- content: `spec/grammar.md` — one sentence, strip special characters, no jailbreak filter.
- content: `spec/graphics-ui.md` — stay on Three.js; current bodies and motion stand; recordings replay events; bottom concept strip when the setting is on.
- content: `spec/terminal.md` — Video app (fast forward, backward, next and previous room); TSA-links setting default off.
- content: `spec/world.md` — per-NPC prompt focus and the general-audience line.
- bookkeeping: `PLAN.md` gates 3, 5, and 6.

## Decisions
- Movement is stored even though it changes no knowledge, because camera playback replays the log.
- O-40 is not a post-game score. The gap sits in a summary or checklist; analyzing the report spends fuel; an NPC may say a load-bearing gap after an act change.
- Music stays open until the story is set.

## Open / next
- Confirm or replace the 100-character cap.
- Wire the audience line into `lib/llm.mjs` when NPC prompts are next edited. The running prompt does not have it yet.

## Key paths
- `game/the-last-safety-review/spec/meta.md`
- `game/the-last-safety-review/spec/engine.md`
- `game/the-last-safety-review/spec/world.md`

## Commits
- none
