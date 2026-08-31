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
  - nodeId: "DeploymentOk"
    kind: "definition"
    summary: "Uninterpreted pause ∨ recovery-on-distinct-instrument. Not an MB; no arrow to Safe."
    module: "AlignmentProofSpine/AlignmentRegime.lean"
  - nodeId: "AlignmentDeployment"
    kind: "definition"
    summary: "DeploymentOk ∨ (certified case ∧ tolerance). Only the certify disjunct feeds MB11 / Safe."
    module: "AlignmentProofSpine/Certification.lean"
  - nodeId: "fin_pause_ok_not_certified"
    kind: "counterexample"
    summary: "Finite flags — pause can hold while a toy certify flag is false. Abstract Safe is an axiom, so the split is not stated on System."
    module: "AlignmentProofSpine/AlignmentRegime.lean"
external:
  - label: "Krym architecture revision plan (Phase 5–6)"
    url: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/drafts/attic/krym-architecture-revision-plan.md"
related:
  - "pointing-problem"
  - "alignment-target"
  - "specify-cev"
  - "specify-constitutional-ai"
  - "specify-gsai"
  - "construct-constitutional-ai"
  - "construct-gsai"
  - "mb2-bundle-identifiability"
  - "mb4-correction-legitimacy"
  - "mb8-cev-process-convergence"
  - "bridge-assumptions"
---

**Lifecycle role:** construct (open spine interface — not an `MB*` matrix column).

Given an alignment target $P$, can we **construct** a system $A$ that robustly tracks $P$? This is distinct from:

- **Identification** (what is $P$? — MB2 / bundle identifiability)
- **Certification** (does evidence license that $A$ tracks $P$? — safety-case layers, `CertifiedAsRealizing`)

Lean types the separation in `AlignmentConstruction.lean`: `Realizes` vs `CertifiedAsRealizing`; `ConstructionCrux` / `TargetRealizable` is **not** axiomatized. `fin_certification_without_construction` exhibits that a certification schema can be satisfied while no finite toy realizes the target.

CEV is not a special bridge: `constitutionalTarget` / `cevConstitution` parameterize an `AlignmentTarget` on the same interface (MB8 is a gravestone only).

Pause and recovery-viable (`DeploymentOk`) are a **regime** on whether certification must be a pre-deployment case. `AlignmentDeployment` in `Certification.lean` is that disjunction or a certified case within tolerance; only the certify disjunct is consumed by `MB11`. `fin_pause_ok_not_certified` exhibits pause without a toy certify flag. They are not a construction method and not an arrow to `Safe`.

**Book:** introduction (four questions); ch33 (certification without construction); ch05 Recover; ch14 pause/stop. **Lifecycle:** [Alignment lifecycle](/cards/alignment-lifecycle/) (construct phase). **Field evidence:** [/field/coverage/](/field/coverage/).
