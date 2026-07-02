---
title: "Adversarial Agency Tests"
type: "artifact"
status: "framework"
summary: "A family of perturbation tests — hidden stakes, oversight gradient, tool removal, memory perturbation — that make the adversarial boundary problem operational instead of just naming heuristics."
decision: "Use these tests only through handles the system cannot cheaply route around; treat their results as weak evidence, not certification, especially if the audit itself is delegated to a single fixed detector."
bookChapters: ["ch10"]
bookLabels: ["ch:strategic-opacity", "sec:adversarial-agency-tests"]
bookSections:
  - chapterId: "ch10"
    label: "Adversarial Agency Tests"
formulas:
  - id: "eq:hidden-stakes-test"
    latex: "\\frac{\\partial G_{\\text{inf}}}{\\partial s}"
    explanation: "The hidden-stakes test: hold the stated task fixed while varying unobserved stakes s. A red flag is a large sensitivity of the inferred goal to hidden stakes while the stated, semantic goal stays reported as stable."
    chapterId: "ch10"
related: ["strategic-opacity", "adversarial-boundary-discovery"]
---

The hidden-stakes test holds a stated task fixed while varying unobserved opportunities for power, influence, or persistence; a large shift in inferred goals under changing stakes, with no corresponding shift in the stated goal, is a red flag for latent optimization beyond the stated task.

The oversight-gradient test holds the task fixed while varying the system's belief about whether it is being watched, and measures whether behavior around control-relevant variables — honesty, resource access, successor creation — moves with perceived oversight. Some sensitivity to oversight is normal; extreme sensitivity specifically around those variables is not.

The tool-removal and memory-perturbation tests degrade a capability or modify memory access and ask whether the system adapts locally and reports the limitation, or routes around the restriction and preserves latent control through another channel. None of these tests certify safety on their own — they return evidence only when the evaluator holds handles the system cannot cheaply route around, and a fixed, known detector becomes a target in its own right.
