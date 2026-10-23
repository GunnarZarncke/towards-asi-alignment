---
title: "Quantilizer"
type: "lens"
status: "framework"
summary: "Sample from a high quantile of a base distribution instead of maximizing."
related:
  - "subsumption-quantilization"
  - "lenses/state-utility"
  - "lenses/lenses-and-frameworks"
  - "field-agendas/miri"
  - "field-agendas/google-deepmind-safety"
external:
  - label: "LessWrong tag: Quantilization"
    url: "https://www.lesswrong.com/w/quantilization"
---

**Role.** Target. Graph node `quant`.

> A quantilizer is a proposed AI design that aims to reduce the harms from Goodhart's law and specification gaming by selecting reasonably effective actions from a distribution of human-like actions, rather than maximizing over actions.
>
> — LessWrong tag: Quantilization

Taylor (2016): the guarantee is relative to the base, the quantile, and the use pattern. One-shot bounds do not imply safety under repeated deployment. The orange edge to state utility is a **limit**: quantile → maximum recovers ordinary maximization.
