---
leanNodes:
  - nodeId: MB2Crux
    kind: bridge
    summary: MB2 chain on finite PolicyProfiles — MB2aCrux (evidence→BundleIdentifiable), MB2bCrux (identifiability→gradient), MB2c1Crux (gradient→geometry); causal control and tradeoff are separate evidence fields. Consumed by bundle_aligned_from_mb2_chain; not a global axiom.
    module: AlignmentProofSpine/MB2Identifiability.lean
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
  - pointing-problem
  - bridge-assumptions
external:
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
  - label: The Value Learning Problem (MIRI)
    url: https://intelligence.org/files/ValueLearningProblem.pdf
  - label: Embedded Agency — Robust Delegation (MIRI)
    url: https://intelligence.org/embedded-agency/
---

This is value/bundle identifiability. In the field it is often called the pointing problem, which also covers construction (how to build a tracker) and preservation (how it keeps tracking); those are not this card. See the [pointing problem](/cards/pointing-problem/) glossary entry. Inverse reinforcement learning is underdetermined: many reward functions fit the same behavior, and separating values from irrationality is still open in CIRL and assistance-game work. Nearby names for the same wall include ELK (does the system report what it knows, or what a human would want to hear?) and reward misspecification under RLHF. If you cannot tell what a system is optimizing for from the evidence you have, later claims about "aligned values" are guessing.

This project's precise bet is **MB2**: behavioral and internal traces are assumed to identify stable [value-bundle](/cards/value-bundle-transport/) geometry well enough to license claims of bundle alignment. The move is not "scalar reward solved," but "replace the flat reward target with measurable bundle geometry." That only helps if the geometry is itself identifiable. Closely related is [bearer import](/cards/mb3-bearer-import/) (MB3), which asks who those values apply to.

**Where agendas agree:** MIRI value learning; CHAI CIRL; Wentworth pointers problem (identification sense); outer alignment "right target." **Where they diverge:** ELK is a latent-readout slice; PreDCA/QACI are peer outer targets; this project splits referent transport to MB3.

Diagnostic evidence shows the failure mode under light instrumentation: bundle drift can be invisible to [correction](/cards/correction-channel-integrity/) handles that are not tracing bearer welfare. That is exactly what this bridge would need to rule out before low-cost measurement is trustworthy.
