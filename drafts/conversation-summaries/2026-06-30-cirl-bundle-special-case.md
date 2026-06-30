# 2026-06-30 — CIRL bundle special case

## Trigger
User clarified that the goal was not a meta theorem-schema wrapper, but an object-level proof that scalar-reward CIRL is a special case of bundle inference in a shared finite domain.

## Done
- Added `BundleInferenceFromPolicy` and `ScalarCIRLInference` to `formal/AlignmentProofSpine/Bundles.lean`.
- Proved `scalar_cirl_is_one_dimensional_bundle_inference`: scalar CIRL over `PolicyProfile ... 1` is equivalent to bundle inference with a constant `Fin 1 -> Int` weight vector.
- Exposed the theorem as `cirl_scalar_is_bundle_inference` in `formal/AlignmentProofSpine/Field/CIRL.lean`.
- Updated `cirl_field_result_records` so the CIRL finite rederivation ledger includes the new exact special-case theorem alongside the existing non-converse separation.
- Updated Appendix I and Lean graph labels to point at `cirl_scalar_is_bundle_inference`; regenerated proof graph PNGs.

## Decisions
- Kept the existing `cirl_subsumption_transport` theorem, but stopped treating it as the main CIRL subsumption claim. The stronger book-facing claim is now: scalar-reward CIRL is exactly `k=1` bundle inference in the finite `PolicyProfile` model.
- Did not attempt to reprove the Hadfield-Menell CIRL assistance-game theorem. It remains an imported field handle; the new proof covers the shared finite/formula fragment.

## Open / next
- Repeat this object-level "shared-domain special case" treatment for other field agendas where the current Lean layer is still mostly a wrapper or separation.
- If editing Chapter 20 or Appendix I again, consider adding a local `\leanspine{}` citation to `cirl_scalar_is_bundle_inference`.

## Key paths
- `formal/AlignmentProofSpine/Bundles.lean`
- `formal/AlignmentProofSpine/Field/CIRL.lean`
- `appendices/appG-lean-proof-spine.tex`
- `context/lean_proof_graphs/02-value-transport.dot`
- `context/lean_proof_graphs/05-field-subsumptions.dot`
- `context/lean_proof_dependency_graph.dot`

## Commits
- None.

## Verification
- `lake -d formal build` passed.
- `./scripts/render_lean_graphs.sh && lake -d formal build` passed.
- IDE diagnostics reported no linter errors for edited Lean / Appendix I files.
