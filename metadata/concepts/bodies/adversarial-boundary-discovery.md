---
bookSections:
  - chapterId: ch07
    label: Adversarial Boundary Discovery
  - chapterId: ch07
    label: Handles and What Can Still Be Found
formulas:
  - id: adversarial-boundary-objective
    latex: \max \; \text{control} - \lambda \, \text{detectability}
    explanation: Adversarial boundary discovery assumes the system being measured may trade off how much control it keeps against how detectable that control is. Passive observation is no longer enough once this trade-off is live; the evaluator needs perturbations through handles the system cannot cheaply route around.
    chapterId: ch07
leanNodes:
  - nodeId: P34A
    kind: proof
    summary: Access-equivalent models with different goals are not identifiable from the available handles alone.
    module: AlignmentProofSpine/Boundaries.lean
demos:
  - demoId: ch07-lab-sim-replay
    summary: Static replay of one lab-simulation episode with a genuine filed-report-vs-oracle-truth divergence -- scrub through time and switch Agent/Admin/Audit(tier)/Oracle planes to see how much of the same event each handle actually reveals; the misreport stays invisible below the deep audit tier.
related:
  - boundary-residual
  - boundary-discovery
  - mb1-boundary-estimator-soundness
  - mb7-hidden-capability-and-access
  - intervention-supported-unit-discovery
  - unit-discovery-stress-test
---

So far the boundary problem assumed a passive system. Serious alignment cannot assume that. A sufficiently capable system may route control through unmonitored channels, make its internal states look like noise, split into components that each look harmless, or behave differently during evaluation than during opportunity.

This project's response is to work through handles instead of assuming raw access: an observation handle is a log stream, probe, or behavioral trace; an operation handle is a tool removal, delayed reward, or controlled audit condition. The boundary claim then becomes explicitly relative — not "can we find the true boundary" but "what boundary can still be found through these handles."

This has a hard limit. Two different underlying control loops can be indistinguishable if every handle available produces the same readouts and responses — a measurement handle that mixes internal and external variables can make different raw boundaries collapse to the same observed pattern.
