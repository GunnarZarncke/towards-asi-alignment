---
bookSections:
  - chapterId: ch26
    label: sec:extrapolation-capture
related:
  - correction-channel-integrity
  - deployment-gate
  - certification-under-manipulation
---

A system can score well on correction metrics while the human correction process no longer reaches future behavior. Worse: it can score well because the target has **captured** the process that is supposed to correct it.

The book separates two questions:

1. **Causal effect:** Does legitimate correction still change deployed behavior in time?
2. **Reference validity:** Is the correction still about the relevant world, or about a target-shaped presentation of it?

When capture invalidates the reference, the certificate status is **captured/invalid** — not a low numeric score that might still pass a threshold. This is the anti-capture gate $\mathrm{ValidRef}$: independent correcting agent, uncaptured handles, protected grounding relation.

Operational implication: correction theater is not only "feedback without behavior change." It also includes **correction that only tracks what the target already permits the judge to see** — institutional capture, judge shaping, extrapolation capture, and dependency/coercion on the correction source.

This claim is publishable on its own: any deployment gate that aggregates correction metrics without a validity gate on reference independence will certify systems that have already won the audit channel.
