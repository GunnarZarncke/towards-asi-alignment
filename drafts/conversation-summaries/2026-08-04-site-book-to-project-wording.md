# 2026-08-04 — Site “book” → “this project” wording

## Trigger
User asked that the companion site not refer to “the book” when meaning the TSA project (site, Lean, experiments, framework). Keep “book” for chapters, PDF, book map, and other directly manuscript-related material.

## Done
- Replaced project-wide “the book / this book / the book’s” with “this project” across site pages, reading paths, badges, SEO, field hub, experiments index, field agenda cards, field news, and synced JSON.
- Updated sync script templates (`sync-field-agendas.mjs`, `sync-chapter-cards.mjs`, `sync-lean-spine.mjs`) so future `npm run sync` preserves the rule (`**How this project treats it.**`, `**Project separates:**`).
- Updated upstream sources: `metadata/concepts/bodies/*`, `metadata/experiments.yml`, `metadata/field-news.yml`, `reference/field-agendas/data/agendas/*.yml`, `llms.txt`.
- Preserved manuscript-specific “book” where appropriate (PDF/book map FAQ, “full book argument”, BioShield example **in the book**, chapter illustrations); regenerated synced chapter pages from LaTeX after an over-broad bulk pass touched `site/src/content/book/`.
- Re-ran `sync:chapters`, `sync:concepts`, `sync:field-agendas`, `sync:field-news`, `sync:experiments`, `sync:lean-spine`, `sync:bot-orientation`.

## Decisions
- **“This project”** = TSA program (framework, site, Lean, experiments). **“Book/manuscript/PDF”** = long-form artifact and chapter content.
- Field comparison heading: `How this project treats it` (not “How this book treats it”).
- Awkward bulk hits fixed manually: Turchin audit “Failures enter the framework indirectly”; Lean graph “same sources as the manuscript”.
- Did not stage unrelated untracked drafts (`lw-*`, `TSA.png`, etc.).

## Open / next
- Optional polish: some field agenda cards now say “This project treats…” immediately after “How this project treats it.” (redundant but accurate).
- Presentation TODO (`metadata/TODO.md`) still tracks de-centering PDF as flagship entry point — separate from this wording pass.

## Key paths
- `site/src/pages/index.astro`, `site/src/lib/seo.ts`, `site/src/lib/badges.ts`
- `site/scripts/sync-field-agendas.mjs`
- `metadata/concepts/bodies/`, `reference/field-agendas/data/agendas/`

## Commits
- `b6b3a46f` Use “this project” on the site when “book” meant the TSA program.
