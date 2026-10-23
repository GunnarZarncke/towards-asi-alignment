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

> On its fixed graph with the stated reachability assumption, endpoint-only additive path value is the exact-potential special case.
>
> — Frames draft §4.1 (Hallgren process-alignment draft, unpublished)

If an edge score is a gradient of a state potential, every closed walk sums to zero. That is why state utility and cycle residue conflict on round trips: see the red edge in Lean (`stateCycleIncompat`).

Exactness is a representation fact about a particular reward, not a claim that endpoints were the intended moral object.
