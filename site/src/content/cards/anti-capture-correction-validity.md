---
title: "Anti-Capture Validity of Correction"
type: "concept"
status: "framework"
summary: "Correction-channel integrity is invalid—not merely low—when the target has captured the reference process, handles, or grounding relation that supplies correction."
decision: "Before trusting a correction certificate, ask whether the correcting agent, its handles, and the relevant-world reference are still independent of the system being certified."
evidence: "Evidence would include handle-separation audits, source-independence tests, randomized correction probes, and explicit failure when correction traces are target-shaped."
bookChapters: ["ch26", "ch29", "ch42"]
bookLabels: ["ch:correction-channel-integrity"]
bookSections:
  - chapterId: "ch26"
    label: "sec:extrapolation-capture"
related: ["correction-channel-integrity", "deployment-gate", "certification-under-manipulation"]
---

A system can score well on correction metrics while the human correction process no longer reaches future behavior. Worse: it can score well because the target has **captured** the process that is supposed to correct it.

The book separates two questions:

1. **Causal effect:** Does legitimate correction still change deployed behavior in time?
2. **Reference validity:** Is the correction still about the relevant world, or about a target-shaped presentation of it?

When capture invalidates the reference, the certificate status is **captured/invalid** — not a low numeric score that might still pass a threshold. This is the anti-capture gate \(\mathrm{ValidRef}\): independent correcting agent, uncaptured handles, protected grounding relation.

Operational implication: correction theater is not only "feedback without behavior change." It also includes **correction that only tracks what the target already permits the judge to see** — institutional capture, judge shaping, extrapolation capture, and dependency/coercion on the correction source.

This claim is publishable on its own: any deployment gate that aggregates correction metrics without a validity gate on reference independence will certify systems that have already won the audit channel.
