# 2026-08-05 — Subsumption-debate leanNodes kind CI fix

## Trigger
GitHub Actions site build failed: `subsumption-debate` card `leanNodes.4.kind` was `separationOnly`, invalid for the Astro cards schema (`proof` | `counterexample` | `bridge` | `definition`).

## Done
- Fixed `metadata/concepts/bodies/subsumption-debate.md`: `debate_truth_is_correction_projection` kind `separationOnly` → `bridge`; summary still notes `(ledger: separationOnly)`.
- Verified `sync-concepts.mjs` + `astro build` locally (857 pages, exit 0).

## Decisions
- Do not extend the cards schema with Lean `FieldResultStatus` values — ledger status belongs in `metadata/projections.yml` / field projections table and can be noted in leanNode summaries; card `kind` stays the spine taxonomy.

## Open / next
- None from this session.

## Key paths
- `metadata/concepts/bodies/subsumption-debate.md`
- `site/src/content.config.ts` (leanNodes schema)

## Commits
- (this session)
