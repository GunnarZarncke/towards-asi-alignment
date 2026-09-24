# 2026-09-24 — Quiz takeaway for mathematics misalignment news

## Trigger
CI `make check` failed on **quiz bank**: `news-takeaway-math-misalignment-sep-2026` missing after the field-news entry.

## Done
- Added the question to `scripts/attic/write_news_takeaway_quiz.py`, regenerated `site/src/content/quiz/drafts/00-01-news-takeaways.yml`, and inserted the same item into `site/src/content/quiz/questions.yml` (216 → 217; 85 → 86 takeaway-tagged).
- `python3 scripts/check_quiz_bank.py` and `check_quiz_length_tell.py` pass.

## Decisions
- Topic is MB9. The open question is whether a method others can learn has moved, or only the true-or-false score. Source link is Chapter 3. `appearOn` is ch03, ch14, ch34, ch16.

## Open / next
- Unstaged working-tree drafts outside this fix were left untouched.

## Key paths
- `scripts/attic/write_news_takeaway_quiz.py`
- `site/src/content/quiz/questions.yml`
- `metadata/field-news.yml`
