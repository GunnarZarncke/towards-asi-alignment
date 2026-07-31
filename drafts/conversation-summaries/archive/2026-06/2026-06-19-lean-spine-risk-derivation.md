# 2026-06-19 — Lean spine strengthen + risk derivation

## Trigger
Return to formalization: note toy proof status, add `lean_proof_dependency_graph.dot`
to source map, add TODO to strengthen proofs, implement critical review point #1
(derive risk bound rather than assume `hrisk`).

## Done
- **`Risk` redefined** in `Capability.lean` as `RiskGap` (`Control − CorrectionCapacity`); removed `axiom Risk` from `Core.lean`.
- **Critical point #1:** added `P13_risk_gap_bounded_by_capacity_slack`,
  `risk_le_delta_of_capacity_slack`, `SpineRiskWitness`, and primary certification
  theorems `P30_certified_class_safety_derived`, `certified_class_safety_spine_derived`,
  `certified_class_safety_from_spine_and_bridges` — conclusion derived from
  `Control A ≤ CorrectionCapacity A + δ`, not bare `hrisk`. Legacy theorems kept.
- **`metadata/source-canon.md`:** book-local note + `formal/` artifact table including
  `context/lean_proof_dependency_graph.dot`.
- **`metadata/TODO.md`:** new § Lean proof spine with toy-status note and three
  strengthening tasks (full chain, manuscript wiring).
- **`formal/README.md`:** toy vs target section, risk derivation note, updated module blurb.
- `lake build` green; no `sorry`/`admit`; `#print axioms certified_class_safety_spine_derived`
  shows no `MB*` (only `Control`/`CorrectionCapacity` + standard props).

## Decisions
- Capacity slack is the first derived link in the certification chain; BIQ ceiling,
  correction weakest-link, and successor-chain propagation left for TODO (honest
  partial fix for #1).
- Legacy `certified_class_safety_spine` / `certified_class_safety_from_bridges` with
  explicit `hrisk` retained for interface compatibility.

## Open / next
- Extend derivation: BIQ (`P10`) → control ceiling → gap bound; weakest-link
  (`P24`) tying `CorrectionCapacity` to graph; successor-safe chain via `P27`.
- Strengthen counterexamples off bare `Bool` toys.
- Not committed.

## Key paths
- `formal/AlignmentProofSpine/Capability.lean`, `Certification.lean`, `Core.lean`
- `metadata/source-canon.md`, `metadata/TODO.md`, `formal/README.md`

## Commits
- none
