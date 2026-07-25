# 2026-07-25 — Concept logo placement (trailing + inline links)

## Trigger
User asked to move concept logos to the **end** of concept names (keep existing title sizes) and show them on **every concept link**, sized to line height. Prior session had wired logos at the start of titles. Also built PDF (`./build.sh` → 1363 pp).

## Done
- **Trailing logos on titles:** concept card `h1` (72px), card index `CardSection` h3 links (40px), badge/gem/status index grids, home “Five Failure Modes”, reading-path card steps.
- **Inline link logos (1em):** rehype plugin appends logo to markdown links targeting `/cards/{slug}/` or relative `../../{slug}/` when a logo exists; `ConceptCardLink.astro` for template links (sidebar, glossary, crosswalk lists, field projections, etc.).
- **Shared infra:** `concept-slug-from-href.mjs`, `concept-logo-svg.mjs`, `rehype-concept-link-logos.mjs`; global `.concept-logo` / `.concept-logo--inline` CSS; `conceptSlugFromHref()` in `concept-logos.ts`.
- **Build verified:** `npx astro build` (768 pages); PDF build succeeded earlier in session.

## Decisions
- Rehype handles markdown bodies (chapters, card prose); `ConceptCardLink` handles Astro template links. Logo only when slug is in `concept-logos.json` manifest.
- Title listings keep fixed px sizes (40/72); inline links use `1em` with slight vertical nudge.
- Did not commit unrelated working-tree edits (RELEASE_NOTES, chapter `.tex` table tweaks, `release-v1-3-0` gitignore line).

## Open / next
- Optional: extend `ConceptCardLink` to experiments/lean pages with hardcoded concept `<a>` tags.
- Optional: logos for eight `subsumption-*` cards.
- Unstaged: `RELEASE_NOTES.md`, four chapter `.tex` files, `site/.gitignore` (v1.3.0 release card).

## Key paths
- `site/scripts/lib/rehype-concept-link-logos.mjs`
- `site/src/components/ConceptCardLink.astro`
- `site/src/components/ConceptLogo.astro`
- `site/src/styles/global.css` (`.concept-logo` rules)

## Commits
- (this session)
