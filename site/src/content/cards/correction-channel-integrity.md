---
title: "Correction-Channel Integrity"
type: "concept"
status: "framework"
summary: "Human correction must still causally change a system's future behavior before irreversible damage."
decision: "Before granting more autonomy, ask whether legitimate correction reaches the system with enough speed, bandwidth, independence, and effect."
evidence: "Evidence would include correction traces showing pre/post behavior change, latency, who controlled the handle, and where correction was ignored or merely acknowledged."
bookChapters: ["ch25", "ch26", "ch27", "ch28", "ch29", "ch39", "ch41", "ch42"]
bookLabels: ["ch:correction-channel-integrity"]
related: ["boundary-discovery", "deployment-gate", "evidence-and-uncertainty"]
---

Feedback is not enough. A dashboard can receive feedback while the real deployed actor ignores it. A model can say it accepted a correction while the future behavior remains unchanged.

Correction-channel integrity asks for a causal path. A legitimate correcting process observes, judges, issues a correction, controls some handle, and that handle reaches the system's future behavior in time.

This turns "is the system corrigible?" into a more concrete audit question: which handles exist, who controls them, what do they reach, how fast do they act, and what evidence shows the system changed rather than performed agreement?

The central warning is correction theater. If correction is only ritual, it may make a deployment look safer while consuming the scarce time in which real correction was still possible.
