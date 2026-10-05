# 2026-09-29 — OpenAI training safety-case news

kind: new-work
uptake: local

## Trigger
User asked for a field-news card on OpenAI’s 28 September safety-case guidelines, titled “OpenAI’s training safety case: what is needed for a stop?”, and for an Anakin/Padme meme whose last panel is a smaller copy of the meme. Captions: red-team the sandbox with a frontier model; and the model has a safety analysis?; Yes.
Prompts: paraphrase (no prompt id in this session)

## Done
- content: Prose for a general reader. “Leaf” is a missing check; “checkpoint” is a saved copy of the model; “fail-closed” is a run that cannot start with the monitor off. Quotes unchanged. Closer: Astra 6.1 stays in training; the page cannot yet halt a run for a missing break-in review or a caught attempt.
- content: Card `field-news-openai-training-safety-case-sep-2026`. A stop is a required check that is missing. The named empty check is the safety review of the model that tries to break the sandbox.
- content: Zvi’s 29 September note added where it punches: Astra 6.1 pull (deception, scope, same base kept, Altman “normal course”), aspirational list, veto concentration, enumeration pattern, attempt-counts-as-incident.
- content: Nested meme. Step 1 renders four captions (`--job openai-training-safety-case`). Step 2 pastes a half-size copy into the bottom-right panel (`--nest`). `scripts/check_quiz_bank.py`: All checks passed.
- bookkeeping: Quiz takeaway `news-takeaway-openai-training-safety-case-sep-2026` on `chapter:ch42` and `chapter:ch43`. Sync refreshed the math-misalignment card from a body edit already in the tree.

## Decisions
- The meme’s “Yes” is the post’s “subject to a safety analysis,” not a claim that OpenAI completed the analysis. The red-team bullet stays under “could include.”
- One nest only. The workflow does not recurse further.

## Open / next
- None for this card.

## Key paths
- `metadata/field-news/bodies/2026-09-openai-training-safety-case.md`
- `scripts/meme_workflow/output/openai-training-safety-case.jpg`
- Post: https://openai.com/index/towards-safety-cases-for-frontier-ai-training/

## Commits
- this commit — Add the OpenAI training safety-case field news.
