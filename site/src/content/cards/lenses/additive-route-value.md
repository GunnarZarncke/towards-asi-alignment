---
title: "Additive route value"
type: "lens"
status: "framework"
summary: "An edge score summed along a walk: what was done, not only where you arrived."
related:
  - "subsumption-low-impact"
  - "lenses/exact-potential"
  - "lenses/cycle-residue"
  - "lenses/lenses-and-frameworks"
  - "field-agendas/chai-russell"
external:
  - label: "LessWrong tag: Reward functions"
    url: "https://www.lesswrong.com/w/reward-functions"
---

**Role.** Target. Graph node `route`.

> Discounted potential-based reward shaping, F(s,a,s′)=γΦ(s′)−Φ(s), preserves optimal policies under its stated assumptions [Ng, Harada, and Russell 1999]; that invariance is not identity of edge values, trajectory returns, or every bounded-rational learning process.
>
> — Frames draft §4.1

Route value is a function of transitions. It is the parent of the exact-potential summand (endpoint-only) and the cycle residue (round trips matter).

A matched-endpoint pair — learning versus rewiring a judge to the same later verdict — is invisible to a state score that stores only the verdict, and visible here if the two edges are labeled differently.
