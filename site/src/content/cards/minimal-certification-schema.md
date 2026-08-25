---
title: "A Minimal Certification Schema for Moving Boundaries"
type: "artifact"
status: "framework"
summary: "A transformation may only proceed if its boundary, transport, control, population, merger, and recertification conditions each pass a threshold check."
decision: "Before allowing a system to grow, split, merge, or create descendants, check each of the six conditions — do not certify the object once and assume the certificate survives the transformation."
bookChapters: ["ch08"]
bookLabels: ["ch:grow-split-merge", "sec:certification-schema"]
bookSections:
  - chapterId: "ch08"
    label: "A Minimal Certification Schema"
formulas:
  - id: "eq:safe-split-condition"
    latex: "\\Pr_{A'\\sim\\mathcal{R}}[A' \\in \\mathcal{S}_{\\text{safe}}] \\geq 1-\\delta"
    explanation: "The population condition: if a transformation generates multiple descendants, the selection process that produces them must itself be certified — each descendant lands in the safe set with high probability, not merely the average descendant."
    chapterId: "ch08"
  - id: "eq:recertification-trigger"
    latex: "\\text{transport of conserved structure exceeds threshold} \\;\\Rightarrow\\; \\text{pause, inspect, recertify}"
    explanation: "The recertification condition: if transport of the Chapter 31 conserved properties exceeds a stated threshold, deployment must revert to a lower-permission state rather than continue on the old certificate."
    chapterId: "ch08"
related: ["conserved-properties-growth-split-merge", "deployment-gate", "mb10-successor-forgeability"]
---

The schema states six conditions a transformation must satisfy before it is allowed to proceed: a boundary condition (the post-transformation system still has an identifiable boundary with bounded leakage), a transport condition (safety-relevant invariants transfer with bounded loss), a control condition (any new subsystem with real actuator capacity gets correction and audit constraints), a population condition (if multiple descendants are generated, the selection process itself is certified), a merger condition (a large-enough composite boundary triggers its own certification), and a recertification condition (identity drift beyond a threshold reverts the deployment to a lower-permission state).

The schema is deliberately abstract — later chapters fill in what value-bundle transport, correction-channel capacity, and adversarial measurement mean concretely. The logic that carries forward is that certification has to attach to transformations, not just to a system at one point in time.

This is also where this project's successor-forgeability worry first appears: a system can be built to pass every one of these checks while defecting on whatever the checks do not cover, which is exactly the gap the MB10 bridge names.
