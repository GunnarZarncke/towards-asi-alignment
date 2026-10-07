# 2026-10-07 — Field news summary trim

kind: correction
uptake: local

## Trigger
Shorten the `summary` field on the last four field-news cards (they were too long for the listing).
Prompts: paraphrase-only

## Done
- content: Cut YAML `summary` on Ward monitoring, OpenAI training safety case, OpenAI DNS chatbot, and embedded evaluators to ~3 sentences each; `cd site && npm run sync:field-news` wrote 32 cards.

## Decisions
- Kept the project cut on the OpenAI cards; dropped Zvi/detail lists that belong in the body.

## Open / next
- None.

## Key paths
- `metadata/field-news.yml`
- `site/src/content/cards/field-news-ward-monitoring-oct-2026.md` (and the three Sep cards)

## Commits
- none
