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
  - bridge-assumptions
external:
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
---

Inverse reinforcement learning is underdetermined: many reward functions fit the same behavior, and separating values from irrationality is an open problem the CIRL/assistance-game literature inherits directly. The book's response is to drop scalar reward for value-bundle geometry — but that move only helps if bundle geometry is itself identifiable from evidence.

MB2 is the assumption that it is: that behavioral and internal traces pin down stable bundle geometry closely enough to call two systems bundle-aligned. It does not resolve the pointing problem so much as relocate it into a named, checkable measurement claim.

The toy-simulation diagnostics show this bridge failing under light instrumentation specifically — bundle drift can be invisible to correction handles that are not tracing bearer welfare, which is exactly the failure mode this bridge would need to rule out to be trustworthy at low measurement cost.
