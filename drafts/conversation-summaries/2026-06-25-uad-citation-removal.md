# 2026-06-25 — UAD citation removal

## Trigger
The user clarified that the manuscript should not cite the Gunnar Zarncke UAD papers directly; the relevant material should be derived or explained within the scope of the book.

## Done
- Removed direct manuscript citations to `zarncke2026access`, `zarncke2026smoothing`, and `zarncke2026stealth` from:
  - `chapters/ch07-finding-boundary.tex`
  - `chapters/ch10-strategic-opacity.tex`
  - `chapters/ch36-passive-observation-not-enough.tex`
  - `chapters/ch39b-verifiability-and-ontology-adequacy.tex`
- Rephrased the surrounding text so handles, measurement blur, stealth costs, and accumulated resources are presented as book-internal arguments rather than imported paper results.
- Verified no `.tex` files still contain those citation keys or the phrases "new UAD bounds" / "new agent-discovery refinements."
- Ran `python3 scripts/check_structure.py` successfully.
- Ran `./build.sh` successfully. The build log contains no references to the removed UAD citation keys and no LaTeX errors.

## Decisions
- Kept the UAD source files and bibliography entries in the repo; the user asked not to cite them in the book prose, not to remove them from project context.
- Left `\leanspine` references in place, because they now serve as the book-internal formal anchor for the same material.

## Open / next
- If future chapters use material from these UAD papers, explain it directly in the book's own terms and cite the Lean spine or local definitions rather than citing the internal UAD papers.

## Key paths
- `chapters/ch07-finding-boundary.tex`
- `chapters/ch10-strategic-opacity.tex`
- `chapters/ch36-passive-observation-not-enough.tex`
- `chapters/ch39b-verifiability-and-ontology-adequacy.tex`

## Commits
- None.
