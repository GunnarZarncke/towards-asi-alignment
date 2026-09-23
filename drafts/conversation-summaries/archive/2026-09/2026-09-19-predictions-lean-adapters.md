# 2026-09-19 — Predictions Lean adapters

## Trigger
User asked to implement the Lean (v1) part of the prediction-interface plan, not Lean 2.0.

## Done
- `formal/AlignmentProofSpine/Evidence.lean`: per-system certificate tokens, eval-soundness adapters (not numbered `MB*`), `HiddenRouteBound`, `CoherentCertificateBundle`, derived `Certified`, `SafeIn` stub + toy that scoped safety ≠ unrestricted `Safe`.
- `Certified` removed as a Core axiom; `SatisfiesInvariants` is `LayeredAlignedDef`.
- `CoherentCertificateBundle.toDirectLayerEvidence` / `toLayeredAligned` in `Certification.lean`.
- `positive_measured_path_eval_soundness` (not a converse of `MB4a`).
- `lake build` + axiom-budget update; SpineModel check passed.
- App G reading note; spine / prediction-interface / TODO / HANDOFF.

## Decisions
- Unary predicates stay; no `AlignmentContext`. Same-`A` indexing is the v1 composition check.
- Adapters are axioms, not new bridges. No market YES constructors. No 80/90/15% in `RiskGap`.
- `MB11` still targets unary `Safe`. `SafeIn` is a stub only.
- Basin inputs (`CorrectionGradientEvidenceSys`, shock, frozen floor) remain extra hypotheses on `toLayeredAligned`; they are not pretended to sit inside the four measurement families.

## Open / next
1. Q1/Q2/Q6 listing (instrument vs criteria-only; titles; platform).
2. Lean 2.0: MB6 `Environment`, then MB11 `SafeIn` (author).
3. Empirical discharge of the new eval-soundness axioms still after Witness H1 / CIRIS.
4. Residuals: recertification (§6/§15), eval-list vs layers (§13).

## Key paths
- [`formal/AlignmentProofSpine/Evidence.lean`](../../formal/AlignmentProofSpine/Evidence.lean)
- [`drafts/plans/predictions/prediction-interface.md`](../plans/predictions/prediction-interface.md)
- [`drafts/plans/spine/spine.md`](../plans/spine/spine.md)

## Commits
- `6c46f4bb` — v1 `Evidence.lean` certificate layer; derived `Certified` / `SatisfiesInvariants`.
