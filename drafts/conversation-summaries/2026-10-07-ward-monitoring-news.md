# 2026-10-07 — Ward monitoring news

kind: new-work
uptake: local

## Trigger
Create a field-news card on Francis Rhys Ward’s 7 October 2026 survey of frontier-lab monitoring. Grant the first step on each crux the survey touches, and state the test that is still open. Use quotes from the book, from Ward, and from the lab sources where those sentences were re-checked.
Prompts: paraphrase (no telemetry id in this session)

## Done
- content: News card `field-news-ward-monitoring-oct-2026` — YAML, body, teal Ward quote color, Anakin meme. Synced with `npm run sync:field-news` (`sync-field-news: wrote 32 cards (generated).`) and `sync:field-news-memes` (`copied 9 image(s)`).
- content: Local page check at `/cards/news/field-news-ward-monitoring-oct-2026/`: title renders, meme is 768×768, Ward/lab/project quote borders are teal `rgb(14, 116, 144)`, blue `rgb(29, 78, 216)`, and near-black `rgb(15, 23, 42)`. `/news/` includes the card. `/cards/appendix/appp/` returns 200.
- content: Meme caption shortened to “So nothing can slip past?” / “Nothing can slip past, right?”; summary cut to four sentences in `metadata/field-news.yml`.

## Decisions
- The card’s cut is “yes, and the bound is still open,” one section per practice: latency, transcript, activations, coverage, the live filter, who the monitor is, and the human tail.
- Lab sentences that could not be re-fetched (March monitoring post, August risk-report PDF, September misalignment-report lines, the activation-classifier paragraph) are labeled “as quoted by Ward.” Auto-review, the 18 August pause and 20% overhead, and the DeepMind June blog are quoted from the pages themselves.

## Open / next
- A manuscript footnote or Appendix B evidence row, if wanted, still sits outside this card. Specific figures should keep citing the lab document Ward quotes.

## Key paths
- `metadata/field-news.yml`
- `metadata/field-news/bodies/2026-10-ward-monitoring.md`
- `site/src/content/cards/field-news-ward-monitoring-oct-2026.md`

## Commits
- none
