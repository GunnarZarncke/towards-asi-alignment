# 2026-10-23 — Lens cards and clickable frame map

kind: new-work
uptake: local

## Trigger
User asked for a new card type `lens`, cards for all graph nodes, agenda links both ways, quotes from the frames draft or LessWrong tags, concept links, an overview card “lenses and frameworks” with a clickable SVG like the bridge map, and edge labels to Lean on GitHub.
Prompts: paraphrase-only

## Done
- content: Card type `lens` (`badges.ts`, `card-urls.mjs`, catalog, visit-history, card page sidebar).
- content: 29 lens cards + overview from `site/scripts/lib/lenses-data.mjs`; `npm run sync:lenses`.
- content: Clickable variant-b SVG (`sync-lens-graph`); nodes → `/cards/lens/{slug}/`; edge labels → `FrameMorphisms` / `FrameComposePaths` / `FrameIncompatibility` / `FrameRelations` on GitHub.
- content: Agenda YAML `related:` on Christiano, MIRI, CHAI, Redwood, GSAI, Safeguarded AI, Anthropic, OpenAI, ARC, DeepMind, MAI/CIP, Orthogonal, CLR.
- content: Concept reverse links on field coverage, field map, CCI.

## Decisions
- Source of truth is `lenses-data.mjs`, not `concepts.yml`. Graph is certification-geometry variant **b**.
- Duplicate `route→cycle` edges share one GitHub href (summand vs project).

## Open / next
- Search-index inclusion of lens cards depends on existing `build-search-index` filters; run full `npm run sync` before deploy.
- Session not committed unless asked.

## Key paths
- `site/src/content/cards/lenses/lenses-and-frameworks.md`
- `site/public/field-graphs/alignment-frames-relations-b.svg`

## Commits
- none
