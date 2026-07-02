---
title: "Subsumption — CIRL / Scalar Reward Inference"
type: "concept"
status: "established"
summary: "Cooperative inverse reinforcement learning treats the inferred object as a scalar reward. On the book's shared finite domain, that is exactly the k=1 bundle case; full bundle transport implies cooperative readability, but scalar inference does not determine bundle geometry."
decision: "When evaluating CIRL-style reward learning, ask whether the target is a single reward coordinate or bundle structure, bearer maps, and the correction process that produces later evidence."
bookChapters: ["ch16", "ch18", "ch46"]
formulas:
  - id: "appi:eq:cirl-scalar-bundle"
    latex: "\\text{ScalarCIRL}(p,r) \\iff \\text{BundleInf}(p,\\,\\bar r),\\quad \\bar r(a)=r\\ \\text{for all actions }a"
    explanation: "Scalar cooperative inference embeds as one-bundle-coordinate bundle inference: the scalar reward r is lifted to a constant bundle coordinate."
    chapterId: "ch16"
  - id: "appi:eq:cirl-transport-forward"
    latex: "\\text{FullTransport}(A,B)\\ \\Rightarrow\\ \\text{CooperativeRewardInference}(A,B)"
    explanation: "Forward subsumption: preserving full bundle/bearer/correction transport implies the weaker CIRL-readable semantics layer."
    chapterId: "ch46"
  - id: "appi:eq:cirl-separation"
    latex: "\\text{CooperativeRewardInference}(p,r)\\ \\wedge\\ \\neg\\text{ValueBundleGeometryPreserved}(p,p')"
    explanation: "Non-converse separation: the same scalar marginal and policy can hide different bundle geometry — scalar inference is strictly weaker than geometry preservation."
    chapterId: "ch46"
leanNodes:
  - nodeId: "cirl_subsumption_forward"
    kind: "proof"
    summary: "Full finite transport implies cooperative reward inference (forward subsumption on FinTransportLayers)."
    module: "AlignmentProofSpine/Field/CIRL.lean"
  - nodeId: "cirl_scalar_is_bundle_inference"
    kind: "proof"
    summary: "ScalarCIRL on a PolicyProfile is equivalent to k=1 bundle inference."
    module: "AlignmentProofSpine/Field/CIRL.lean"
  - nodeId: "cirl_separation_profiles"
    kind: "counterexample"
    summary: "Finite witness: cooperative scalar inference without bundle geometry preservation."
    module: "AlignmentProofSpine/Field/CIRL.lean"
  - nodeId: "CIRL_assistance_game_deference_imported"
    kind: "definition"
    summary: "Imported handle: reward uncertainty can make deference/inquiry instrumentally valuable under symmetric flip costs."
    module: "AlignmentProofSpine/Field/Imported.lean"
citeKeys: ["hadfieldmenell2016"]
related: []
---

The field object is cooperative inverse reinforcement learning: a human knows a reward (or latent type); the robot infers it from observations and acts to maximize cooperative return. Scalar CIRL collapses the inferred object to one coordinate.

The book's stronger target is bundle inference — value directions, bearer maps, and transport that survive transformation. Lean proves the honest special case: scalar assistance games embed as bundle games with k=1, and full transport implies cooperative readability. It also proves the separation: cooperative scalar inference can hold while bundle geometry fails to preserve across profiles that share the same scalar marginal.
