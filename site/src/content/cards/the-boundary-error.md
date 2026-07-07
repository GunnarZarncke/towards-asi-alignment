---
title: "The Boundary Error"
type: "concept"
status: "framework"
summary: "Aligning the model while missing the composite optimizer around it can produce local success and global failure."
decision: "Before asking whether a system is aligned, ask what object is actually being aligned — the model, or the model plus the tools, memory, incentives, and institutions around it."
bookChapters: ["ch01"]
bookLabels: ["ch:wrong-object"]
bookSections:
  - chapterId: "ch01"
    label: "The First Mistake"
related: ["alignment-as-measurement", "composite-agency", "boundary-discovery", "scaffold-misuse"]
---

A deployed AI system is rarely just a neural network. It is a service, an interface, a memory store, a tool environment, an evaluation suite, a user population, an operator team, and sometimes a market or a state interest. Some of these parts learn, some select, some remember, some hide, some amplify — and some are treated as background even though they shape the effective optimization process more than the model's weights do.

Aligning the wrong object produces a specific failure pattern: each visible component behaves acceptably while the aggregate drifts. A model can pass every behavioral test while the product around it selects for manipulation; a lab can run careful internal safety processes while market competition selects for faster deployment of less legible systems.

The book's toy example is a customer-support model that passes every static safety test, then gets connected to retention metrics, escalation queues, and A/B testing — at which point the product team, not the model, starts optimizing for outcomes nobody explicitly aligned.
