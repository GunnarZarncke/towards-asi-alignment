---
title: "Target Realization"
type: "concept"
status: "framework"
summary: "Open construct-lifecycle crux — given target P, can we build a system that tracks P? Lean model only (ConstructionCrux); not an MB bridge."
bookChapters:
  - "ch33"
bookLabels:
  - "ch:certification-without-construction"
  - "sec:construction-demand-ch33"
leanNodes:
  - nodeId: "ConstructionCrux"
    kind: "definition"
    summary: "Open construction crux — ∃ system realizing an AlignmentTarget. Not axiomatized; not an MB bridge."
    module: "AlignmentProofSpine/AlignmentConstruction.lean"
  - nodeId: "TargetRealizable"
    kind: "definition"
    summary: "Alias for ConstructionCrux — some system realizes the target."
    module: "AlignmentProofSpine/AlignmentConstruction.lean"
  - nodeId: "Realizes"
    kind: "definition"
    summary: "System A realizes target P when required spine layers hold for P's slots."
    module: "AlignmentProofSpine/AlignmentConstruction.lean"
  - nodeId: "CertifiedAsRealizing"
    kind: "definition"
    summary: "Certification claim (epistemic); distinct from Realizes. fin_certification_without_construction separates schema from construction."
    module: "AlignmentProofSpine/AlignmentConstruction.lean"
  - nodeId: "fin_certification_without_construction"
    kind: "counterexample"
    summary: "Finite witness — certification schema can hold while no toy realizes the target."
    module: "AlignmentProofSpine/AlignmentConstruction.lean"
external:
  - label: "Krym architecture revision plan (Phase 5–6)"
    url: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/drafts/krym-architecture-revision-plan.md"
related:
  - "pointing-problem"
  - "mb2-bundle-identifiability"
  - "mb4-correction-legitimacy"
  - "mb8-cev-process-convergence"
  - "bridge-assumptions"
---

# Target Realization

**Lifecycle role:** construct (open spine interface — not an `MB*` matrix column).

Given an alignment target $P$, can we **construct** a system $A$ that robustly tracks $P$? This is distinct from:

- **Identification** (what is $P$? — MB2 / bundle identifiability)
- **Certification** (does evidence license that $A$ tracks $P$? — safety-case layers, `CertifiedAsRealizing`)

Lean types the separation in `AlignmentConstruction.lean`: `Realizes` vs `CertifiedAsRealizing`; `ConstructionCrux` / `TargetRealizable` is **not** axiomatized. `fin_certification_without_construction` exhibits that a certification schema can be satisfied while no finite toy realizes the target.

CEV is not a special bridge: `constitutionalTarget` / `cevConstitution` parameterize an `AlignmentTarget` on the same interface (MB8 is a gravestone only).

**Book:** introduction (three questions); ch33 (certification without construction). **Field preview:** `/field/v2/`.
