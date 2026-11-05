# 2026-11-05 — Knecht shutdown sabotage cite + news

kind: new-work
uptake: local

## Trigger
User asked to add one hedged Ch. 35 sentence with an App P reference, and a field-news card (agent-count / what is the agent, prompts are not stops, irreversibility; skip the task-coupling finding).
Prompts: paraphrase-only

## Done
- content: One sentence in `chapters/ch35-multi-agent-strategic-coupling.tex` citing `knecht2026shutdownsabotage` and App P Market 7; hedge that the pattern may depend on capability.
- content: App P Market 7 closest-work cite list now includes Knecht beside Schlatter and Potter.
- content: Bib + `\bibsummary{knecht2026shutdownsabotage}`.
- content: Field-news card `field-news-knecht-shutdown-sabotage-sep-2026` and quiz takeaway.
- bookkeeping: `cd site && npm run sync:field-news` wrote 34 cards. `make check`: citations, bibliography summaries, quiz bank pass. Markdown-link FAIL is five blocking links to untracked `papers/alignment-frames/` (pre-existing, not this card).

## Decisions
- Primary chapter is 35 (coupled unit vs nameplates), not a Schlatter/Potter replacement.
- Skip the independent-vs-coupled-task finding as requested.
- No meme.

## Open / next
- Optional: author pass on the Ch. 35 sentence.
- Uncommitted in tree (other sessions): alignment-frames paper, lw-wiki-tags, viable-values attic, field-agenda matrix, generated book-stats, etc.

## Key paths
- `chapters/ch35-multi-agent-strategic-coupling.tex`
- `metadata/field-news/bodies/2026-09-knecht-shutdown-sabotage.md`
- `appendices/appP-bridge-predictions.tex`

## Commits
- none
