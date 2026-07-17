---
bookSections:
  - chapterId: ch03
    label: What Is a Dynamical Guarantee?
  - chapterId: ch03
    label: Safety Sets, Bad Sets, and Basins
formulas:
  - id: eq:dynamical-guarantee-probabilistic
    latex: \Pr\left( X_t \in \mathcal{S} \;\forall t \in [0,T] \mid X_0 \in \mathcal{B},\; E \in \mathcal{E},\; A \in \mathcal{C} \right) \geq 1-\delta
    explanation: 'A dynamical guarantee, not a static one: the system stays in the acceptable region S across the whole horizon T with probability at least 1-delta, conditional on starting in a safety basin B, the environment falling in a specified class E, and the system belonging to a certified class C. The guarantee is only as meaningful as how narrow and testable that certified class is.'
    chapterId: ch03
leanNodes:
  - nodeId: P01
    kind: proof
    summary: If a state predicate holds initially and is preserved by every step, it holds after any finite number of iterations.
    module: AlignmentProofSpine/Certification.lean
  - nodeId: P30
    kind: proof
    summary: The certification spine packages certified/layered evidence with the risk leaf; the numeric risk bound follows from Control <= CCI + delta.
    module: AlignmentProofSpine/Certification.lean
related:
  - grounding-viability
  - boundary-discovery
  - successor-stability
---

A static alignment claim has the form "at time t, system A has property P." That is useful for ordinary software — does a program pass a test suite, respect an access policy, return a correct output — but it breaks for superintelligence, where the system learns, acquires tools, persuades users, and eventually produces successors.

The book's replacement is a dynamical guarantee: a probabilistic claim that the system remains in, or returns to, an acceptable region of state space over a time horizon, conditional on starting inside a safety basin, the environment staying in a specified class, and the system belonging to a certified class of allowed transformations.

The distinction between a safe set, a bad set, and a basin matters here. A system can be safe right now while sitting outside the basin — a lab that behaves responsibly today while funding and competitive pressure push it toward dangerous deployment. A system can also enter a locally risky state while remaining inside a basin that reliably corrects it. The dynamical guarantee tracks the basin, not the snapshot.
