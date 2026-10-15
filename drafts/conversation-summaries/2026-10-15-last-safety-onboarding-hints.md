# 2026-10-15 — Last Safety onboarding hints

kind: new-work
uptake: local

## Trigger
Playtests: people wander, miss what they can do, and do not realize speaking and the phone are the main tasks. Add a composer bubble until the first sent line, then a Lab Access bubble with a phone mark until it is opened, and one non-misleading mechanic note in each room that had no hotspot, including text mode.
Prompts: paraphrase

## Done
- content: Composer blinks with “write here to get information from persons in the room” until a line is sent (`spoken` on client state). Lab Access then shows a phone mark, blinks, and “access tools, chat and information on your phone” until the launcher is opened.
- content: One readable note in each room that had no evidence screen (visitor card, whiteboard agenda, garden card, and signs in the corridor, bay, studio, quiet room, kitchen, test bay, and control room). Inspect marks them read and does not add a fact or a showable record. Text `look` / `read` and the headless options list include them.
- content: Reading a hotspot opens the transcript so the note text is on screen. A follow-up put the remaining notes in in-room language, moved the visitor card onto the commons standing table, and offers each card in the Add to Notes dialog (`keep` in the text console).
- content: Lab map button stays hidden until that corridor note is read, then blinks until opened once. Lunch plan, demo scrap, bay verse, and camera-log scribble replace the earlier mechanic cards.
- content: Author pass on `ROOM_NOTES` copy (visitor welcome, lab map, Jun demo scrap, bay whistle, CCTV scribble, and the rest) in in-room voice.
- bookkeeping: Engine and text-console tests for the notes and the text hints. Browser check of the commons card, the speak bubble, and the phone bubble.
- housekeeping: `npm test` in `game/last-safety-autocomplete-prototype`: 119 pass, 4 fail (Jun glue apostrophe regex, grammar room movement, Hi opener, text-console first-visit courtyard — logged as pre-existing on `main`).

## Decisions
- Notes are a separate `ClientState.notes` list, not evidence, so they cannot be shown as records and do not enter learned facts.
- Rooms that already have a screen (platform, evaluation, people) keep that one object.
- The phone bubble is dismissed in this browser tab (`sessionStorage`), including from the text page after a successful phone command. Reset clears it.

## Open / next
- `go courtyard` from a fresh text session still fails: the console plans the whole path at clearance 0, before the first step would turn Lab Access on. Pre-existing; not changed here.
- Grammar tests “room movement” and “Hi social opener” also fail on current `main` without these edits (clearance recompute, and Justine present in platform after the clock reaches doubt).

## Key paths
- `game/last-safety-autocomplete-prototype/lib/game.mjs` (`ROOM_NOTES`, `spoken`)
- `game/last-safety-autocomplete-prototype/public/app.js`, `public/index.html`, `public/style.css`
- `game/last-safety-autocomplete-prototype/public/render/layouts.mjs`
- `game/last-safety-autocomplete-prototype/lib/text/console.mjs`

## Commits
- `82cd1e0a7` — Last Safety: onboarding bubbles, room notes, and map unlock.
