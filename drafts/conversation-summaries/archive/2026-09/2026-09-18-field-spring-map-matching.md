# 2026-09-18 — Spring-map matching + evidence audit

## Trigger

Fix heuristic/cluster matching; inspect evidence that drives matrix inherit.

## Done

- Token/acronym name match (no `arc` ⊂ `research`). Tests in `scripts/test_matching.py`.
- Collapse clustering `--` slugs to matrix `-` slugs so Pause/CLR/GSAI/etc. inherit.
- Phrase-level keyword heuristics; `--remap-existing` rescores frozen listings.
- Inspect panel lists evidence IDs per bridge; `matrix-only` when the cell bridge is not on `evidence.yml`.
- Remapped `data/snapshot.json`: inherited 38→63; MB6∩MB10 40→12.

## Decisions

- Weights still follow **matrix cell placement**, not `evidence.bridges` intersection. Eight matrix citations sit on a bridge the evidence row does not list (MB4→MB4a copies; METR #36 on MB11).
- Genuine MB6+MB10 remaining: Christiano (#20 vs #22), Anthropic (#28 vs #13), Apollo #148 and METR #36 (single artifacts tagged to both).

## Open / next

- MATS / Kairos / CAIS / BlueDot / Apart have clustering rows but no matrix row — still heuristic/unmatched.
- Optional: retag evidence #17/#19/CIRIS/TSA with MB4a, or stop copying MB4 IDs into MB4a cells.
