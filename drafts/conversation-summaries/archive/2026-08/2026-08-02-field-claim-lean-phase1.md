# 2026-08-02 — Field-claim Lean Phase 1

## Trigger
Implement/prove the Phase 1 Lean parts of `drafts/field-claim-formalization-and-bridge-review-plan.md`. Do not edit the book or field-agenda matrix; do not add new `MB*` bridges.

## Done
- `formal/AlignmentProofSpine/Defeaters.lean`: named `EstimatorNonstationary`; misspec signals `ModelClassMisspecified` / `GrainOfTruthViolated`; `MeasuredPathCaptured` (MB4a), `SignatureForgeableAtCapability` (MB10), `SafetyCaseScopeExceeded` (MB11); finite toys for misspec / MB4a / MB10 / MB11; kept `MB1_defeater_toy_nonstationary_shift` signature for SpineModel compatibility and added `MB1_defeater_toy_nonstationary_signal`.
- `formal/AlignmentProofSpine/Field/Finite/Nonrealizability.lean`: realizability, off-class unsafe counterexample, ambiguity-set transfer, class-certificate ⇏ deployment safety.
- `formal/AlignmentProofSpine/Field/Finite/RegretSafety.lean`: zero-regret/wrong-loss and prefix-catastrophe counterexamples; `RegretSafetyCertificate` + conditional zero-harm transfer; regret-alone blocked export.
- `formal/AlignmentProofSpine/Field/Finite/CompositePathBypass.lean`: green named path + composite bypass ⇏ correction integrity; positive path certificate requires no-bypass (does not reverse MB4a).
- Wired via `Field.lean`; module map notes in `AlignmentProofSpine.lean` and `formal/README.md`.
- Verified: `lake build`, `python3 scripts/check_spine_model.py`, `python3 scripts/check_axiom_budget.py` (no axiom-budget drift).

## Decisions
- No new numbered bridge (`MB12`).
- Logical uncertainty module still deferred; reflection remains in `LobTiling.lean`.
- Book, App B, and field-agenda matrix left untouched (per request).

## Open / next
- Phase 2 interfaces: epistemic-coverage → `GroundingCertificate`; regret leaf vs layer consumer; positive path certificate premises (`MB1`/`MB7a` + no-bypass).
- Book decision on ambient MB1/MB9 vs defeater-only for misspec.
- App B / matrix sync when authorized.

## Key paths
- `formal/AlignmentProofSpine/Defeaters.lean`
- `formal/AlignmentProofSpine/Field/Finite/Nonrealizability.lean`
- `formal/AlignmentProofSpine/Field/Finite/RegretSafety.lean`
- `formal/AlignmentProofSpine/Field/Finite/CompositePathBypass.lean`
- `drafts/field-claim-formalization-and-bridge-review-plan.md`

## Commits
- None.
