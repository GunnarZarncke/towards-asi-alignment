# 2026-09-22 — OpenAI RSI standards field news

## Trigger
User asked for a site news entry commenting on OpenAI’s 21 September 2026 post [Building standards for the next phase of AI](https://openai.com/index/building-standards-next-phase-ai/).

## Done
- Field-news YAML entry `field-news-openai-rsi-standards-sep-2026` (`kind: policy`, `eventDate` 2026-09-21, site `date` 2026-09-22).
- Body at `metadata/field-news/bodies/openai-rsi-standards-sep-2026.md` (quote-bridge: OpenAI blue / this book black).
- News takeaway quiz item; regenerated and merged quiz drafts (215 questions).
- `cd site && npm run sync:field-news && npm run generate:card-redirects && npm run build:feed`.

## Decisions
- Cut is the same as Anthropic’s pace measurements and OpenAI’s August hold: a shared RSI ruler is not a stop unless a finding can delay the next model’s use for further AI R&D.
- Did not ingest PK Sharma’s ISO-secretariat / commercial-interest analysis as a second quote voice; the card comments on OpenAI’s text against the book.
- Seed report linked (`research-acceleration-view-inside-openai`) as the lab’s own measurement, not reviewed as a separate news item.
- No manuscript cite or bib key.

## Open / next
- Optional: a separate card on the 6 September research-acceleration report if the author wants the numbers, not only the standards ask.
- Optional: bibliography key if the post should appear in the PDF.

## Key paths
- `metadata/field-news.yml`
- `metadata/field-news/bodies/openai-rsi-standards-sep-2026.md`
- `/cards/news/field-news-openai-rsi-standards-sep-2026/`
