# 2026-08-03 — MB bridge graph + MB11 bridge card

## Trigger
User asked for a simplified Graphviz dependency graph of MB* bridges using field nouns; iterated layout (solid styling, black assembly edges, spacing); then noticed MB10/MB11 bridge cards missing on the site; requested end-of-session commit.

## Done
- Added `reference/field-agendas/graphs/mb-bridge-dependencies.dot` and `.png` — MB1–MB11 field-noun nodes, red logical edges, black assembly edges into MB11.
- Added **MB11 — Deployment Safety** bridge roster entry in `metadata/bridges.yml` + body `metadata/concepts/bodies/mb11-deployment-safety.md`.
- Pointed field matrix / crosswalk / Lean spine card links from `dynamical-guarantee` → `mb11-deployment-safety` (`reference/field-agendas/data/bridges.yml`, `site/src/data/bridge-crosswalk.json`, `site/src/data/field-agendas.json`, `sync-lean-spine.mjs`).
- Updated `bridge-assumptions` and `dynamical-guarantee` concept bodies; `site/.gitignore` for generated card; ran `sync:bridges`, `sync:field-agendas`, `sync:concepts`; site build OK.

## Decisions
- MB11 gets its own bridge card (not only the ch03 dynamical-guarantee concept); dynamical-guarantee now links to MB11 for the safety-case closure step.
- MB10 was already in `metadata/bridges.yml`; missing appearance was MB11 + generated-card sync, not a absent MB10 roster entry.

## Open / next
- Optional: wire `graphs/mb-bridge-dependencies` into Field hub if readers should see it on-site.
- Regenerate `reference/field-agendas/field-agenda-index.md` if matrix prose should mention MB11 card slug (JSON already updated).

## Commit
(session commit on main)
