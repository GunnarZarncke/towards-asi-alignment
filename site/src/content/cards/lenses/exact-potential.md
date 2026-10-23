---
title: "Exact potential summand"
type: "lens"
status: "framework"
summary: "The part of an additive route score that depends only on endpoints."
related:
  - "lenses/additive-route-value"
  - "lenses/state-utility"
  - "lenses/lenses-and-frameworks"
external:
  - label: "LessWrong tag: Utility functions"
    url: "https://www.lesswrong.com/w/utility-functions"
---

**Role.** Target. Graph node `exact`.

> If every state is reachable from a fixed start, path worth depends only on the final state exactly when r is an exact potential: each edge scores the utility of its target minus the utility of its source.
>
> — Frames relations note

If an edge score is a gradient of a state potential, every closed walk sums to zero. That is why state utility and cycle residue conflict on round trips: see the red edge in Lean (`stateCycleIncompat`).

Exactness is a representation fact about a particular reward, not a claim that endpoints were the intended moral object.
