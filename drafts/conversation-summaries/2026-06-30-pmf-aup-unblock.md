# 2026-06-30 — PMF / AUP unblock

## Trigger
User gave more reasoning budget and asked why `PMF.ofFintype` / `quantilizerPMF` was difficult, whether it could be unblocked, and to try AUP after.

## Done
- Added `formal/AlignmentProofSpine/Field/Finite/PMF.lean`.
- Unblocked the PMF path by avoiding brittle `IntMass → ENNReal` normalization first:
  - `finitePMFOfFintype`
  - `quantilizerPMF`
  - `mem_support_quantilizerPMF_iff`
  - `quantilizerPMF_bad_apply_eq_zero_of_ineligible_bad`
  - `quantilizerPMF_soundness_transfers`
- Wired PMF quantilizer theorems through `Field/Quantilization.lean` and `Field.lean`.
- Added finite-horizon value iteration in `Field/Finite/MDP.lean`:
  - `finiteHorizonOptimalValue`
  - `finiteHorizonActionValue`
  - `finiteHorizonActionValue_le_optimal`
- Added finite-horizon AUP preservation in `Field/Finite/Probability.lean` and exported it from `Field/Impact.lean`:
  - `horizonAttainableUtility`
  - `AUPHorizonStep`
  - `AUPHorizonAttainableUtilityPreserved`
  - `aup_horizon_attainable_utility_preserves_previous_value`
- Verification:
  - `lake -d formal build` passes (1719 jobs).
  - `rg "sorry|admit" formal/AlignmentProofSpine/Field` has no matches.
  - IDE lints on edited Lean files are clean.

## Decisions
- The prior PMF attempt failed because it tried to normalize integer masses into `ℝ≥0∞` using `ENNReal` nat-cast plumbing before establishing the PMF-native theorem. The cleaner route is `PMF.filter` on eligible support; `PMF.ofFintype` is now represented for already-normalized finite mass functions.
- `IntMass` remains the arithmetic base-rate layer; PMF now supplies the source-shaped support/soundness layer.
- AUP extension is finite-horizon value-iteration preservation, not full Turner AUP penalty learning dynamics.

## Open / next
- Optional: derive an actual `IntMass → PMF` normalizer if useful, but it is no longer required for quantilizer support soundness.
- Strengthen AUP from horizon-value preservation to penalty comparisons over auxiliary reward families.
- Update Appendix I table / proof graph names if the new theorem handles should be visible in the manuscript.

## Key paths
- `formal/AlignmentProofSpine/Field/Finite/PMF.lean`
- `formal/AlignmentProofSpine/Field/Finite/MDP.lean`
- `formal/AlignmentProofSpine/Field/Finite/Probability.lean`
- `formal/AlignmentProofSpine/Field/Quantilization.lean`
- `formal/AlignmentProofSpine/Field/Impact.lean`

## Commits
- (none — user did not request commit)
