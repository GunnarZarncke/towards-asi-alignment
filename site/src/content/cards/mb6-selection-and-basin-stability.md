---
title: "MB6 — Selection and Basin Stability"
type: "bridge"
status: "bridge"
summary: "Percolation-style cooperation evidence is assumed to warrant basin stability (MB6a), and a stable socio-technical basin is assumed to support correction integrity rather than select against it (MB6b)."
decision: "Before trusting that an aligned equilibrium will persist, ask whether the basin is stable because it is good, or merely because it is stable — a bad basin can be just as sticky."
evidence: "Evidence would include tracking whether deployment-mass selection pressure preserves or erodes correction-channel integrity over time, independent of any single system's weights."
bookChapters: ["ch33", "ch34", "ch35", "ch36", "ch37", "ch38"]
leanNodes:
  - nodeId: "MB6a_percolation_evidence_to_basin_stability"
    kind: "bridge"
    summary: "Cooperation/percolation evidence is assumed to warrant the abstract basin-stability predicate."
    module: "AlignmentProofSpine/Core.lean"
  - nodeId: "MB6b_basin_stability_to_correction_integrity"
    kind: "bridge"
    summary: "A stable socio-technical basin is assumed to support correction integrity rather than select against it."
    module: "AlignmentProofSpine/Core.lean"
  - nodeId: "sharedChokepoint_steerable_blocks_both_routes"
    kind: "counterexample"
    summary: "If MB6b and MB8 route through the same self-report/cooperation-signal instrument, their disjunction buys no independent failure tolerance — a shared, steerable chokepoint blocks both routes at once."
    module: "AlignmentProofSpine/Chokepoint.lean"
evidenceNotes:
  - source: "embedded-simulation MB coverage"
    scenario: "selection_basin / basin_lock_in"
    finding: "open"
    summary: "Both scenarios exist in the embedded audit's MB coverage table, but there is no dedicated negative-result entry yet distinguishing a genuinely correction-supporting basin from a stably bad one. Treat the disjunctive MB6b/MB8 route as one point of failure until independence is demonstrated."
    resultsPath: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/embedded-simulation/README.md"
related: ["attractor-control", "bridge-assumptions", "mb8-cev-process-convergence"]
external:
  - label: "Bridges and the Field: A Crosswalk (appendix source)"
    url: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex"
---

Most alignment agendas hold a single system fixed and ask about its weights. This bridge does the opposite: it makes deployment-mass selection and basin stability load-bearing, on the claim that outcomes depend on which systems institutions select, not on any one system's internals alone.

MB6 is really two linked bridges. MB6a says percolation-style cooperation evidence is enough to call a basin stable. MB6b says a stable basin actually supports correction integrity, rather than merely being stable. That second step is the sharper bet: value lock-in is a direct counterexample to MB6b, because a stable basin can be a stably bad one.

The book's own formal spine flags a further weakness: if this bridge's evidence and MB8's legitimacy-theater check both route through the same self-report or cooperation signal, treating them as two independent lines of defense is a mistake — a single steerable chokepoint can block both at once. No experiment has yet shown that the two instruments are independent in practice.
