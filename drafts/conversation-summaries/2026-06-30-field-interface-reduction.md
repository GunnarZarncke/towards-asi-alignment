# 2026-06-30 — Field interface reduction

## Trigger
User asked to improve the field-special-case formalization for the suggested agendas except Debate and ELK, and after review to reduce "baking in" the desired relationship.

## Done
- Added finite native/interface models:
  - `Field.Finite.MDP`: named `shutdownAction` / `continueAction`, `CorrectionPrefersShutdown`, and `shutdown_optimal_if_correction_prefers_shutdown`.
  - `Field.Finite.Reachability`: predicate-level `ReachabilityInterface`, `AuxiliaryReachabilityPreserved`, `CorrectionReachabilityPreservedByInterface`, `CorrectionOptionsTrackedByAuxiliary`, and `auxiliary_reachability_preserves_correction_options`.
  - `Field.Finite.Weights`: `QuantileEligibilitySound` and `quantile_safe_transfers_soundness`.
  - `Correction`: policy-factorized safe-interruptibility interface (`InterruptInvariantPolicy`, `CorrectionMediatedInterruptPolicy`, `InterruptBitIrrelevantToCorrectionState`, `correction_mediated_policy_interrupt_invariant`).
  - `Field.CIRL`: finite `ScalarAssistanceGame` / `BundleAssistanceGame` and `scalar_assistance_game_is_bundle_game_k1`.
- Exposed less-baked field theorem names:
  - `shutdown_optimal_under_correction_preference`
  - `interrupt_policy_invariant_from_correction_interface`
  - `auxiliary_reachability_preserves_correction_reachability`
  - `quantile_soundness_preserves_trajectory_cci`
  - `scalar_assistance_game_is_bundle_game_k1`
- Updated field result ledgers, Appendix I, `formal/README.md`, and graph labels to prioritize these interface-condition theorems over equality-style shortcuts.
- Marked Debate and ELK as later in `metadata/TODO.md` and Appendix I, noting they need native debate-game and ELK reporter/training models rather than capacity-identification shortcuts.

## Decisions
- Kept older `κ_C` projection lemmas for compatibility, but no longer use them as the headline book-facing results for the strengthened agendas.
- For AUP/RR, the stronger theorem now says auxiliary reachability preserves correction reachability only if correction-relevant options are explicitly included in the auxiliary basis.
- For quantilization, the stronger theorem now says quantile safety transfers to trajectory CCI only under an independently supplied eligibility-soundness condition.
- Debate and ELK were not strengthened in this pass because doing so honestly requires native protocol/reporter semantics.

## Reviewer posture
- Defensible claim: Lean now proves shared finite-fragment relationships where field-agenda targets are special cases, projections, or consequences of book predicates under explicit interface conditions; non-converse separations remain visible.
- Avoid claiming: Lean proves the book subsumes the full CIRL, AUP/RR, quantilization, shutdown, interruptibility, Debate, or ELK theorems under their published assumptions.
- Likely accepted by critics: CIRL `k=1` bundle/assistance-game embedding, interruptibility policy-factorization interface, AUP/RR auxiliary-basis interface, and quantilization soundness interface are clearer and less circular than the earlier equality shortcuts.
- Likely critic objections: models remain finite/shared-domain fragments; interface conditions are still substantial assumptions; CIRL lacks full belief/deference optimality; AUP/RR lacks full attainable-utility machinery; quantilization lacks probabilistic base-distribution/risk-bound machinery; Debate and ELK remain deferred.

## Open / next
- Native Debate model: two-prover game, transcript, judge, truth predicate, completeness/soundness, then interface to judge correction reliability.
- Native ELK model: latent state, model knowledge, reporter output, training objective, truthful-vs-simulator distinction, then interface to correction uptake.
- Optional cleanup: typed field-result certificates replacing the trivial `all_crosswalk_subsumptions_proved` inventory.

## Key paths
- `formal/AlignmentProofSpine/Field/Finite/MDP.lean`
- `formal/AlignmentProofSpine/Field/Finite/Reachability.lean`
- `formal/AlignmentProofSpine/Field/Finite/Weights.lean`
- `formal/AlignmentProofSpine/Field/CIRL.lean`
- `formal/AlignmentProofSpine/Field/Shutdown.lean`
- `formal/AlignmentProofSpine/Field/Interruptibility.lean`
- `formal/AlignmentProofSpine/Field/Impact.lean`
- `formal/AlignmentProofSpine/Field/Quantilization.lean`
- `formal/AlignmentProofSpine/Correction.lean`
- `appendices/appI-lean-proof-spine.tex`
- `metadata/TODO.md`

## Commits
- None.

## Verification
- `lake -d formal build` passed.
- `./scripts/render_lean_graphs.sh && lake -d formal build && make check` passed.
- IDE diagnostics reported no linter errors for edited Lean / Appendix / README / TODO files.
