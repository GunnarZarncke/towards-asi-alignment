# 2026-11-11 — Hugging Face card, talker and doer

kind: new-work
uptake: local

## Trigger

The user judged Yudkowsky’s LessWrong reading of the Hugging Face incident compatible with this project’s field-news card, asked to add that comparison, then asked for news-card quote format and committed at end of session.
Prompts: paraphrase-only

## Done

- content: `metadata/field-news/bodies/2026-08-openai-hf-roadahead.md` — AI Village and Yudkowsky sections; amber quotes; LessWrong external link; Yudkowsky on source legend.
- content: Author tightened Village and Yudkowsky tails (condensed quote block, wrong-object closing on talk-y vs do-y within one model).
- content: `site/src/content/cards/field-news-openai-hf-roadahead-aug-2026.md` via `npm run sync:field-news`.
- bookkeeping: Handoff, session index, this log.

## Decisions

- Yudkowsky and Village split into separate `##` sections instead of one “Related observations” block.
- “Grader” stays his term.

## Open / next

- Unrelated dirty tree (field-agendas sync, book-stats, lw-wiki-tags plan, deleted `context/viable-values.*`, etc.) left unstaged.

## Key paths

- `metadata/field-news/bodies/2026-08-openai-hf-roadahead.md`

## Commits

- (this session)
