# 2026-09-28 — OpenAI DNS-chatbot field news

## Trigger
User asked for a high-quote field-news card on OpenAI’s 20 September RL-training incident (DNS to an external chatbot), including the monitoring timeline and the 2.5-hour kill, Carroll’s and Liu’s posts, and the 2021 Yudkowsky/Tallinn and 2022 Gwern pieces. Focus: capability ahead of the stop, and evals when the effect is not on the expected interface.

## Done
- Quote-driven card: OpenAI report, August 30-minute pause rule, Liu, Carroll, Gwern warning-shot block, Ch. 14/12/25/13/11.
- User edits: async effect prose, Gwern moved to timeline section, Yudkowsky block removed, section “Watching the wrong exit,” updated Ask list.
- Anakin/Padme meme (`openai-dns-chatbot`): “And then the run stopped?”
- Amber `src-quote--prior` CSS for prior-writing quotes.
- `metadata/field-news/bodies/2026-09-openai-dns-chatbot.md`
- `metadata/field-news.yml` entry `field-news-openai-dns-chatbot-sep-2026` (title, hook, summary, decision)
- Quiz takeaways: `news-takeaway-openai-dns-chatbot-sep-2026`, `news-takeaway-embedded-evaluators-sep-2026` (CI gap)
- `make check` passed (2026-09-28)

## Decisions
- Gwern is the warning shot beside the timeline, not a closing afterthought.
- Reward/monitor grade arrives after the query leaves; prose names async effects explicitly.
- Carroll’s pause wording wider than report; May token + prompt-injection notes named once only.
- Hook (user): box shape unclear, alarm fast, stop hours later.

## Open / next
- None.

## Key paths
- `metadata/field-news/bodies/2026-09-openai-dns-chatbot.md`
- Report: https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/
