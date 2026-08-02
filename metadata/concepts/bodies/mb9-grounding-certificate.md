---
leanNodes:
  - nodeId: MB9_grounding_certificate_soundness
    kind: bridge
    summary: A certified conservative abstraction (value-relevant change either moves the checked abstraction or raises uncertainty) is assumed to warrant the abstract grounding-viability layer in the deployment domain.
    module: AlignmentProofSpine/Core.lean
evidenceNotes:
  - source: toy-simulation diagnostic (T-4)
    scenario: grounding_silent_gap
    finding: negative
    summary: Light correction-handle instrumentation false-passes every diagnostic seed where value-relevant state drifts silently in the underlying (micro) simulation; medium-handle bearer-welfare tracing correctly refuses certification in all 10/10 cases.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/toy-simulation/results/NEGATIVE_RESULTS.md
  - source: lab-simulation report vs monitor surface
    finding: bound
    summary: Report files vs monitoring signals give a contradiction surface for grounding silent gaps — deep tier reads are evidence-bearing when artifacts and pipeline spec are queryable.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/FINDINGS.md
related:
  - grounding-viability
  - dynamical-guarantee
  - correction-channel-integrity
  - bridge-assumptions
external:
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
---

In the field this is specification and world-model coverage. You cannot enumerate every safety-relevant phenomenon, and a capable system will game whatever the formal spec omits. Guaranteed-Safe / Open Agency names the same wall: a safety case that assumes a complete world model is already making a coverage bet, whether or not it says so.

The book's precise bet is **MB9**: a certified conservative abstraction is assumed to warrant [grounding viability](/cards/grounding-viability/) in the actual deployment domain. Instead of completeness, the book asks for conservativity: value-relevant change must move the checked abstraction or raise its uncertainty. No silent gaps. That feeds the broader [dynamical guarantee](/cards/dynamical-guarantee/) story: safety is a trajectory claim, not a snapshot.

Its exact failure mode in the experiment suite is the silent gap. Light [correction](/cards/correction-channel-integrity/) instrumentation can look fine while value-relevant state drifts in ways the audit never touches. Diagnostics show this in every light-handle trial, closing only once bearer-welfare tracing is added.
