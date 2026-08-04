---
formulas:
  - id: appi:eq:embed-boundary-forward
    latex: \text{PositiveBoundaryMargin}(A)\ \Rightarrow\ \varepsilon\text{-BoundaryCertificate}(A)
    explanation: 'Forward projection: positive boundary margin arithmetic yields an ε-boundary certificate on the finite interface.'
    chapterId: ch07
  - id: appi:eq:embed-bypass-separation
    latex: \text{PathLegitimate}(\text{named})\ \wedge\ \neg\text{CorrectionIntegrity}(\text{composite})
    explanation: 'Non-converse separation: green named-path audit can coexist with composite bypass of real correction.'
    chapterId: ch29
  - id: appi:eq:embed-mb1-defeater
    latex: \text{EstimatorNonstationary}\ \Rightarrow\ \neg\text{MB1_estimator_soundness}
    explanation: 'Bridge defeater: nonstationary shift breaks estimator soundness without refuting margin arithmetic locally.'
    chapterId: ch07
leanNodes:
  - nodeId: positive_margin_implies_epsilon_boundary
    kind: proof
    summary: Positive boundary margin implies ε-boundary certificate (margin arithmetic).
    module: AlignmentProofSpine/Boundaries.lean
  - nodeId: green_named_path_with_bypass_not_integrity
    kind: counterexample
    summary: 'Finite separation: path legitimate on named unit while composite bypass breaks correction integrity.'
    module: AlignmentProofSpine/Field/Finite/CompositePathBypass.lean
  - nodeId: MB1_defeater_toy_nonstationary_shift
    kind: counterexample
    summary: 'MB1 toy defeater: nonstationary shift refutes estimator soundness.'
    module: AlignmentProofSpine/Defeaters.lean
  - nodeId: MB1_estimator_soundness
    kind: bridge
    summary: 'Bridge MB1: measured boundary estimator is sound enough for certification.'
    module: AlignmentProofSpine/Core.lean
citeKeys:
  - demski2019embedded
---

Embedded agency denies that the real optimizer sits in a clean Cartesian box separate from the environment. This project treats the agent–environment cut as a measurable object: ε-boundary discovery asks whether the certified unit is the real control locus.

Lean proves margin arithmetic that yields ε-boundary certificates on the finite interface, and finite separations that break the converse: a green named measured path can coexist with composite bypass (`green_named_path_with_bypass_not_integrity`), and MB1 estimator-soundness has explicit nonstationary defeaters. MB1 forward discharge remains a bridge assumption, not a rederived theorem from boundary metrics alone.

*What embedded-agency work keeps that this crosswalk does not replace:* the full Demski–Garrabrant embedded-agency problem map, causal discovery baselines, and training protocols for finding real controllers. Relocating ε-boundary as a projection does not solve boundary discovery in the wild.
