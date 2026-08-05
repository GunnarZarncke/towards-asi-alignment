# 2026-08-05 — Jailbreak disclosure field news

## Trigger
User asked for a general-audience news entry on the AI Frontiers article “AI Jailbreak Disclosure Is Broken. Here’s How to Fix It,” then to link the Boko Haram and Fable 5 examples to primary sources and Zvi writeups.

## Done
- Added `field-news-jailbreak-disclosure-aug-2026` (`kind: policy`, date 2026-08-03): body, roster entry, synced site card.
- Linked stakes paragraph to CASP Boko Haram report, Anthropic Fable suspension statement, and three Zvi posts (AI #177, Fable takedown, “Fix This Code” follow-up).
- Ran `npm run sync:field-news`.
- Added RSS subscribe CTA on `/news/` index below the lede (`site/src/pages/news/index.astro`).

## Decisions
- Site-only; no manuscript cite or bib key.
- Primary links taken from AI Frontiers article footnotes; Zvi added as readable secondary context.
- Book links: ch27, ch33, ch38, ch39, appC; bridges MB4, MB6.

## Open / next
- Optional: cross-link from insurance-audits or pacing-frontier news cards (same disclosure/institutional theme).
- Optional: bibliography key if the Barton-Cooper/Gleave essay should appear in the PDF.

## Key paths
- `metadata/field-news/bodies/jailbreak-disclosure-aug-2026.md`
- `metadata/field-news.yml`
- `site/src/content/cards/field-news-jailbreak-disclosure-aug-2026.md`

## Commits
- `444ed2f7` Add jailbreak disclosure field news with sourced examples.
- (pending) Add RSS subscribe CTA on news index.
