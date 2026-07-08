---
title: "Field crosswalk — Christiano Corrigibility"
type: "concept"
status: "established"
summary: "Christiano corrigibility is a dynamical desideratum — operators stay informed and able to correct over time. Lean reads it as basin contraction toward a correction manifold plus a correction-capacity floor; local act preferences can satisfy the weak predicate while dynamical corrigibility fails."
decision: "Evaluate corrigibility proposals by whether they preserve correction capacity across capability growth and successor change, not whether the system accepts a single local shutdown or edit command."
bookChapters: ["ch28", "ch46"]
formulas:
  - id: "appi:eq:christiano-corrigibility"
    latex: "\\mathrm{DynamicalCorrigibilityInvariant}\\ \\Leftrightarrow\\ \\mathrm{CorrBasinContractive}\\ \\wedge\\ \\mathrm{UsableCorrectionInformation}(\\Delta_H,\\Delta_A,\\kappa_{\\min})"
    explanation: "Book-facing corrigibility as dynamical invariant: contractive return to a correction manifold plus usable correction bandwidth."
    chapterId: "ch28"
  - id: "appi:eq:contraction"
    latex: "d(A_{t+1},\\mathcal M_C)\\le \\alpha\\, d(A_t,\\mathcal M_C)+\\eta,\\qquad \\alpha<1"
    explanation: "Basin contraction: scaled distance to the correction manifold decreases under the certified step relation."
    chapterId: "ch28"
leanNodes:
  - nodeId: "christian_corrigibility_is_correction_invariant"
    kind: "proof"
    summary: "Dynamical corrigibility equivalent to basin contraction plus correction-capacity floor."
    module: "AlignmentProofSpine/Field/Corrigibility.lean"
  - nodeId: "christian_corrigibility_system"
    kind: "proof"
    summary: "Under MB4, CorrectionIntegrity implies the Christiano corrigibility system projection."
    module: "AlignmentProofSpine/Field/Corrigibility.lean"
  - nodeId: "act_based_separated_from_dynamical"
    kind: "counterexample"
    summary: "Separation: act-based preference satisfaction without dynamical corrigibility."
    module: "AlignmentProofSpine/Field/Corrigibility.lean"
  - nodeId: "Christiano2018_corrigibility_desideratum_imported"
    kind: "definition"
    summary: "Imported handle: corrigibility includes preserving operators' ability to correct over time (informal desideratum)."
    module: "AlignmentProofSpine/Field/Imported.lean"
citeKeys: ["christiano2018corrigibility"]
related: []
---

Christiano corrigibility is not a single preference over acts; it is a claim about trajectories under amplification — operators remain able to steer as capability grows. The book aligns this with correction-channel integrity extended in time: contraction toward a correction manifold and a floor on usable correction information.

Lean makes the equivalence explicit on the finite spine and separates act-based satisfaction from the dynamical invariant. That separation is why MB4 (correction legitimacy) matters: a system can perform corrigibility theater while eroding the judge's future ability to correct.

*What Christiano's corrigibility keeps that this crosswalk does not replace:* an act-level desideratum usable in today's training loops. The dynamical invariant is not yet operationalized for training.
