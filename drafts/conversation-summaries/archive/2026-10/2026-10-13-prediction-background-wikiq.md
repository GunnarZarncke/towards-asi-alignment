# 2026-10-13 — Prediction background wiki quotes (markets 1–4)

kind: new-work
uptake: local

## Trigger
Apply LessWrong wiki quotes in Metaculus `predictionbackground` for the first four catalog markets; suggest-only pass was already done.
Prompts: paraphrase-only

## Done
- content: Appendix P Markets 1–4 `predictionbackground` — one `\wikiq` (embedded agency, complexity of value, ontological crisis, corrigibility) plus a TSA operational sentence; registry-style checklists cut; card links kept.
- housekeeping: `cd site && npm run sync:predictions` → `sync-predictions: wrote 20 cards and predictions.json`.

## Decisions
- Quotes live inside `predictionbackground` (not authbars) so listings stay self-contained; chapter homes named in the lead-in.
- Market 2 uses complexity-of-value, not value-learning (that page is a learner, not a bundle).
- Market 3 uses ontological crisis only; personal-identity stays at Ch. 31.

## Open / next
- Markets 5+ unquoted. Suggested next: 12, 8, 15/18, then 6.
- Refresh `drafts/predictions/metaculus-all-markets.md` if listing on Metaculus.
- PDF not rebuilt this session.

## Key paths
- `appendices/appP-bridge-predictions.tex`
- `site/src/content/cards/predictions/market-01.md` (and 02–04)

## Commits
