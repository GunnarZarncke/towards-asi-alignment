# 2026-07-19 — Graded lab GL-79–85 on companion site

## Trigger
User: "reflect in site" after manuscript harvest; then end-of-session commit.

## Done
- Updated `metadata/experiments.yml` (headline findings GL-76/79/80/81/84/85, role, howToRead, MB coverage cells, plan link → PLAN_v4.md).
- Ran `npm run sync:experiments` (+ chapter-cards + search-index for local preview).
- Committed synced `site/src/data/experiments.json`.

## Decisions
- Site source of truth is `metadata/experiments.yml`; experiment cards and search index are gitignored generated artifacts.

## Open / next
- Deploy via normal site CI on push.

## Key paths
- `metadata/experiments.yml`
- `site/src/data/experiments.json`

## Commits
- `a9616e2` Sync graded-lab PLAN_v4 findings (GL-79–85) to companion site.
