# Field agenda graphs

| File | Content |
|------|---------|
| [`mb-bridge-dependencies-v2.dot`](mb-bridge-dependencies-v2.dot) | **Live** MB1–MB11 bridge dependency graph (field nouns from [`data/bridges.yml`](../data/bridges.yml)); includes MB1→MB3 bearer-admission edge; synced to `/cards/bridge-assumptions/#bridge-dependencies` |
| [`mb-bridge-dependencies-v1.dot`](mb-bridge-dependencies-v1.dot) | **Archived** graph frozen at v1 cutover (no MB1→MB3 edge); synced to `/field/v1/#bridge-dependencies` |
| [`mb-bridge-dependencies.dot`](mb-bridge-dependencies.dot) | Canonical copy of v2 (regenerate PNG from this or v2) |
| [`mb-bridge-dependencies.png`](mb-bridge-dependencies.png) | Rendered PNG (regenerate from repo root) |

Companion site: clickable SVGs via `site/scripts/sync-bridge-graph.mjs` (run `npm run sync:bridge-graph` in `site/`). Live hub at `/field/v2/`; `/field/` redirects there.

```bash
dot -Tpng -o reference/field-agendas/graphs/mb-bridge-dependencies.png \
  reference/field-agendas/graphs/mb-bridge-dependencies-v2.dot
```

Lean proof-spine graphs (P*, full bridge context) live under [`context/lean_proof_graphs/`](../../../context/lean_proof_graphs/).
