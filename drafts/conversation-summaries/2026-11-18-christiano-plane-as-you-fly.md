# 2026-11-18 — Christiano "plane as you fly it" field news

kind: new-work
uptake: local

## Trigger
Fetch transcript of Dwarkesh × Paul Christiano (2026-11-16); compare with RSI card; write follow-on news card that only adds what the interview adds.
Prompts: paraphrase-only.

## Done
- bookkeeping: Transcript saved to `drafts/references/dwarkesh-2026-11-16-paul-christiano-2-transcript.md` (sponsor copy dropped).
- content: Field news `field-news-christiano-plane-as-you-fly-nov-2026` (body, YAML, quiz takeaway). Links to the RSI card; does not repeat its Brown/eval/five-problem points.
- bookkeeping: `npm run sync:field-news` → `wrote 36 cards (generated).`; `check_quiz_bank.py` → `All checks passed.`; `check_quiz_length_tell.py` → `Length-tell checks passed.`
- content: Card close links `/predictions/` (author tightened wording on stop rule + markets).

## Decisions
- New angle owned by this project: Christiano's two saving throws (AI-found fix, stop) are not independent; both read observations the system is pushed to hide.
- Christiano quotes use the `letter` (purple) legend color.

## Open / next
- Author copy pass; bookChapters/bridges copied as a subset of the RSI card, check fit.

## Commits
- `c9397dcbc3` Add field news on Christiano’s alignment plan after Dwarkesh RSI card.

## Key paths
- `metadata/field-news/bodies/2026-11-christiano-plane-as-you-fly.md`
- `metadata/field-news.yml`
- `site/src/content/quiz/questions.yml`
