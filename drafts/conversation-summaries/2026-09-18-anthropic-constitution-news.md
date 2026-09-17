# 2026-09-18 — Anthropic constitution field news

## Trigger
User parked the Goldstein “thousand constitutions” talk as adjacent, not news. Then asked whether Anthropic’s January 2026 constitution ([anthropic.com/constitution](https://www.anthropic.com/constitution)) is field news: preface hedges (training is hard; system cards; work in progress) vs causal claims (directly shapes Claude; final authority; embodiment; honesty almost a hard constraint) that are not separately proven.

## Done
- Field-news YAML entry `field-news-anthropic-constitution-jan-2026` (`kind: policy`, `eventDate` 2026-01-21, site `date` 2026-09-18).
- Body at `metadata/field-news/bodies/anthropic-constitution-jan-2026.md` (preface quotes; unofficial-preface note; Ch. 40 / 42 / *The words stayed*).
- Pointed the Constitutional AI specify card at the 2026 document and this news card.
- Added a CIRIS comparison (engineer split is better; storefront fusion is the same move). Quotes from CIRISVerify and CIRISAgent READMEs; teal quote style.
- `cd site && npm run sync:field-news && npm run sync:concepts && npm run generate:card-redirects && npm run build:feed`.

## Decisions
- Ingest: specify vs construct split, not a review of the constitution’s ethics content.
- Goldstein talk stays parked (no card).
- Extra finding from the PDF: the “directly shapes” sentence is in the preface, which Anthropic says is not part of the official constitution.
- CIRIS vs this constitution: better on naming authentic≠ethical / accountable≠correct and on shipping a builder that can fail; not better on public fusion (hero “safer, more ethical” vs Honest read, no precedence rule). Same structure as unofficial preface vs official body.

## Open / next
- Optional: one reference line in `specify-construct-instances.yml` (needs `sync:field-v2`).
- Optional: quiz takeaway for `/news/`.

## Key paths
- `metadata/field-news.yml`
- `metadata/field-news/bodies/anthropic-constitution-jan-2026.md`
- `/cards/news/field-news-anthropic-constitution-jan-2026/`
