# 2026-10-19 — Last Safety open-ask hints

kind: new-work
uptake: local

## Trigger
Playtest follow-up: glossary pack-gating and NPC leads; adapt tests to author glossary; Jun clarity; playthrough metrics; design and implement open-ask handling (volunteer-only hints, no pendingQuestion, shared initiative cooldown). End-of-session commit for game tree.
Prompts: paraphrase only (no prompt id).

## Done
- content: Open-ask path in `lib/world/npcs.mjs` — goal questions first (ranked), one volunteer `hint_ask` or `hintShare` doc, refer fallback, `work`; domain filter from `open_content` + agenda; initiative cooldown shared; removed redirect `catchall`.
- content: Jun player lines; volunteer initiative wording; `documents.test.mjs` aligned to author `wiki-glossary.md`; playthrough smoke/full tests; grammar Hi gate; grammar/text-console test paths.
- housekeeping: `spec/npcs.md`, `spec/testing.md`, `spec/grammar.md`; session log and HANDOFF.

## Decisions
- Broad vs narrow asks stay on existing parser (grounded `ask` still uses `answer` / one-edge-away); only ungrounded `ask`/`ask_why` use hint path.
- Topic “catchall” multi-disclose rejected; single volunteer-equivalent hint only.
- Meta redirect `glue.catchall` removed; refer/work cover empty pool.

## Open / next
- Optional `glue.volunteerHint` / `glue.shareHint` per NPC after playtest.
- Wire `pendingQuestion` for hint asks when actionability is ready.
- Broad `ask|about|topic=*` hint path if parser gains reliable broad/narrow.

## Key paths
- `game/last-safety-autocomplete-prototype/lib/world/npcs.mjs` (`openAskHintMove`, `isOpenAsk`)
- `game/last-safety-autocomplete-prototype/tests/catchall.test.mjs`, `tests/playthrough.test.mjs`

## Verification
- `cd game/last-safety-autocomplete-prototype && npm test` → 140 pass, 1 skipped (full playthrough unless `PLAYTHROUGH_FULL=1`).

## Commits
- (this session)
