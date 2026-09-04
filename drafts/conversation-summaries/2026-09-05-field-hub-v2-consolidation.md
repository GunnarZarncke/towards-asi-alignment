# 2026-09-05 — Field hub v2 consolidation + bridge card table

## Trigger
Continuation after adjacent-voice commit: consolidate `/field/` on v2 preview panels, split external maps to a concept card, plain-language Alignment Target intro, bridge-assumptions panel on hub, drop redundant Bridge/Card table columns; end session with commit.

## Done
- **`/field/` → `/field/v2/`:** `field/index.astro` redirect; live hub trimmed intro + `FieldPreviewHub` panels; removed `FieldHubNav`.
- **`FieldPreviewHub.astro`:** eight preview panels (coverage, bridge graph, research programs, bridge assumptions box, lifecycle, alignment target, consciousness/welfare, field maps); bridge assumptions linked after research programs.
- **`field/intro.md`:** trimmed through “multitude of agendas”; dropped “What you will find here” / “A map of the field” block.
- **New concept card `field-map-starting-points`:** external surveys/maps + how this site relates (`metadata/concepts.yml` + body + synced card).
- **`alignment-target`:** general-audience summary + body opening; FAQ points at v2 hub + field-map card.
- **`bridge-assumptions`:** table is two columns (Field open problem | Bridge with links); `bridges.yml` summary tweak.
- **Sync artifacts:** `field-v2.json`, `card-redirects.json`, generated concept/bridge cards; script comment updates; `docs/MANUSCRIPT.md` field blurb.

## Decisions
- `/field/` redirects; canonical reader URL is `/field/v2/`.
- “A map of the field” lives on `field-map-starting-points`, not the hub intro.
- Bridge index table links live in the Bridge column only (Card column dropped).
- Did **not** commit unrelated tree: conversation-summary archive moves, W-17 `experiments.json` sync noise, `chapter-reading-graph.json` timestamp, untracked alignment decomposition draft.

## Open / next
- Expand `ch18` / MB shorthand to full named links in adjacent-work copy; render markdown in `FieldAdjacentWork.astro` — still open from prior slice.
- Deploy to production when ready (local dev verified on `:4321`).

## Key paths
- `site/src/pages/field/v2/index.astro`
- `site/src/components/FieldPreviewHub.astro`
- `metadata/concepts/bodies/field-map-starting-points.md`
- `metadata/concepts/bodies/bridge-assumptions.md`

## Commits
- (this session — after `c61d7c44` adjacent-voice slice)
