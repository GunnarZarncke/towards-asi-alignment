---
bookSections:
  - chapterId: ch09
    label: The Object-Level Mistake
leanNodes:
  - nodeId: UADDiscoveryAudit
    kind: definition
    summary: Formal audit certificate for unsupervised agency discovery — the machinery behind detecting a composite agent from traces rather than labels.
    module: AlignmentProofSpine/CooperationGraph.lean
demos:
  - demoId: ch09-uad-coalition-board
    summary: Multiplayer demo where each browser tab is a player; an admin can run an unsupervised-agency-discovery (UAD) pass to detect coalitions and audit their sensor/action/internal/external roles and Markov-blanket plausibility.
related:
  - agent-without-anthropomorphism
  - detecting-composite-agents
  - the-boundary-error
---

A common first move in alignment is to pick an object — a model, a chatbot, a company — and ask whether it is aligned. That move is often wrong, because the object that matters may not be the object that is easiest to name. A deployed language model is part of a loop containing users, system prompts, tools, memory stores, monitoring dashboards, product incentives, and competitive pressures, and the real optimizing process may be spread across the whole loop.

The book's basic claim: an agent can be distributed across components that are not individually agents. More carefully, the real alignment target is the smallest dynamically coherent system whose internal states, actions, memories, and selection pressures jointly explain future intervention on the world.

If only the model is aligned while it sits inside a larger process that selects for engagement, opacity, or dependency, the aligned component can become a tool of a misaligned composite. The `ch09-uad-coalition-board` demo makes this concrete: it detects when several independently-acting players are functioning as one coordinated group-agent from their traces alone, the same move the chapter asks an auditor to make on a deployed system.
