# 2026-10-05 — Prediction contract migration (Markets 1–18, 21)

kind: new-work
uptake: status

## Trigger
Apply the four-environment Metaculus contract structure (front `predictionbox` + Background / Resolution criteria / Fine print) from Markets 19–20 to all other prediction markets and common rules.

Prompts: (paraphrase — prior session handoff)

## Done
- content: Migrated `appendices/appP-bridge-predictions.tex` — common qualification and Markets 1–18, 21 now use `predictionbox`, `predictionbackground`, `predictionresolution`, and `predictionfineprint`; authbar closes before contract blocks and reopens for closest-existing-work prose.
- content: Restored `\subsection` / `\label{sec:appp-mN}` headers dropped by the first migration pass; fixed duplicate `\end{authbar}`, bracketed predictionbox titles, common-rule glossary authbar wrap.
- housekeeping: Added `scripts/migrate_prediction_contracts.py` (one-off migrator).
- housekeeping: Updated `site/scripts/sync-predictions.mjs` to read YES requires / Output from `predictionresolution`.
- verification: `latexmk -pdf book.tex` → `Output written on book.pdf`; `npm run sync:predictions` → `wrote 20 cards and predictions.json`.

## Decisions
- Post-box “Prefer …” paragraphs (Markets 9, 16, 18) → `predictionfineprint`; interpretive / closest-existing-work prose stays in authbar after the contract block.
- Common rules: short front box + resolution/background/fine print; shared glossary remains authbar prose after the contract block.

## Open / next
- Phase 4 pilot/listing for Markets 19–21 unchanged.
- `make pdf` still fails at generate step (`PyYAML required`) before LaTeX; direct `latexmk` succeeds.
- Remaining mdframed “non splittable” warnings are from small front `predictionbox` tcolorboxes (expected).

## Key paths
- `appendices/appP-bridge-predictions.tex`
- `metadata/preamble.tex` (four environments)
- `site/scripts/sync-predictions.mjs`
- `drafts/predictions/metaculus-question-template.md`

## Commits
- `373487891` — Restructure Appendix P prediction contracts for Metaculus listing.
