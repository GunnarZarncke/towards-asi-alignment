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
  - bridge-assumptions
  - mb6-selection-and-basin-stability
external:
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
---

Coherent Extrapolated Volition names an appealing but hard-to-verify idea: correction is legitimate if it moves toward what people would want if they knew more and were more the people they wished to be. MB8 is the narrow formal version of that appeal — if some external theory certifies that a system preserves the right value-update process, that is enough for correction integrity, even without pinning down what the process converges to.

The book is explicit that this is not the load-bearing route. The main certification path goes through grounding, correction-channel measurement, and adversarial testing directly, without needing this bridge. MB8 exists mainly as a comparison point for readers evaluating CEV-flavored proposals.

The legitimacy-theater diagnostic is the relevant stress test: a system can perform preference agreement and stall correction lineage while looking compliant, and only handle-level instrumentation reliably catches it — a reminder that "preserves the value-update process" is itself gameable if measured passively.
