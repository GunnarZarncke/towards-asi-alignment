# 2026-09-22 — Project consistency review

## Trigger
Review the whole project and the plan; assess how well it meets stated and implied expectations and whether expectations or implementation should be adapted to reach a consistent state quickly. Write the result as a report in `drafts/`. Old conversation logs and attic folders excluded.

## Done
- Six read-only area reviews (manuscript, Lean, experiments/backtests, site/demos, predictions+papers+funding, plans/metadata/docs) plus direct checks: `make check` (13/13 pass), `lake build` (green, sorry-free, 40-theorem ledger no drift), site build (1,113 pages), demo build, git cadence, naming and link greps.
- Report written: [`drafts/project/consistency-review-2026-09-22.md`](../project/consistency-review-2026-09-22.md).
- No manuscript, plan, or metadata files edited.

## Decisions
- None taken; the report recommends a consolidation program (Batch A expectation resets, Batch B hygiene, Batch C content correctness) and a do-not-do list.

## Open / next
- Highest-severity content issue: `ch46` collapse from the 2026-06-30 renumber still present in `metadata/notation.md`, `assumptions-ledger.md`, `uncertainty-ledger.md`, `REVIEWING_FOR_AGENTS.md`, `llms.txt`, and the June `review/` files.
- ~135 broken relative links in `drafts/plans/` after the 2026-09-19 restructure; "Witness" rename debt in plans, `RELEASE_NOTES.md`, `experiments/README.md`, `CONTRIBUTING.md`.
- Recommended: run Batch A + B (one to two sessions) before the next content lane.

## Key paths
- `drafts/project/consistency-review-2026-09-22.md`
- `metadata/TODO.md`, `drafts/plans/README.md`, `review/strategic-advice-2026-06-28.md`

## Commits
- none
