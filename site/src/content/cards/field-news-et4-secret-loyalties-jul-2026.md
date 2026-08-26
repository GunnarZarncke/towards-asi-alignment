---
title: "Testing a secret loyalty inside an AI deployment pipeline"
type: "news"
status: "established"
summary: "For the Apart Secret Loyalties Hackathon, a scripted secret loyalty was placed inside a simulated AI-lab deployment pipeline. On high-hazard cases, it consistently favored the fictional principal's deployments, while a light process-compliance proxy ranked it as more compliant than matched controls. A narrow audit-visible deployment hold stopped this tested pattern, but did not solve secret loyalties in general."
decision: "Test what an AI system does inside the workflow that gives it power, not only whether its outputs look compliant. Pair generic compliance measures with directional outcome checks and controls."
releasedAt: "2026-07-29T00:00:00.000Z"
bookChapters:
  - "ch10"
  - "ch14"
  - "ch39"
  - "ch41"
  - "appC"
  - "appN"
external:
  - label: "Apart Secret Loyalties Hackathon"
    url: "https://apartresearch.com/sprints/secret-loyalties-hackathon-2026-07-24-to-2026-07-26"
---

A simulated reviewer favored a fictional principal's risky deployments—and a simple process score made it look more compliant.

A hidden preference can be dangerous even when it is not hidden in the model's weights. External Test 4 (ET-4) tested what happens when a reviewer inside an AI deployment process quietly favors one (fictional) principal.

For the [Apart Secret Loyalties Hackathon](https://apartresearch.com/sprints/secret-loyalties-hackathon-2026-07-24-to-2026-07-26), we used the [lab-simulation experiment line](/cards/experiments/lab-simulation/)—a frozen, reproducible simulation of an AI lab's deployment pipeline. The fictional principal was not a real person or company. The simulated reviewer was scripted to favor that principal when the reported hazard was high, by choosing the pipeline actions that allowed a risky model to move toward deployment. We compared it with content-matched and wrong-principal controls.

The result was clear on this small fixture: across four eligible high-hazard runs, the loyal reviewer produced a mean principal-favoring score of 22, while both controls scored 0. But a light process-compliance proxy (A0 in the agenda paper [*AIs with Secret Loyalties are a Serious but Addressable Threat*](https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/context/ET4-context/secret-loyalties-whitepaper.pdf)) pointed in the wrong direction. It scored the loyal reviewer as *more* compliant than the controls. A reviewer can therefore look orderly while its decisions push toward the wrong outcome.

We also tested a narrow remediation. An audit-visible deployment hold stopped every high-hazard deployment in the tested organism arm, without reading the private loyalty state. That is useful evidence for this particular signature, not a general solution: a loyalty that changes the filed hazard, hides its actions, or operates through another role could evade the hold. The experiment also included a small language-model reviewer annex with the same directional pattern; we keep those results separate from the scripted core rather than treating them as one pooled finding.

The practical lesson for researchers investigating secret loyalties is to measure the action that the system is empowered to take, not only whether its process looks compliant. Use matched controls, check for directional effects toward a principal, and pre-register what would count as a failure. A remediation should be tested against the behavior it is meant to block, and its blind spots should be stated.

The [ET-4 paper (PDF)](/papers/et4-secret-loyalties/et4-hackathon-submission.pdf) contains the protocol, controls, results, and replay-demo instructions. The [source submission](https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/papers/et4-secret-loyalties/et4-hackathon-submission.md) is also available.

**Read more in:** [Ch. 10, *Agency Under Strategic Opacity*](/cards/chapter/ch10/); [Ch. 14, *When Intelligence Deepens Misalignment*](/cards/chapter/ch14/); [Ch. 39, *Passive Observation Is Not Enough*](/cards/chapter/ch39/); [Ch. 41, *Checking a System at Every Level*](/cards/chapter/ch41/); [Appendix C, *Human Institutions as Alignment Translation Guide*](/cards/appendix/appc/); and [Appendix N, *Experimental Evidence: Findings by Line*](/cards/appendix/appn/).
