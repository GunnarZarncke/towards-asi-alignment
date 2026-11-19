# 2026-11-16 — Kaufman on Good + home latest news

kind: correction
uptake: local

## Trigger
Field-news card on Kaufman's Good reread → replaced with Ch. 14 footnote and bib. Homepage: latest field news before Continue reading; More news → `/news/#field-news`.
Prompts: paraphrase-only.

## Done
- content: Removed short-lived Good field-news card (YAML/body/quiz/synced card, not committed).
- content: Ch. 14 Good epigraph footnote + `kaufman2026goodreading`.
- content: `HomeLatestNews` on home; `latestFieldNewsItem`; news index `id="field-news"`.
- bookkeeping: `scripts/check_bibliography_summaries.py` → 583/583 passed (pre-commit via make check).

## Decisions
- No field-news card; footnote only on Ch. 14 (Ch. 30 epigraph unchanged).

## Open / next
- None.

## Key paths
- `chapters/ch14-intelligence-deepens-misalignment.tex`
- `site/src/components/HomeLatestNews.astro`

## Commits
- `d8d8dd1ff7` Link Kaufman’s Good reread on Ch. 14 and surface latest field news on the home page.