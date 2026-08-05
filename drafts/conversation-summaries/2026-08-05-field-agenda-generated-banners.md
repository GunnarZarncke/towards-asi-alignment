# 2026-08-05 — Field agenda generated banners

## Trigger
User asked why field agendas exist as both `.yml` and `.md`; agreed to keep checked-in generated outputs for now but mark them unmistakably as generated, with a deferred TODO for build-time-only generation once structure settles.

## Done
- Added `GENERATED FILE` HTML comment banners in `site/scripts/sync-field-agendas.mjs` (agenda cards after frontmatter; `field-agenda-index.md` line 1).
- Regenerated 28 agenda cards + `field-agenda-index.md` (`npm run sync:field-agendas`; `--check` clean).
- Documented edit-YAML-only rule in `reference/field-agendas/README.md` and `site/README.md`.
- Added deferred TODO in `metadata/TODO.md` for gitignoring generated artifacts later.

## Decisions
- **Keep committed generated outputs** for now (CI `--check`, same pattern as concept/bridge cards).
- **Defer build-time-only generation** until `reference/field-agendas/data/` schema churn is low.

## Open / next
- When field-agenda structure stabilizes: implement deferred TODO (stop committing generated `.md` / JSON / index; rely on sync in CI).

## Key paths
- `reference/field-agendas/data/agendas/*.yml` — edit surface
- `site/scripts/sync-field-agendas.mjs` — banner + codegen
- `site/src/content/cards/field-agendas/*.md` — generated (do not edit)

## Commits
- `19119d56` Mark field agenda generated outputs with visible banners.
