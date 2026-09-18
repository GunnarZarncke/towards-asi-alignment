# 2026-09-18 — Anthropic constitution field news

## Trigger
User parked the Goldstein “thousand constitutions” talk as adjacent, not news. Then asked whether Anthropic’s January 2026 constitution ([anthropic.com/constitution](https://www.anthropic.com/constitution)) is field news: preface hedges (training is hard; system cards; work in progress) vs causal claims (directly shapes Claude; final authority; embodiment; honesty almost a hard constraint) that are not separately proven.

## Done
- Field-news YAML entry `field-news-anthropic-constitution-jan-2026` (`kind: policy`, `eventDate` 2026-01-21, site `date` 2026-09-18).
- Body at `metadata/field-news/bodies/anthropic-constitution-jan-2026.md` (preface quotes; unofficial-preface note; Ch. 40 / 42 / *The words stayed*).
- Pointed the Constitutional AI specify card at the 2026 document and this news card.
- Added a short CIRIS comparison: ships a runtime and names authentic≠ethical / accountable≠correct. No CIRIS changelog in the news body.
- `cd site && npm run sync:field-news && npm run sync:concepts && npm run generate:card-redirects && npm run build:feed`.

## Decisions
- Ingest: specify vs construct split, not a review of the constitution’s ethics content.
- Goldstein talk stays parked (no card).
- Extra finding from the PDF: the “directly shapes” sentence is in the preface, which Anthropic says is not part of the official constitution.
- CIRIS comparison in the news card is only what it does better (named split + runtime). Residual public fusion stays in the CIRIS delta finding, not here.

## Open / next
- Optional: one reference line in `specify-construct-instances.yml` (needs `sync:field-v2`).
- Optional: quiz takeaway for `/news/`.

## Key paths
- `metadata/field-news.yml`
- `metadata/field-news/bodies/anthropic-constitution-jan-2026.md`
- `/cards/news/field-news-anthropic-constitution-jan-2026/`

## End of session
- Trimmed CIRIS section per user: only what CIRIS does better (runtime + named split); no upstream changelog or fusion critique in news body.
- Added `--src-ciris` quote styling for CIRIS blockquotes on the card.
