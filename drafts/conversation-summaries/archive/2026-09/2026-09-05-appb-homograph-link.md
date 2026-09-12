# 2026-09-05 — Appendix B ontology-homograph link

## Trigger
User reported a broken “Ontology homographs” link on `/cards/bridge/bridge-assumptions/` (`/full/appB/…`). Working URL is `/cards/appendix/appb/`. Asked to check for other copies.

## Done
- Pointed both live copies at `/cards/appendix/appb/#sec:ontology-homographs-appb` (`bridge-assumptions`, `field-map-starting-points`).
- Same sentence on the field-map card: Appendix B href from `/cards/chapters/appB/` to `/cards/appendix/appb/`.
- Redirects `/full/appb/` and `/full/appB/` → `/cards/appendix/appb/`.
- Corrected stale `/full/` path docs in `AGENTS.md` and `site/README.md` (overview hubs are `/cards/appendix/{id}/` + `/full/` suffix).
- Regenerated concept/bridge cards and `card-redirects.json`.

## Decisions
- Kept the section fragment: synced App B still has `<span id="sec:ontology-homographs-appb">`.
- Did not rewrite the many `/cards/chapters/…` body links; those still redirect.
- Left `drafts/plans/cousin-product-comparison.md` (closed plan) mentioning the old pair of URLs.

## Open / next
- None for this link. Deploy picks up the card hrefs and the `/full/appB/` redirect.
- Left uncommitted (not this task): August log archive moves, `2026-09-05-v1-6-0-release-notes.md`, `drafts/plans/field.md`, `experiments.json`, `chapter-reading-graph.json`, `drafts/alignment-problem-alternative-decomposition.md`.

## Key paths
- `metadata/concepts/bodies/bridge-assumptions.md`
- `metadata/concepts/bodies/field-map-starting-points.md`
- `site/scripts/generate-card-redirects.mjs`

## Commits
- `2382b0a3` Fix broken Appendix B ontology-homograph links on the site.
