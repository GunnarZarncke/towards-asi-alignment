# 2026-10-13 — Last Safety: text console and overlay UI

kind: new-work
uptake: local

## Trigger
Gunnar asked for two game modifications. First, extend headless mode into a text-only interface: text descriptions for rooms, a text console with commands for navigation and phone use, and no reprinting of unchanged UI. Second, make the room view fill most of the screen (scrolling sideways with the player on mobile), put everything else in overlays, and show debug info only in a test mode.
Prompts: paraphrase-only (no prompt id resolved)

## Done
- content: The player-visible text view (`sentences`, `presentIds`, `options`, `render`) moved from `scripts/playtest.mjs` into `lib/text/view.mjs`; the playtest imports it. Line phrasing moved from `server.mjs` into `lib/phrase.mjs` so the server and the console share it.
- content: Text console `lib/text/console.mjs`. It reads only ClientState and TerminalState and acts through `applyAction`. Room descriptions come from the floorplan `role` and `windows` fields. After each command it prints only what changed; static parts reprint on request; numbered lists can be picked by number. It covers navigation, screens, talk, think, filing the review, and the handset.
  - Terminal front end: `scripts/text-play.mjs` (`npm run text`, `--demo`), which adds save, load, reset, and quit.
  - Browser front end: `public/text.html` on the new `POST /api/text`, sharing the cookie session with the room view.
- content: Overlay layout. `public/index.html` and `style.css` were rebuilt as a full-window room with a top bar, notebook drawer, bottom talk and composer panel, thought and ending overlays, and a ☰ menu. Dead rules for the three-column shell were removed from `style.css`. On a narrow viewport the canvas is at least 1.5 × the viewport height wide; `RoomRenderer.playerScreen()` and `onFrame` let `app.js` keep the player centered, pausing after a manual swipe. Test mode (`?test=1`, always on in dev-ui) shows the parser inspector, the demo/live pill, and the parser indicator.
- content: `tests/text-console.test.mjs` has four cases, including no unlearned fact text in the console output.
- bookkeeping: `spec/text-console.md` (new); `spec/README.md`, `PLAN.md` (Text console lane, `lib/phrase.mjs` under composition, "Text only" test row), `spec/contract.md` (`/api/text`), `spec/graphics-ui.md` (Interface: overlay layout, follow-scroll, test mode), `spec/playtest.md` (view module), game `README.md`.

Verification (from `game/the-last-safety-review/`):
- `npm test` → `ℹ tests 78` / `ℹ pass 78` / `ℹ fail 0`.
- `npm run test:engine` → `ℹ tests 21` / `ℹ pass 21` / `ℹ fail 0`.
- Smoke playtest after the move: `node scripts/playtest.mjs --work-only-max 0.5 --repeat-max 0.3 --stall-max 10 --max-steps 30` → `leaks 0 · empty 0`, "Below every threshold".
- Piped CLI session (`printf 's\n1\nphone\n…' | node scripts/text-play.mjs --demo`): Act II banner, Ian's lines, `[phone] Lab Access is active`, glossary read with `(noted)` fact, courtyard first visit in full, commons revisit short, NORA message reply.
- Browser (DEMO_MODE server, port 3011):
  - At 390×844 emulation, room scroller `sw 1266`, `cw 390`, `scrollLeft 455` (player centered), and the inspector reads `display: none`.
  - One composed exchange with Ian moved the clock to 09:02 and switched to Act II.
  - `?test=1` shows the inspector and the DEMO pill.
  - `/text.html` on the same session printed `go collab` and numbered suggestions.
  - `npm run dev:ui` renders Platform Operations with test mode on.

## Decisions
- The text interface ships as both a terminal script and a browser page, built on one console module.
- Test mode is a URL flag, not a persisted setting. The handset's own Parser inspector setting stays separate.

## Open / next
- Suggestion quality shows through more plainly in text: openings like "Show Ian" or "What about Ian" to Ian, and "Can Ian access …" to Daniel. This is the ranker finding from the previous session; it is not new.
- The drawer overlaps the bottom panel when open on desktop; acceptable for now.
- Gate 2 LLM battery at frozen O-47 thresholds still open from the implement-spec session.

## Key paths
- `game/the-last-safety-review/lib/text/` · `scripts/text-play.mjs` · `public/text.html` · `lib/phrase.mjs`
- `game/the-last-safety-review/public/index.html` · `public/style.css` · `public/app.js` · `public/render/three-scene.mjs`
- `game/the-last-safety-review/spec/text-console.md` · `spec/graphics-ui.md`

## Commits
- `0be3cd7e8` — Last Safety prototype: implement spec, text console, overlay UI (game tree + session logs).
