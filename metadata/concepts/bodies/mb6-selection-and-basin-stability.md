---
leanNodes:
  - nodeId: MB6a_percolation_evidence_to_basin_stability
    kind: bridge
    summary: Cooperation/percolation evidence is assumed to warrant the abstract basin-stability predicate.
    module: AlignmentProofSpine/Core.lean
  - nodeId: MB6b_basin_stability_to_correction_integrity
    kind: bridge
    summary: A stable socio-technical basin is assumed to support correction integrity rather than select against it.
    module: AlignmentProofSpine/Core.lean
  - nodeId: sharedChokepoint_steerable_blocks_both_routes
    kind: counterexample
    summary: If MB6b and MB8 route through the same self-report/cooperation-signal instrument, their disjunction buys no independent failure tolerance — a shared, steerable chokepoint blocks both routes at once.
    module: AlignmentProofSpine/Chokepoint.lean
evidenceNotes:
  - source: embedded-simulation MB coverage
    scenario: selection_basin / basin_lock_in
    finding: open
    summary: Both scenarios exist in the embedded audit's MB coverage table, but there is no dedicated negative-result entry yet distinguishing a genuinely correction-supporting basin from a stably bad one. Treat the disjunctive MB6b/MB8 route as one point of failure until independence is demonstrated.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/embedded-simulation/README.md
  - source: lab-simulation architect plan (D3)
    finding: open
    summary: Extended ecology selection (workstream D3) is planned; partial drift coverage may arrive via D2 spec/model upgrades first. No pre-registered basin battery yet on the lab substrate.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/PLAN.md
related:
  - attractor-control
  - bridge-assumptions
  - mb8-cev-process-convergence
external:
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
---

Most alignment agendas hold a single system fixed and ask about its weights. This bridge does the opposite: it makes selection by deployment leverage (which systems institutions copy, fund, and deploy) and basin stability load-bearing, on the claim that outcomes depend on which systems institutions select, not on any one system's internals alone.

MB6 is really two linked bridges. MB6a says percolation-style cooperation evidence is enough to call a basin stable. MB6b says a stable basin actually supports correction integrity, rather than merely being stable. That second step is the sharper bet: value lock-in is a direct counterexample to MB6b, because a stable basin can be a stably bad one.

The book's own formal spine flags a further weakness: if this bridge's evidence and MB8's legitimacy-theater check both route through the same self-report or cooperation signal, treating them as two independent lines of defense is a mistake — a single steerable chokepoint can block both at once. No experiment has yet shown that the two instruments are independent in practice.
