# 2026-10-05 — Mixed qualifying attempts resolve YES

kind: correction
uptake: rule

## Trigger
Contracts should resolve YES when several qualifying attempts exist and at least one met the frozen bars, even if another missed them.
Prompts: paraphrase

## Done
- content: Appendix P reading rules and resolution section state the priority: YES if any qualifying attempt met the bars; NO only if every qualifying attempt missed them; OTHER only if none existed.
- content: All 21 question lines in the boxes and all 18 `marketQuestion` strings in `metadata/predictions.yml` now use "at least one" / "every qualifying attempt."
- content: Prediction card footer and yaml `reconstructibility` text match the rule.
- bookkeeping: `npm run sync:predictions` and `npm run sync:chapters` succeeded; local `astro sync` reported "Synced content."

## Decisions
- Mixed YES and NO across qualifying attempts resolves YES, not ambiguous and not NO.

## Open / next
- Draft lane plans under `drafts/plans/predictions/` still use the old one-attempt wording; appendix is canon.

## Key paths
- `appendices/appP-bridge-predictions.tex`
- `metadata/predictions.yml`
- `site/scripts/sync-predictions.mjs`

## Commits
- none
