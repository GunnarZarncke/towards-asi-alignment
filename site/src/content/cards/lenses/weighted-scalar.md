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
  - label: "LessWrong tag: Goodhart's law"
    url: "https://www.lesswrong.com/w/goodharts-law"
---

**Role.** Target. Graph node `weighted_scalar`.

> If a violation is non-compensatory, a sufficiently large but finite reward elsewhere must not purchase it.
>
> — Frames draft §4.2

Lean’s `no_finite_weights_represent_floor` carries the deontic–, AU-floor–, and CCI–scalar red edges: for every strictly positive finite weighting there is a menu where every scalar-optimal choice violates the floor.
