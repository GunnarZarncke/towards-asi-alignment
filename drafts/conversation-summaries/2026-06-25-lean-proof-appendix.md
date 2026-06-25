# 2026-06-25 — Lean proof appendix

## Trigger
The user noted that `\leanspine` references proofs throughout the book, but the appendices did not render the Lean proof spine in standard mathematical form.

## Done
- Added `appendices/appI-lean-proof-spine.tex`.
- The new appendix translates the Lean proof spine into ordinary mathematical statements with compact proofs, counterexamples, and bridge-assumption entries.
- Covered the proof/counterexample nodes used by the manuscript and the current Lean spine, including the new access/K-equivalence and hidden-BIQ nodes (`P34A`, `P34K`, `P35M`, `P38H`, `P10H`) plus `MB7a`--`MB7c`.
- Revised the appendix into a more formal mathematical development:
  - definitions and numbered equations for core quantities;
  - imported assumptions `S01`--`S09`;
  - bridge assumptions `MB1`--`MB8`;
  - numbered lemmas, theorems, and corollaries with internal cross-references.
- Included the appendix from `book.tex`.
- Updated appendix-count references in `README.md`, `INSTRUCTIONS.md`, and `scripts/check_structure.py`.
- Added theorem-style environments (`lemma`, `theorem`, `corollary`) to `metadata/preamble.tex`.
- Ran `python3 scripts/check_structure.py` successfully.
- Ran `./build.sh` successfully; the PDF was regenerated. A final no-change build reports the PDF target up to date.

## Decisions
- Rendered the appendix as mathematical propositions/proofs rather than raw Lean code, because the user asked for standard mathematical form.
- Kept bridge assumptions separate from Lean-proved propositions to avoid implying that empirical or philosophical bridges are mechanically proved.
- Used compact proof sketches for finite toy counterexamples and definitional theorems, since many Lean nodes are intentionally minimal witness constructions.
- Namespaced appendix labels with `appi:` to avoid collisions with existing chapter equation labels such as `eq:epsilon-boundary` and `eq:biq`.

## Open / next
- If the proof spine grows, keep `appendices/appI-lean-proof-spine.tex` synchronized with `formal/AlignmentProofSpine/*.lean` and `context/lean_proof_dependency_graph.dot`.
- Consider adding hyperlinks from `\leanspine` references to appendix anchors later; the current macro still renders plain text.
- Existing bibliography warnings remain outside this change.

## Key paths
- `appendices/appI-lean-proof-spine.tex`
- `book.tex`
- `formal/AlignmentProofSpine/*.lean`
- `context/lean_proof_dependency_graph.dot`
- `scripts/check_structure.py`

## Commits
- None.
