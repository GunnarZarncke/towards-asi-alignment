# 2026-10-15 — Last Safety transcript reveal and composer focus

kind: correction
uptake: local

## Trigger
After send, the transcript should scroll smoothly and reveal NPC reply one sentence per second (not instant). After Enter or Send, focus must stay in the chat input; it was lost when clicking Send.

Prompts: paraphrase only (no prompt id).

## Done
- content: `public/app.js` — sentence-split transcript reveal after `/api/respond` (player lines in the turn instant, NPC one per second, smooth scroll; effect notice after reveal); `composerBusy` + Send `mousedown` preventDefault + `focusComposer()` so the dock stays open and `#utterance` keeps focus.
- content: `spec/graphics-ui.md` — transcript reveal behavior documented.

## Decisions
- Load, move, and other full `render()` paths still paint the transcript instantly.

## Open / next
- None.

## Key paths
- `game/last-safety-autocomplete-prototype/public/app.js`
- `game/last-safety-autocomplete-prototype/spec/graphics-ui.md`

## Verification
- `npm test` in `game/last-safety-autocomplete-prototype` — `ℹ tests 107` / `ℹ pass 107` / `ℹ fail 0`.

## Commits
- `31213aba9` Last Safety: stagger NPC transcript lines and keep composer focus.
