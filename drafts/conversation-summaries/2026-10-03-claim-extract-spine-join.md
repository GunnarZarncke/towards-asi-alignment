# 2026-10-03 — Claim-extract spine join

kind: correction
uptake: local

## Trigger
The eight safety-case layers are a simplification of the spine dependency tree. Stay closer to that tree in the chapter and in the assembly. Prefer a graph, at the prose's grain, over the layer longtable.
Prompts: none resolved (paraphrase-only)

## Done
- bookkeeping: `drafts/plans/claim-extract/claim-extract.md` — principle 2 is the four-spine join; a Figure section specifies the chapter graph; the longtable item is replaced by that figure.
- bookkeeping: `drafts/plans/spine/spine.md` 2.0 bullet and `drafts/plans/construct/construct.md` completeness item retargeted from "eight layers" to the join.

## Decisions
- Chapter figure grain is four boxes in chapter words (boundary and measurement, value and transport, correction and successors, selection), with overview edges, a conjunctive join, and `MB11` to `SafeFor`. Bridge ids are edge tags.
- Lean spine graphs stay in Appendix I. The field bridge graph stays on the field overview. Neither is the chapter figure.
- `00-overview.dot`'s `P02` label (seven layers, grounding omitted) is corrected before the chapter cites that figure.
- Lean assembly change (drop `DirectLayerEvidence` / `BridgeDerivedLayerEvidence`) is 2.0, not this prose pass.

## Open / next
- P1 pass on the Ch. 42 change table, including drawing the figure. Not started.
- Source checks in the plan (lab findings, independence examples, `#print axioms`) still open.

## Key paths
- `drafts/plans/claim-extract/claim-extract.md` (Figure section)
- `context/lean_proof_graphs/00-overview.dot`
- `chapters/ch42-safety-case.tex`

## Commits
- none
