# 2026-09-30 — Apply LW wiki chapter quotes

kind: new-work
uptake: local

## Trigger
User asked to apply the plan in `drafts/plans/lw-wiki-chapter-quotes.md`.
Prompts: paraphrase-only (telemetry prompt ids not copied this turn).

## Done
- content: Wiki openings quoted at planned homes (ch04, ch06, ch07, ch10, ch14, ch16, ch17, ch21, ch23, ch25, ch31, ch33, ch43, ch46) and planned later mentions / section-level sites. `{GZ}` spans not edited. `{GZ+AI}` quotes sit in new `{AI}` blocks outside those environments (ch06, ch07, ch01 physical-boundary pointer).
- content: `\wikiq` indented unboxed quotes; `references/lw-wiki.bib` plus summaries; URL footnotes replaced by `\autocite`.

## Decisions
- Attribution is memoir `quote` plus `\autocite` on `@online` keys in `references/lw-wiki.bib` (no URL footnotes).
- Full quotation once; later chapters use a clause plus `\ref`.

## Open / next
- Author read of whether the quotations add legitimacy or imported authority. Pilot order was executed as part of the full apply, not as a stop.

## Key paths
- `drafts/plans/lw-wiki-chapter-quotes.md`
- `chapters/ch*.tex` (homes and cross-refs)

## Commits
- none
