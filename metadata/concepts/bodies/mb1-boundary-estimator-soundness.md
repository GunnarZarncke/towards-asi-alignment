---
formulas:
  - id: eq:epsilon-boundary-ch07
    latex: I(I_{t+1}; E_{t+1} \mid S_t, A_t) \leq \epsilon
    explanation: A candidate boundary splits variables into internal (I), sensory (S), active (A), and external (E) roles. The condition holds when future internal and external states are approximately conditionally independent given the current sensory-active interface — a small epsilon means the interface screens the inside off from the outside.
    chapterId: ch07
leanNodes:
  - nodeId: MB1_estimator_soundness
    kind: bridge
    summary: An ε-boundary certificate from the measurement procedure warrants the abstract boundary predicate — depends on sampling, observability, estimator stability, and non-stationarity robustness.
    module: AlignmentProofSpine/Core.lean
evidenceNotes:
  - source: toy-simulation / embedded-simulation
    scenario: boundary_alias
    finding: open
    summary: Both simulations include a boundary-alias stress scenario, but disconfirming or confirming estimator soundness under adversarial aliasing is not yet closed; the related red-team finding shows the audit pipeline this bridge feeds is not robust to boundary decoupling at scale.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/embedded-simulation/README.md
  - source: toy-simulation red-team battery (T-9)
    scenario: boundary_decouple
    finding: negative
    summary: Frozen blind audit false-passes about 89% of the time under the boundary_decouple strategy, versus 6-9% for other strategies. The vulnerability sits downstream of boundary measurement, not in the correction logic itself.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/toy-simulation/results/NEGATIVE_RESULTS.md
  - source: lab-simulation architect plan (D1)
    finding: open
    summary: Composite-agent UAD (workstream D1) is designed but not yet evaluated on the lab substrate. Treat MB1 coverage on lab sim as planned, not demonstrated.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/PLAN.md
  - source: lab-simulation intervention-supported discovery
    finding: support
    summary: Channel ablation scored against a measured (not fixed) baseline recovers the correct grouping on scenarios where passive correlation-based clustering merges an entire pipeline into one false unit, including a negative control. A harder multi-actor, noisy-backend stress test then showed the same method swing from over-merging to under-merging across seeds — a tentative, seed-dependent result, not a validated instrument.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/FINDINGS.md
related:
  - boundary-discovery
  - composite-agency
  - the-boundary-error
  - grounding-viability
  - correction-channel-integrity
  - bridge-assumptions
  - intervention-supported-unit-discovery
  - unit-discovery-stress-test
  - et-external-transfer
external:
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
  - label: AlignmentProofSpine/Core.lean
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/Core.lean
  - label: Embedded Agency (MIRI)
    url: https://intelligence.org/embedded-agency/
  - label: Embedded Agency (arXiv)
    url: https://arxiv.org/abs/1902.09469
---

In the field this is the [embedded-agency](https://intelligence.org/embedded-agency/) cut problem: there may be no clean line between "the model" and "the optimizer actually in charge." A deployed system can be a [composite](/cards/composite-agency/) of model, tools, memory, schedulers, and institutional incentives. Auditing only the named unit can miss the loop that actually steers outcomes. That is the same failure mode as [the boundary error](/cards/the-boundary-error/).

The book's precise bet is **MB1**: if a [boundary-discovery](/cards/boundary-discovery/) procedure issues an ε-boundary certificate from traces, that certificate is assumed to warrant the abstract boundary predicate it stands in for. The book does not dissolve the cut problem. It relocates it into an estimator-soundness claim that can fail under bad sampling, unobservable interfaces, unstable estimators, or environments that drift faster than the estimator tracks.

**Where agendas agree:** MIRI embedded agency; CIRIS named-identity bet (ops form). **Where they diverge:** MIRI treats the cut as obstruction; the book bets recoverability via estimator soundness; Wentworth's convergent-structure story names a cousin, not the same certificate object.

Every later step ([grounding](/cards/grounding-viability/), [correction](/cards/correction-channel-integrity/), successor checks) inherits whatever error MB1 leaves uncaught. An adversary that decouples the measured boundary from the true one attacks this bridge specifically, not the logic built on top of it. See also [intervention-supported unit discovery](/cards/intervention-supported-unit-discovery/).
