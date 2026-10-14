# 2026-10-15 — Last Safety photo pipeline and transcript collapse

kind: correction
uptake: status

## Trigger
Follow-up on handset/room UX: photos not viewable or black; transcript log should hide off-input but suggestions and Show more must remain clickable. User requested end-of-session commit.

Prompts: (paraphrase — no prompt ids in export)

## Done
- content: `photo-export.mjs` JPEG downscale before save; `photo-data.mjs` validate image payloads; `/api/handset-file` path (prior commit) wired through phone viewer; WebGL `preserveDrawingBuffer` + pre-capture render; transcript collapse on outside tap / focusout (not textarea blur); capture-phase dock pointerdown for chips. Specs `terminal.md`, `graphics-ui.md`.
- bookkeeping: Session log; HANDOFF/INDEX.

## Decisions
- Reject truncated or tiny image data at `writeNote` instead of storing broken photos.
- Collapse transcript on pointerdown outside `#transcriptDock`, not on input blur, so mousedown reaches suggestions.

## Open / next
- Playtest photo framing with pan/zoom on `#roomMount` vs canvas crop alignment if reports drift.

## Key paths
- `game/last-safety-autocomplete-prototype/public/app.js`
- `game/last-safety-autocomplete-prototype/public/render/three-scene.mjs`
- `game/last-safety-autocomplete-prototype/lib/photo-data.mjs`

## Commits
- (this session)

## Verification
- `npm test` in `game/last-safety-autocomplete-prototype`: 99 pass.
