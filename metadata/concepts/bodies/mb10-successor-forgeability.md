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
  - bridge-assumptions
  - mb5-successor-ontology-shift
external:
  - label: AlignmentProofSpine/Forgeability.lean
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/Forgeability.lean
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
---

The seven conserved properties (boundary closure, memory lineage, value-bundle response geometry, bearer-map continuity, correction-channel capacity, transparency policy, control-locus continuity) are the book's successor checklist. MB10 names what that checklist cannot do on its own: a predecessor capable enough to build a successor could, in principle, build one that reads green on every check while routing harm through whatever the checklist does not cover.

This is not a hedge added for caution. It is a checked finite counterexample: the Lean spine proves that "all seven conserved properties hold, and measured risk is bounded" does not, by itself, bound the successor's actual harm. The gap is real and quantitative, not a vague worry.

MB10 is the bridge that would close it: the conserved-property audit channel itself must be adversarially verifiable up to the successor's capability — the same cost-of-faking-versus-affordable-surplus condition used for verifiability elsewhere in the book — before a passing score counts as evidence against a capable adversarial predecessor. This bridge shares its deceptive-alignment lineage with MB7, and it is currently the least experimentally probed bridge in the set.
