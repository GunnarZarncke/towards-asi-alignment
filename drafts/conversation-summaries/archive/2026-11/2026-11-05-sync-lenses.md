# 2026-11-05 — sync-lenses hardening

kind: correction
uptake: local

## Trigger
Review `sync-lenses.mjs` for missing edges, typos, and errors; fix and commit at session end.

## Done
- housekeeping: Hardened `site/scripts/sync-lenses.mjs` — row validation, duplicate-slug check, stale card removal, `ENOENT`-only read handling, overview path from `OVERVIEW_ID`, pinned `repoBlobBase()` externals.
- content: Restored author overview summary/body in `renderOverview()` (typo fixes only); regenerated `site/src/content/cards/lenses/lenses-and-frameworks.md`.

## Decisions
- Overview prose stays in `sync-lenses.mjs` (not the hand-edited generated card); rejected swapping in the correction-centered blurb that had overwritten the author draft.

## Open / next
- None for this lane.

## Key paths
- `site/scripts/sync-lenses.mjs`
- `site/scripts/lib/lenses-data.mjs` (frame card source)
- `site/scripts/sync-lens-graph.mjs` (graph edges / Lean links)

## Verification
- `cd site && node scripts/sync-lenses.mjs --check` → `sync-lenses: check mode, all up to date.`

## Commits
- `67235efc46` Harden sync-lenses and restore overview copy in the generator.
