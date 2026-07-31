# 2026-07-25 — Tier A field news (manuscript + site)

## Trigger
Implement Tier A from the recent AI-safety events catalog: six widely discussed incidents with brief manuscript `\autocite{}` mentions and a companion-site “related news” layer.

## Done
- **Site:** `metadata/field-news.yml` + six body files; `site/scripts/sync-field-news.mjs`; `"news"` card type; `/news/` index; chapter-card “Related news” sidebar; nav/footer links; `.gitignore` for generated artifacts; `site/README.md` note.
- **Bibliography:** six keys in `references/manuscript-citations.bib` + matching `\bibsummary` lines (`aisi2026cheatingbehaviour`, `anthropic2026mythosalignment`, `metr2026frontierriskreport`, `openai2026accidentalcotgrading`, `openai2026huggingfaceincident`, `openai2026longhorizonsafety`).
- **Manuscript:** one-sentence cites in ch11, ch12, ch14, ch22, ch28, ch30, ch33, ch38, ch39, ch40, ch41, ch42 (footnote → `/news/`), ch43, appB.
- **Verify:** `python3 scripts/check_bibliography_summaries.py` passed; `npm run sync && npm run build` in `site/` succeeded (`/news/index.html` built).

## Decisions
- Bridge slugs on the news index were dropped (card slugs are longer than bare `mb*` ids); bridges remain in YAML for future sidebar/filter use.
- Generated news cards + `field-news.json` stay gitignored (same pattern as other sync outputs); CI runs `sync:field-news --check`.
- ch42 footnote points readers to `https://towards-alignment.com/news/` as the live incident index.

## Open / next
- Optional: ch26 long-horizon mention if a natural insertion point is wanted (Tier A table listed it; manuscript pass did not).
- Run `./build.sh` if a full PDF compile is needed to confirm LaTeX cites resolve.
- User did not request commit.

## Key paths
- `metadata/field-news.yml`, `metadata/field-news/bodies/`
- `site/scripts/sync-field-news.mjs`, `site/src/pages/news/index.astro`
- `chapters/ch39-passive-observation-not-enough.tex`, `chapters/ch42-safety-case.tex`

## Commits
- (none)
