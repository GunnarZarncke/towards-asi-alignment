---
title: "How would you find what actually decides?"
type: essay
status: framework
summary: "Do not start from the labeled model. Start from what changes outcomes, then draw a boundary around that process."
essayRole: branch
essayParent: the-chatbot-passed-the-test
essayNext: the-hospital-is-the-ai
minutes: 7
related:
  - boundary-discovery
bookChapters:
  - ch01
---

The parent essay says the labeled model is often the wrong object. Fine. Then what do you look at instead?

A practical method, borrowed from how you would hunt a leak in a building: do not start with the architectural drawing. Start with the wet floor. Ask which process, if you modeled it as something with memory, inputs, outputs, and the ability to steer, would predict the changes you actually care about.

In the support-bot story, the wet floor is ticket-closure patterns, refund rates, user phrasing that "works," and the weekly fine-tune. The labeled model is on the drawing. The loop is on the floor.

That does not mean every dashboard is an agent, or that you should panic at every spreadsheet. It means you should be willing to draw a bigger box when the small box fails to explain the behavior. Tools, memory, A/B tests, queues, and incentive schemes can be inside the box even when the org chart says they are "just infrastructure."

A crude test: if you froze the model weights and the outcomes still drift, the actor was not only the weights. If you froze the product metrics and the "personality" of the system still shifts, something else is learning. If neither freeze is possible, you do not yet know where the actor is, which is information, not a reason to pretend you do.

Researchers have more technical versions of this (searching traces for control, measuring what compresses the future). You do not need those tools to accept the question. You need them if you want an answer you can defend in a lab.

This page is a tangent. The main thread goes to the hospital, where the wet floor is a reserved room at 2 a.m.
