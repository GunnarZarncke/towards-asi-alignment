# 2026-08-06 — MB7a–c bridge cards

## Trigger
User: create explicit MB7a–c bridge cards linked from MB7 overview (MB7d stays); then rename cards to book terminology (access-model soundness, filter coverage, bounded hidden capability) rather than alternate field-facing labels.

## Done
- Added `mb7a-access-model-soundness`, `mb7b-filter-coverage`, `mb7c-bounded-hidden-capability` to `metadata/bridges.yml` with body files under `metadata/concepts/bodies/`.
- Updated MB7 overview + MB7d sibling links; `reference/field-agendas/data/bridges.yml` MB7a–c rows + `mbBridgeCards`.
- `bridge-crosswalk.json` split into MB7 overview + MB7a/b/c rows; `BridgeCrosswalkTable.astro` letter-suffix card routing; `bridge-card-slug.mjs` + Lean check slug map.
- `site/.gitignore` for generated MB7a–c cards; ran `sync:bridges`, `sync:field-agendas`, `sync:lean-spine`, `sync:bridge-graph`.
- TODO in `metadata/TODO.md`: consider field-standard noun aliases later without collapsing MB7a–c split.

## Decisions
- Card titles follow **book** names (Access-Model Soundness / Filter Coverage / Bounded Hidden Capability), not the alternate labels suggested in the first prompt.
- MB7 overview keeps no per-sub-bridge `leanNodes` (MB4/MB4a pattern); each sub-card carries its Lean node.

## Open / next
- Optional: App B longtable rows for MB7a–c individually (sync-bridges warns grouped MB7a–c only today).
- Track 2 field-noun divergence (`metadata/TODO.md` MB7a–c item).

## Not committed (other working tree)
- `DebateGame.lean` + `appG-lean-proof-spine.tex` negation extension (separate session).
- Untracked drafts/assets: `TSA.png`, `TSA.svg`, `context/David-low-dim-personality-tweets.md`, `drafts/lw-*.md`, `drafts/secret-loyalties-*.md`, `2026-08-05-mackinlay-*.md`.
