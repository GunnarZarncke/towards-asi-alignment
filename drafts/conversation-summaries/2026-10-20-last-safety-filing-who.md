# 2026-10-20 — Last Safety filing UX and Who roster

kind: new-work
uptake: status

## Trigger
Filing felt like a targetless command; tie commit to Ian in person or Lab Access DM. Check player/Ian copy against Ian’s voice. End of session commit.

Prompts: (paraphrase-only — no prompt id in transcript export)

## Done
- content: **Commit addressing** — `commit` requires Ian present or DM to Ian (`labAccessActive`); openings **Ian, I'm ready to sign.** / **Sign the review.**; handset chip **I'm ready to sign.**; engine error and text-console hints updated (`lib/game.mjs`, `public/grammar.js`, `terminal-host.mjs`, `view.mjs`, `actions.mjs`, `app.js`, `spec/grammar.md`).
- content: **Ian voice** — Meeting and early-commit Ian lines use **sign** not **file**; spec notes player copy uses sign.
- content: **Who prefix** — Local `Who` opening; roster asks withhold with Ian `glue.attendeeAsk`; `utterance` into `responseCandidates` (`npcs.mjs`, `ian.yml`, `catchall.test.mjs`, `grammar.md`).
- content: Tests — commit gate without Ian; filing chip gating; `commit()` helper walks to Ian via `npcs.ian.room`.
- bookkeeping: Session log and HANDOFF.

## Decisions
- Filing chip only when `reviewCallable` or fuel 0 (not on every Ian encounter) so Welcome suggestions stay tutorial-safe.
- Engine term `commit` unchanged; player-facing and Ian dialogue use **sign**.

## Open / next
- Manual playtest: call review from handset vs in review room with Ian on investor prep.
- Uncommitted outside lane: Ch. 1 claim-extract, conversation-summary archive moves, field-news drafts.

## Key paths
- `game/the-last-safety-review/lib/game.mjs` — `commit`, `dmSend` commit branch
- `game/the-last-safety-review/public/grammar.js` — `FILING_OPENINGS`
- `game/the-last-safety-review/spec/grammar.md` — Commit + Who sections

## Commits
- `fe0ee83e5` Last Safety: Ian-addressed commit, sign copy, and Who roster withhold.

## Verification
- `cd game/the-last-safety-review && npm test` — 147 pass, 0 fail, 1 skip
