# 2026-06-29 — Field subsumptions implementation

## Trigger
User asked to implement the plan for deeper field-result subsumptions: add a Lean folder/package structure, cite imported theorem handles, improve finite rederivations, update Appendix I math/presentation, and use final theorem nodes in dependency diagrams.

## Done
- Added `formal/AlignmentProofSpine/Field.lean` and `formal/AlignmentProofSpine/Field/`:
  - `Common.lean`: `FieldAgendaTag`, `FieldResultStatus`, `FieldProjection`, `SubsumedForward`, `SeparatedFrom`, `ImportedFieldTheorem`, `FieldResultRecord`.
  - `Finite/Basic.lean`, `Finite/MDP.lean`, `Finite/Weights.lean`, `Finite/Reachability.lean`, `Finite/Contraction.lean`: no-Mathlib helpers for finite agenda analogues.
  - `Imported.lean`: source-cited imported theorem handles for CIRL, safe interruptibility, off-switch/corrigibility, Christiano corrigibility, AUP, relative reachability, quantilization, debate, and ELK.
  - Agenda modules: `CIRL.lean`, `Shutdown.lean`, `Interruptibility.lean`, `Corrigibility.lean`, `Impact.lean`, `Quantilization.lean`, `Debate.lean`, `ELK.lean`.
- Converted `FieldSubsumptions.lean` into a compatibility re-export preserving the existing public import path and theorem names.
- Updated `formal/README.md` and `formal/AlignmentProofSpine.lean` module maps to distinguish local proofs/counterexamples, imported field theorem handles, and `MB*` book bridges.
- Updated Appendix I:
  - Added a field-subsumption status section and table.
  - Added imported-handle status marker.
  - Rendered the ch46/ch46/ELK formulas as equations.
  - Added a new field-subsumption inner-structure figure.
- Updated `appendices/appB-bridge-crosswalk.tex` to point to the Appendix I formal status ledger.
- Updated proof graphs:
  - Existing value/correction diagrams now show final `Field.*` theorem nodes.
  - Added `context/lean_proof_graphs/05-field-subsumptions.dot`.
  - Regenerated graph PNGs.
- Updated `metadata/TODO.md` to mark the field-agenda subsumption package complete and narrow the remaining Lean TODOs to core chapter models, non-field toy counterexamples, and chapter-local `\leanspine{}` citations.
- Fixed Appendix I Table J.1 overlap: added breakable `\leanid` macro, ragged-right `L{}` columns, smaller table font; audited and cleaned stale entries in `metadata/TODO.md`.

## Decisions
- Kept the original formula-shaped witnesses in `Bundles.lean` and `Correction.lean`; the new `Field/` modules wrap them rather than moving every definition in one risky pass.
- Imported theorem handles are explicit `axiom ... : Prop` handles with metadata records. They are not counted as `MB*` book bridges.
- Full external theorems are not rederived. The honest status is finite analogue, source-cited import, or separation from the stronger book invariant.

## Open / next
- Optional later cleanup: physically move formula-shaped field definitions from `Bundles.lean` / `Correction.lean` into the agenda modules once the public API has settled.
- Optional later wiring: add `\leanspine{}` citations in the specific chapters to the new final theorem handles.
- Amplification remains outside this field-subsumption package except for existing correction-layer separation.

## Key paths
- `formal/AlignmentProofSpine/Field.lean`
- `formal/AlignmentProofSpine/Field/`
- `formal/AlignmentProofSpine/FieldSubsumptions.lean`
- `appendices/appG-lean-proof-spine.tex`
- `context/lean_proof_graphs/05-field-subsumptions.dot`
- `figures/lean_proof/05-field-subsumptions.png`
- `metadata/TODO.md`

## Commits
- `d5df093` Add Field module package for crosswalk subsumptions with cited imports.
- `3ac438e` Refresh project TODOs and log field-subsumption session handoff.

## Verification
- `lake -d formal build` passes.
- `make check` passes.
- `PAR_GLOBAL_TMPDIR="$PWD/.biber-par-cache" ./build.sh` passes.
