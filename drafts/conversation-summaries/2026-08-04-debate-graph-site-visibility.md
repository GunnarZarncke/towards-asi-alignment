# 2026-08-04 — Debate graph + site visibility

## Trigger
Reviewer feedback: field-subsumption graph had no `FINITE → DEB` edge; DEB node page showed interface toys only, wrong GitHub path, misleading Mathlib note; DebateGame work invisible.

## Done
- **`05-field-subsumptions.dot`:** `FINITE → DEB (DebateGame)` plus missing finite edges for CIRL, INT, ELK; FINITE folder label expanded; DEB/ELK node labels lead with rederived theorems.
- **`03-correction-successors.dot`, `lean_proof_dependency_graph.dot`:** FDEB labels updated to debate-game theorems.
- **`lean_graph_node_aliases.json`:** DEB/FDEB → `debate_tracks_truth`, `erring_judge_flips_debate`, separation; ELK → `elk_reporter_nonidentifiability`.
- **`subsumption-debate.md` + projection card:** DebateGame leanNodes; removed stale "native matching deferred" prose.
- **`/lean/check/debate/`:** new check page + hero button on `/lean/`.
- **`LeanSpineSource.astro`:** Mathlib note calibrated (core Mathlib-free; Field/Finite may import).
- **`figures/lean_proof/05-field-subsumptions.png`:** regenerated from dot.

## Verification
- `npm run sync:projections`, `sync:lean-checks`, `sync:lean-spine`, `npm run build` — 858 pages; `/lean/node/DEB/`, `/lean/check/debate/` present.
- DEB node source: `formal/AlignmentProofSpine/Field/Finite/DebateGame.lean`.
