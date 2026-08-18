---
title: "Specify — GSAI / Open Agency"
type: "concept"
status: "framework"
summary: "gsaiConstitution instance — openWorldCoverage flag; paired with spec-relative builder."
bookChapters:
  - "ch33"
leanNodes:
  - nodeId: "gsaiConstitution"
    kind: "definition"
    summary: "GSAI / Open Agency spec as ConstitutionalRule (openWorldCoverage = true)."
    module: "AlignmentProofSpine/AlignmentConstruction.lean"
  - nodeId: "gsaiSpecifyConstruct"
    kind: "definition"
    summary: "Paired specify + construction bet for GSAI."
    module: "AlignmentProofSpine/AlignmentConstruction.lean"
external:
  - label: "Dalrymple et al. 2024 (GSAI)"
    url: "https://arxiv.org/abs/2405.06624"
related:
  - "alignment-target"
  - "construct-gsai"
  - "field-agendas/davidad-guaranteed-safe-ai-gsai"
  - "mb9-grounding-certificate"
  - "target-realization"
---

**Lean instance:** `gsaiConstitution` — `openWorldCoverage = true`, `extrapolation = false`, `aggregation = true`.

Guaranteed-Safe AI centers an explicit **specification plus world model** and treats open-world **coverage** as the central wall. Lean flags `openWorldCoverage` to distinguish this family from CEV-style extrapolation (the AlignmentTarget does not require a correction-channel slot via the extrapolation flag).

Completeness of the spec is a **cousin of MB9** (conservativity vs completeness); not the same crux.

**Construction bet:** [spec-relative formal builder](/cards/construct-gsai/) — `gsaiConstructionBet`.

**Instance table:** [/cards/alignment-target/#specify-construct-instances](/cards/alignment-target/#specify-construct-instances).
