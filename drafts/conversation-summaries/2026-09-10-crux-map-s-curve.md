# 2026-09-10 — Crux map S-curve on funding card

## Trigger
Add the S-curve map from the original Alignment Crux Map application to the public Alignment Crux Map funding card.

## Done
- Copied the S-process cumulative U vs $ chart onto the funding card as a `book-figure`, after the Minimum / Ideal ask table.
- Public PNG at `site/public/funding/alignment-crux-map-s-process-curve.png` (same curve as the application; footer is the U definition, not the gitignored source path).

## Decisions
- Keep the original step dollars on the chart ($15,500 minimum). Card chrome still rounds the ask to two significant figures ($16,000).
- Caption is listing voice: what the marks mean and what 1 U is. Named contractors stay off the public card.

## Open / next
- Production site updates on next deploy.

## Key paths
- [`site/src/content/cards/funding/alignment-crux-map.md`](../../site/src/content/cards/funding/alignment-crux-map.md)
- `site/public/funding/alignment-crux-map-s-process-curve.png`
- `funding-applications/alignment-crux-map/` (local; gitignored)

## Commits
- `4afc17b4` Add S-process curve to Alignment Crux Map funding card.
