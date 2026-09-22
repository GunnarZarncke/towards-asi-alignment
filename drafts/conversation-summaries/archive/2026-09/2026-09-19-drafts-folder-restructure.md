# 2026-09-19 — Drafts folder restructure

## Trigger
User asked to go through `drafts/` and structure it into subfolders (e.g. predictions).

## Done
- Created topic subfolders: `predictions/`, `ontology/` (+ `reviews/`), `editorial/`, `project/`, `outreach/`, `benchmarks/`, `experiment-notes/`, `v2/`.
- Split `plans/` into lane subfolders: `backtest/`, `field/`, `spine/`, `construct/`, `predictions/`.
- Added [`drafts/README.md`](../README.md) and [`drafts/plans/README.md`](../plans/README.md).
- Updated live cross-refs (~71 files): `metadata/TODO.md`, `HANDOFF.md`, lane plans, LaTeX maintainer comments, experiments/backtest, site field-news URLs, active session logs.
- Moved `sandboxed-agent-mcp.md` into `plans/construct/`.

## Decisions
- Archived session logs keep old paths (historical record); active logs and canonical pointers updated.
- Left `slides/`, `quiz-*`, `adverse-process-generator/` at top level until they grow.

## Open / next
- Optional: fold `slides/` or `quiz-*` into `editorial/` or another category.
- User WIP in `drafts/predictions/bridge-predictions-Lean-improvements.md` — included in commit if staged.

## Key paths
- [`drafts/README.md`](../README.md)
- [`drafts/predictions/`](../predictions/)
- [`drafts/plans/README.md`](../plans/README.md)

## Commits
- (this session)
