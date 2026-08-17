---
title: "Alignment Target"
type: "concept"
status: "framework"
summary: "Open specify-lifecycle interface — ConstitutionalRule → AlignmentTarget; field programs are instances, not extra MB columns. SpecifyCrux is a placeholder."
bookChapters:
  - "ch01"
  - "ch28"
bookLabels:
  - "sec:pointing-problem"
leanNodes:
  - nodeId: "AlignmentTarget"
    kind: "definition"
    summary: "Minimal alignment target — correction-channel and bundle-structure slots."
    module: "AlignmentProofSpine/AlignmentConstruction.lean"
  - nodeId: "ConstitutionalRule"
    kind: "definition"
    summary: "Specify-side schema — constituency, extrapolation, aggregation, plus field-family flags."
    module: "AlignmentProofSpine/AlignmentConstruction.lean"
  - nodeId: "constitutionalTarget"
    kind: "definition"
    summary: "Maps a ConstitutionalRule to an AlignmentTarget."
    module: "AlignmentProofSpine/AlignmentConstruction.lean"
  - nodeId: "SpecWellFormedness"
    kind: "definition"
    summary: "Uninterpreted well-formedness placeholder — never axiomatized in this development."
    module: "AlignmentProofSpine/AlignmentConstruction.lean"
  - nodeId: "SpecifyCrux"
    kind: "definition"
    summary: "TargetSpecifiable alias — open specify-phase crux; explicit hypothesis only."
    module: "AlignmentProofSpine/AlignmentConstruction.lean"
external:
  - label: "Field hub — specify / construct table"
    url: "/field/v2/#specify-construct-instances"
related:
  - "target-realization"
  - "pointing-problem"
  - "specify-cev"
  - "specify-constitutional-ai"
  - "specify-gsai"
  - "specify-institutional"
  - "mb8-cev-process-convergence"
---

# Alignment Target (specify interface)

**Lifecycle role:** specify (open spine interface — not an `MB*` matrix column).

State a coherent **alignment target** by filling a `ConstitutionalRule` and mapping it to an `AlignmentTarget` via `constitutionalTarget`. Field programs (CEV residue, Constitutional AI, GSAI, institutional constitutions) are **instances** of that schema — not separate bridges.

**Well-formedness is out of scope here.** `SpecWellFormedness` / `SpecifyCrux` type the missing criteria (non-vacuity, aggregation coherence, legitimacy) as an **uninterpreted placeholder**. Theorems that need it take `hSpec : SpecifyCrux W C` explicitly; this project does not discharge outer-alignment philosophy.

**Distinct from MB2:** identification asks what values are *in* a deployed system; specify asks whether the *stated* target is coherent enough to parameterize construction and certification.

**Field hub:** [specify / construct instance table](/field/v2/#specify-construct-instances).
