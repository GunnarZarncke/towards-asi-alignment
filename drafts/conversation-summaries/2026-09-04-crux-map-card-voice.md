# 2026-09-04 — Crux map card uses listing voice

## Trigger
The public Alignment Crux Map card was mostly generated prose. Replace it with the grant listing wording in `funding-applications/alignment-crux-map/alignment-crux-map-final.md`.

## Done
- Rewrote [`site/src/content/cards/funding/alignment-crux-map.md`](../../site/src/content/cards/funding/alignment-crux-map.md): lede, problem, approach, and success/fail follow the listing.
- Grouped milestones into **Minimum** / **Ideal**; dropped named researchers (kept generic external lab / CHAI-or-equivalent where needed).
- Kept funding-card section headings and existing frontmatter (dependsOn TSA, field-hub link, related cards).
- Dropped listing-only third person and grantmaking chrome. Fixed listing typo "ad a simulated" → "and a simulated"; added missing "that" in "field that tells you".

## Decisions
- Do not keep the generated "job / dollar buying / hold-always ruleset / month 1–3" expansion. The listing is the voice source.
- Minimum package: core lab + one external lab evaluation (deception and evals).

## Open / next
- Production site updates on next deploy.
- Left unstaged: conversation-summary archive moves, `field.md`, `experiments.json`, `chapter-reading-graph.json`, `card-redirects.json`, `alignment-problem-alternative-decomposition.md`.

## Key paths
- `funding-applications/alignment-crux-map/alignment-crux-map-final.md` (local; gitignored)
- [`site/src/content/cards/funding/alignment-crux-map.md`](../../site/src/content/cards/funding/alignment-crux-map.md)
- [`drafts/plans/alignment-crux-map.md`](../plans/alignment-crux-map.md)

## Commits
- (this session)
