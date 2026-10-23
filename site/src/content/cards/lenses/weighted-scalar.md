---
title: "Weighted scalar"
type: "lens"
status: "framework"
summary: "A fixed-weight collapse of a criteria vector. Finite weights cannot represent a hard floor."
related:
  - "lenses/criteria-vector"
  - "lenses/non-compensatory-constraint"
  - "lenses/lenses-and-frameworks"
  - "field-agendas/openai-lab"
  - "field-agendas/anthropic-lab"
external:
  - label: "LessWrong tag: Goodhart's Law"
    url: "https://www.lesswrong.com/w/goodhart-s-law"
---

**Role.** Target. Graph node `weighted_scalar`.

> If a violation is non-compensatory, a sufficiently large but finite reward elsewhere must not purchase it.
>
> — Frames draft §4.2

Lean’s `no_finite_weights_represent_floor`: for every strictly positive integer weighting there is a menu where every scalar-optimal choice violates the floor. The real-valued version is expected to follow by the same argument but is not yet proven. Pulled back along the floor-coordinate maps, it gives the deontic– and AU-floor–scalar red edges for every such weighting (`deontic_no_finite_weights`, `nonobs_no_finite_weights`).
