# Field crux spring-map prototype

Status: **built** (2026-09-18). Demo: [`demos/appB-field-spring-map/`](../../demos/appB-field-spring-map/).

Research toy — not manuscript canon, not `/field/` hub integration.

## Goal

Ingest AISafety.com map listings, assign non-binary `MB*` bridge weights, lay out with a spring model. Compare placement modes (fixed bridge anchors vs movable bridges vs project similarity).

## Delivered

- `scripts/build_snapshot.py` — fetch API, cluster match, matrix inherit, heuristic fallback
- Frozen `data/snapshot.json` (369 listings, CC-BY-4.0)
- Canvas demo: modes A/B/C, filters, inspect panel
- Vitest on weights + physics

## Crux assignment

- **Inherited:** listing matches [`clustering.yml`](../../reference/field-agendas/data/clustering.yml) → agenda row from [`matrix.yml`](../../reference/field-agendas/data/matrix.yml) + [`evidence.yml`](../../reference/field-agendas/data/evidence.yml)
- **Heuristic:** unmatched listings — keyword/category scoring (optional `--llm` refresh)

## Layout modes

| Mode | Behavior |
|------|----------|
| A (default) | Pinned bridge nodes; project springs weighted by crux affinity |
| B | Movable bridges + dependency springs from v2 bridge graph |
| C | Project–project cosine similarity edges only |

## Out of scope

Writing classifier output into field YAML; claiming bridge discharge; live API in browser.
