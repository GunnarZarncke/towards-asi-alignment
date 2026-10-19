# 2026-10-15 — Last Safety NPC dialogue and DM phrasing

kind: new-work
uptake: status

## Trigger
Explain the reply pipeline (parse → engine → phrasing), what is not phrased, and why dialogue felt terse or generic; then implement content levers, run `phraseLines` on handset DMs, and slightly relax the composition prompt.

Prompts: (paraphrase-only — no resolvable prompt ids in telemetry)

## Done
- content: NPC YAML — `work_alt` alternates, authored `refer.line` entries (Elena, Pavel, Jun), glue/agenda copy tweaks across cast.
- content: Engine — `textureDialogue` prefers agenda/glue over third-person FACTS; refer template and `workMove` alternation; Act III Ian filing prompts rotated; commit nudge variants.
- content: `dmSend` async with `phraseLines` before queue (demo/replay/API-fail safe); server/text console await DM tool; async `importSession` / `loadSaveFile`.
- content: `freeReply` prompt — same facts, natural voice (not “phrase exactly that”).
- housekeeping: Tests updated for DM handset visibility vs stored text; `dm()` helper uses `tool: 'dm.send'`; fixed duplicate event log on DM.
- bookkeeping: Verification — `cd game/the-last-safety-review && DEMO_MODE=1 npm test` → 107 pass, 0 fail.

## Decisions
- DM phrasing runs at send time (queued text is final); room `conversations` are not updated for DM (handset release unchanged for transcript).
- Left unstaged in working tree: `public/app.js` transcript sentence reveal animation and minor `spec/graphics-ui.md` edit (separate UX lane).

## Open / next
- Playtest live phrasing on handset threads with a capped API key; tune `work_alt` / refer lines if playtests still repeat.
- Optional: Act III `meetingTurn` through `npcTurn` + phrasing (still hardcoded Ian loop for non-request lines).
- Commit or revert the unstaged transcript animation in `public/app.js` when that lane is ready.

## Key paths
- `game/the-last-safety-review/lib/game.mjs` — `dmSend`, meeting Ian lines
- `game/the-last-safety-review/lib/world/npcs.mjs` — `textureDialogue`, refer, work
- `game/the-last-safety-review/content/npcs/*.yml`
- `game/the-last-safety-review/lib/llm.mjs` — `freeReply`

## Commits
- `72c6c4ab4` Last Safety: richer NPC templates, DM phrasing, softer composition.
