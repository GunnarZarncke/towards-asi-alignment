# 2026-09-18 — Anthropic pace-measurements field news

## Trigger
User asked to ingest Anthropic Institute *Measurements for understanding the pace of AI development inside frontier labs* as a field-news card in the quote-bridge style: book + report quotes, minimal commentary, connective causal logic (not summary of the quotes).

## Done
- Field-news YAML entry `field-news-anthropic-pace-measurements-sep-2026` (`kind: policy`, `eventDate` 2026-09-17, site `date` 2026-09-18).
- Body at `metadata/field-news/bodies/anthropic-pace-measurements-sep-2026.md` (automation index, oversight latency, compute share; Ch. 11 / 12 / 25 / 39 / 42 / 43).
- `cd site && npm run sync:field-news && npm run generate:card-redirects && npm run build:feed`.

## Decisions
- Same cut as the August risk report: production-process dashboard ≠ correction keeping pace; 26% AL4 and week-scale human review are measurements of the race, not a stop.
- `eventDate` is the day the piece was brought as new (2026-09-17); the snapshot itself is August 2026.
- No manuscript cite or bib key (same as constitution / risk-report cards).

## Open / next
- Optional: quiz takeaway for `/news/`.
- Optional: bibliography key if the Institute post should appear in the PDF.

## Key paths
- `metadata/field-news.yml`
- `metadata/field-news/bodies/anthropic-pace-measurements-sep-2026.md`
- `/cards/news/field-news-anthropic-pace-measurements-sep-2026/`
