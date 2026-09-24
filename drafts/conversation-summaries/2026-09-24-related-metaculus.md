# 2026-09-24 — Related Metaculus links

## Trigger
Link Metaculus 31707, 38190, and 38597 from the predictions hub as related questions, not in the same slot as 44423. Explain why 6509 does not fit the catalog.

## Done
- `metadata/predictions.yml`: `relatedForecasts` for 38190 (US safety-check mandate), 38597 (US deployment veto), and 31707 (2029 expert-sufficiency survey).
- `site/scripts/sync-predictions.mjs` and `/predictions/`: a Related forecasts section with outbound links. 44423 stays the only `externalFactors` entry.
- Catalog overview card lists the same three under a separate heading.
- Plan note in `drafts/plans/predictions/assurance-risk-modelling.md`.
- Metaculus 6509 listed as an underspecified-question example on the hub and in Appendix H’s judgment section. Control is not defined; a later consensus records how experts use the word.

## Decisions
- No embeds, no prediction cards, and no assurance-model role for the three related links. They are context only.
- 6509 is not a bridge market or related forecast. It is listed only under `underspecifiedExamples` because “control” is undefined and expert consensus tracks future use of the word.

## Open / next
- 44423’s live question is conditional on control of Congress. The appendix gloss still describes it as one unconditional legislation price.

## Key paths
- `metadata/predictions.yml` (`externalFactors`, `relatedForecasts`)
- `site/src/pages/predictions/index.astro`

## Commits
- `c9662fc66` Link nearby Metaculus forecasts on the predictions hub and cite 6509 as an underspecified question.
