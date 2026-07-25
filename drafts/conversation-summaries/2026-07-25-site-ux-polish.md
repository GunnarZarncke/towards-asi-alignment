# 2026-07-25 — Site UX polish (illustrations, nav, experiments table, standalone claims)

## Trigger
User requested small companion-site corrections: chapter illustrations overflowing the content box; MB bridge links duplicated below the experiments coverage table; standalone claims grid on homepage should move to a hub card; navigation order should reflect reader interest with glossary second-last and search last.

## Done
- **`site/src/styles/global.css`** — global `.book-figure` sizing; `min-width: 0` on two-column grid children to stop wide chapter art overflowing.
- **`site/src/components/ExperimentCoverageTable.astro`** + **`site/src/pages/experiments/index.astro`** — MB1–MB10 row labels link to bridge cards; removed redundant bridge-card list below the table.
- **`metadata/concepts.yml`**, **`metadata/concepts/bodies/standalone-claims.md`**, generated **`site/src/content/cards/standalone-claims.md`** — new hub card; homepage links to it instead of listing four cards inline.
- **`site/src/pages/index.astro`**, **`site/src/pages/illustrations/[id].astro`** — homepage hub link; dropped duplicate figure CSS (now global).
- Nav reorder (Book/FAQ before meta items; Glossary + Search last) was already present in HEAD before this commit (`SiteLayout.astro` unchanged in working tree).

## Decisions
- MB7d coverage row links to the shared MB7 bridge card (no separate MB7d card exists).
- Standalone-claims hub is a generated concept card roster entry, not a bespoke Astro page.

## Open / next
- **`site/scripts/sync-chapters.mjs`** roadmap → `current-status.tex` fix is still uncommitted (see [2026-07-25-site-roadmap-sync-fix.md](2026-07-25-site-roadmap-sync-fix.md)).
- **Concept logo** work (`CardSection.astro`, `ConceptLogo.astro`, `sync-concept-logos.mjs`, `public/concept-logos/`) is untracked — not part of this session.
- **HF field-news body** rewrite (`metadata/field-news/bodies/openai-huggingface-jul-2026.md`) still uncommitted.
- Full `npm run build` may still need the sync-chapters fix before prebuild completes.

## Key paths
- `site/src/styles/global.css`
- `site/src/pages/experiments/index.astro`
- `site/src/content/cards/standalone-claims.md`
- `metadata/concepts/bodies/standalone-claims.md`

## Commits
- (filled after commit)
