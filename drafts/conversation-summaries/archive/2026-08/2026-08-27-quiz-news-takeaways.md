# 2026-08-27 — Quiz items from news takeaways

## Trigger
User: news takeaways usually refer to the manuscript; add matching quiz inventory if missing, but do not put the quiz on the news card.

## Done
- 21 questions (`news-takeaway-*`) from each `metadata/field-news.yml` `decision` / remember-one-thing claim.
- `appearOn` is `chapter:chNN` only (the news `bookChapters` list, appendices skipped). No `news:` keys.
- Card template: `QuizBlock` stays off news (`!isNewsCard`; news also has no `bookEntry`).
- `scripts/write_news_takeaway_quiz.py` + merge; `check_quiz_bank.py` requires one question per news slug and forbids news-card `appearOn`.
- Bank: 211 questions; 80 takeaway-tagged.

## Decisions
- Source links point at the primary chapter card, not the news card.
- Tagged `takeaway` so they list first on those chapter quiz blocks.
- Blinded subagent pass that **saw `correct: true`**: void. Real protocol + full-bank solver round: `2026-08-27-quiz-blind-eval.md`.

## Open / next
- Most news items still have joke distractors (WEAK); concept near-misses not done.
- Essay/chapter takeaway batch was not fully blinded (Phase 2 was a famous-name spot sample).
- Gunnar wording pass vs news decisions.
- Phase 3: agenda/concept `QuizBlock`.

## Key paths
- `scripts/write_news_takeaway_quiz.py`
- `site/src/content/quiz/drafts/00-01-news-takeaways.yml`
- `scripts/check_quiz_bank.py`

## Commits
- `bfaa4ceb` Ship the companion-site field quiz with a 5% multi-correct floor.
