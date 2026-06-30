# 2026-06-30 — Adversarial steerability review → TODOs

## Trigger
User pasted external reviewer feedback (high: correlated steerability failure across WWCTV surfaces and disjunctive-tolerance overclaim; medium: operationalization-by-deferral for composite indices). Asked to record and add TODOs — no manuscript edits this session.

## Done
- Recorded full feedback in `review/adversarial-steerability-correlated-failure-2026-06-30.md` (paths, suggested fixes, tracking links to 2026-06-28 composition session).
- `metadata/TODO.md`:
  - New **BIG REVIEW — Correlated steerability chokepoint** (ch07/ch19b/ch28/ch37/ch39b, appBridge-crosswalk, appH disjunctive-tolerance paragraph).
  - New **Measurand instantiation table** cross-cutting chore (composite → estimator → dataset/sim).
- `experiments/toy-simulation/TODO.md`: **Composite-index ↔ estimator matrix** item with target artifact `results/measurand_instantiation_matrix.{json,md}`.

## Decisions
- Stored as review record + TODOs only; no prose changes to appH/crosswalk/chapters until a dedicated reconciliation pass.
- Linked the new BIG REVIEW to existing uncertainty items U-03/U-05/U-14/U-16 rather than adding U-17 immediately — the chokepoint may consolidate those rather than duplicate them.

## Open / next
- Execute BIG REVIEW: either weaken appH §`sec:research-dependency-order` disjunctive-tolerance language or argue independent antecedents for MB6b vs MB8 under instrument capture.
- Build measurand instantiation table in toy-sim harness; wire into ch39b or appB when user lifts experiments→manuscript boundary.
- Optional: add U-17 "single adversarial measurand-steerability chokepoint" after claim-strength decision.

## Key paths
- `review/adversarial-steerability-correlated-failure-2026-06-30.md`
- `metadata/TODO.md` (Big reviews + Manuscript sections)
- `appendices/appH-research-program.tex` §`sec:research-dependency-order`
- `appendices/appBridge-crosswalk.tex` (takeaway)
- `drafts/conversation-summaries/2026-06-28-research-order-composition-argument.md`

## Commits
- (none)
