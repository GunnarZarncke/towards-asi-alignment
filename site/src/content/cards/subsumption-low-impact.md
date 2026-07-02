---
title: "Subsumption — AUP / Relative Reachability (Low Impact)"
type: "concept"
status: "established"
summary: "Attainable Utility Preservation and relative reachability penalize side effects by preserving auxiliary options or baseline reachability. Trajectory correction integrity (CCI) can imply calibrated low-impact bounds when interfaces align — but option preservation and reachability are strictly weaker than preserving human correction capacity."
decision: "Before adopting a low-impact or AUP penalty as a safety proxy, ask whether the auxiliary basis tracks correction-relevant options and whether reachability preservation implies usable correction bandwidth."
bookChapters: ["ch27", "ch45", "ch46"]
formulas:
  - id: "appi:eq:field-impact-separation"
    latex: "\\text{preserve attainable utility or reachability}\\ \\not\\Rightarrow\\ \\text{preserve human correction capacity}"
    explanation: "Field separation named in the manuscript: low-impact agendas optimize a different object than correction-channel integrity."
    chapterId: "ch27"
  - id: "appi:eq:aup-interface"
    latex: "\\mathrm{AuxReachPres}(m)\\ \\wedge\\ \\mathrm{CorrOptsTracked}(m)\\ \\Rightarrow\\ \\mathrm{CorrReachPres}(m)"
    explanation: "Conditional forward link: when auxiliary reachability tracks correction-relevant options, interface preservation lifts to correction reachability."
    chapterId: "ch27"
  - id: "appi:eq:low-impact-projection"
    latex: "\\mathrm{TrajectoryCCIPreserved}\\ \\Rightarrow\\ \\mathrm{LowImpactPenaltyBound}"
    explanation: "Trajectory CCI preservation projects to a calibrated low-impact penalty bound under explicit interface definitions."
    chapterId: "ch46"
leanNodes:
  - nodeId: "trajectory_cci_subsumption_impact"
    kind: "proof"
    summary: "Trajectory CCI preservation implies low-impact penalty bound (forward projection)."
    module: "AlignmentProofSpine/Field/Impact.lean"
  - nodeId: "low_impact_is_trajectory_cci_projection"
    kind: "proof"
    summary: "Low impact as projection of trajectory correction integrity."
    module: "AlignmentProofSpine/Field/Impact.lean"
  - nodeId: "low_impact_separated_from_trajectory"
    kind: "counterexample"
    summary: "Separation: low-impact penalty can hold while trajectory CCI fails."
    module: "AlignmentProofSpine/Field/Impact.lean"
  - nodeId: "reachability_not_correction_capacity"
    kind: "counterexample"
    summary: "Graph reachability preservation separates from correction-capacity preservation."
    module: "AlignmentProofSpine/Field/Impact.lean"
  - nodeId: "Turner2019_AUP_penalty_imported"
    kind: "definition"
    summary: "Imported handle: AUP penalizes reductions in attainable auxiliary utility."
    module: "AlignmentProofSpine/Field/Imported.lean"
  - nodeId: "Krakovna2018_relative_reachability_imported"
    kind: "definition"
    summary: "Imported handle: relative reachability penalizes loss of reachability to baseline states."
    module: "AlignmentProofSpine/Field/Imported.lean"
citeKeys: ["turner2019aup", "krakovna2018relative"]
related: []
---

AUP and relative reachability are influential side-effect controls: preserve auxiliary goals or stay close to a baseline trajectory. Chapter 27 states the book's separation plainly — preserving those objects does not entail preserving human correction capacity.

Lean proves conditional forward links when the auxiliary basis tracks correction-relevant options, and multiple non-converse separations on finite graphs and trajectory steps. Low-impact metrics can be useful stress tests inside a deployment gate, but they are not substitutes for correction-channel integrity certificates.
