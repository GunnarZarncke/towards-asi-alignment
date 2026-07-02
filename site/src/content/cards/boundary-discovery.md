---
title: "Boundary Discovery"
type: "concept"
status: "plausible"
summary: "Find the effective optimizer in the deployed loop, not just the model or product name."
decision: "Before auditing goals or correction, determine what system actually preserves state and exerts control over time."
evidence: "Evidence would include traces showing which model, memory, tools, dashboards, teams, and release processes form the operative controller."
bookChapters: ["ch06", "ch07", "ch08", "ch09", "ch10"]
bookLabels: ["ch:finding-boundary", "ch:agent-without-anthropomorphism"]
related: ["correction-channel-integrity", "bridge-assumptions", "deployment-gate", "agent-without-anthropomorphism", "boundary-residual", "adversarial-boundary-discovery", "composite-agency", "mb1-boundary-estimator-soundness"]
---

The deployed agent may not be "the model." It may be a loop: model endpoint, tool runner, memory store, retrieval index, scheduler, dashboard incentives, and human operators who learn to rubber-stamp the queue.

Boundary discovery asks where the operative controller is. Which internal states help predict and control future interaction with the environment? Which interface separates sensor, action, internal state, and external effect well enough to audit?

This matters because every later question depends on the boundary. A correction channel that reaches only the visible model may miss the memory, tool policy, or institutional loop that actually drives behavior.

The first audit question is therefore simple: what is the thing being deployed?
