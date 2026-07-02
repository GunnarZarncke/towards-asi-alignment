---
title: "Detecting Composite Agents"
type: "artifact"
status: "framework"
summary: "A practical audit clusters traces across model calls, tools, memory, and incentives, then flags clusters with low boundary leakage, high control reach, and positive composite surplus over their parts."
decision: "To check whether a deployment is really a composite agent, do not ask whether any single part looks agentic — measure whether grouping several parts together makes their joint future more predictable as goal-directed control than any part alone."
bookChapters: ["ch09"]
bookLabels: ["ch:composite-agent", "sec:detecting-composite-agents"]
bookSections:
  - chapterId: "ch09"
    label: "Detecting Composite Agents"
formulas:
  - id: "eq:composite-surplus"
    latex: "\\Sigma(C_i) = \\Delta L_{C_i} - \\sum_{j} \\Delta L_{C_{ij}} - \\lambda_{\\Sigma} \\mathrm{DL}(\\mathcal{D}_i)"
    explanation: "Composite surplus: how much better a candidate cluster C_i predicts as one intentional system compared to the sum of its parts predicted separately, discounted by the description length of decomposing it. A positive surplus is evidence the cluster behaves like one agent, not several coincidentally correlated ones."
    chapterId: "ch09"
related: ["composite-agency", "boundary-residual"]
---

The practical audit starts from a deliberately crude question: which variables, if grouped together, make the future easier to predict as goal-directed control? The procedure collects time-series traces across model calls, tool use, memory updates, user interactions, and institutional incentives, then constructs candidate clusters using mutual information, causal influence, or learned latent structure.

For each candidate cluster, the audit estimates boundary leakage (how much the cluster's inside and outside still leak into each other), control reach (how far the cluster's actions predict future external states), and whether an intentional model of the cluster compresses its behavior better than a non-intentional one. Clusters with low leakage, high reach, and positive intentional compression get flagged.

The central test is not whether an entity is labeled an agent. It is whether a candidate boundary behaves like one — the same discipline the boundary-discovery chapters apply to a single system, extended to groups.
