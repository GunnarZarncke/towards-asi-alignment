---
leanNodes:
  - nodeId: gsaiConstructionBet
    kind: definition
    summary: GSAI spec-relative formal builder bet.
    module: AlignmentProofSpine/AlignmentConstruction.lean
  - nodeId: ConstructionCrux
    kind: definition
    summary: Open ∃ builder crux for gsaiConstitution target.
    module: AlignmentProofSpine/AlignmentConstruction.lean
related:
  - specify-gsai
  - field-agendas/davidad-guaranteed-safe-ai-gsai
  - target-realization
  - mb11-deployment-safety
external:
  - label: Dalrymple et al. 2024
    url: https://arxiv.org/abs/2405.06624
---

# Construct — GSAI spec-relative builder

**Lean bet:** `gsaiConstructionBet` with `claimsExplicitBuilder = true`.

GSAI's constructive program: build and certify systems **relative to an explicit spec and world model** (constructivist safety case). That is the associated construction bet for `gsaiConstitution`.

Discharging `ConstructionCrux` still requires showing a real system **Realizes** the target — not merely that a safety-case schema can be written (`fin_certification_without_construction`).

**Field table:** [/field/v2/#specify-construct-instances](/field/v2/#specify-construct-instances).
