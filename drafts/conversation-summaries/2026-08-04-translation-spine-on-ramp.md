# 2026-08-04 — Translation spine on-ramp (Phases 1–2)

## Trigger
User feedback: Lean unread due to translation cost, not emptiness; field projections crosswalk is the on-ramp. Plan: invert Lean page, add check pages, expand projection roster, wire graph→cards.

## Done
- **`/lean/` reframe:** question-first hero; projections table above fold; Common checks callout; full spine under `#spine-detail`.
- **`FieldProjectionsTable`:** Lean status column (`proof` / `counterexample`) from `metadata/projections.yml`.
- **`/lean/check/corrigibility/`:** roster in `metadata/lean-checks/`; `sync-lean-checks.mjs`; stepping stones, forward/separation lists, MB4/MB4a caveats.
- **Four new projection rows:** `subsumption-embedded-agency`, `subsumption-selection-basin`, `subsumption-grounding-drift`, `subsumption-deployment-gate` (+ bodies with formulas/leanNodes).
- **Graph wiring:** `PROJECTION_CARD_SLUG` in `sync-lean-spine.mjs`; four nodes in `05-field-subsumptions.dot`; aliases in `lean_graph_node_aliases.json`; SVG clicks → projection cards.
- **Reverse term-links:** extended `term-links.yml`; `sync-term-links.mjs` → `term-links-reverse.json`; `TermLinksReverse.astro` on projection cards and check sidebar.
- **Cards:** `graphNodeId` in projection card frontmatter; field graph link on projection card sidebars; removed unused `FieldProjectionsTable` import from card template.

## Decisions
- **Check namespace:** `/lean/check/{slug}/` under Lean spine (not separate `/audit/` hub).
- **Hidden BIQ deferred:** ~~no `subsumption-hidden-biq` row until Field-style separation or explicit bound-framing~~ **Superseded 2026-08-04 follow-on:** bound-framed card (appearance ceilings, no Field-style converse).
- **Stable URLs:** kept `subsumption-*` slugs and `field-subsumptions` graph slug.

## Verification
- `npm run sync:projections`, `sync:lean-checks`, `sync:lean-spine`, `sync:term-links`, `build:search-index` — ok.
- `npm run build` — 853 pages including `/lean/check/corrigibility/`.
- Graph SVG: field nodes link to `/cards/subsumption-*/`.
- **Follow-up (same session):** `declIndex` in `lean-spine.json` (1289 decls) with GitHub `#L` anchors; `LeanDeclLinks.astro` on projection cards (main + sidebar); check page uses same index.
- **Phase 2 (same day):** `/lean/check/cirl/`, `/lean/check/elk/`; `subsumption-hidden-biq` projection + graph `BIQ`; hero check buttons on `/lean/`.

## Open / next (Phase 2)
- ~~Check pages for CIRL and ELK.~~ **Done 2026-08-04 (follow-on):** `/lean/check/cirl/`, `/lean/check/elk/`; hero buttons on `/lean/`.
- ~~`subsumption-hidden-biq` after Lean work.~~ **Done 2026-08-04 (follow-on):** bound-framed projection card (`leanStatus: proof`); graph node `BIQ`; term-links for trace/hidden BIQ.
- App G opener mirroring site projections table.
- Full `/glossary/reverse/` hub (optional).

## Key paths
- `site/src/pages/lean/index.astro`, `site/src/pages/lean/check/[slug].astro`
- `metadata/projections.yml`, `metadata/lean-checks/index.yml`
- `site/scripts/sync-lean-checks.mjs`, `site/scripts/sync-term-links.mjs`
- `context/lean_proof_graphs/05-field-subsumptions.dot`

## End of session (2026-08-04)
- Committed translation spine Phases 1–2: field-first `/lean/` on-ramp, check pages (corrigibility, CIRL, ELK), 13 projection rows incl. hidden-BIQ, Lean decl source links, graph→card wiring, reverse term-links.
- **Not staged:** `TSA.png`/`TSA.svg`, LW debate drafts, hackathon entries, `node_modules/`, unrelated session-log commit-hash touch-ups.
