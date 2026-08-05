---
title: "Chapter Reading Dependency Graph"
type: "artifact"
status: "framework"
summary: "Combined symbol-bridge and informal-concept prerequisites for all 48 chapters — a scroll-friendly alternative to strict PDF order."
decision: "When display math or concept continuity matters, follow the reading graph layers before jumping ahead in PDF order; role-based guided paths remain the default tour."
bookChapters: []
related: ["boundary-discovery", "value-bundle-transport", "correction-channel-integrity", "successor-stability", "attractor-control"]
external:
  - label: "Interactive graph (guided tour)"
    url: "/paths/chapter-reading-graph/"
  - label: "Repo markdown report"
    url: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/metadata/concept-graph/chapter-reading-dependency.md"
---

The manuscript has three overlapping navigation aids:

1. **PDF order (ch01→ch48)** — narrative arc; tolerates forward pointers.
2. **Symbol layers** — minimize undefined bridge symbols in display math (24 chapters participate).
3. **Informal concept edges** — prose concepts introduced in no-symbol chapters that later chapters assume (curated YAML).

The **combined reading graph** merges (2) and (3), transitively thins redundant edges, and includes all **48 chapters** as nodes. Orange boxes participate in cross-chapter symbol bridges; light-blue boxes rely on informal prerequisites only.

**Use the interactive graph** on the [guided tour](/paths/chapter-reading-graph/) — each chapter box links to its chapter card. Blue solid edges are symbol prerequisites; green dashed edges are informal concept prerequisites.

Source files (regenerate locally):

- `metadata/concept-graph/chapter-informal-edges.yml` — curated informal edges
- `scripts/build_chapter_symbol_dependency.py --mode combined`
- `metadata/concept-graph/chapter-reading-dependency.md` — topo layers and edge table
