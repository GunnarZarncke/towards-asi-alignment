---
leanNodes:
  - nodeId: forgeability_gap
    kind: counterexample
    summary: 'A checked finite counterexample: for any claimed harm bound, there is a toy successor that reads green on every conserved-property check, has measured risk at or below the bound, and yet has hidden harm strictly above it. Passing the score alone is evidence of nothing about the unmeasured remainder.'
    module: AlignmentProofSpine/Forgeability.lean
  - nodeId: MB10_conserved_property_signature_not_forged
    kind: bridge
    summary: A successor-safe step with bounded measured risk also bounds true harm, but only if the conserved-property audit itself was adversarially verifiable up to the successor's capability.
    module: AlignmentProofSpine/Forgeability.lean
  - nodeId: true_harm_bound_of_successor_safe_step
    kind: proof
    summary: Combines the risk-monotonicity theorem for successor-safe steps with MB10 to turn a predecessor's numeric risk bound into a bound on the successor's true harm, not just its measured risk.
    module: AlignmentProofSpine/Forgeability.lean
evidenceNotes:
  - source: formal spine
    finding: open
    summary: 'No experiment scenario yet directly red-teams conserved-property-audit forgeability specifically (as opposed to the individual MB1-MB9 measurement channels). This is a named gap, not a rounding error: ch08 and ch31''s own "What Would Change This View" sections raised the worry that a capable predecessor could engineer a successor to pass every conserved-property check while defecting on whatever was not conserved.'
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/Forgeability.lean
  - source: goal-agent-simulation escalation + twins (F-21)
    finding: bound
    summary: Escalation ladder and twin semantics probe whether audit channels can be gamed without disclosing style — partial stress on measurement forgeability, not full seven-property successor checklist.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/goal-agent-simulation/results/FINDINGS.md
  - source: lab-simulation Phase 8 LLM spot-checks (G-7, G-8)
    finding: open
    summary: Exploratory LLM red-team adapter produced nulls — no systematic deception surface yet — but Phase 8 is not a pre-registered battery. MB10 forgeability of conserved-property audits remains the least probed bridge.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/FINDINGS.md
related:
  - successor-stability
  - conserved-properties-growth-split-merge
  - strategic-opacity
  - certification-under-manipulation
  - mb5-successor-ontology-shift
  - mb7-hidden-capability-and-access
  - bridge-assumptions
external:
  - label: AlignmentProofSpine/Forgeability.lean
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/Forgeability.lean
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
  - label: Tiling Agents (MIRI)
    url: https://intelligence.org/files/TilingAgentsDraft.pdf
  - label: Vingean Reflection (MIRI)
    url: https://intelligence.org/files/VingeanReflection.pdf
  - label: Risks from Learned Optimization
    url: https://arxiv.org/abs/1906.01820
---

In the field this is **Successor Gaming**: a system can pass every audited checklist while defecting on whatever the checklist omits. For successors, the tiling / Vingean worry returns in audit form. A capable predecessor building the next system has incentive and opportunity to forge the checks. Field "deceptive alignment" usually names MB7 (hidden capability under eval); MB10 is the successor certification channel specifically.

The book's precise bet is **MB10**: a successor that reads green on all [seven conserved properties](/cards/conserved-properties-growth-split-merge/) and has bounded measured risk is assumed to have bounded true harm only if the conserved-property audit itself was adversarially verifiable up to the successor's capability. Same MIRI lineage as [MB5](/cards/mb5-successor-ontology-shift/); the book's split is that MB5 is transport and ontology closure, while MB10 asks whether that green checklist is forgeable. Related: [certification under manipulation](/cards/certification-under-manipulation/).

**Where agendas agree:** certification-under-manipulation; measurement/checklist gaming; tiling-line successor-trust worry in audit form. **Where they diverge:** field deceptive alignment / alignment faking usually tags MB7; MB5 = transport composition.

This is not a hedge. The Lean spine has a finite counterexample: "all seven conserved properties hold, and measured risk is bounded" does not by itself bound actual harm. The gap is real and quantitative. Closing it requires the same cost-of-faking-versus-affordable-surplus condition used for verifiability elsewhere. This bridge shares its deceptive-alignment lineage with [MB7](/cards/mb7-hidden-capability-and-access/) and is currently the least experimentally probed in the set.
