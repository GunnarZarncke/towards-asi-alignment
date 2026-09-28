# 2026-09-28 — Embedded evaluators field news

## Trigger
User asked to map the Hinton–Russell–Narayanan embedded-evaluator conditions onto TSA, say what the conditions still omit, and file a quote-driven news card; then edit bridges, add App M and privacy quotes, and ship an Anakin/Padme meme.

## Done
- Quote-driven field news: letter, Amodei, Anthropic, Zvi vs Ch. 26/13/32/39 and App M dual-mandate (Andersen, developer-terms access).
- Purple `--src-letter` source color for Hinton-letter quotes.
- Anakin/Padme meme: “The auditors can run their own tests, right?”
- `metadata/field-news/bodies/embedded-evaluators-sep-2026.md`
- `metadata/field-news.yml` entry `field-news-embedded-evaluators-sep-2026`
- `scripts/meme_workflow/memes.json` + `output/embedded-evaluators.jpg`
- `site/public/field-news/memes/field-news-embedded-evaluators-sep-2026.jpg`
- Synced site card via `sync:field-news-memes` + `sync:field-news`

## Decisions
- Bridges point at what to read (emphasis tags), not restate quotes.
- Letter = purple; Amodei/Anthropic = existing lab blue.
- Meme cashes Ch. 39 read vs perturb (Ask #3).

## Open / next
- Optional quiz takeaway if CI requires a news-takeaway id for this slug.

## Key paths
- `metadata/field-news/bodies/embedded-evaluators-sep-2026.md`
- Letter: https://aievaluatorforum.org/initiatives/embedded-evaluation-letter
- Zvi: https://thezvi.substack.com/p/the-quest-for-embedded-evaluators
- Amodei: https://darioamodei.com/post/we-must-pace-the-frontier

## Commits
- `90abe339c` Add embedded evaluators field news on Hinton letter and Accenture pick.
