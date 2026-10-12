# 2026-10-11 — FLI Safety Index chapter cites

kind: new-work
uptake: local

## Trigger
Cite the Future of Life Institute AI Safety Index (Summer 2026) in chapters only, quoting the report rather than paraphrasing where appropriate; footnotes allowed.
Prompts: none resolvable (paraphrase only).

## Done
- content: Quoted FLI lines in Ch. 42 (documentation / weak teeth), Ch. 34 (competitor-contingent pause; compliance attractor), Ch. 43 (detection is not prevention).
- bookkeeping: Bib key `flisafetyindex2026` in `references/governance-institutions.bib` plus `\bibsummary`. `scripts/check_bibliography_summaries.py` passed (554/554).

## Decisions
- Chapters only; no field-news card, no Appendix M, no prediction-market background.
- Grades are not cited as measurements. Ch. 43 footnote states they are not a bound on \(c_{\mathrm{fake}}\).
- Ch. 42 footnote quotes the report's verification limit.

## Open / next
- None for this pass. Field-news card remains optional and unasked.

## Key paths
- `chapters/ch42-safety-case.tex`
- `chapters/ch34-selection-environment.tex`
- `chapters/ch43-verifiability-and-ontology-adequacy.tex`
- `references/governance-institutions.bib`

## Commits
- `3f07a32fe` Cite FLI Summer 2026 AI Safety Index in Ch. 34, 42, and 43.
