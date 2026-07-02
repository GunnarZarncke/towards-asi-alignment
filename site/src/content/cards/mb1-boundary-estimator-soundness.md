---
title: "MB1 — Boundary Estimator Soundness"
type: "bridge"
status: "bridge"
summary: "A measured epsilon-boundary certificate is assumed to warrant the abstract boundary predicate it stands in for."
decision: "Before trusting a boundary-discovery result, ask what sampling, observability, and non-stationarity conditions the estimator needed in order to be sound."
evidence: "Evidence would include estimator stability under resampling, robustness across non-stationary environments, and agreement between independent measurement procedures on the same deployed system."
bookChapters: ["ch06", "ch07", "ch08", "ch09", "ch10", "ch36"]
bookLabels: ["ch:finding-boundary"]
formulas:
  - id: "eq:epsilon-boundary-ch07"
    latex: "I(I_{t+1}; E_{t+1} \\mid S_t, A_t) \\leq \\epsilon"
    explanation: "A candidate boundary splits variables into internal (I), sensory (S), active (A), and external (E) roles. The condition holds when future internal and external states are approximately conditionally independent given the current sensory-active interface — a small epsilon means the interface screens the inside off from the outside."
    chapterId: "ch07"
leanNodes:
  - nodeId: "MB1_estimator_soundness"
    kind: "bridge"
    summary: "An ε-boundary certificate from the measurement procedure warrants the abstract boundary predicate — depends on sampling, observability, estimator stability, and non-stationarity robustness."
    module: "AlignmentProofSpine/Core.lean"
evidenceNotes:
  - source: "toy-simulation / embedded-simulation"
    scenario: "boundary_alias"
    finding: "open"
    summary: "Both simulations include a boundary-alias stress scenario, but disconfirming or confirming estimator soundness under adversarial aliasing is not yet closed; the related red-team finding shows the audit pipeline this bridge feeds is not robust to boundary decoupling at scale."
    resultsPath: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/embedded-simulation/README.md"
  - source: "toy-simulation red-team battery (T-9)"
    scenario: "boundary_decouple"
    finding: "negative"
    summary: "Frozen blind audit false-passes about 89% of the time under the boundary_decouple strategy, versus 6-9% for other strategies. The vulnerability sits downstream of boundary measurement, not in the correction logic itself."
    resultsPath: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/toy-simulation/results/NEGATIVE_RESULTS.md"
related: ["boundary-discovery", "bridge-assumptions"]
external:
  - label: "Bridges and the Field: A Crosswalk (appendix source)"
    url: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex"
  - label: "AlignmentProofSpine/Core.lean"
    url: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/Core.lean"
---

Embedded-agency arguments deny a clean cut between an agent and its environment. The book does not dissolve that problem. It relocates it into a falsifiable, measurable bet: a directed epsilon-boundary can be estimated from traces, and passing the estimator's certificate is assumed to mean the real, semantic boundary condition holds.

That assumption is MB1. It is not proved. It depends on sampling being adequate, the interface being observable, the estimator being stable under resampling, and the environment not drifting faster than the estimator can track.

This is why boundary discovery is described as a hypothesis rather than a fact: every later step in the book — grounding, correction, successor checks — inherits whatever error MB1 leaves uncaught. An adversary that can decouple the measured boundary from the true one attacks this bridge specifically, not the logic built on top of it.
