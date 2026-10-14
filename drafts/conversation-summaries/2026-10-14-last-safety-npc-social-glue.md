# 2026-10-14 — Last Safety NPC social glue

kind: new-work
uptake: local

## Trigger
Daniel and Elena both used the same generic work line; conversations were too factual. Add non-fact sentences at conversation start and before someone leaves, optional mid lines at person-specific frequency, driven by the status/Person layer and configurable.
Prompts: (none recorded)

## Done
- content: `spec/npcs.md` social glue + `work` fallback; `spec/world.md` Person drives glue stance; `spec/engine.md` no status number.
- content: `CONFIG.GLUE` and `lib/world/glue.mjs`; per-NPC `glue` + agenda `work` in `content/npcs/*.yml`.
- content: Opening/mid/closing lines in `talkTo` / `relocateNpcs`; work fallback is agenda/`glue.work`, not a shared shrug.
- content: Phrasing prompt includes the Person layer; glue moves may be rephrased without adding facts.
- content: `tests/glue.test.mjs`. `npm test` in the prototype: 91/91 pass.

## Decisions
- Stance is a discrete label (`pleasant` / `busy` / `pushy` / `thin` / `deferential`), not a stored trust score (O-21).
- Glue carries no fact id and is skipped on the handset. Mid rate is a replay-stable hash.
- Domain keys on `onDomain` are ranking domains (`staffing`, `metrics`), not entity ids.

## Open / next
- Tune `midRate` and lines after live play. Live phrasing of glue still needs a key (`--demo` uses templates).

## Key paths
- `game/last-safety-autocomplete-prototype/spec/npcs.md`
- `game/last-safety-autocomplete-prototype/lib/world/glue.mjs`
- `game/last-safety-autocomplete-prototype/content/npcs/`

## Commits
- (none)
