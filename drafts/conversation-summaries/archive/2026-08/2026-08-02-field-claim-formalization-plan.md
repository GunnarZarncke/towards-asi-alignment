# 2026-08-02 — Field-claim formalization plan

## Trigger
Review every “Missing-bridge candidate” in the field-agenda index, sketch formal models, assess the existing Lean spine, and propose a plan without editing Lean.

## Done
- Added `drafts/field-claim-formalization-and-bridge-review-plan.md` with formal objects, predicates, theorem/counterexample shapes, bridge assessments, decision gates, and a phased future implementation plan.
- Reviewed `formal/README.md`, `Core.lean`, `Certification.lean`, `Correction.lean`, `Defeaters.lean`, `Chokepoint.lean`, `Forgeability.lean`, `SpineModel.lean`, and `Field/Finite/LobTiling.lean`.
- Recorded formal-hygiene gaps: the `EstimatorNonstationary` defeater-table name has no matching predicate; `Defeaters.lean` omits `MB4a`, `MB10`, and `MB11`; App B still needs the deferred bridge inventory sync.
- Updated the existing model-class misspecification TODO with the plan and current recommendation.

## Decisions
- Do not add `MB12` now.
- Treat model-class misspecification as a formalization gap near `MB1`/`MB9`, not as already discharged by them.
- Reject unconditional regret-to-safety transfer; regret needs loss-to-harm, coverage, safe-exploration/tail, and safety-case interface premises.
- Split logical uncertainty from reflection. The existing Löb/tiling module is an adequate narrow reflection obstruction; logical induction remains field-local/exclude-by-reference unless the book consumes it.
- Keep `MB11`, `MB4a`, and `MB8`; clarify that `MB4a` is a necessary condition/falsifier, not a positive green-path-to-integrity rule, and that `MB8` is an opaque legacy route.

## Open / next
- Phase 0: normalize the field-index claims and queue the separately authorized App B `MB4a`/`MB11` sync.
- First future Lean pass, if authorized: repair defeater vocabulary and build finite nonrealizability, regret-safety, and composite green-path counterexamples before changing core bridges.
- Decide whether regret evidence supplies an existing layer, a new typed safety-case leaf, or no book-consumed result.

## Key paths
- `drafts/field-claim-formalization-and-bridge-review-plan.md`
- `reference/field-agendas/field-agenda-index.md`
- `formal/README.md`
- `formal/AlignmentProofSpine/Defeaters.lean`
- `formal/AlignmentProofSpine/Certification.lean`
- `metadata/TODO.md`

## Commits
- None.
