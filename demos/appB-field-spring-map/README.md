# Field Crux Map

Place [AISafety.com](https://aisafety.com/map) organizations on the book's bridge cruxes (MB1–MB11). Springs pull each listing toward the bridges it works on — inherited from the Appendix B field matrix when the org matches, otherwise from a conservative heuristic. A short spring means the org *touches* that crux, not that the crux is solved.

This is an **Appendix B / field-hub illustration**, not a Chapter 5 manuscript demo. It extends the curated field matrix ([`reference/field-agendas/`](../../reference/field-agendas/)) with spatial layout — not the Alignment Crux Map grant’s six-word disambiguation.

## What it shows

- **Who:** all map organizations (frozen snapshot).
- **What crux:** non-binary weights per bridge — inherited from agenda matrix cells where clustering matches, otherwise keyword heuristics.
- **Where:** spring layout with fixed bridge anchors (dependency graph or circle). Toggle geometry in the demo.

Scores mean “touches this crux in field evidence or classifier/heuristic,” **not** bridge discharge to Safe.

## Limitations

- Cluster grain ≠ org grain: listings that **match a clustering label** inherit that agenda’s matrix row (token/acronym match, not substring).
- Empty matrix cell = zero weight in this demo, not “agenda silent on crux.”
- Heuristic scores for unmatched listings use specific phrases, not generic words like `research` / `eval`.
- Default view includes any listing whose **comma-split** AISafety.com categories contain a research/governance token (MIRI is `Governance, Advocacy, Conceptual research`).
- Matrix cells sometimes cite evidence tagged to a different bridge (mostly MB4 rows copied onto MB4a). The inspect panel marks those `matrix-only`.
- Category-based AISafety.com `x,y` is not used for placement (diagnostic only in snapshot).

## Run

```bash
cd demos
python3 serve.py
# open http://127.0.0.1:8765/appB-field-spring-map/
```

## Refresh data

```bash
# Bridge positions from field hub Graphviz (requires `dot`):
python3 demos/appB-field-spring-map/scripts/extract_bridge_layout.py

# Listings, weights, and map logos (CC-BY-4.0 → data/logos/):
python3 demos/appB-field-spring-map/scripts/build_snapshot.py
python3 demos/appB-field-spring-map/scripts/build_snapshot.py --remap-existing  # re-score frozen listings
# optional: --llm with OPENAI_API_KEY in repo-root .env
```

Dependency geometry uses [`data/bridge-layout.json`](data/bridge-layout.json) (from `mb-bridge-dependencies-v2.dot`), including red antecedent edges and dark assembly edges into MB11 — matching the field overview chart.

## Files

- `data/snapshot.json` — frozen listings + weights (CC-BY-4.0 attribution in `meta`)
- `weights.ts` / `physics.ts` / `layout.ts` — weight model and force simulation
- `scripts/build_snapshot.py` — ingest pipeline
