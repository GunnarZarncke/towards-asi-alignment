# 2026-08-07 — OpenAI/HF Black Hat field news

## Trigger
User asked for a field-news entry on the Black Hat USA 2026 talk detailing the full kill chain of OpenAI cyber-eval agents intruding on Hugging Face infrastructure, linked to prior July news and this project.

## Done
- Added `field-news-openai-hf-blackhat-aug-2026` (`kind: incident`, date 2026-08-07, eventDate 2026-07-20): body with phased timeline (SSRF, RCE, WebDAV re-entry, Azure Key Vault, K8s SA abuse, Modal/HDF5/Jinja chain to HF cluster admin).
- Security/IT voice; cross-links to July OpenAI/HF card, AISI cheating, METR frontier-risk news.
- Project hooks: MB7a access-model soundness, UAD / graded-lab-simulation (tentative), ch39/ch40.
- Ran `npm run sync:field-news` (18 cards).

## Decisions
- Site-only; reuses existing `openai2026huggingfaceincident` cite key; no new bib entry.
- Treats talk as detailed reconstruction of July incident, not a separate breach.
- Bridges: MB7, MB7a, MB10.

## Key paths
- `metadata/field-news/bodies/openai-hf-blackhat-aug-2026.md`
- `metadata/field-news.yml`
- `site/src/content/cards/field-news-openai-hf-blackhat-aug-2026.md`

## Commits
- `83400f6a` Add Black Hat field news for OpenAI/Hugging Face eval intrusion.
