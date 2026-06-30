# 2026-06-30 — Field formalization gem

## Trigger
User noted that completing Mathlib-backed field-agenda formalizations (CIRL, AUP/RR, quantilization, etc.) could be a community gem in itself, and asked to add it to the gem list, name it in the Lean appendix, and update math rendering there.

## Done
- Added **field-agenda Lean formalization (community gem in progress)** to `REVIEWING_FOR_AGENTS.md` gem map.
- Named the gem in Appendix I: `\paragraph{Gem: field-agenda formalization.}` with label `sec:appi-field-formalization-gem`.
- Replaced the old cramped field-formula `align` block with interface-condition formulas (CIRL \(k=1\) embed, scalar/bundle inference, shutdown/interrupt bits, AUP reachability interface, quantile soundness, contraction/readout) and symbol glossary.
- Cross-linked from `appendices/appB-bridge-crosswalk.tex` and `formal/README.md`.

## Decisions
- Framed as **in progress / prospective community artifact**, not as completed full-field theorem reproduction.
- Kept Debate/ELK deferral unchanged; gem scope is the shared finite fragment already under construction.

## Open / next
- Mathlib-backed `Field/Finite/Probability.lean` and full CIRL/AUP/quantilization rederivations (see `metadata/TODO.md`).
- Optional: promote gem in `llms.txt` or part opener if reviewers still miss it.

## Key paths
- `REVIEWING_FOR_AGENTS.md`
- `appendices/appG-lean-proof-spine.tex`
- `appendices/appB-bridge-crosswalk.tex`
- `formal/README.md`

## Commits
- None.

## Verification
- `make check` passed.
- `pdflatex book.tex` passed after removing duplicate `\label` in `align`.
