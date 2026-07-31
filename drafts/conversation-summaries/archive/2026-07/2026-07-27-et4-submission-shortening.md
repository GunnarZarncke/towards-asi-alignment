# 2026-07-27 — ET-4 submission shortening

## Trigger

User requested one-hour hackathon advice to be applied to the LaTeX submission.

## Done

- Added explicit primary/secondary track fit in the introduction.
- Moved the affordance mapping into a clearly labeled appendix.
- Moved the code/artifact mapping into a separate clearly labeled appendix.
- Kept the main Code and data section before the appendices.
- Shortened execution/replay and remediation prose.
- Removed the pipeline-quirk paragraph, compressed pilot and related-work
  descriptions, condensed scripted results and discussion/future work, and
  moved the replay summary into Appendix B.
- Validated the revised LaTeX with two successful `pdflatex` passes and no linter errors.

## Open / next

- Copy the validated PDF from the build output into the context folder if a refreshed PDF is desired.
- Consider a final visual/page-count check before submission.

## Key paths

- `context/ET4-context/et4-hackathon-submission.tex`
- `context/ET4-context/et4-hackathon-submission.pdf`
