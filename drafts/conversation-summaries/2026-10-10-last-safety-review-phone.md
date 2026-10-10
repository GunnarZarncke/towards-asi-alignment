# 2026-10-10 — Last Safety Review phone draft

kind: new-work
uptake: local

## Trigger
Build a draft of the mobile terminal for the Last Safety Review prototype.
Prompts: paraphrase (no telemetry id)

## Done
- content: Player phone in `game/last-safety-autocomplete-prototype/public/terminal/` (homescreen, nine apps, viewers). Narrow viewports are full screen with a Lab control; wider windows keep the phone on the right over a dummy room.
- content: Fixture `fixtures/terminal-session.json` and projection in `public/terminal/project.mjs`. Oracle-only paths are dropped. Unreleased replies stay hidden. NORA chips omit one discriminating line; typed text can still send it. Pipeline step ids are not controls.
- bookkeeping: `npm run dev:terminal` (port 3002). `npm test` runs `tests/terminal.test.mjs` with the grammar tests.
- bookkeeping: Contract `TerminalState` records optional viewer text, chips, and omit. Plan no longer calls `dev:terminal` a missing harness.

## Decisions
- The harness applies the six isolate tools locally. It does not call the engine or a model. Composition still owns the real tool route.
- One allowed request in the fixture is `cap.meeting_summary`. `cap.deploy` is denied as not on the evaluator role. O-43 stays open.
- Wiki pages the player does not own cannot be overwritten. Creating notes and photos can.

## Open / next
- Wire `GET`/`POST` tool routes in composition when the engine can return `TerminalState`.
- Grammar ranker is not inside the phone yet. Chips come from the fixture.
- Graphics still draws its own room. This harness blinks a dummy handset when the overlay is closed and a notice is unread.

## Key paths
- `game/last-safety-autocomplete-prototype/spec/terminal.md`
- `game/last-safety-autocomplete-prototype/public/terminal/`
- `game/last-safety-autocomplete-prototype/fixtures/terminal-session.json`

## Commits
- none

## Verification
`cd game/last-safety-autocomplete-prototype && npm test` → `ℹ pass 15` / `ℹ fail 0`, including `fixture session matches the solo phone check`.
Browser at `http://127.0.0.1:3002`: homescreen, NORA send of the omitted line, Files, wiki link, calendar now-line, note saved into Files, video play, unknown-file preview, API grant and `cap.deploy` denial, photo capture, contacts open Pavel with “No reply yet”, Lab closes the phone and the handset blinks. At 390×844 the phone slot is `position: fixed` and fills the viewport.
