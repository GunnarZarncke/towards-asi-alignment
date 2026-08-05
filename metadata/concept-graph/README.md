# Concept / section reference graph

Section-level dependency DAG for the manuscript: which `\label{sec:...}` / `\label{ch:...}`
blocks cite which others. Complements the [symbol census](../symbol-census/graphs/README.md)
graphs, which trace **symbols and equation definition chains**.

**Generated `.dot` / `.svg` files here are gitignored** — regenerate locally (see below).

---

## Graph catalog — how each graph works

| Graph | Best for |
|-------|----------|
| [`section-reference-graph-units.dot`](section-reference-graph-units.dot) | **Chapter/appendix overview** (~55 units, citation-driven ranks). |
| [`section-reference-graph.dot`](section-reference-graph.dot) | **Section drill-down** (~400 xref/glossary sections + cited eqs). |

Both are built by `scripts/build_section_reference_graph.py`.

### What question these answer

**Where does the manuscript cite itself at section or chapter granularity?** (Not: which
symbol is defined where — that is `equation-chain-graph.dot` in symbol-census.)

Prose almost always says `\ref{ch:…}` or `\ref{sec:…}`; individual `\eqref{eq:…}` cites are
rare (~70 book-wide). This graph makes the dominant citation style visible.

### Nodes

| ID | Shape | Meaning |
|----|-------|---------|
| `book:manuscript` | — | Weak root anchor only |
| `unit:ch07`, `unit:appB-bridge-crosswalk`, … | box | One node per chapter/appendix `.tex` file |
| `sec:…` | box | Section `\label{sec:…}` (**only** sections that cross-ref or hold glossary anchors) |
| `eq:…` | box | Labeled equation when cited via `\eqref` / `\ref{eq:…}` from prose |

Glossary-defining sections are blue; sections in the xref graph use bold borders.

### Visible edges

| Style | Direction | Meaning |
|-------|-----------|---------|
| Orange / amber dashed | citing → target | `\ref{sec:…}` or `\ref{ch:…}` (one edge per source→target pair) |
| Solid green | `sec:…` → `eq:…` | Prose `\eqref{eq:…}` / `\ref{eq:…}` |
| Solid gray | book → first unit; unit → first sec | Entry anchors (`constraint=false`) |

### Invisible edges (layout only)

| Style | Direction | Role |
|-------|-----------|------|
| Invis, weight 80 | consecutive `sec:` within a unit | **Section line-order spine** |
| Invis, weight 80 | consecutive `eq:` within a unit | **Equation line-order spine** |
| Invis, weight 1 | earlier → later on back-refs only | **Back-reference rank** — places cited material to the *left* of citing material (cite arrow points forward; rank edge reversed) |

**Transitive thinning (default):** back-ref rank edges are transitively reduced before layout
(e.g. unit ranks ~405 → ~76) so redundant rank constraints do not stack. Forward cites stay
low-weight and non-constraining. Pass `--no-thin-transitive` to keep every back-ref rank edge.

**Chapters are not forced into reading-order line** `ch01→ch02→…`. Inter-chapter placement
comes from citation-driven back-ref ranks only.

### Citing / target resolution

- **Citing node:** active `\label{sec:…}`, or `unit:chNN` for prose before the first section in a file.
- **Target:** `sec:…`, or **`unit:chNN`** when the source uses `\ref{ch:…}` (not the old `ch:` label node).
- **Definitions:** `\begin{definition}` blocks inherit the active section as home (glossary validation).
- **One edge per (source, target)** — repeated cites in the same section do not multiply edges.

Unresolved `\ref{sec:appm-*}` (appendix files outside `chapters/*.tex`) are a known parser gap.

### Audit sidecars (not graphs)

| File | Purpose |
|------|---------|
| [`glossary-section-audit.md`](glossary-section-audit.md) | Glossary definitional-home validation vs `metadata/concepts.yml` |
| [`terminal-backref-audit.md`](terminal-backref-audit.md) | Terminal-node classes; back- vs forward-ref counts |

---

## Regenerate

```bash
python3 scripts/build_section_reference_graph.py

# Chapter-level overview:
dot -Tsvg metadata/concept-graph/section-reference-graph-units.dot \
  -o metadata/concept-graph/section-reference-graph-units.svg

# Section drill-down (large — prefer sfdp):
sfdp -Goverlap=prism -Gsep="+25" -GK=2 -Gmaxiter=400 -Tsvg \
  metadata/concept-graph/section-reference-graph.dot \
  -o metadata/concept-graph/section-reference-graph.svg
```

Layered alternative (can be tall): `dot -Tsvg section-reference-graph.dot -o section-reference-graph-dot.svg`.

## Relation to symbol-census graphs

| Concern | Graph |
|---------|--------|
| Section/chapter narrative cites | **here** (`section-reference-graph`) |
| Symbol **definition vs use** chains | `symbol-census/graphs/equation-chain-graph.dot` |
| Symbol appears anywhere in math | `symbol-census/graphs/symbol-formula-graph.dot` |
| Manuscript → Lean | `symbol-census/graphs/manuscript-lean-crosswalk-graph.dot` |
