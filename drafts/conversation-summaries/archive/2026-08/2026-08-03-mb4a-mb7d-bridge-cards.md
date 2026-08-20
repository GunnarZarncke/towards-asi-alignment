# 2026-08-03 — MB4a / MB7d explicit bridge cards

## Trigger
User: introduce explicit MB4a and MB7d bridge cards on the site; disambiguate matrix column links; link from MB4 → MB4a and MB7 → MB7d in card text.

## Done
- Added `mb4a-measured-path-legitimacy` and `mb7d-acausal-coordination` to `metadata/bridges.yml` with body files under `metadata/concepts/bodies/`.
- Updated `reference/field-agendas/data/bridges.yml` `cardSlug` for **MB4a** and **MB7d** (matrix headers now link to distinct cards).
- MB4 / MB7 body prose links to sibling cards; `bridge-crosswalk.json`, `sync-lean-spine.mjs`, `sync-chapter-cards.mjs`, `site/.gitignore` updated.
- Ran `sync:bridges`, `sync:field-agendas`, `sync:lean-spine`.

## Key paths
- `/cards/mb4a-measured-path-legitimacy/`
- `/cards/mb7d-acausal-coordination/`
- Field matrix columns **MB4a** / **MB7d** → respective cards via `mbBridgeCards` in `field-agendas.json`
