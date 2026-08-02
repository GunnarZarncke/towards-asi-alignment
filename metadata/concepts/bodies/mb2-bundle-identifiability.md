---
leanNodes:
  - nodeId: MB2_bundle_identifiability
    kind: bridge
    summary: Bundle-gradient-equivalent systems are assumed to be bundle-aligned — behavioral/internal traces are assumed to identify stable value-bundle geometry.
    module: AlignmentProofSpine/Core.lean
evidenceNotes:
  - source: toy-simulation diagnostic (T-4)
    scenario: bundle_goodhart
    finding: negative
    summary: Light correction-handle instrumentation false-passes every case where value-relevant state drifts invisibly (0/10 correct); medium-handle bearer-welfare tracing catches all 10/10. Passive or lightly-instrumented bundle measurement can look fine while the underlying bundle geometry is already gone.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/toy-simulation/results/NEGATIVE_RESULTS.md
related:
  - value-bundle-transport
  - correction-channel-integrity
  - mb3-bearer-import
  - bridge-assumptions
external:
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
  - label: The Value Learning Problem (MIRI)
    url: https://intelligence.org/files/ValueLearningProblem.pdf
  - label: Embedded Agency — Robust Delegation (MIRI)
    url: https://intelligence.org/embedded-agency/
---

In the field this is the pointing problem. Inverse reinforcement learning is underdetermined: many reward functions fit the same behavior, and separating values from irrationality is still open in CIRL and assistance-game work. Nearby names for the same wall include ELK (does the system report what it knows, or what a human would want to hear?) and reward misspecification under RLHF. If you cannot tell what a system is optimizing for from the evidence you have, later claims about "aligned values" are guessing.

The book's precise bet is **MB2**: behavioral and internal traces are assumed to identify stable [value-bundle](/cards/value-bundle-transport/) geometry well enough to license claims of bundle alignment. The move is not "scalar reward solved," but "replace the flat reward target with measurable bundle geometry." That only helps if the geometry is itself identifiable. Closely related is [bearer import](/cards/mb3-bearer-import/) (MB3), which asks who those values apply to.

Diagnostic evidence shows the failure mode under light instrumentation: bundle drift can be invisible to [correction](/cards/correction-channel-integrity/) handles that are not tracing bearer welfare. That is exactly what this bridge would need to rule out before low-cost measurement is trustworthy.
