# 2026-09-05 — Field overview adjacent-work voice + panel order

## Trigger
User traced the “Consciousness and welfare neighborhood” block on `/field/`, then asked to rewrite it for a general audience (including funders): drop “bearer admission” jargon, use glossary-aligned plain language, reorder panels, and end session with commit.

## Done
- **`FieldPreviewHub.astro`:** Plain-language consciousness/welfare panel; moved **The research programs** to position 3 (after bridge dependency graph).
- **`FieldHubNav.astro`**, **`site/src/content/field/intro.md`:** Matching nav tile and v2 intro list copy.
- **`metadata/concepts.yml`** + **`bearer-admission-adjacent`** body/card: retitled “Consciousness and Who Counts”; general-audience intro with glossary + field coverage links.
- **`adjacent-work-v2.yml`** intro + **`FieldAdjacentWork.astro`** section heading aligned; `sync:field-v2` → `field-v2.json`.
- **`sync-concepts`** regenerated `site/src/content/cards/bearer-admission-adjacent.md`.
- Started `./serve-site.sh` in background for local review (http://127.0.0.1:4321/).

## Decisions
- Overview teaser stays hardcoded in `FieldPreviewHub` (short); full intro stays in adjacent-work YAML / v2 section.
- Technical MB3 / bearer-admission detail remains on `mb3-bearer-import` and Lean spine — not duplicated on the overview.
- Did **not** commit unrelated working-tree items (conversation-summary archive moves, `field.md`, sync noise from full site serve, untracked drafts).

## Open / next
- User asked to expand shorthand refs (e.g. `ch18`, `MB3`) into full named links in adjacent-work copy and `FieldAdjacentWork` — **not done** (intro/firewall/item `book:` fields still plain text; component does not render markdown).
- Optional: plain-language lead-in for firewall paragraph on `/field/v2/#adjacent-work`.

## Key paths
- `site/src/components/FieldPreviewHub.astro`
- `metadata/concepts/bodies/bearer-admission-adjacent.md`
- `reference/field-agendas/data/adjacent-work-v2.yml`

## Commits
- (this session)
