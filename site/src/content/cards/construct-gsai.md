---
title: "Construct — GSAI spec-relative builder"
type: "concept"
status: "framework"
summary: "GSAI constructivist safety-case / spec-relative builder (gsaiConstructionBet)."
bookChapters:
  - "ch33"
leanNodes:
  - nodeId: "gsaiConstructionBet"
    kind: "definition"
    summary: "GSAI spec-relative formal builder bet."
    module: "AlignmentProofSpine/AlignmentConstruction.lean"
  - nodeId: "ConstructionCrux"
    kind: "definition"
    summary: "Open ∃ builder crux for gsaiConstitution target."
    module: "AlignmentProofSpine/AlignmentConstruction.lean"
external:
  - label: "Dalrymple et al. 2024"
    url: "https://arxiv.org/abs/2405.06624"
related:
  - "specify-gsai"
  - "field-agendas/davidad-guaranteed-safe-ai-gsai"
  - "target-realization"
  - "mb11-deployment-safety"
---

**Lean bet:** `gsaiConstructionBet` with `claimsExplicitBuilder = true`.

GSAI's constructive program: build and certify systems **relative to an explicit spec and world model** (constructivist safety case). That is the associated construction bet for `gsaiConstitution`.

Discharging `ConstructionCrux` still requires showing a real system **Realizes** the target — not merely that a safety-case schema can be written (`fin_certification_without_construction`).

**Instance table:** [/cards/alignment-target/#specify-construct-instances](/cards/alignment-target/#specify-construct-instances).
