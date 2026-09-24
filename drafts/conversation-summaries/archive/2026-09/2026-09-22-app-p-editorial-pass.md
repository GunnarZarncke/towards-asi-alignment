# 2026-09-22 — Appendix H editorial pass

## Trigger

User requested an editorial read of Appendix H for a reader already familiar with the book, with obvious improvements applied and larger changes raised for decision.

## Done

- Smoothed local grammar, number agreement, self-reference, compressed market shorthand, and awkward transitions throughout `appendices/appP-bridge-predictions.tex`.
- Clarified that Market 3 establishes bearer transport only; later value-bundle transport also needs a separate Market 2-style priority witness.
- Distinguished Market 11 hidden coordination from common-cause correlation using generating-mechanism and intervention labels.
- Clarified that market prices forecast research readiness; only deployment-specific method outputs can become PRA evidence.
- Added a short conclusion reconnecting the catalog to \(E\), \(\kappa\), \(S_R\), \(S_U\), \(F\), and \(D\).
- Moved the bridge-spine float outside the authorship-bar environment and added a PDF rendering for the LaTeX build.
- `make check` passed.

## Decisions

- Reverted stricter contract hardening after review: extra coverage, sample-balance, held-out-validation, and matched-control features are described as preferable evidence, not additional YES requirements.
- Kept conceptual clarifications and assurance exposition because they change interpretation, not the difficulty of producing qualifying evidence.

## Open / next

- The clean PDF rebuild was launched after fixing the float and SVG incompatibilities; confirm its final status if needed.
- If Appendix H contracts are later versioned, reconcile the preference language with `metadata/predictions.yml` and regenerated site cards.

## Key paths

- `appendices/appP-bridge-predictions.tex`
- `figures/appp-bridge-spine.svg`
- `figures/appp-bridge-spine.pdf`
- `metadata/predictions.yml`

## Commits

- Session-end commit follows this log.
