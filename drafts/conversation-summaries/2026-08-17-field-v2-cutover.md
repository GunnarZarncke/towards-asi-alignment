# Session: Field v2 hub cutover

**Date:** 2026-08-17

## Goal

Backup bridge dependency graph as v1; ship v2 graph on live field hub; archive v1 overview at `/field/v1/`; redirect `/field/` → `/field/v2/`.

## Shipped

### Bridge graphs
- Frozen **`mb-bridge-dependencies-v1.dot`** (pre-cutover graph, no MB1→MB3).
- Live **`mb-bridge-dependencies-v2.dot`** (+ `MB1 → MB3` bearer-admission edge); canonical `mb-bridge-dependencies.dot` updated to match v2.
- `sync-bridge-graph.mjs` syncs both → `bridge-dependencies-v1.*` / `bridge-dependencies-v2.*` + JSON metadata.

### Site routes
- **`/field/`** — 301 redirect to `/field/v2/`.
- **`/field/v2/`** — live hub (lifecycle axis, stance marks, v2 graph).
- **`/field/v1/`** — archived v1 matrix + v1 graph (no lifecycle / stance).

### Copy / meta
- `meta.yml` openSpineInterfaces no longer says "Preview".
- `sync-field-v2.mjs` note updated; `target-realization` concept body → Field hub link.

## Verification

- `npm run sync:bridge-graph` — pass (v1 + v2 SVGs)
- `npm run sync:field-v2` — pass
- `npm run build` (site) — pass; `/field/index.html` redirects to `/field/v2/`

## Open

- Consciousness Phase 4: v2-only adjacent-work YAML (separate from this cutover).
- Regenerate `mb-bridge-dependencies.png` from v2 dot if PNG parity wanted (optional).
