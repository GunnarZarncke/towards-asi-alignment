# 2026-08-28 — Slim experiment coverage page

## Trigger
User: coverage page too crowded; experiment-line cards duplicate `/experiments/`; build order should be a separate card or fold; table headers should link to each line. Asked whether Witness belongs here.

## Done
- Removed the Experiment lines `CardSection` from `/experiments/coverage/`. Hub card now links to `/experiments/`.
- Folded the build-order table in `<details>`.
- Coverage-matrix column headers link to the matching experiment card.

## Decisions
- **Witness stays as a matrix column**, not as a second listing on this page. W-1–W-6 already sit on the MB rows they pay (fail/refuse vs authored sim). Do not add ET-1–4 as columns; they remain on the experiments hub. Sim-only rows can omit Witness (column is optional).

## Open / next
- None for this page. If the matrix is still too wide, next cut is shorter cell text, not another listing.

## Key paths
- `site/src/pages/experiments/coverage/index.astro`
- `site/src/components/ExperimentCoverageTable.astro`

## Commits
- `422deb1c` Slim experiment coverage hub so the matrix stays the focus.
