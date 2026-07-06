---
title: "MB9 — Grounding Certificate Soundness"
type: "bridge"
status: "bridge"
summary: "A certified conservative abstraction is assumed to warrant grounding viability in the actual deployment domain."
decision: "Before trusting a safety case's grounding claim, ask whether the checked abstraction actually moves when value-relevant reality changes, or whether it can stay silent while something important drifts."
evidence: "Evidence would include tests that inject value-relevant change into a deployment and confirm the checked abstraction either moves or its uncertainty rises — no silent gaps."
bookChapters: ["ch03", "ch47"]
leanNodes:
  - nodeId: "MB9_grounding_certificate_soundness"
    kind: "bridge"
    summary: "A certified conservative abstraction (value-relevant change either moves the checked abstraction or raises uncertainty) is assumed to warrant the abstract grounding-viability layer in the deployment domain."
    module: "AlignmentProofSpine/Core.lean"
evidenceNotes:
  - source: "toy-simulation diagnostic (T-4)"
    scenario: "grounding_silent_gap"
    finding: "negative"
    summary: "Light correction-handle instrumentation false-passes every diagnostic seed where value-relevant state drifts silently in the underlying (micro) simulation; medium-handle bearer-welfare tracing correctly refuses certification in all 10/10 cases."
    resultsPath: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/toy-simulation/results/NEGATIVE_RESULTS.md"
  - source: "lab-simulation report vs monitor surface"
    finding: "bound"
    summary: "Report files vs monitoring signals give a contradiction surface for grounding silent gaps — deep tier reads are evidence-bearing when artifacts and pipeline spec are queryable."
    resultsPath: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/FINDINGS.md"
related: ["grounding-viability", "bridge-assumptions"]
external:
  - label: "Bridges and the Field: A Crosswalk (appendix source)"
    url: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex"
---

The Guaranteed-Safe/Open Agency program names the same open problem this bridge inherits: a formal specification and world model cannot enumerate every safety-relevant phenomenon, and a system will game whatever the spec omits. The book's answer is to demand conservativity instead of completeness — value-relevant change must move the checked abstraction or raise its uncertainty, rather than pass through silently.

MB9 is the assumption that a certificate of this conservative-abstraction property, in practice, actually warrants grounding viability in the deployment domain the system runs in. It is a coverage bet, not a coverage guarantee.

Its exact failure mode has a name in the experiment suite: the "silent gap." Light correction instrumentation can look fine while value-relevant state drifts in ways the audit never touches — the diagnostic evidence shows this happening in every light-handle trial and closing only once bearer-welfare tracing is added.
