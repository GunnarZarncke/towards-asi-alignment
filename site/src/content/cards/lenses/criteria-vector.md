---
title: "Criteria vector"
type: "lens"
status: "framework"
summary: "A Pareto / multi-objective vector of task, cost, or stakeholder coordinates — not a CCI certificate."
related:
  - "lenses/weighted-scalar"
  - "correction-channel-integrity"
  - "lenses/lenses-and-frameworks"
  - "field-agendas/mai-cip-institutional-alignment"
external:
  - label: "LessWrong tag: Goodhart's Law"
    url: "https://www.lesswrong.com/w/goodhart-s-law"
---

**Role.** Target. Graph node `criteria_vector`.

> A vector does not choose its scalarization, Pareto solution, bargaining rule, or lexicographic order.
>
> — Frames draft §4.2 (Roijers et al. 2013)

Whether a Pareto objective clashes with a correction floor depends on the coordinates. With the floor coordinate inside the vector, Pareto never excludes the floor but does not require it (`pareto_with_floor_coordinate_meets_floor`, `pareto_does_not_entail_floor`). On task coordinates only, it excludes the floor wherever every admissible option is task-dominated (`vectorCCIIncompat`). Do not call a stakeholder vector a CCI score.
