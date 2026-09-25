# 2026-09-25 — Glossary CI fix

## Trigger
CI `make check` failed during the generate step: `build_section_reference_graph.py` exited 1 with three missing glossary anchors (VFS, BIQ, EAI on the `experiment-methodology` card).

## Done
- Added `\label{sec:experimental-methodology-shorthand}` to Appendix E's Experimental-methodology shorthand section (`appendices/appE-glossary.tex`).
- Added `bookLabels: [sec:experimental-methodology-shorthand]` to the `experiment-methodology` card in `metadata/concepts.yml`.
- Regenerated `metadata/concept-graph/glossary-section-audit.md` and `terminal-backref-audit.md` (0 missing; 2 chapter-only warnings remain and do not fail CI).

## Decisions
- Anchor the three experiment-methodology glossary terms at the existing Appendix E shorthand section rather than inventing per-term section labels — matches where the definitions already live.

## Open / next
- Two `chapter-only` glossary entries still warn (Adversarial measurement, Paternalism boundary); optional follow-up to add narrow `sec:` labels.
- One unresolved manuscript ref remains: `sec:three-alignment-questions`.

## Key paths
- `scripts/build_section_reference_graph.py` — exits 1 when glossary audit has `missing` entries.
- `appendices/appE-glossary.tex` — Experimental-methodology shorthand section.
- `metadata/concepts.yml` — `experiment-methodology` card.

## Commits
- (this session)
