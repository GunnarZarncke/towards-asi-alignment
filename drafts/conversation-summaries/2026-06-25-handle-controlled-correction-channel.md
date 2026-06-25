# 2026-06-25 — Handle-controlled correction channel

## Trigger
The user wanted correction channel and correction-channel integrity put on less ad-hoc footing using handles, then rejected a role-list framing (`observation`, `interpretation`, `deliberation`, `authority`, `effect`) as importing ontology. The agreed direction was to ground correction in what agent controls what handles.

## Done
- Refactored Lean correction formalism:
  - Added handle-control primitives in `formal/AlignmentProofSpine/Core.lean`: `ControlsHandle`, `HandleReachesSystem`, `CorrectingAgentFor`, `CoincidesWithHumanity`, `HandleControlPersists`, and `CapturesHandleControl`.
  - Redefined `CorrectionChannelFor A G` / `CorrectionChannel A` around legitimate correcting-agent control of reaching handles.
  - Parameterized `CorrectionPath` by target system and added fields for corrector, access model, controlled handles, reach, persistence, non-capture, and effective link capacity.
  - Replaced graph-path `P23` with `P23_no_handle_control_no_correction`.
  - Kept `CCI` as the exported correction measurand and preserved weakest-link `P24` over effective handle capacities.
- Updated manuscript and metadata:
  - Revised ch24/ch25 correction-channel definitions from a fixed observe/judge/deliberate role ontology to a correcting-agent/handle-control model.
  - Updated book-wide CCI formulas from `min_i I(X_i;X_{i+1})` to `min_i \kappa_i(A,G_t,h_i)` in live chapters and instructions.
  - Updated `appendices/appI-lean-proof-spine.tex`, `appendices/appF-glossary.tex`, `metadata/notation.md`, `metadata/terminology.md`, `metadata/TODO.md`, `formal/README.md`, and `formal/AlignmentProofSpine.lean`.
  - Updated `context/lean_proof_dependency_graph.dot` labels and regenerated `context/lean_proof_dependency_graph.png`.
- Verification:
  - `cd formal && lake build` passed.
  - `python3 scripts/check_structure.py` passed.
  - ReadLints reported no linter errors for edited core files.
  - `./build.sh` passed and rebuilt the PDF. Remaining warnings are existing undefined citations; no new undefined commands or new label-reference failures were found.

## Decisions
- Treat observation/operation handles as primitive, but treat judgment, deliberation, authority, and effects as states/actions of a correcting agent, not handle kinds.
- Model the human correction process itself as a discoverable/composite agent \(G_t\) that must sufficiently coincide with humanity or the legitimate human process.
- Keep the familiar \(W\to O\to J\to D\to C\to U\to A\) trace as a diagnostic trace, not an ontology of primitive correction roles.
- Define raw correction capacity as weakest effective controlled-handle capacity \(\min_i \kappa_i(A,G_t,h_i)\).

## Open / next
- The Lean capacities are still abstract integers. A future strengthening could define \(\kappa_i\) from concrete observation/operation data.
- Some review/history files still mention the old MI weakest-link formulation; these were left untouched as historical notes.
- Consider whether ch23/ch26/ch31 need a fuller explanatory paragraph, beyond formula replacement, in a later continuity pass.

## Key paths
- `formal/AlignmentProofSpine/Core.lean`
- `formal/AlignmentProofSpine/Correction.lean`
- `chapters/ch24-correction-causal-channel.tex`
- `chapters/ch25-correction-channel-integrity.tex`
- `appendices/appI-lean-proof-spine.tex`
- `metadata/notation.md`
- `metadata/terminology.md`
- `context/lean_proof_dependency_graph.dot`

## Commits
- None.
