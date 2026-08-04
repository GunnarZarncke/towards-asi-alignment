# Field agenda graphs

| File | Content |
|------|---------|
| [`mb-bridge-dependencies.dot`](mb-bridge-dependencies.dot) | MB1–MB11 bridge dependency graph (field nouns from [`data/bridges.yml`](../data/bridges.yml)); red edges = logical MB→MB antecedents; black edges = safety-case assembly into MB11 |
| [`mb-bridge-dependencies.png`](mb-bridge-dependencies.png) | Rendered PNG (regenerate from repo root) |

Companion site: clickable SVG synced to `/field/#bridge-dependencies` via `site/scripts/sync-bridge-graph.mjs` (run `npm run sync:bridge-graph` in `site/`).

```bash
dot -Tpng -o reference/field-agendas/graphs/mb-bridge-dependencies.png \
  reference/field-agendas/graphs/mb-bridge-dependencies.dot
```

Lean proof-spine graphs (P*, full bridge context) live under [`context/lean_proof_graphs/`](../../../context/lean_proof_graphs/).
