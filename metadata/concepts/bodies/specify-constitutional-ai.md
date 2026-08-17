---
leanNodes:
  - nodeId: caiConstitution
    kind: definition
    summary: Constitutional AI / RLAIF as ConstitutionalRule instance.
    module: AlignmentProofSpine/AlignmentConstruction.lean
  - nodeId: caiSpecifyConstruct
    kind: definition
    summary: Paired specify + construction bet for Constitutional AI.
    module: AlignmentProofSpine/AlignmentConstruction.lean
related:
  - alignment-target
  - construct-constitutional-ai
  - field-agendas/anthropic-lab
  - mb2-bundle-identifiability
  - target-realization
external:
  - label: Bai et al. 2022 (Constitutional AI)
    url: https://arxiv.org/abs/2212.08073
---

# Specify — Constitutional AI

**Lean instance:** `caiConstitution` (constituency, extrapolation, aggregation all true).

Anthropic's Constitutional AI states **principles** (the constitution) and iterates training with AI-generated feedback (RLAIF). The specify-side content is the principle set and who they apply to; extrapolation and multi-value structure are flagged true in Lean to match the correction-channel and bundle slots on the resulting `AlignmentTarget`.

**Construction bet:** [RLAIF stack](/cards/construct-constitutional-ai/) — `caiConstructionBet` with `claimsExplicitBuilder = true`.

Matrix evidence on this agenda often tags **identify/certify** (MB2, MB7) rather than a specify column — the table separates schema placement from where field evidence landed.

**Field table:** [/field/v2/#specify-construct-instances](/field/v2/#specify-construct-instances).
