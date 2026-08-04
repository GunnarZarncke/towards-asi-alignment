# 2026-08-02 — Field-claim Lean Phase 2

## Trigger
Continue after Phase 1: implement Phase 2 interfaces from the field-claim plan to book predicates. No book/matrix edits; no new numbered `MB*` bridges.

## Done
- `formal/AlignmentProofSpine/FieldInterfaces.lean`:
  - `EpistemicCoveragePackage` / `EpistemicCoverageEvidence` → `GroundingViable` via existing `MB9`; finite non-safety specialization.
  - `SystemRegretSafetyEvidence` / `DeploymentHarmBounded` distinct from `RiskGap`; independence toys vs `Safe` and vs risk-gap leaf; decision: not a safety-case consumer.
  - `PositiveMeasuredPathCertificate` (legitimacy + coverage + no-bypass); `MB4a` unchanged; no positive→integrity axiom.
- `Chokepoint.lean`: `SystemTransition` carrier.
- `Forgeability.lean`: `conservedPropertyAuditChannel`, `ConservedPropertySignatureVerifiableUpTo`, interface axiom `ConservedPropertySignatureVerifiable_of_chokepoint`, chokepoint-gated true-harm corollary, `conservedPropertyGatedBridge`.
- Wired in root module + `formal/README.md`; plan/TODO/HANDOFF updated.
- Verified: `lake build`, `check_spine_model.py`, `check_axiom_budget.py` (no drift on curated headline set).

## Decisions
- Coverage interface is definitional packaging + `MB9`, not a new bridge.
- Regret evidence is an optional side channel, not a `NumericRiskLeaf` / `CertifiedSafetyCase` field.
- Positive path→integrity remains a Phase 3 decision (structure only for now).
- MB10 chokepoint reading uses an interface axiom, not `MB12`.

## Open / next
- Phase 3: ambient vs defeater-only vs new bridge for misspec; whether to add positive-path→`CorrectionIntegrity` as a numbered/threaded bridge.
- App B / matrix / Appendix G reader sync when authorized.
- Optional: add `true_harm_bound_of_successor_safe_step_via_chokepoint` to axiom-budget curated list if it should be mechanically guarded.

## Key paths
- `formal/AlignmentProofSpine/FieldInterfaces.lean`
- `formal/AlignmentProofSpine/Forgeability.lean`
- `formal/AlignmentProofSpine/Chokepoint.lean`
- `drafts/field-claim-formalization-and-bridge-review-plan.md`

## Commits
- None.
