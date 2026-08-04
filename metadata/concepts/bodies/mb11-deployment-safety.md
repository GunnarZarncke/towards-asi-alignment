---
leanNodes:
  - nodeId: P30_certified_class_safety_derived
    kind: proof
    summary: 'Assembly, not derivation: packages certification, invariants, layered alignment, and RiskGap ≤ δ into a CertifiedSafetyCase record for MB11 to consume.'
    module: AlignmentProofSpine/Certification.lean
  - nodeId: MB11_safety_case_adequacy
    kind: bridge
    summary: A full certified-class safety case whose residual risk is within deployment tolerance is assumed to suffice for the abstract Safe predicate.
    module: AlignmentProofSpine/Certification.lean
  - nodeId: P30_safe_of_case
    kind: proof
    summary: Given a CertifiedSafetyCase and WithinDeploymentRiskTolerance, derives Safe via MB11 — the open research step is explicit, not implied by record shape.
    module: AlignmentProofSpine/Certification.lean
evidenceNotes:
  - source: formal spine
    finding: open
    summary: 'ToyDeploymentGate shows the shape of a frozen-validation battery gate; mapping that gate to WithinDeploymentRiskTolerance remains a governance judgment, not a computed probability.'
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/ToyDeploymentGate.lean
  - source: embedded-simulation worked instance
    finding: bound
    summary: Trace-computed CCI certificates on real fixture data discriminate honest vs capture-theater rows under pre-registered thresholds — the gate shape works; tolerance discharge is still MB11-shaped.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/WorkedInstance.lean
related:
  - dynamical-guarantee
  - deployment-gate
  - bridge-assumptions
  - evidence-and-uncertainty
  - what-not-claiming
  - mb9-grounding-certificate
  - mb10-successor-forgeability
external:
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
  - label: AlignmentProofSpine/Certification.lean
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/Certification.lean
---

In the field this is **Deployment Safety** and the safety-case gap: does audited layer evidence plus bounded measured risk actually warrant deploying? Safety-case methodology, eval-to-deployment warrant talk, and GSAI-style assurance closure all orbit this crux. **Where agendas agree:** packaging a safety case; naming deployment risk tolerance. **Where they diverge:** Kosoy regret on [MB2](/cards/mb2-bundle-identifiability/) is a value-learning cousin, not regret ⇒ Safe; packaging alone is not a bridge discharge; scope-exceeded is a defeater.

This project's precise bet is **MB11**: a [certified safety case](/cards/deployment-gate/) within deployment risk tolerance is assumed to warrant abstract Safe. Lean assembles the case record (`CertifiedSafetyCase`: certification, invariants, eight alignment layers, `RiskGap ≤ δ`) from spine evidence — that step is bookkeeping. The only labeled arrow to Safe is **MB11** plus a governance judgment `WithinDeploymentRiskTolerance` (a Prop-valued acceptance gate, not a computed failure probability).

This sits downstream of the other bridges and of the [dynamical guarantee](/cards/dynamical-guarantee/) framing in Chapter 3: safety is a trajectory claim, not a snapshot. MB11 names the residual bet that, once the antecedent is filled honestly, it is enough to act on. It is independently load-bearing — case plus tolerance do not imply Safe by logic alone.
