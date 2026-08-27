# 2026-08-26 — FAQ update for current site

## Trigger
User: the FAQ is outdated; update it.

## Done
- Rewrote `site/src/lib/faq-items.ts` against the current site (essays door, `/start/`, typed card URLs, on-site PDF, Field, Lean dependency spine).
- Dropped the July hedge that translations wait on card-structure stability; English is the working language, other editions are not in progress.
- Answers now carry real links (no `"essays"`/`"book"` stubs or hardcoded `/cards/six-thesis-claims/`).
- Merged the experiment-docs item into the experiments question; added “is alignment solved?” and Field.
- Start Here `what-not-claiming` link uses `/cards/objection/…`.
- Checked `/faq/` and `/start/`; all 22 unique FAQ answer URLs return 200.

## Decisions
- Keep engineer and policy as separate questions; fold generalist start into the first item.
- Structured `FaqSegment` links instead of magic-string special cases in `FaqList.astro`.

## Open / next
None for this pass.

## Key paths
- `site/src/lib/faq-items.ts`
- `site/src/components/FaqList.astro`
- `site/src/pages/faq.astro`, `site/src/pages/start/index.astro`

## Commits
- `bfe74565` Update the companion-site FAQ for current entry paths and typed card URLs.
