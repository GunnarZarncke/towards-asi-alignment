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
  - goodhart-as-selector
  - correction-channel-integrity
  - institutional-selection-gating
  - mb8-cev-process-convergence
  - bridge-assumptions
external:
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
---

Most model-centric agendas hold one system fixed and ask about its weights. The field still has a quieter structural risk — **Goodhart Selection** at deployment scale: which systems get copied, funded, and deployed can matter more than any one model's internals. Gradual-disempowerment and competition-dynamics arguments name versions of this. A bad equilibrium can be sticky. [Goodhart pressure](/cards/goodhart-as-selector/) can select for systems that look aligned under the metrics institutions use.

The book's precise bet is **MB6**, in two linked parts. **MB6a** assumes percolation-style cooperation evidence warrants [basin stability](/cards/attractor-control/). **MB6b** assumes a stable socio-technical basin supports [correction-channel integrity](/cards/correction-channel-integrity/) rather than selecting against it. The sharper claim is MB6b: value lock-in is a direct counterexample, because a stable basin can be a stably bad one. Outcomes depend on [institutional selection](/cards/institutional-selection-gating/), not weights alone.

**Where agendas agree:** Goodhart-as-selector; gradual disempowerment narrative; governance/pause on selection handles. **Where they diverge:** Demski "selection vs control" is a homograph (inside-optimizer search, not deployment ecology); CLR multipolar conflict is a different layer; model-centric agendas often leave this column empty.

The formal spine flags a further weakness: if this bridge's evidence and [MB8](/cards/mb8-cev-process-convergence/)'s legitimacy-theater check both route through the same self-report or cooperation signal, treating them as two independent defenses is a mistake. A single steerable chokepoint can block both at once. No experiment has yet shown the two instruments are independent in practice.
