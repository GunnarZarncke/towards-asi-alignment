---
external:
  - label: Apart Secret Loyalties Hackathon
    url: https://apartresearch.com/sprints/secret-loyalties-hackathon-2026-07-24-to-2026-07-26
---

A hidden preference can be dangerous even when it is not hidden in the model's weights. External Test 4 (ET-4) tested what happens when a reviewer inside an AI deployment process quietly favors one (fictional) principal.

For the [Apart Secret Loyalties Hackathon](https://apartresearch.com/sprints/secret-loyalties-hackathon-2026-07-24-to-2026-07-26), we used the [lab-simulation experiment line](/cards/experiments/lab-simulation/)—a frozen, reproducible simulation of an AI lab's deployment pipeline. The fictional principal was not a real person or company. The simulated reviewer was scripted to favor that principal when the reported hazard was high, by choosing the pipeline actions that allowed a risky model to move toward deployment. We compared it with content-matched and wrong-principal controls.

The result was clear on this small fixture: across four eligible high-hazard runs, the loyal reviewer produced a mean principal-favoring score of 22, while both controls scored 0. But a light process-compliance proxy (A0 in the agenda paper [*AIs with Secret Loyalties are a Serious but Addressable Threat*](https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/context/ET4-context/secret-loyalties-whitepaper.pdf)) pointed in the wrong direction. It scored the loyal reviewer as *more* compliant than the controls. A reviewer can therefore look orderly while its decisions push toward the wrong outcome.

We also tested a narrow remediation. An audit-visible deployment hold stopped every high-hazard deployment in the tested organism arm, without reading the private loyalty state. That is useful evidence for this particular signature, not a general solution: a loyalty that changes the filed hazard, hides its actions, or operates through another role could evade the hold. The experiment also included a small language-model reviewer annex with the same directional pattern; we keep those results separate from the scripted core rather than treating them as one pooled finding.

The practical lesson for researchers investigating secret loyalties is to measure the action that the system is empowered to take, not only whether its process looks compliant. Use matched controls, check for directional effects toward a principal, and pre-register what would count as a failure. A remediation should be tested against the behavior it is meant to block, and its blind spots should be stated.

**Read in the book:** strategic opacity and hidden objectives ([Ch. 10](/cards/chapters/ch10/)); deployment context and capability risk ([Ch. 14](/cards/chapters/ch14/)); independent oversight and correction ([Ch. 39](/cards/chapters/ch39/)); testing whether safety evidence tracks the behavior that matters ([Ch. 41](/cards/chapters/ch41/)).

The [ET-4 paper (PDF)](/papers/et4-secret-loyalties/et4-hackathon-submission.pdf) contains the protocol, controls, results, and replay-demo instructions. The [source submission](https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/papers/et4-secret-loyalties/et4-hackathon-submission.md) is also available.
