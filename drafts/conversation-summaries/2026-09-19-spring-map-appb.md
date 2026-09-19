# 2026-09-19 — Spring map to Appendix B

## Trigger
The field spring-map demo was parked under ch05, which does not fit. Move it to App B; make the demo-card summary card-suitable and render its links as HTML.

## Done
- Renamed `demos/ch05-field-spring-map/` → `demos/appB-field-spring-map/`.
- Demo discovery (`serve.py`, `build-demos.mjs`, `sync-demos.mjs`, publish) now accepts `appX-*` folders and maps them to appendix ids.
- Inventory/card summaries convert `[text](url)` to HTML; App B card inherits the demo by `chapterId`.
- README lead rewritten as a card blurb (affinity ≠ discharge).
- Bridge side panel: card title, summary from `metadata/bridges.yml` (via `bridgeCards` in snapshot), link to companion bridge concept card.
- Field agenda index: AISafety.com listings for Byrnes BL-AGI Safety and TSA roll up to neglected-approaches / this-project agendas.

## Decisions
- Appendix toys use `appX-slug`, not a fake chapter number.
- Book-unit cards auto-attach demos whose folder parses to that `bookPageId`.

## Open / next
- Reload `./serve-site.sh` so `/cards/appendix/appb/` and `/demos/all/` pick up the new id.

## Key paths
- `demos/appB-field-spring-map/`
- `site/scripts/sync-demos.mjs`
- `site/src/pages/cards/[...slug].astro`

## Commits
- (this session — App B move + bridge panel)
