# Concept / section reference graph

Section-level dependency DAG for the manuscript: which `\label{sec:...}` / `\label{ch:...}`
blocks cite which others, aggregated from `\ref{sec:...}` and `\ref{ch:...}` only (no
per-line prose nodes).

Complements the [symbol census](../symbol-census/) graphs, which trace symbols and
equations. Cross-chapter narrative structure lives here; equation-level `\eqref` chains
stay in `metadata/symbol-census/graphs/`.

## Regenerate

```bash
python3 scripts/build_section_reference_graph.py

# Chapter-level overview (citation-driven chapter ranks):
dot -Tsvg metadata/concept-graph/section-reference-graph-units.dot \
  -o metadata/concept-graph/section-reference-graph-units.svg

# Section drill-down (large — use sfdp, not dot):
sfdp -Goverlap=prism -Gsep="+25" -GK=2 -Gmaxiter=400 -Tsvg \
  metadata/concept-graph/section-reference-graph.dot \
  -o metadata/concept-graph/section-reference-graph.svg
```

## Graph layout

No subgraph clusters (they forced unreadable grouping).

| Node | Meaning |
|------|---------|
| `book:manuscript` | Root (weak anchor only) |
| `unit:ch07`, `unit:appB-bridge-crosswalk`, … | One node per chapter/appendix `.tex` file |
| `sec:…` | Section label (**cross-ref or glossary participants only**) |
| `eq:…` | Labeled equation (when cited via `\\eqref` or defining a cited eq) |

| Edge | Style | Layout role |
|------|-------|-------------|
| book → first unit | solid gray | anchor only, `constraint=false` |
| unit → first `sec:` in file | solid gray | entry into chapter block |
| `sec:` → `sec:` within unit (line order) | invisible, weight 80 | **within-chapter spine** |
| cross-ref (visible) | orange / amber dashed | cite direction, `constraint=false` |
| `\\eqref` (visible) | solid green | section → `eq:` |
| `eq:` line-order within unit | invisible, weight 80 | equation spine |
| back-ref rank (invisible) | weight 1 | **earlier→later** (reversed vs cite arrow) |

**Within-chapter structure:** consecutive sections and labeled equations each follow an
invisible line-order spine. Prose `\\eqref{eq:...}` cites appear as green **section → eq**
edges (~105 in the full book). Intra-chapter `\\ref{sec:…}` edges are sparse (~40); symbol→
formula **`sym → eq`** chains live in the symbol census graph.

**Transitive thinning (default on):** back-reference rank edges are transitively
reduced before layout — e.g. unit ranks drop from ~405 to ~76 because
``ch40→ch07`` is implied by ``ch40→ch26→ch07``. Pass ``--no-thin-transitive`` to
keep every back-ref rank edge (very dense unit graph). Visible cite edges show the
thinned back-ref set plus all forward cites at low weight.

**Chapters are not forced into a reading-order line.** Inter-chapter placement comes from
back-reference rank edges. The dashed unit→unit chain in the **units** graph is a
non-constraining reading-order hint only.

Glossary-defining sections are blue; sections that participate in cross-refs use bold borders.

## Renderers

```bash
# Force-directed (good for browsing the full graph with cycles):
sfdp -Goverlap=prism -Gsep="+25" -GK=2 -Gmaxiter=400 -Tsvg \
  metadata/concept-graph/section-reference-graph.dot \
  -o metadata/concept-graph/section-reference-graph.svg

# Layered (section-level; large):
dot -Tsvg metadata/concept-graph/section-reference-graph.dot \
  -o metadata/concept-graph/section-reference-graph-dot.svg
```

## Outputs

| File | Purpose |
|------|---------|
| `section-reference-graph-units.dot` | **Chapter/appendix overview** (~55 units, citation-driven ranks) |
| `section-reference-graph.dot` | Section-level drill-down (~400 xref/glossary sections) |
| `glossary-section-audit.md` | Glossary definitional-home validation |
| `terminal-backref-audit.md` | Terminal-node classes; back- vs forward-ref counts |

## Semantics

- **Citing node:** active `\label{sec:...}`, or **`unit:chNN`** for prose before the first section in a file.
- **Target node:** `sec:…`, or **`unit:chNN`** / **`unit:appX-…`** when the manuscript uses `\ref{ch:…}`.
- **Definitions:** `\begin{definition}` blocks inherit the active section as their home;
  used when inferring glossary anchors from chapter-only hints.
- **One edge per (source, target) pair** — repeated citations in the same section do not
  multiply edges.

Glossary validation prefers explicit `sec:` entries in each card's `bookLabels`. Chapter-only
anchors are flagged for tightening.
