---
leanNodes:
  - nodeId: cevConstitution
    kind: definition
    summary: CEV as ConstitutionalRule instance (all three core flags true).
    module: AlignmentProofSpine/AlignmentConstruction.lean
  - nodeId: cevSpecifyConstruct
    kind: definition
    summary: Paired specify + construction bet for CEV.
    module: AlignmentProofSpine/AlignmentConstruction.lean
related:
  - alignment-target
  - construct-cev
  - field-agendas/miri
  - mb8-cev-process-convergence
  - target-realization
external:
  - label: Yudkowsky, CEV (2004)
    url: https://intelligence.org/files/CEV.pdf
---

**Lean instance:** `cevConstitution` → `constitutionalTarget cevConstitution` (correction channel + bundle structure both required).

After factorizing CEV onto MB2–MB4 and preservation bridges, what remains is a **constitutional rule** — constituency, extrapolation, aggregation — not a live `CEV → CorrectionIntegrity` bridge (MB8 gravestone).

**Construction bet:** [CEV construction](/cards/construct-cev/) — `cevConstructionBet` with `claimsExplicitBuilder = false` (no named builder in the original writeup).

**Instance table:** [/cards/alignment-target/#specify-construct-instances](/cards/alignment-target/#specify-construct-instances).
