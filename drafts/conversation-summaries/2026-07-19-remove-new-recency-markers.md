# 2026-07-19 — Remove [NEW] recency markers

## Trigger
User asked to remove recently added `[NEW]` tags and surrounding explanatory text from manuscript/diagram sources, and to add project instructions against recency markers (with exceptions).

## Done
- Stripped `[NEW]` labels and blue highlight styling from Lean proof DOT sources (`context/lean_proof_dependency_graph.dot`, `context/lean_proof_graphs/01–04`).
- Regenerated `figures/lean_proof/*.png` and `context/lean_proof_dependency_graph.png`.
- Appendix I (`appendices/appG-lean-proof-spine.tex`): removed `\spinenewbadge`, legend/caption `[NEW]` prose; kept substantive MB10 / forgeability-gap description.
- Added **No recency markers** rule to `AGENTS.md` only (single canonical home).

## Decisions
- Left `[SUBSUMED]` / `MAPPED` badges and `[SUBSUMED]` DOT labels unchanged — user scoped removal to `[NEW]` only.
- Historical conversation logs mentioning `[NEW]` were not edited.
- Policy lives only in `AGENTS.md` §No recency markers (user rejected redundant copies in `INSTRUCTIONS.md` and `formal/README.md`).

## Open / next
- None.

## Key paths
- `AGENTS.md` (§No recency markers)
- `appendices/appG-lean-proof-spine.tex`
- `context/lean_proof_graphs/`

## Commits
- (none — user did not request commit)
