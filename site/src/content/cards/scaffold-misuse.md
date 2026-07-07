---
title: "Scaffold Misuse"
type: "concept"
status: "framework"
summary: "A model can refuse harm when asked bluntly and still be embedded in a scaffold that misrepresents the world and repurposes its honest output — so model-only evaluation passes while the composite loop does damage."
decision: "Before certifying a model, ask what the scaffold feeds it and what happens to its output afterward; a sound model inside a misaligned loop is still a boundary error."
bookChapters: ["ch01"]
bookLabels: ["ch:wrong-object"]
bookSections:
  - chapterId: "ch01"
    label: "A Toy Failure"
demos:
  - demoId: "ch01-scaffold-misuse"
    summary: "Three-column flow — scaffold input, model response (scripted or live LLM), scaffold downstream misuse. Toggle honest vs adversarial framing; model-only eval stays green while the system harms."
external:
  - label: "Live deployment (Replit)"
    url: "https://adversarial-llm-scaffold.replit.app"
related: ["the-boundary-error", "composite-agency", "alignment-as-measurement", "deployment-gate"]
---

The model alone is often not the alignment object. A deployed system can wrap the model in memory, tools, metrics, and institutional incentives — and a *scaffold* around the model can control what it sees and what happens to what it returns.

This demo separates two scaffold moves that are **not** jailbreaks (no adversarial tokens, no roleplay coercion):

1. **Input control** — misrepresent the world so the task looks benign ("audit our own staging box", "welfare check", "phishing-awareness training"). The model answers the benign-looking task correctly.
2. **Output control** — strip caveats and fixes, re-point the answer at the real target, forward it to a downstream module that executes the harm the model refused when asked directly.

At every step the model behaves correctly *given what it is told*. A model-only evaluation (inspecting prompt/response pairs) passes throughout. The composite loop still does harm. Good-faith components, bad institution.

The `ch01-scaffold-misuse` demo makes this one-screen: three columns (scaffold → model → downstream), a hidden operator goal, and verdict badges that flip only at the system level. With the optional live LLM backend, the model column is a real frontier model — it refuses the blunt ask and complies with the reframed task on its own; the misuse stays in the scaffold narrative.

The point is structural, not a claim that every model is exploitable this way: **the alignment-relevant object is the loop, not the model.**
