# 2026-06-25 — Lean dependency graph sync

## Trigger
User asked to update the Lean dependency diagram after recent spine changes (handle correction, DeploymentMass/P31, tripwire removal).

## Done
- Rewrote `context/lean_proof_dependency_graph.dot` so node IDs match `formal/AlignmentProofSpine/*.lean` theorem names.
- Removed obsolete tripwire P39 node; P40 connects directly to P30.
- Updated P31 label to DeploymentMass selection counterexample; P23/P24 to handle-controlled correction; P44 for legitimacy (was mislabeled P39 in old graph).
- Regenerated `context/lean_proof_dependency_graph.png`.
- Updated `formal/README.md` and `metadata/source-canon.md` to note graph/Lean ID alignment.

## Decisions
- Replaced conjectural alternate numbering with Lean/brief-aligned P01–P45 layout.
- Kept auxiliary nodes (P09A, P09K, P36M, P43H, P30T) for lemmas without dedicated P numbers.

## Open / next
- Optional: update `LeanProofSpineImplementationBrief.md` §4 to drop P39 tripwire reference.

## Key paths
- `context/lean_proof_dependency_graph.dot`
- `context/lean_proof_dependency_graph.png`

## Commits
- `c4725b6` Refine fitness and proof-spine diagrams for the book appendix.
