---
formulas:
  - id: appi:eq:ground-class-cert
    latex: \text{ClassCertificate}(S)\ \equiv\ \forall \mu\in S.\ \text{InRepresentedClass}(\mu)
    explanation: 'Field object: every environment in plausible set S is marked checked relative to the represented class.'
    chapterId: ch43
  - id: appi:eq:ground-drift-separation
    latex: \text{ClassCertificate}(S)\ \wedge\ \text{RobustUnderAmbiguity}(\pi,S)\ \wedge\ \neg\text{SafeIn}(\mu_{\text{true}},\pi)
    explanation: 'Non-converse separation: class-green plus in-class robustness while true environment is off-class and unsafe.'
    chapterId: ch43
  - id: appi:eq:ground-mb9-bridge
    latex: \text{GroundingCertificate}\ \Rightarrow\ \text{GroundingViable}
    explanation: 'Forward bridge packaging: MB9 grounding certificate soundness (bridge assumption).'
    chapterId: ch03
leanNodes:
  - nodeId: class_certificate_not_deployment_safety
    kind: counterexample
    summary: 'Finite separation: class certificate and in-class robustness do not imply safety in off-class true environment.'
    module: AlignmentProofSpine/Field/Finite/Nonrealizability.lean
  - nodeId: epistemic_coverage_finite_shape_not_deployment_safety
    kind: counterexample
    summary: 'Interface re-export of nonrealizability separation for epistemic coverage packages.'
    module: AlignmentProofSpine/FieldInterfaces.lean
  - nodeId: MB9_grounding_certificate_soundness
    kind: bridge
    summary: 'Bridge MB9: grounding certificate supports grounding viability when assumptions hold.'
    module: AlignmentProofSpine/Core.lean
citeKeys:
  - dalrymple2024gsai
---

Grounding certificates and conservative-abstraction agendas ask monitors to stay tied to value-relevant state as ontologies shift. The book separates class-level coverage from deployment-level safety: a monitor can be green on the certified class while the true environment drifts off-class.

Lean proves `class_certificate_not_deployment_safety` on a finite toy: narrow class certificate plus in-class robustness can hold while the true environment is nonrealizable under the represented class and unsafe for the deployed policy. MB9 forward discharge remains a bridge; the separation is load-bearing for claim calibration.

*What grounding-certificate work keeps that this crosswalk does not replace:* proof-carrying code pipelines, conservative extension lemmas, and engineering protocols for ontology updates. Relocating drift as a separation does not automatically produce drift detectors.
