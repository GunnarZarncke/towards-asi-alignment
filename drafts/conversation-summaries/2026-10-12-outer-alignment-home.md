# 2026-10-12 — Outer alignment field home

kind: new-work
uptake: status

## Trigger
Give TSA a clear home for Outer Alignment as a named AT safety subject (not a native TSA object): how TSA treats it, plus field-agenda and crosswalk pointers, and a site card.
Prompts: paraphrase-only (no telemetry prompt id in this session)

## Done
- content: Glossary concept `outer-alignment` (`metadata/concepts.yml` + `metadata/concepts/bodies/outer-alignment.md`); synced site card `/cards/outer-alignment/`.
- content: Factorization table: specify / MB2+MB3 / target realization / preservation-if-optimized; complementary to MB7 inner alignment.
- content: App B — “not one bridge” paragraph, Specify row in the crosswalk table, Shared takeaway sentence.
- content: App E operational glossary entry `\label{sec:outer-alignment}`; Ch. 10 cites Appendix~\ref{appf-glossary}, Section~\ref{sec:outer-alignment} (not App B in the same sentence).
- content: Inter-agenda glossary Cross-agenda for outer (and inner) alignment; `term-links.yml`; field README; field hub intro; lifecycle `gapsNote`; MB2 `fieldAgree` identification-slice qualifier.
- bookkeeping: Related links on alignment-target, pointing-problem, field-coverage, target-realization, MB2, MB7, field-map starting points. Duplicate `### P` heading in the inter-agenda glossary removed (erasure while editing that file).
- bookkeeping: `cd site && npm run sync:concepts && sync:bridges && sync:field-agendas && sync:field-v2 && sync:term-links` — sync-concepts wrote 70 cards; term-links 119 reverse entries.

## Decisions
- Home is a **glossary card + App E**, not a new MB. Alignment Target stays the TSA-native specify object; Outer Alignment is the field heading that factorizes onto it.
- Post-commit trim (author): drop redundant outer-alignment sentences from MB7 and field-map starting-points bodies; card home stays on `/cards/outer-alignment/` and App E.
- App B table gained a non-MB “Specify” row so the name is findable next to inner alignment’s MB7 row.

## Open / next
- Optional: LW wiki quote if an `lwwiki-outer-alignment` bib key is added (inner alignment already has one).
- PDF/`make check` not run this session (LaTeX App B landscape row). Author review of the factorization table wording.

## Key paths
- `site/src/content/cards/outer-alignment.md`
- `appendices/appB-bridge-crosswalk.tex`
- `appendices/appE-glossary.tex`
- `reference/field-agendas/inter-agenda-term-glossary.md`

## Commits
- `38ce36ba6` Add outer alignment as a field glossary home factorized across TSA. (amended: MB7/field-map cross-link trim)
