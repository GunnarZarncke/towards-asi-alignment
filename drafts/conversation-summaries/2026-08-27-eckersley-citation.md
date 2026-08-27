# 2026-08-27 — Eckersley impossibility citation

## Trigger
User asked whether arXiv:1901.00064 (Eckersley, *Impossibility and Uncertainty Theorems in AI Value Alignment*) is cited; where it should go; then to apply the recommended ch. 4 cites and commit.

## Done
- Confirmed the paper was not previously in the bibliography or manuscript.
- Added `eckersley2019impossibility` to `references/external-alignment.bib` and `\bibsummary` in `references/bibliography-summaries.tex`.
- Two `\autocite{eckersley2019impossibility}` in `chapters/ch04-fixed-values-wrong-target.tex`:
  - `sec:fixed-utility-too-small` — impossibility results vs strict total-order objectives.
  - CIRL paragraph — learned rewards that collapse to a single total order do not escape the same constraints.
- `python3 scripts/check_bibliography_summaries.py` passed (483/483).

## Decisions
- Cite lightly in ch. 4 only (not ch. 19): Eckersley is parallel prior art rejecting scalar/total-order targets; the book's answer remains process + bundle geometry + correction, not uncertain objectives as the main fix.
- Did not add population-ethics exposition; one sentence + CIRL clause only.

## Open / next
- Optional light ch. 19 footnote at “social-choice artifacts” if a second pass wants field crosswalk coverage.
- Unrelated working-tree changes (quiz stack, site nav, etc.) left unstaged.

## Key paths
- `chapters/ch04-fixed-values-wrong-target.tex` (`sec:fixed-utility-too-small`, sample-complexity / CIRL block)
- `references/external-alignment.bib` (`eckersley2019impossibility`)

## Commits
- (pending)
