# 2026-10-15 — Last Safety NPC click addressee

kind: correction
uptake: local

## Trigger
In the 3D room, clicking an NPC still selected them for floor movement (leftover from testing). Clicking a person should set the default speak addressee, same as the transcript dock chips.

Prompts: paraphrase only (no prompt id).

## Done
- content: `public/render/three-scene.mjs` — NPC click calls `onFocusActor` only; floor walks always use the player; removed the debug “Moving: …” chip; tooltips updated.
- content: `public/app.js` — scene hint text.
- content: `spec/graphics-ui.md` — click behavior documented.

## Decisions
- 2D CSS fallback already routed actor hotspots to `onFocusActor`; no change there.

## Open / next
- None for this fix.

## Key paths
- `game/the-last-safety-review/public/render/three-scene.mjs`
- `game/the-last-safety-review/public/app.js`

## Verification
- `npm test` in `game/the-last-safety-review` — `ℹ tests 107` / `ℹ pass 107` / `ℹ fail 0`.

## Commits
- `d96576a27` Last Safety: public-hosting hardening and NPC click addressee.
