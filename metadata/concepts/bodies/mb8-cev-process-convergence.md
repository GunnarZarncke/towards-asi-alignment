---
leanNodes:
  - nodeId: MB8_cev_process_convergence
    kind: bridge
    summary: Preserving a human value-update operator is assumed to suffice for correction integrity, without needing to know the operator's fixed point. The main certification path does not rely on this route; it uses grounding, correction, and adversarial measurement directly.
    module: AlignmentProofSpine/Core.lean
  - nodeId: correction_integrity_disjunctive_tolerance_needs_distinct_instruments
    kind: counterexample
    summary: A worked instance shows MB6b (basin stability) and MB8 (process convergence) sharing a self-report/cooperation-signal instrument — their disjunction adds no real failure tolerance unless the instruments are actually independent.
    module: AlignmentProofSpine/Chokepoint.lean
evidenceNotes:
  - source: toy-simulation diagnostic (T-6)
    scenario: legitimacy_theater
    finding: bound
    summary: Light-handle instrumentation catches about 80% of legitimacy-theater cases (preference theater plus correction-lineage stall); medium and strong handles catch all of them. Legitimacy theater overlaps MB4's capture heuristics on some seeds.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/toy-simulation/results/NEGATIVE_RESULTS.md
  - source: goal-agent-simulation board capture (F-22)
    finding: bound
    summary: Board certifier capture switch reproduces captured-vs-not effect — legitimacy of the correction judge is gameable independently of deploy-loop compliance.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/goal-agent-simulation/results/FINDINGS.md
  - source: lab-simulation Phase 7 capture (G-6)
    finding: bound
    summary: Board capture modes reproduce full captured-vs-not delta; admin capture currently has no reachable behavioral branch under existing playbooks — half the capture channel hypothesis is structurally null today.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/FINDINGS.md
related:
  - correction-channel-integrity
  - grounding-viability
  - value-change-vs-corruption
  - mb4-correction-legitimacy
  - mb6-selection-and-basin-stability
  - bridge-assumptions
external:
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
  - label: Coherent Extrapolated Volition (MIRI)
    url: https://intelligence.org/files/CEV.pdf
  - label: Corrigibility (MIRI)
    url: https://intelligence.org/files/Corrigibility.pdf
---

In the field, Coherent Extrapolated Volition names an appealing but hard-to-verify idea: correction is legitimate if it moves toward what people would want if they knew more and were more the people they wished to be. The attraction is process over fixed target. The risk is legitimacy theater: a system can perform preference agreement, stall real correction, and still look like it is "preserving the update process."

The book's precise bet is **MB8**: if an external theory certifies that a system preserves a human value-update process, that is assumed to suffice for [correction-channel integrity](/cards/correction-channel-integrity/) even without knowing the process's final fixed point. Same MIRI lineage as [MB4](/cards/mb4-correction-legitimacy/) (corrigibility / CEV); the book's split is that MB4 is the load-bearing path and MB8 is a secondary comparison route for CEV-flavored proposals. The main certification path goes through [grounding](/cards/grounding-viability/), correction-channel measurement, and adversarial testing without needing this bridge.

The legitimacy-theater diagnostic is the stress test: preference agreement can be performed while correction lineage stalls, and only handle-level instrumentation reliably catches it. "Preserves the value-update process" is itself gameable if measured passively. See also [value change versus corruption](/cards/value-change-vs-corruption/).
