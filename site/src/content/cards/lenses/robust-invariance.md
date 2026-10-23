---
title: "Robust invariance"
type: "lens"
status: "framework"
summary: "The same geometry as viability, with ∀ disturbance in a named class."
related:
  - "lenses/existential-viability"
  - "lenses/correction-relation"
  - "certification-under-manipulation"
  - "lenses/lenses-and-frameworks"
  - "field-agendas/davidad-guaranteed-safe-ai-gsai"
external:
  - label: "LessWrong tag: Robustness"
    url: "https://www.lesswrong.com/w/distributional-shift"
---

**Role.** Guarantee. Graph node `robust`.

> Compare ∃π ∀t: X_t^π ∈ K with ∀d∈D ∀t: X_t^{π,d} ∈ K. They support different deployment conclusions.
>
> — Frames draft §3.2

Purple edge: strengthens ∃ control to ∀ disturbance. Red edge with correction: if correction inputs sit in the disturbance class and the target lies outside K, both cannot hold (`robustCorrectionIncompat`). Exempting corrections from the class is the boundary where both can hold.
