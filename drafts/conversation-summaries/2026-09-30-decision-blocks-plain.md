# 2026-09-30 — Decision blocks plain language

kind: new-work
uptake: status

## Trigger
Complete the open site-notes item: rewrite "What decision changes?" on cards in non-technical language (pilot CIRL, then all projections/bridges/jargon-heavy concepts).

## Done
- content: Pilot `subsumption-cirl` in `metadata/projections.yml`; then all 13 projections, 16 bridges, 18 jargon-heavy concepts in `metadata/*.yml`. Plain concepts, field news, and release cards unchanged.
- content: Hand card `site/src/content/cards/unsupervised-agent-discovery.md` aligned with synced concept wording.
- bookkeeping: `sync:projections`, `sync:bridges`, `sync:concepts`. Closed plan → `drafts/attic/site-notes-pass.md`.

## Decisions
- Edit `decision:` in YAML only (generated concept/bridge/projection cards are gitignored); hand artifact cards updated when they duplicate a concept decision.
- Pattern: Monday-morning question; swap jargon for glossary paraphrases without changing the decision bite.

## Open / next
- (none — site-notes plan closed)

## Key paths
- `metadata/projections.yml`, `bridges.yml`, `concepts.yml`
- `drafts/attic/site-notes-pass.md`

## Commits
- (filled in at session end)
