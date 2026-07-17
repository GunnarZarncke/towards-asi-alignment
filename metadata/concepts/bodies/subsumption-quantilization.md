---
formulas:
  - id: appi:eq:quant-soundness
    latex: \mathrm{QuantSound}(\theta,\mathcal P)\ \wedge\ \mathrm{QuantSafeLocal}(\theta,x)\ \Rightarrow\ \mathcal P(\mathrm{pt}(x))
    explanation: 'Forward projection: quantile eligibility soundness transfers to the sampled point under the quantilizer setup.'
    chapterId: ch27
  - id: appi:eq:quant-separation
    latex: \mathrm{QuantileSafeLocalAction}\ \wedge\ \neg\mathrm{TrajectoryCCIPreserved}
    explanation: 'Non-converse separation: local quantile-safe choices without trajectory CCI preservation.'
    chapterId: ch27
leanNodes:
  - nodeId: quantile_soundness_preserves_trajectory_cci
    kind: proof
    summary: Quantile soundness links to trajectory CCI under weighted witnesses.
    module: AlignmentProofSpine/Field/Quantilization.lean
  - nodeId: quantilizer_distribution_soundness_transfers
    kind: proof
    summary: Distribution-level quantilizer soundness transfers to sampled actions.
    module: AlignmentProofSpine/Field/Quantilization.lean
  - nodeId: quantile_separated_from_trajectory
    kind: counterexample
    summary: 'Separation: local quantile safety without trajectory correction integrity.'
    module: AlignmentProofSpine/Field/Quantilization.lean
  - nodeId: Taylor2015_quantilizer_bound_imported
    kind: definition
    summary: 'Imported handle: sampling from a high-performing quantile bounds optimizer-induced risk under probabilistic assumptions.'
    module: AlignmentProofSpine/Field/Imported.lean
citeKeys:
  - taylor2015quantilizers
---

Quantilization is an early answer to Goodhart under optimization: instead of taking the argmax, sample from the top quantile of a base policy. Taylor's bound limits optimizer-induced risk when eligibility is sound.

The book treats quantile safety as a local projection — useful when paired with trajectory-level correction certificates, insufficient alone. Lean proves soundness transfer lemmas and a finite separation showing quantile-safe local actions can coexist with failed trajectory CCI. Chapter 27 groups quantilization with other tempting weaker invariants that fail the correction-channel stress test.

*What quantilization keeps that this crosswalk does not replace:* a concrete, analyzable sampling mechanism with a quantifiable risk/performance tradeoff. The book offers no closed-form knob of comparable simplicity.
