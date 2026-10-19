# 2026-10-15 — Last Safety notebook dialog and free notes

kind: new-work
uptake: local

## Trigger
Remove the redundant room Notebook drawer (doors, records, knowledge strip duplicated by the 3D room, map, and Lab Access). When new learned facts appear, offer a dialog to copy them into handset Notes. Notes should not cost fuel — learning is already tracked; saving is convenience.

## Done
- content: Removed `#drawer` / Notebook button; deleted `renderSidebar` from `public/app.js`.
- content: Added `#notebookPrompt` dialog — queues new `learnedFacts` ids, Add → `file.write` under `notes/`, Not now / Esc skips for the session.
- content: `notes/` writes and thought-bubble copy no longer call `spend()`; photos still cost 1 fuel (`terminal-host.mjs`, `thoughtAction` in `game.mjs`).
- content: Spec updates — `graphics-ui.md`, `text-console.md`, `engine.md`, `terminal.md`.
- content: Test `notes cost no fuel; photos still do` in `engine.test.mjs`.
- housekeeping: Composer/suggestions full dock width retained in `style.css` (transcript scroll stays narrow).

## Decisions
- Bootstrap learned-fact snapshot on first render so opening facts do not spam dialogs; only deltas after that prompt.
- Dismissed fact ids live in memory until reset/load (not persisted).

## Open / next
- Optional: re-offer skipped facts when Lab Access first activates.
- Optional: document notebook dialog in `graphics-ui.md` with screenshot-level detail if playtesters miss it.

## Key paths
- `game/the-last-safety-review/public/app.js` — `trackNewLearnedFacts`, dialog handlers
- `game/the-last-safety-review/lib/world/terminal-host.mjs` — fuel on `file.write`

## Commits
- `00b71df9c` Last Safety: notebook dialog for new facts and free note saves.

## Verification
- `cd game/the-last-safety-review && npm test` — 94 pass.
