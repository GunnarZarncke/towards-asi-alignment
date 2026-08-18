---
title: "Construct — RLAIF / Constitutional AI"
type: "concept"
status: "framework"
summary: "RLAIF principles-as-feedback as caiConstructionBet; catalog builder claim ≠ ConstructionCrux discharge."
bookChapters:
  - "ch21"
leanNodes:
  - nodeId: "caiConstructionBet"
    kind: "definition"
    summary: "RLAIF / principles-as-feedback construction bet."
    module: "AlignmentProofSpine/AlignmentConstruction.lean"
  - nodeId: "fin_claimed_builder_without_realization"
    kind: "counterexample"
    summary: "claimsExplicitBuilder = true does not imply FinRealizes — catalog ≠ construction."
    module: "AlignmentProofSpine/AlignmentConstruction.lean"
external:
  - label: "Bai et al. 2022"
    url: "https://arxiv.org/abs/2212.08073"
related:
  - "specify-constitutional-ai"
  - "field-agendas/anthropic-lab"
  - "target-realization"
  - "mb2-bundle-identifiability"
---

**Lean bet:** `caiConstructionBet` with `claimsExplicitBuilder = true`.

The agenda's constructive hypothesis: train models with **principles-as-feedback** (RLAIF) so the resulting system tracks the stated constitution. That is an explicit builder claim in the catalog sense.

`fin_claimed_builder_without_realization` separates **catalog flags** from **`ConstructionCrux`**: a claimed builder does not discharge the open ∃-system crux.

**Instance table:** [/cards/alignment-target/#specify-construct-instances](/cards/alignment-target/#specify-construct-instances).
