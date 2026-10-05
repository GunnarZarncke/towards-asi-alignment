# 2026-10-05 — Predictions hub catalog label

kind: correction
uptake: status

## Trigger
Move related forecasts below the catalog. Fold Metaculus 6509 into that list. Keep underspecification discussion in the appendix. Do not head the catalog as “the eighteen markets.”

Prompts: (paraphrase — this session)

## Done
- content: Hub and overview card heading is “AI alignment subproblem markets.” Related forecasts sit after that list; 6509 is a related item with a short question note only.
- content: Appendix H keeps the underspecified-question paragraph and catalog section title match.
- housekeeping: Dropped `underspecifiedExamples` from YAML and sync.

## Decisions
- Catalog count stays an implementation detail (`market-01`–`market-18` IDs), not a public heading.

## Open / next
- None for this copy pass.

## Key paths
- `site/src/pages/predictions/index.astro`
- `metadata/predictions.yml`
- `appendices/appP-bridge-predictions.tex`

## Commits
- none
