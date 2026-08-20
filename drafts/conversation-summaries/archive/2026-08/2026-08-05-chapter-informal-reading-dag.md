# 2026-08-05 — Informal chapter reading DAG

## Trigger
Extend chapter dependency graphs: no-symbol chapters (24/48) need informal concept prerequisites; add modes to merge with symbol DAG and report missing chapters.

## Done
- **`chapter-informal-edges.yml`** — 74 curated provider→consumer edges from no-symbol chapters (concept slugs, book-part structure).
- **`build_chapter_symbol_dependency.py`** — three modes: `symbol`, `informal`, `combined`; `--all-modes`; combined graph shows all 48 chapters (blue = symbol participants, light blue = informal-only).
- **Outputs:** `chapter-informal-dependency.*`, `chapter-reading-dependency.*`; updated symbol MD with missing-chapter report.
- **Eq-chain hook** builds all three modes on extract.
- **Docs:** `metadata/concept-graph/README.md`.

## Decisions
- Informal edges are **curated YAML**, not auto-mined from prose cites (complements `\ref{ch:…}` DAG and eq-chain).
- Combined graph transitively thins symbol + informal layers together.
- **48/48 chapters** in combined graph after curation; `ch48` terminal (incoming only).

## Open / next
- Refine informal edges as editorial pass continues (YAML is living source).
- Optional: companion-site reading paths from `chapter-reading-dependency.md` layers.
- C12 basin operationalization still open (symbol island).

## Key paths
- `metadata/concept-graph/chapter-informal-edges.yml`
- `metadata/concept-graph/chapter-reading-dependency.md`
- `scripts/build_chapter_symbol_dependency.py`

## Commits
- `8738d3a0` Add informal concept layer to chapter reading dependency graphs.
