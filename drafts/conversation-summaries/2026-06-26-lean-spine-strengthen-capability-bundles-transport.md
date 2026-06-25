# 2026-06-26 — Lean spine strengthen (Capability, Bundles, transport, Successors, Boundaries)

## Trigger

User requested implementation of spine strengthening for Capability, finite bundle counterexamples, ch23 transport stack, successor monotonicity, and boundaries — explicitly skipping Correction (beyond existing) and Adversarial/Philosophy/Certification changes.

## Done

- **`Capability.lean`**: `Control` defined as `IctrlSys` (ch11); removed `Control_le_IctrlSys` axiom; added ch13 `CollectiveCompetence`, `CoordinationLoss`, bottleneck lemmas; strengthened `P32` κ threshold (requires `c > 0`).
- **`Core.lean`**: ch23 four-layer transport stack (`PreservesSemanticLabels` … `CorrectionTransportLayer`); `FullTransport` = correction layer; `BoundaryMarginCertificate` + ch07 leakage doc; removed abstract `Control` axiom.
- **`Bundles.lean`**: Replaced `Bool` toys with finite `PolicyProfile`, `ValueProfile`, `TradeoffProfile`, `FinTransportLayers` counterexamples for `P15`/`P17`/`P18`/`P22b`; transport implication lemmas for abstract systems.
- **`Successors.lean`**: `SuccessorSafe_risk_monotone` proved from witness + modular linking axioms `CCIPreserved_implies_monotone`, `ControlLocusPreserved_implies_control_antitone`.
- **`Boundaries.lean`**: Margin-certificate theorems tying ch07 ε-blankets to positive margin.

## Verification

```bash
cd formal && lake build  # success
```

`P15_same_policy_not_same_bundle_geometry` axiom footprint: `propext`, `Quot.sound` only.

## Open / not in scope (this session)

- Correction link capacities from concrete handle data (ch24–25).
- Adversarial / Philosophy finite-model upgrades.
- ~~Appendix I prose still describes old Boolean toy proofs~~ — updated 2026-06-26 (same session, follow-up).

## Key paths

- `formal/AlignmentProofSpine/Capability.lean`
- `formal/AlignmentProofSpine/Core.lean`
- `formal/AlignmentProofSpine/Bundles.lean`
- `formal/AlignmentProofSpine/Successors.lean`
- `formal/AlignmentProofSpine/Boundaries.lean`
- `appendices/appI-lean-proof-spine.tex` (definitions and proof sketches aligned to above)

## Commit

- Hash: (pending)
- Staged: Lean spine modules above + Appendix I + this log + INDEX row.
- **Not staged** (other working-tree edits): definition-deduplication chapter cross-refs, `context/Alignment Attractor.md`, `2026-06-26-definition-deduplication-pass.md`, LaTeX aux save-error files.

## Next

- Correction: ground `CorrectionLinkCapacities` from handle/observation data (ch24–25).
- Adversarial / Philosophy: replace remaining Boolean counterexample prose in Appendix I when those Lean modules are strengthened.
- Optional: sync `metadata/TODO.md` § Lean mapping gaps for completed items.
