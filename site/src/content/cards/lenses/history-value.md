---
title: "History / trajectory value"
type: "lens"
status: "framework"
summary: "A preference or score on whole paths, not on a snapshot state."
related:
  - "static-target-trap"
  - "value-change-vs-corruption"
  - "lenses/lenses-and-frameworks"
  - "field-agendas/christiano-lineage"
  - "field-agendas/miri"
external:
  - label: "LessWrong tag: Decision theory"
    url: "https://www.lesswrong.com/w/decision-theory"
---

**Role.** Target. Graph node `hist`.

> A utility or preference over a history represents delayed and path-dependent value directly. A pathwise safety predicate is different.
>
> — What Does Alignment Secure? (draft), §4.1

A history-valued lens scores the sequence `(s₀, a₀, s₁, …)`. Two deployments can share an endpoint and still differ if manipulation, dissent removal, or withheld evidence is visible in the history.

Encoding a finite history into an augmented state is always available in principle. The cost is compactness, locality, observability, or stationarity — not a proof that the snapshot object was already enough.
