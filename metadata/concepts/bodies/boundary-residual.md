---
bookSections:
  - chapterId: ch07
    label: Boundary as Conditional Independence
formulas:
  - id: eq:epsilon-boundary-ch07
    latex: I(I_{t+1}; E_{t+1} \mid S_t, A_t) \leq \epsilon
    explanation: Variables around a candidate system split into internal (I), sensory (S), active (A), and external (E) roles. The boundary condition holds when future internal and external states are approximately conditionally independent given the current sensory-active interface — a small epsilon means the interface screens the inside off from the outside, without requiring the inside to be isolated from the world.
    chapterId: ch07
leanNodes:
  - nodeId: P05
    kind: proof
    summary: Boundary-related results in the capability/boundary spine (see module map for the full P05-P09 group).
    module: AlignmentProofSpine/Boundaries.lean
related:
  - boundary-discovery
  - adversarial-boundary-discovery
  - mb1-boundary-estimator-soundness
---

The boundary condition divides variables around a candidate system into internal, sensory, active, and external roles, then asks whether the deep inside and deep outside become approximately conditionally independent once the sensory-active interface is known. A sensory variable is anything through which the outside predicts the future inside; an active variable is anything through which the inside predicts the future outside — no eyes, muscles, or motors required.

A small residual means the system has a boundary, at least approximately: it depends on the world, senses it, and acts on it, but does not leak into or out of it except through the interface. This is not the claim that the system is isolated. It is the claim that its dependence on the world is organized.

This condition, not a fixed list of examples, is what lets the same measurement apply to a chatbot, a firm, or a biological organism.
