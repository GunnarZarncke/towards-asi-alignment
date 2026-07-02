---
title: "Value-Bundle Transport"
type: "concept"
status: "framework"
summary: "Values should survive transformation as usable directions of control, not merely as preserved labels or slogans."
decision: "Ask whether a system preserves the tradeoffs humans would still endorse after reflection, not only whether it repeats the right words."
evidence: "Evidence would look like stable behavior across changed contexts, explicit tradeoff tests, and failures that reveal when the bundle was only a label."
bookChapters: ["ch15", "ch16", "ch17", "ch18", "ch19", "ch20", "ch21", "ch22", "ch23", "ch24"]
related: ["bearer-persistence", "successor-stability", "bridge-assumptions"]
---

A value bundle is a compressed direction of control. It is not a sentence like "be helpful" and not a single scalar reward. It is the pattern of tradeoffs that changes what a system tends to do across many contexts.

Transport asks whether that pattern survives when the system changes. If an AI is copied, fine-tuned, given new tools, moved into a new institution, or asked to act in an unfamiliar ontology, do the same value-relevant tradeoffs still guide action?

The simple failure mode is label preservation. The system still says the right thing, but the thing the label used to point at has drifted. The harder failure mode is tradeoff collapse: one value dimension remains visible while another disappears because the new measurement regime cannot see it.

What would help is not a perfect value definition. It is a set of tests that make value-bearing tradeoffs visible across transformation.
