# 2026-08-26 — OpenAI HF road-ahead field news

## Trigger
User asked for a follow-up news article on OpenAI’s 26 Aug 2026 Hugging Face postmortem, in the same quoted-voice style as the pacing card, using quotes from the report and the book.

## Done
- Added `field-news-openai-hf-roadahead-aug-2026` (`kind: incident`, date 2026-08-26).
- Body: four sections (trained-in cheat, impossible-task metagame, swarm as object, hindsight-tuned CoT monitor). Added 30-minute human page vs six-minute agent `GO` clock.
- Yes-and pass on opening and close: use OpenAI’s “future incidents may not resemble this one” / stay-ahead / agent-speed acknowledgement; offer boundary discovery, UAD/graded-lab, MB7a, Ch. 25 clock, Ch. 43 cost-of-faking.
- Bib key `openai2026huggingfaceroadahead` plus bibliography summary.
- Ran `sync:field-news` (21 cards), `build:feed`, `sync:reference-cards`.
- Verified `/news/` lead item, card quotes, Ch. 7 related-news sidebar, RSS item.

## Decisions
- Separate card, not a fold into July / Black Hat / pacing.
- Two voices (OpenAI + this book). No Zvi: he has not written on this post.
- Opening/close as yes-and, not as a pure “this does not fix it” lead.
- No manuscript `\autocite{}` yet; the July key already covers the incident in ch14/ch40/ch42.

## Open / next
- Optional surgical cite of `openai2026huggingfaceroadahead` in ch14/ch40/ch39 if a chapter footnote should point at the postmortem rather than the July disclosure.
- METR/Redwood independent report was claimed published the same day; URL not retrieved. Add a third voice if that write-up lands.
- Left unstaged: later site work (read-next, experiment coverage, field-agenda cards, search/feed scripts, etc.).

## Key paths
- `metadata/field-news.yml`
- `metadata/field-news/bodies/openai-hf-roadahead-aug-2026.md`
- `site/src/content/cards/field-news-openai-hf-roadahead-aug-2026.md`
- `references/manuscript-citations.bib`

## Commits
- `67bed526` Add field news on OpenAI’s Hugging Face postmortem.
