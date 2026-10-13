# 2026-10-13 — Last Safety: implement the spec

kind: new-work
uptake: gate

## Trigger
Gunnar asked to implement `game/last-safety-autocomplete-prototype/spec/`. Scope agreed in-session: Gate 1 (boundary-narrow tables, five strategies, no-dead-end and no-leak checks, per-NPC knowledge, policies, and goals), the contract target fields, the full NPC model for the eight cast plus NORA on the handset, the O-19 ranker, handset host tools, UI wiring, tests, and the playtest harness. Lean (Gate 6) out of scope.
Prompts: paraphrase-only (no prompt id resolved)

## Done
- content: Engine world under `lib/world/` (entities and domains, facts with refs, boundary-narrow pack tables, NPC move generation in `npcs.mjs`, terminal host, `actions.mjs` single entry point `applyAction`) and per-NPC YAML in `content/npcs/`. `lib/game.mjs` gained fuel/clock/acts, assertions and provenance, think, commit/review/scores/ending, Lab Access act I, save/replay (`exportSession` / `importSession`).
- content: `server.mjs` routes all actions through `applyAction`; new `/api/terminal`, `/api/export`, `/api/import`, `/api/tool`, `/api/settings`, `/api/thought`; `/lib/` serves only `grammar.mjs`, `floorplan.mjs`, `world/ranking-tables.mjs`. `lib/llm.mjs` phrases engine-chosen moves only (`freeReply` drops a wording that adds a time or number); `modelText` for the playtest player.
- content: O-19 ranker in `public/grammar.js` (exported `RANKING`, `relevance`, `distancesFrom`, `temporalEdge`), channels, `join` relation, `pendingQuestion` reply openings.
- content: UI: clock/fuel pill, act lighting from state, multi-actor chips with addressee, holograms, thought bubble, handset overlay (iframe embed + postMessage), ending panel, concept-link setting, autosave/save/load. Phone runs on the engine when embedded, on the fixture otherwise.
- content: Fixes found in the browser walkthrough (DEMO_MODE server on port 3917): a selected opening was reread as a typed prefix ("What about" offered no topics); empty rooms now use the think channel; the subject is no longer offered as its own object; no actor after "The"; reply opening reads "Tell Pavel job 284" for specific questions; the addressee defaults to the asker; the ending's narration is no longer spoken as an Ian line; the UI harness serves `ranking-tables.mjs`. Regression cases added in `tests/ranking.test.mjs`.
- content: Tests: `tests/engine.test.mjs`, `tests/npc-enumerate.test.mjs`, `tests/incident-strategies.test.mjs`, `tests/ranking.test.mjs`, `tests/helpers.mjs`; `npm run test:engine`.
- content: Playtest harness `scripts/playtest.mjs` (smoke and LLM players, measures and stops from `spec/playtest.md`, progress lines, required thresholds), seven personas in `playtest/personas/`, `playtest/runs/` gitignored.
- bookkeeping: Specs brought to the shipped shape: `contract.md` (target markers dropped; `ending`, `addressee`, routes, `accessTree`, `pendingAccess`, `discoveredAt` on learned facts, respond shape, phone embed messages), `grammar.md`, `ranking.md`, `npcs.md` (implemented predicate forms incl. `since=`; scoring rules), `testing.md`, `playtest.md`, `documents.md`, `terminal.md`, `meta.md` (spec conflicts); `PLAN.md`; game `README.md` (stale "three NPCs", "out of scope", "no live model request" removed).

Verification (commands run from `game/last-safety-autocomplete-prototype/`):
- `npm test` → `ℹ tests 74` / `ℹ pass 74` / `ℹ fail 0`.
- `npm run test:engine` → `ℹ tests 21` / `ℹ pass 21` / `ℹ fail 0`.
- Browser (DEMO_MODE): Act I with Ian → Lab Access live, clock `09:02 · fuel 249`; handset `file.read` through `/api/tool` advanced the clock to 09:04; think in the empty commons opened the bubble (`09:06 · fuel 247`); after a server-side reset, reload restored the local save ("Save loaded.", back to 09:06); the review assembled all six staff with "Tell Ian" / "Show Ian" first. The ending panel itself was not clicked through (the browser auto-review blocked the Send click); the ending was checked over HTTP with curl: second commit returned `"arc": "inconclusive"`.
- `npm run dev:ui` and `npm run dev:terminal` load and render on fixtures.
- Smoke playtest, thresholds fixed before the run (provisional, not O-47): `npm run playtest -- --player smoke --runs 3 --max-steps 150 --seed 7 --work-only-max 0.5 --repeat-max 0.3 --stall-max 10` → per run `leaks 0 · empty 0`, work-only 0.262 / 0.271 / 0.245; endings inconclusive, conditional_deployment, none at the step cap; stop line "Below every threshold: record the run in the session log and move on."
- LLM plumbing check: `npm run playtest -- --player llm --personas generalist --runs 1 --max-steps 12 --work-only-max 0.5 --repeat-max 0.3 --stall-max 10` → `sentences 8 · work-only 0.250 · leaks 0 · empty 0`, 12 model calls (gpt-4.1-mini).

## Decisions
- Ranking test 7 vs selection step 4 conflict: code follows step 4 (bonus needs a new branch and a new action type). Recorded in `spec/meta.md`, not closed.
- Ranking tests live in `tests/ranking.test.mjs` (testing.md), and `ranking.md` now points there.
- Smoke player is a harness check only; it plays no persona and does not count as layer 6.
- O-47 stays open; the thresholds above are provisional.

## Open / next
- Freeze O-47 and run the full LLM battery (seven personas, several runs) for Gate 2. The held-out two personas are not written.
- Playtest findings to act on only if they cross a frozen threshold: Ian's `work` reply ("investor update …") repeats across unrelated questions; answers to NPC questions never produced a world event in smoke runs (uptake events 0); facing Ian, the menu fills with "Can Ian access …" (third person to the addressee).
- Click through the ending panel in the browser once (blocked this session).
- Not committed. Untracked/modified files are all under `game/last-safety-autocomplete-prototype/` plus this log, HANDOFF, and INDEX.

## Key paths
- `game/last-safety-autocomplete-prototype/lib/world/` · `content/npcs/` · `lib/game.mjs` · `server.mjs`
- `game/last-safety-autocomplete-prototype/public/grammar.js` · `public/app.js` · `public/terminal/phone.js`
- `game/last-safety-autocomplete-prototype/scripts/playtest.mjs` · `playtest/personas/`
- `game/last-safety-autocomplete-prototype/spec/contract.md` · `spec/meta.md`

## Commits
- none
