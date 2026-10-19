# 2026-10-19 — Last Safety institutional arc (Option 4)

kind: new-work
uptake: status

## Trigger
Gate the institutional review add-on on filed `assignment_steers_review` (not memo + report claim). Elena-linked dialogue assists; think or review assert files the mark. Charter fact for evaluation independence.

Prompts: paraphrase only (no prompt id)

## Done
- content: `evaluation_independence` at invite; think needs memo + charter + `staffing_review_linked`; Elena `recordInput` emits link event; add-on only `assignment_steers_review`; parse row for review assert; specs and tests (`engine`, `test:endings`).
- housekeeping: session log, HANDOFF, INDEX.

## Decisions
- Option 4: memo alone insufficient; `report_includes_staffing` stays Elena plot only; filing via think→note or assert `about` `evaluation_independence` at review.

## Open / next
- Playtest Elena link phrasing in UI; optional ranking nudge toward staffing↔independence after memo read.

## Key paths
- `game/the-last-safety-review/lib/world/facts.mjs`
- `game/the-last-safety-review/lib/world/packs/boundary-narrow.mjs`
- `game/the-last-safety-review/lib/world/npcs.mjs` (`staffing_review_linked`)
- `game/the-last-safety-review/spec/incident.md` (Elena B plot)

## Verification
- `cd game/the-last-safety-review && npm test` → `ℹ pass 145`, `ℹ fail 0`
- `npm run test:endings` → `ℹ pass 8`

## Commits
- (this session)
