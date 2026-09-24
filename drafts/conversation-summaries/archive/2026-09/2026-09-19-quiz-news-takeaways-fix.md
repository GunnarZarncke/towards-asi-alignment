# 2026-09-19 — Quiz news-takeaways CI fix

## Trigger
CI `make check` failed on **quiz bank**: three `news-takeaway-*` questions missing for field-news entries added in `feafdccd`.

## Done
- Added three `Q(...)` items to `scripts/write_news_takeaway_quiz.py` (pace measurements, constitution, containment verification).
- Regenerated `site/src/content/quiz/drafts/00-01-news-takeaways.yml` and merged into `questions.yml` (211 → 214 questions; 80 → 83 takeaway-tagged).
- Verified `python3 scripts/check_quiz_bank.py` and `check_quiz_length_tell.py` pass.

## Decisions
- Root cause: `feafdccd` added three rows to `metadata/field-news.yml` without running the paired quiz workflow (`write_news_takeaway_quiz.py` → `merge_quiz_drafts.py`). The gate in `check_quiz_bank.py` (since `bfaa4ceb`) was working as designed.

## Open / next
- Unstaged in working tree (not this session): demo `app.js` tweaks under `demos/ch01`, `ch07`, `ch16`, `ch17`, `ch35`; untracked `drafts/plans/sandboxed-agent-mcp.md`.

## Key paths
- `scripts/write_news_takeaway_quiz.py` — source for news takeaway items
- `scripts/check_quiz_bank.py` — one question per `field-news-*` slug
- `metadata/field-news.yml` — inventory the check reads

## Commits
- (this session)
