# 2026-10-12 — Greenblatt control-measures cite

kind: new-work
uptake: local

## Trigger
Cite Greenblatt 2025 *An overview of control measures* (tier 1 + App B + Ch. 43). Do not hang a catalog in Ch. 42. Adopt the three-way split only if natural; otherwise say why we split differently.
Prompts: paraphrase-only (no telemetry prompt id in this session)

## Done
- content: Bib `greenblatt2025controloverview` + `\bibsummary`. App B AI Control row and MB7 note; Ch. 43 handles section + chapter references. Three-way split named as staffing map; book keeps handle / cost-of-faking cut. Ch. 42 uncited.
- content: Field-agenda Redwood links, evidence `174`, inter-agenda Sources line; extract year 2023→2025.
- bookkeeping: `check_bibliography_summaries.py` passed (`555 summaries for 555 bib keys`). `cd site && npm run sync:field-agendas` — 31 agenda cards.

## Decisions
- Do not import the measures list into Ch. 42: a cite without the catalog would hang.
- Do not replace `shlegeris2023aicontrol` or `greenblatt2024aicontrol`.

## Open / next
- PDF/`make check` not run this session.
- Optional later: translated catalog as a dedicated appendix if Ch. 42 needs the cite.

## Key paths
- `references/external-alignment.bib`
- `appendices/appB-bridge-crosswalk.tex`
- `chapters/ch43-verifiability-and-ontology-adequacy.tex`

## Commits
- (none)
