# 2026-09-30 — Site notes: ch01, serious, cards hub

kind: feedback
uptake: local

## Trigger
Implement the first three items of the site-notes plan: simpler Chapter 1 opening, book-wide `serious` pass, plain-language `/cards/` hub.
Prompts: paraphrase-only (no resolvable prompt id in this session)

## Done
- content: Rewrote ch01 thesis (model / alignment / optimizer); deleted the introduction three-questions back-reference; replaced Operational Definition formalism with a Ch. 7 / App. E preview; deleted “The argument should not be overextended.”; trimmed epistemic-status list.
- content: Replaced tell-don’t-show `serious`/`seriously` in chapters, introduction successor claim, claims ledger, ch06 concept body; left Debian severity and App P evaluation bars; one App P “serious candidate” line.
- content: `/cards/` lede and meta description; catalog section title Tools and checklists (`id` still `artifacts`).
- bookkeeping: `cd site && npm run sync:chapter-cards && npm run sync:chapters && npm run sync:concepts`; working copy `drafts/site-notes-pass.md`.

## Decisions
- Dropped the ch01 “serious alignment cannot rely on these” sentence rather than paraphrase it, because the next paragraph already shows the notebook / market / approve-click cases.
- Successor claim wording is now “does not cover this claim unless…” in intro, ch48, and the ledger.

## Open / next
- Remaining site-notes items: decision blocks, field intro, notes save button, preview images, graphics instruction, offline SW, ch15 overlap.
- `make check` still fails on pre-existing `drafts/plans/tsa-on-itself.md` markdown link and `sync:field-v2 --check` (field-v2.json). Structure, citations, claim spine passed.

## Key paths
- `chapters/ch01-wrong-object.tex`
- `site/src/pages/cards/index.astro`
- `site/src/lib/card-catalog.ts`
- `drafts/site-notes-pass.md`

## Commits
- `d8d21a72a` Simplify Chapter 1 opening and trim tell-don't-show "serious" across the book.
