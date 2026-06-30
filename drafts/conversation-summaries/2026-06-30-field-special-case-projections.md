# 2026-06-30 — Field special-case projections

## Trigger
User asked to try the CIRL-style object-level special-case treatment for the other field results where it may work.

## Done
- Added shared-domain projection predicates / theorem names in `formal/AlignmentProofSpine/Correction.lean`:
  - `InterruptCorruptionSuboptimal`
  - `correction_channel_projects_to_interrupt_safety`
  - `ShutdownAsCorrectionProjection`
  - `shutdown_is_one_bit_correction_projection`
  - `christiano_corrigibility_is_basin_plus_capacity`
  - `CalibratedLowImpactProjection`
  - `low_impact_is_calibrated_trajectory_cci_projection`
  - `ELKReadoutAsCorrectionProjection`
  - `elk_readout_is_correction_uptake_projection`
  - `DebateTruthAsJudgeCorrectionProjection`
  - `debate_truth_is_judge_correction_projection`
- Exposed book-facing field theorem names in agenda modules:
  - `interrupt_safety_is_correction_projection`
  - `shutdown_capacity_is_correction_projection`
  - `christian_corrigibility_is_correction_invariant`
  - `low_impact_is_trajectory_cci_projection`
  - `trajectory_cci_is_quantile_score_projection`
  - `debate_truth_is_correction_projection`
  - `elk_readout_is_correction_projection`
- Updated field result ledgers, Appendix I table rows, `formal/README.md`, and Lean proof graph labels to use the stronger projection/special-case names.
- Regenerated Lean proof graph PNGs.

## Decisions
- Kept older theorem names such as `interrupt_subsumption_ch24` and `elk_subsumption_readout` as compatibility wrappers.
- Did not claim full external theorem subsumption. The new results are shared finite/formula-domain projections or special cases, paired with existing non-converse separations.
- Quantilization remains limited: the new theorem shows the local score-projection fragment (`TrajectoryCCIPreserved` supplies quantile eligibility when score is next-step correction capacity), not the full probabilistic quantilizer theorem.

## Open / next
- Optional manuscript pass: add chapter-local `\leanspine{}` citations to the new projection theorem names in chapters 24, 25b, 26, 27, 39b, and the field crosswalk appendix prose if desired.
- Optional proof-spine cleanup: replace the trivial `all_crosswalk_subsumptions_proved` inventory with a typed certificate that records projection theorem + separation theorem + imported handle per agenda.

## Key paths
- `formal/AlignmentProofSpine/Correction.lean`
- `formal/AlignmentProofSpine/Field/*.lean`
- `appendices/appI-lean-proof-spine.tex`
- `formal/README.md`
- `context/lean_proof_graphs/03-correction-successors.dot`
- `context/lean_proof_graphs/05-field-subsumptions.dot`
- `context/lean_proof_dependency_graph.dot`

## Commits
- None.

## Verification
- `lake -d formal build` passed.
- `./scripts/render_lean_graphs.sh && lake -d formal build && make check` passed.
- IDE diagnostics reported no linter errors for edited Lean / Appendix I / README files.
