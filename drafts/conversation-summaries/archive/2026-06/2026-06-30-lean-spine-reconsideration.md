# 2026-06-30 — Lean spine reconsideration

## Trigger
User asked to build the reconsidered Lean proof-spine plan in order, adding a new step for numeric leaves: `Control A ≤ CCI A + δ`, vector CCI support, and BIQ-derived slack via Markov-blanket / B-IQ derivations.

## Done
- `Certification.lean`:
  - added `DirectLayerEvidence`, `BridgeLayerInputs`, `BridgeDerivedLayerEvidence`, and `NumericRiskLeaf`;
  - added `certified_class_safety_from_bridge_record` consuming explicit `BridgeAssumptions`;
  - kept `certified_class_safety_from_spine_and_bridges` as the `standardBridges` corollary;
  - replaced abstract `Claim` / `Supported` / `LeafUnsupported` axioms with finite `Fin n` support certificate theorem `P40_unsupported_leaf_blocks_root`;
  - added numeric leaf constructors from vector CCI, BIQ slack, and Markov-blanket/B-IQ slack.
- `Capability.lean`:
  - added `MarkovBlanketBIQProfile`;
  - proved `MarkovBlanketBIQProfile.biq_le_capacity_sum`;
  - added `MarkovBlanketBIQDerivedCCISlack` and `control_le_cci_from_markov_blanket_biq`.
- `Successors.lean`:
  - added `SuccessorMeasurandLink` / `SuccessorMeasurandChain`;
  - proved risk propagation over explicit numeric successor links without changing the abstract `SuccessorSafeWitness` API.
- Field result ledgers:
  - added missing records for shutdown / interruptibility separations and Debate / ELK projection lemmas;
  - left Debate/ELK/Christiano imported handles in place.
- Docs:
  - updated `formal/README.md`, `appendices/appG-lean-proof-spine.tex`, and `metadata/TODO.md` for explicit bridge records, finite P40, PMF quantilizer, finite-horizon AUP, and Markov-blanket/B-IQ numeric leaves.

## Decisions
- Kept empirical validity in `MB*` bridges; the new bridge-record theorem only makes those dependencies explicit.
- Did not redefine opaque `CCIPreserved` / `ControlLocusPreserved`; instead added an explicit numeric successor-chain variant.
- Treated Markov-blanket/B-IQ profile equations as certificate inputs, not as measured estimator soundness.

## Open / next
- IntMass-to-PMF normalizer and PMF base-rate theorem matching Taylor more directly.
- AUP auxiliary-family penalty comparison over finite horizons.
- Native Debate and ELK protocol/reporter models.
- Replace remaining non-field Bool/toy counterexamples with finite structural witnesses.
- Commit this tranche if requested.

## Key paths
- `formal/AlignmentProofSpine/Certification.lean`
- `formal/AlignmentProofSpine/Capability.lean`
- `formal/AlignmentProofSpine/Successors.lean`
- `formal/AlignmentProofSpine/Field/Debate.lean`
- `formal/AlignmentProofSpine/Field/ELK.lean`
- `formal/AlignmentProofSpine/Field/Interruptibility.lean`
- `formal/AlignmentProofSpine/Field/Shutdown.lean`
- `formal/README.md`
- `appendices/appG-lean-proof-spine.tex`
- `metadata/TODO.md`

## Commits
- None.

## Verification
- `lake -d formal build` passed (1719 jobs).
- `rg "sorry|admit" formal/AlignmentProofSpine` found no placeholders (only the word "admit" in prose).
- IDE lints clean on edited Lean files.
- `make check` passed.
