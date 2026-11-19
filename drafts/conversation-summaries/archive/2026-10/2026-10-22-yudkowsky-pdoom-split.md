# 2026-10-22 — Yudkowsky P(doom) split on odds calculator

kind: correction
uptake: local

## Trigger

User: does [Yudkowsky 20 Sep 2026](https://x.com/ESYudkowsky/status/2101804209528271092) inform the P(doom) calculator; add the source to the card either way.

Prompts: paraphrase-only

## Done

- **content:** Odds calculator keeps one-attempt F then D; no P(ASI) slider. Copy now says P(D | attempt, E) is not P(ruin|ASI)×P(ASI).
- **content:** Overview prediction card + safety-case YAML/JSON + odds page cite the tweet.
- **content:** Predictions aggregation blurb (YAML + sync) drops headline P(doom) as P(ruin|ASI)×P(ASI). Author reverted Appendix H prose; site and metadata carry the split.

## Decisions

- Informs the *framing*, not the PRA graph. Adding P(ASI) would be the conflation the tweet rejects.

## Open / next

- None for this lane.

## Key paths

- `site/src/content/cards/predictions/overview.md`
- `site/src/pages/predictions/safety-case/index.astro`
- `appendices/appP-bridge-predictions.tex`
- `metadata/predictions.yml`
