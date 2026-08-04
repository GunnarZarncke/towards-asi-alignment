# 2026-08-02 — Bridge cards field-first prose

## Trigger
User: now that bridges feature prominently on the Field hub, each bridge card should open with the field crux in general technical-audience language, then introduce the precise book definition, with links into concept (and related) cards.

## Done
- Rewrote body prose for MB1–MB10 + `bridge-assumptions` under `metadata/concepts/bodies/` to the pattern: field crux → **precise bet (MBn)** → evidence/consequence note.
- Added inline `/cards/...` links to concept and sibling bridge cards (boundary discovery, CCI, strategic opacity, conserved properties, etc.).
- Softened `metadata/bridges.yml` summaries to lead with the field wall, then "Precise bet: …".
- Expanded `related:` side-panel lists to match in-prose links.
- Regenerated site cards: `cd site && npm run sync:bridges` (11 cards; `--check` clean).

## Decisions
- Keep experimental-evidence paragraphs; do not bury them under new headings. Flowing prose with an explicit "precise bet" sentence is enough structure for card length.
- Do not invent a separate MB11 bridge card; matrix already maps MB11 → `dynamical-guarantee` (prior Field-hub decision).
- Summaries stay short teasers; full field framing lives in the body.

## Open / next
- Optional: same field-first pass on MB11-facing `dynamical-guarantee` / MB4a-facing CCI card if Field-hub readers land there next.
- Optional: spot-check live card pages once deployed.

## Key paths
- `metadata/bridges.yml`
- `metadata/concepts/bodies/mb*.md`, `bridge-assumptions.md`
- `site/src/content/cards/mb*.md` (generated)
- Field hub: `site/src/content/field/intro.md`, `/field/`

## Commits
- `5f60f9b0` Make bridge cards field-first for Field hub readers.
