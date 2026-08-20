# 2026-08-03 — Site projection phrasing + formalizations table rename

## Trigger
User asked to replace remaining site “subsumption” reader-facing phrasing with “projection,” then rename the field-subsumptions graph table section from “Field-agenda crosswalk” to “Overview of existing formalizations” (broader Field hub matrix now owns crosswalk framing). Session ended with commit.

## Done
- **Projection phrasing:** Lean spine section title → “Field agenda projections”; graph dot label → “Field-agenda projections”; spine graph badges `[SUBSUMED]` → `[PROJECTED]` on value-transport and correction-successors; projection card Lean summaries updated (CIRL, shutdown, interrupt); `sync-lean-spine.mjs` prefers scripted graph title over dot label; `llms.txt` → “Existing-Work Projections To Notice.”
- **Table section rename:** `FieldProjectionsTable.astro` h2 → “Overview of existing formalizations” (on `/lean/` and `/lean/graph/field-subsumptions/`).
- Regenerated site artifacts locally (`sync:projections`, `sync:lean-spine`, `sync:bot-orientation`, `build:search-index`) — generated outputs gitignored; deploy needs `npm run sync` in `site/`.

## Decisions
- **Stable slugs unchanged:** `/cards/subsumption-*` and `/lean/graph/field-subsumptions/` URLs kept (externally posted / bookmarked).
- **Lean identifiers unchanged:** theorem `nodeId`s and `SubsumedForward` in graphs remain as formal-spine names.
- **Section vs page title:** only the projections table section renamed; graph nav tab (“Field crosswalk”) and graph page h1 unchanged this pass.

## Open / next
- Optional: rename graph slug `field-subsumptions` → `field-projections` with redirect; align LeanGraphNav label with “Overview of existing formalizations” if the whole graph page should drop “crosswalk.”
- Site build/deploy to pick up regenerated gitignored assets.

## Key paths
- `site/src/components/FieldProjectionsTable.astro`
- `site/scripts/sync-lean-spine.mjs`
- `context/lean_proof_graphs/05-field-subsumptions.dot`, `02-value-transport.dot`, `03-correction-successors.dot`
- `metadata/concepts/bodies/subsumption-*.md`
- `llms.txt`

## Commits
- `92e5bc69` Replace site subsumption phrasing with projection framing.
