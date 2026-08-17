---
leanNodes:
  - nodeId: MB8_cev_process_convergence
    kind: bridge
    summary: "Gravestone — retired matrix bridge. CEV factorizes through AlignmentTarget; not a live route to correction. Legacy axiom kept for the Chokepoint special-case instance only."
    module: AlignmentProofSpine/AlignmentConstruction.lean
  - nodeId: constitutionalTarget
    kind: definition
    summary: CEV constitutional rule → AlignmentTarget (no special CEV→Alignment bridge).
    module: AlignmentProofSpine/AlignmentConstruction.lean
  - nodeId: TargetRealizable
    kind: definition
    summary: Open construction crux — ∃ system realizing a target. Not axiomatized.
    module: AlignmentProofSpine/AlignmentConstruction.lean
  - nodeId: correction_integrity_disjunctive_tolerance_needs_distinct_instruments
    kind: counterexample
    summary: "Gravestone instance: packaging legacy MB8 beside MB6b does not add an independent certificate under a shared instrument. CEV itself is an AlignmentTarget, not that backup arrow."
    module: AlignmentProofSpine/Chokepoint.lean
evidenceNotes:
  - source: toy-simulation diagnostic (T-6)
    scenario: legitimacy_theater
    finding: bound
    summary: Light-handle instrumentation catches about 80% of legitimacy-theater cases; medium and strong handles catch all. Evidence now tags MB4/MB4a (capture resistance), not a separate MB8 column.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/toy-simulation/results/NEGATIVE_RESULTS.md
  - source: goal-agent-simulation board capture (F-22)
    finding: bound
    summary: Board certifier capture switch reproduces captured-vs-not effect — tags MB4/MB4a judge-channel capture.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/goal-agent-simulation/results/FINDINGS.md
related:
  - correction-channel-integrity
  - mb4-correction-legitimacy
  - mb4a-measured-path-legitimacy
  - specify-cev
  - construct-cev
  - alignment-target
  - bridge-assumptions
external:
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
  - label: Coherent Extrapolated Volition (MIRI)
    url: https://intelligence.org/files/CEV.pdf
---

**Gravestone — MB8 retired from the field matrix (Krym Phase 5).**

Opening the CEV black box showed that volition, referent, extrapolation, coherence, correction, and preservation largely map onto existing TSA bridges (MB2–MB4, MB3, grounding, successors). What remains of CEV is a **constitutional rule** parameterizing an `AlignmentTarget`, not an independent `CEV → Alignment` bridge.

In Lean (`AlignmentConstruction.lean`):

- `ConstitutionalRule` + `cevConstitution` → `constitutionalTarget`
- `Realizes` / `TargetRealizable` — open **construction** crux (not axiomatized)
- `CertifiedAsRealizing` — separate **certification** claim

The legacy axiom `MB8_cev_process_convergence` is kept only for the Chokepoint special-case instance (why a packaged backup arrow is not independent under a shared instrument). It is **not** in `BridgeAssumptions` or the live certification derive path.

**Where agendas agreed:** MIRI CEV process/legitimacy language. **Where this project diverges:** live path is [MB4](/cards/mb4-correction-legitimacy/) + [MB4a](/cards/mb4a-measured-path-legitimacy/); legitimacy theater diagnostics tag capture resistance there, not a separate matrix column.

For the old summary of what MB8 used to claim, see git history of this card before Phase 5.
