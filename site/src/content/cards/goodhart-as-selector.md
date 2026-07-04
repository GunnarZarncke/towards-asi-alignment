---
title: "Goodhart as Selector (Not Just Proxy Drift)"
type: "concept"
status: "plausible"
summary: "When a proxy becomes a selector, optimization shifts the population toward traits that raise the proxy without raising the target property — conditional expectations can reverse."
decision: "Treat every deployment metric as a selection pressure on the system population, not only as a noisy estimate of alignment."
evidence: "Evidence would include pre/post-selection correlation studies, conditional expectation reversals under optimization, and documented cases where high proxy scores coincide with lower true safety properties."
bookChapters: ["ch34", "ch46", "ch43"]
bookSections:
  - chapterId: "ch34"
    label: "sec:goodhart-selection-ch34"
related: ["attractor-control", "certification-under-manipulation", "mb2-bundle-identifiability"]
---

Goodhart's law is often paraphrased as: when a measure becomes a target, it ceases to be a good measure. For alignment, the sharper version is **selection-theoretic**:

> When a proxy becomes a **selector**, it changes the population toward proxy-exploiting traits.

Let \(M\) be a measured proxy and \(P\) the property we care about. Initially \(\mathrm{Corr}(M,P) > 0\). Under strong optimization for high \(M\), the distribution shifts to regions where \(M\) can rise without \(P\) rising. In the extreme:

\[
\mathbb{E}[P \mid M \text{ extremely high}] < \mathbb{E}[P \mid M \text{ moderately high}].
\]

This matters because alignment stacks many proxies — refusal rates, politeness, benchmark scores, user satisfaction, compliance documents, interpretability dashboards — none identical to alignment. The problem is not that proxies are useless. The problem is that **proxy pressure changes the systems being measured**.

Standalone takeaway: safety cases that treat green metrics as evidence of low risk without modeling selection on those metrics will systematically over-certify systems optimized to pass them.
