# 2026-11-15 — Dwarkesh RSI alignment gap

kind: new-work
uptake: local

## Trigger
Draft a standard field-news card from Dwarkesh Patel's RSI essay and Noam Brown interview, granting capability proxies while stressing alignment as the missing gate; author tightened copy, summary, quiz, and decision.
Prompts: paraphrase-only; no resolvable prompt id was exposed in this session.

## Done
- content: Added `field-news-dwarkesh-rsi-alignment-gap-nov-2026` with body quotes from Patel and Brown; author shortened prose to opening thesis (capability hill vs alignment path).
- content: `metadata/field-news.yml` hook kept author wording; short summary and one-line decision synced.
- content: Quiz takeaway `news-takeaway-dwarkesh-rsi-alignment-gap-nov-2026` aligned to opening.
- housekeeping: `npm run sync:field-news` → `sync-field-news: wrote 35 cards (generated).`
- bookkeeping: `.venv/bin/python scripts/check_quiz_bank.py` → `All checks passed.`
- bookkeeping: `.venv/bin/python scripts/check_quiz_length_tell.py` → `Length-tell checks passed.`

## Decisions
- Grant Patel's verifiable-proxy / RSI-on-capability case; do not relitigate timelines.
- Proxies measure capability progress, not alignment; eval realism does not remove spec-gaming risk.
- Quiz and decision mirror card opening: capability has a scored path; alignment does not yet.

## Open / next
- Optional card-specific social preview image.

## Key paths
- `metadata/field-news.yml`
- `metadata/field-news/bodies/2026-11-dwarkesh-rsi-alignment-gap.md`
- `site/src/content/cards/field-news-dwarkesh-rsi-alignment-gap-nov-2026.md`
- `site/src/content/quiz/questions.yml`

## Commits
- (this session)