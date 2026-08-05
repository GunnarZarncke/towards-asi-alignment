# Symbol–formula graph (Graphviz)

Machine-generated coverage of manuscript symbols and the formulas they appear in, plus the Lean proof-spine dependency graph and the combined manuscript↔Lean crosswalk. Part of the [symbol census](../README.md) — see that file for how this fits with the contribution audit and coverage tables.

**Generated `.dot` / `.svg` files in this folder are gitignored** — regenerate locally after editing `chapters/` or `formal/` (see below).

Section/chapter prose citations live separately in [`metadata/concept-graph/`](../../concept-graph/README.md).

---

## Graph catalog — how each graph works

| Graph | Script | Best for |
|-------|--------|----------|
| [`equation-chain-graph.dot`](equation-chain-graph.dot) | `extract_symbol_formula_graph.py` | **Start here.** Symbol definition chains only (`eq→sym→eq`). |
| [`equation-chain-graph-chapters.dot`](equation-chain-graph-chapters.dot) | same | Same chains + one **chapter → anchor eq** link per defining chapter. |
| [`equation-chain-graph-vertical.dot`](equation-chain-graph-vertical.dot) | same | Same as eq-chain, **top-to-bottom** layout (`rankdir=TB`). |
| [`equation-chain-graph-chapters-vertical.dot`](equation-chain-graph-chapters-vertical.dot) | same | Chapters variant, **vertical** layout. |
| [`symbol-formula-graph.dot`](symbol-formula-graph.dot) | same | Full symbol↔formula reachability + sparse `\eqref` + prose `\eqref` hubs. |
| [`lean-dependency-graph.dot`](lean-dependency-graph.dot) | same | Lean declaration `uses` graph only. |
| [`manuscript-lean-crosswalk-graph.dot`](manuscript-lean-crosswalk-graph.dot) | same | Manuscript symbols/formulas wired to `\leanspine{}` → Lean. |
| [`section-reference-graph*.dot`](../../concept-graph/) | `build_section_reference_graph.py` | Section/chapter `\ref` DAG (narrative structure, not symbols). |

### `equation-chain-graph.dot` — definition chains

**Question it answers:** Which labeled equations *define* a symbol (LHS of `=`, or tuple
intro), and where is that symbol *reused* later (RHS only)?

**Included nodes**

- **`eq:…`** — labeled display equations that participate in at least one bridge symbol chain.
- **`symdef:chNN:line`** — explicit `\symboldef[canonical-id]{math}` definition sites (amber note nodes).
- **`symref:chNN:line`** — explicit `\symbolref[canonical-id]{math}` use sites (light-blue note nodes).
- **`sym:…`** — symbols **defined** in ≥1 eq/symdef and **used** in ≥1 later eq/symref (manuscript
  order). Re-statements on the LHS of a later eq do not count as “use.”

**Visible edges**

| Color | Direction | Meaning |
|-------|-----------|---------|
| Purple | `eq \| symdef → sym` | **Definition** — symbol on LHS of `=`, tuple intro, or marked with `\symboldef`. |
| Blue | `sym → eq \| symref` | **Use** — symbol on RHS of a later labeled eq, or marked with `\symbolref`. |

**Invisible edges (layout only — not drawn in SVG)**

| Style | Direction | Meaning |
|-------|-----------|---------|
| `style=invis, weight=60, constraint=true` | `eq → eq` within each chapter | **Line-order spine** — consecutive kept equations in source file order. Pulls same-chapter eqs into a readable left-to-right band even when they are not linked by def/use. |

**Node labels** (three lines): equation slug · `chNN · Lline` · `eq:label`; symbol name ·
`def <slug>` · first-def chapter/line. `Lline` is the `\label{eq:…}` line in the `.tex` file
(jump target in your editor), not a PDF equation number.

**Layout quirks**

- An equation can appear **with no visible edges** (~14 in the full book) but still sit near
  neighbors: it is kept because a bridge symbol references it, while the **use edge is suppressed**
  (symbol used *before* its first definition in source order), and the **invis spine** still
  ranks it among same-chapter equations. Example: `eq:reproduction-guarantee` (used by `sym:R`
  at L541, but `R` is first defined at L671).
- Cross-chapter **use** edges (`sym → eq`) are weaker for layout than the within-chapter invis
  spine — e.g. `sym:L_{t}` (defined ch08) → `eq:control-locus-ch10` (ch10) can look far from
  the symbol while the eq sits next to `eq:goal-divergence` on the ch10 spine.

**Not included:** sections, chapters, `\ref{ch:…}`, `\ref{sec:…}`, Lean, prose `\eqref` hubs.

### `equation-chain-graph-chapters.dot` — chains + chapter anchors

Everything in **`equation-chain-graph.dot`**, plus:

**Extra nodes**

- **`unit:chNN`** — folder node for each chapter that first-defines at least one bridge symbol.

**Extra visible edge**

| Color | Direction | Meaning |
|-------|-----------|---------|
| Amber | `unit:chNN → eq \| symdef` | **One edge per chapter** to the **earliest** first-def site in that chapter (`constraint=true`). |

Chapter label: `chNN` · anchor slug · `Lline · filename.tex`.

**Not included:** inter-chapter links, chapter→symbol fan-out (removed after it cluttered layout).

**Symbol id normalization:** `\symboldef[D_G]` and equation extraction both map to hub id `D_G`
(extractor may emit `D_{G}` before normalization). Same for `Omega_Q` / `Omega_{Q}`, `B_race` /
`\mathbb{B}_{\mathrm{race}}`, etc. Boundary partitions `\mathcal{C}_t` (ch08) extract as
`mathcal_C_{t}`, distinct from correction signal `C_t` (ch25 `\symboldef`).

**Isolated clusters:** A bridge symbol appears disconnected when its def/use chain never shares a
**labeled** `eq:…` with another bridge symbol. Examples: `ICI` (only `eq:ici-ch35`; κ̃ and UAD live
in unlabeled `\[…\]` blocks); `R_i` (uses `C_{act}` / MI, not `K_X`); `B_race`/`B_certified`
(selection basins, not value bundle `B_i`). Fix by labeling a shared equation, adding `\symbolref`
in a labeled eq, or accepting intentional isolation. Optional dashed gray **sym↔sym** co-occurrence
edges (same labeled equation) are available with `--cooccur`; omitted by default.

**Anchor note labels:** `symdef`/`symref` nodes show `ICI (def anchor)` / `ICI (use anchor)`, not
`\symbolref ICI`. When an anchor sits inside a labeled equation, the eq box is shown and the
duplicate note is suppressed.

### Marking definitions with `\symboldef`

Opt-in macro in `metadata/preamble.tex` (like `\leanspine`):

```tex
\symboldef{\mathrm{CCI}}                    % canonical id inferred from math
\symboldef[CCI]{\vec{\mathrm{CCI}}}         % explicit id (matches metadata/notation.md)
\symboldef[mu_E]{\mu_E(A)}
```

Use when a symbol is defined in prose or display math without a clean labeled-eq LHS, or when
the canonical home should be recorded explicitly. Renders as the inner math only (no visible
marker).

### Marking uses with `\symbolref`

Opt-in use-site marker (pair with `\symboldef` or a labeled-eq definition):

```tex
\symbolref[RiskGap]{\mathrm{RiskGap}(A)\leq\delta}
\symbolref[Fit_E]{\mathrm{Fit}_E(A)}
```

Light-blue `symref:chNN:line` note nodes in the eq-chain graph; blue `sym → symref` edges count
as **uses** for bridge-symbol admission (same rules as labeled-eq RHS uses: after first def,
not a re-definition). Prefer `\label{eq:…}` when the display is already a theorem leaf; use
`\symbolref` for unlabeled `\[…\]` or inline math only.

### `symbol-formula-graph.dot` — full manuscript reachability

**Question it answers:** Where does each extracted symbol appear, and what do labeled equations
cite via `\eqref`?

**Nodes:** all labeled `eq:…` plus `sym:…` that appear in them; optional `ghost:eq:…` for
missing targets; `eqcite:chNN` hubs aggregating prose `\eqref{eq:…}` per citing chapter.

**Edges:** thinned blue **symbol → formula** (any appearance, not def/use split); green
**formula → formula** (`\eqref` inside labeled eq blocks); dashed green **eqcite → formula**
(prose `\eqref`). Chapter/section `\ref` edges were **removed** from this graph — see
concept-graph.

**Layout:** `sfdp` force-directed (too large/cyclic for `dot`). No within-chapter invis spine.

### `lean-dependency-graph.dot` — Lean spine only

**Question it answers:** Which Lean declarations reference which others (heuristic body scan)?

**Nodes:** `lean:DeclarationName` from `formal/AlignmentProofSpine/**/*.lean`.

**Edges:** green **`uses`** — whole-name token match in declaration body (coarse, not elaborator-accurate).

**Layout:** `sfdp`. No manuscript nodes.

### `manuscript-lean-crosswalk-graph.dot` — manuscript ↔ Lean

**Question it answers:** Can I trace from a manuscript symbol/formula to a Lean theorem?

**Nodes:** manuscript `sym:`, `eq:`, prose lines, `\leanspine{kind}{node}{gloss}` diamonds,
`lean:` boxes.

**Edges:** symbol→formula (blue), formula refs (green), leanspine→lean (purple, labeled
`proof` / `counterexample` / `bridge`), lean→lean (`uses`). Chapters with **zero**
`\leanspine{}` anchors are genuine dead ends until anchors are added.

**Layout:** `sfdp`. See [coverage limits](#coverage-limits) for anchor gaps.

---

## Regenerate

Run from the repo root:

```bash
python3 scripts/extract_symbol_formula_graph.py
# optional co-occurrence overlay on eq-chain graphs:
python3 scripts/extract_symbol_formula_graph.py --cooccur
# single chapter:
python3 scripts/extract_symbol_formula_graph.py --chapter ch14 --out metadata/symbol-census/graphs/symbol-formula-graph-ch14.dot
```

## Outputs

| File | Description |
|------|-------------|
| `symbol-formula-graph.dot` | **Reachability graph**: 166 labeled `eq:...` nodes + chapter-level `chcite`/`chref` hubs (not every `chNN:unlabeled` / `chNN:prose` line) |
| `symbol-formula-graph-detailed.dot` | Optional (`--detailed`): all 1004 parsed nodes including unlabeled blocks and per-line prose refs — debug only |
| `symbol-formula-graph-ch14.dot` | ch14 reachability subgraph (labeled eq only) |
| `equation-chain-graph.dot` | **Minimal eq→sym→eq chains** (def vs use; no sections/cites) |
| `equation-chain-graph-chapters.dot` | Same + **one unit:chNN → eq** (earliest first-def eq in chapter; no inter-chapter edges) |
| `equation-chain-graph-vertical.dot` | Eq-chain only, **vertical** (`rankdir=TB`) |
| `equation-chain-graph-chapters-vertical.dot` | Chapters variant, **vertical** |
| `../symbol-formula-coverage.md` | Per-chapter tables: symbol → list of formulas, plus Lean spine coverage and text cross-reference sections |
| `symbol-formula-graph-ch14.svg` | Rendered ch14 graph (after `dot`) |
| `lean-dependency-graph.dot` | **Lean-only** declaration graph, parsed from `formal/AlignmentProofSpine/**/*.lean` (1016 declarations, 37 files) |
| `manuscript-lean-crosswalk-graph.dot` | **Combined** graph: symbol → formula → `\leanspine{}` anchor → Lean declaration → deeper Lean dependency chain |

Counts drift slightly release to release as chapters are edited; regenerate rather than trusting the numbers above verbatim.

## Why the first version had short chains and no Lean nodes

The first pass only parsed `chapters/*.tex` for `\eqref`/`\ref{eq:...}`, which is genuinely
sparse (~70 such refs across ~640 formula nodes) because the manuscript almost always
cross-references at chapter/section granularity in prose, not at individual-equation
granularity. It also never looked at `formal/` at all, so no Lean node could appear —
even though the Lean spine's import graph and proof-term dependencies (1016 declarations,
2751 direct `uses` edges, chains many hops deep, e.g.
`certified_class_safety_from_bridge_record → risk_bound_from_cci_slack → risk_le_delta_of_cci_slack → ...`)
are far denser than anything visible from equation labels alone.

The actual manuscript↔Lean crosswalk anchor is the `\leanspine{kind}{node}{gloss}` macro
(68 occurrences across 22 chapters; `kind` ∈ `proof`/`counterexample`/`bridge`), which the
extractor now parses and resolves against the Lean declaration set — including short
proof-spine ids like `P13`/`MB8` that alias to full names like `P13_control_outpaces_correction`/
`MB1_estimator_soundness`, and ids like `MB7a--MB7d` that alias to a *range* of bridges — see
`resolve_lean_alias()` / `expand_leanspine_node()` in the script. 26 chapters currently have
**zero** `\leanspine{}` anchors (ch01, ch02, ch04, ch05, ch06, ch09, ch12, ch13, ch14, ch15,
ch16, ch18, ch19, ch20, ch22, ch23, ch24, ch32, ch34, ch36, ch37, ch38, ch40, ch44, ch45, ch46)
— their formulas are real dead ends in the combined graph until someone adds crosswalk anchors,
not an extraction bug. (This list grew from 17 to 26 once the extractor started emitting prose
nodes for chapters whose only manuscript content is chapter/section text-refs, see below — those
chapters were previously invisible to the coverage report entirely, not just leanspine-free.)
5 anchors (`P34A`, `P34K`, `P35M`, `P38H`, `inferential-ici`) don't resolve to any parsed Lean
declaration — these are manuscript claims naming Lean nodes that either aren't formalized yet
under that name, or use a naming convention the alias resolver doesn't cover; check
`metadata/TODO.md`'s Lean proof-spine gap list.

## Text-only cross-references (concept-graph)

Chapter/section prose citations (`\ref{ch:...}`, `\ref{sec:...}`) and the section-level DAG
(invis spines, back-ref rank thinning, glossary validation) are documented in
[`metadata/concept-graph/README.md`](../../concept-graph/README.md).

**Equation references** in prose (`\eqref{eq:...}`) appear there as green **section → eq**
edges. This folder keeps sparse **`eqcite:chNN → eq`** hubs in `symbol-formula-graph.dot` only.

The `--detailed` flag still emits per-line prose nodes for equation-level debugging only.

## Graph semantics (symbol-formula + Lean graphs)

**Node types**

| Shape | ID pattern | Meaning |
|-------|------------|---------|
| Ellipse | `sym:C_{raw}` | Extracted symbol |
| Box (green) | `eq:alignment-margin` | Labeled display equation |
| Box (purple) | `ch14:unlabeled:177` | Unlabeled `equation`/`align` block — **only in `--detailed` graph** |
| Octagon (dashed, red) | `ghost:eq:cci-ch26` | Referenced equation defined elsewhere |
| Note (gray) | `ch14:prose:394` | Prose line containing `\eqref`/`\ref` — **only in `--detailed` graph** |
| Folder (green) | `eqcite:ch44` | Prose `\eqref{eq:...}` hub for citing chapter (eq refs only) |
| CDS/tab (amber) | `chref:ch11` | *(removed from default graph)* — see `metadata/concept-graph/` |
| Folder (amber) | `chcite:ch44` | *(removed from default graph)* — see `metadata/concept-graph/` |
| Octagon (dashed, red) | `textref:sec:appm-constraint-inheritance` | Text-ref target that doesn't resolve to any parsed `\label` |

**Edge types**

| Color | Label | Direction | Meaning |
|-------|-------|-----------|---------|
| Blue, thinned (`penwidth=0.4`, ~40% opacity), unlabeled | — | symbol → formula | Symbol appears in that formula block. Thinned/unlabeled deliberately: this is by far the highest-count edge type (~3000+) and the least interesting to trace visually — a fixed `"in"` label on every one of them used to render as a fog of identical text. Color still identifies it. |
| Green, unlabeled | — | formula → formula | `\eqref` / `\ref{eq:...}` from labeled eq blocks |
| Green, dashed | — | `eqcite:chNN` → formula | prose `\eqref{eq:...}` (aggregated per citing chapter) |
| Amber (dashed), labeled only when informative | `sec:...` (section id) or unlabeled | *(removed)* — section DAG in `metadata/concept-graph/` |

**If you edit `build_dot`/`build_combined_dot`/`build_lean_dot`:** don't add a fixed/constant
`label=` to a bulk edge type again — with 1000+ nodes, any label that is the same string on
every edge of a type just renders as visual noise (Graphviz places a text box at each edge's
midpoint) and makes the graph *less* readable, not more informative. Vary edge color/style
instead, and reserve `label=` for values that differ edge-to-edge (e.g. the `sec:...` id, or the
`proof`/`counterexample`/`bridge` kind on `leanspine` edges).

**Reachability paths (manuscript-only graph)**

- **Symbol → downstream use:** follow blue `in` edges to formulas, then green `ref` edges to other formulas.
- **Formula → dependencies:** follow green `ref` edges backward (reverse graph) or forward for what cites this eq.
- **Formula → cited chapters:** follow dashed amber `text-ref` edges to `chref:chNN` nodes — this is the majority of cross-chapter structure now that chapter/section-level citations are edges too.
- **Orphan symbols:** symbols with only one formula node and no outgoing `ref`/`text-ref` edges are chapter-local (e.g. ch14 `M_{A}`) *in the manuscript-only graph* — check the combined graph below before concluding a symbol is a dead end.

Example (ch14): `sym:M_{A}` → `eq:alignment-margin` → (no refs) — dead end in the manuscript-only graph (ch14 has no `\leanspine{}` anchors either, so it is also a dead end in the combined graph — a real gap, not an artifact).

Example (ch14, text-ref): `ch14:prose:80` → `chref:ch11` — the line citing "Chapter~\ref{ch:capability-without-task-ontology}" for the reused competence functional now has an explicit edge, instead of being invisible to the graph.

Example (ch14): `ch14:prose:394` → `eq:misalignment-growth-condition` (internal self-ref only).

Example (ch14): `ch14:prose:512` → `ghost:eq:correction-chain-ch25` — forward pointer, target in ch25.

**Reachability paths (combined `manuscript-lean-crosswalk-graph.dot`)**

Node/edge types add: diamond `leanspine:chNN:LLL` (a `\leanspine{}` anchor), box `lean:Name`
(a Lean declaration; octagon+red if a bridge axiom `MBn_...`), purple `leanspine`-kind edge
(anchor → Lean node, labeled `proof`/`counterexample`/`bridge` — kept, since this label varies),
green `uses` edge (Lean declaration → Lean declaration it references in its body/proof term;
unlabeled, same rationale as `ref` above — 2751 edges all saying `"uses"` was noise, not
signal). Full chain example (verified in the generated graph): `ch25:prose:321` → `leanspine:ch25:322` (`proof`, node `P13`) → `lean:P13_risk_gap_bounded_by_cci_slack` → `lean:RiskGap` / `lean:CCI` / `lean:Control` — now traceable end to end instead of stopping at the equation label.

## Render

All four graphs are pre-rendered as `.svg` in this folder (open directly in a browser — they
are large, so use the browser's zoom/pan or Graphviz's SVG pan-zoom rather than expecting a
single screen-sized view). To regenerate after editing chapters or `formal/`:

```bash
# Equation chains only (eq defines sym, sym uses eq — start here for a clean view):
# Node labels: slug, chNN · Lline, eq:label (equations); sym + def eq + line (symbols).
dot -Tsvg metadata/symbol-census/graphs/equation-chain-graph.dot \
  -o metadata/symbol-census/graphs/equation-chain-graph.svg

# With chapter → first-defining equation in that chapter (one edge per chapter):
dot -Tsvg metadata/symbol-census/graphs/equation-chain-graph-chapters.dot \
  -o metadata/symbol-census/graphs/equation-chain-graph-chapters.svg

# Vertical (top-to-bottom) variants:
dot -Tsvg metadata/symbol-census/graphs/equation-chain-graph-vertical.dot \
  -o metadata/symbol-census/graphs/equation-chain-graph-vertical.svg
dot -Tsvg metadata/symbol-census/graphs/equation-chain-graph-chapters-vertical.dot \
  -o metadata/symbol-census/graphs/equation-chain-graph-chapters-vertical.svg

# ch14 subgraph only (small, ~350 lines): dot's layered ranking works fine
dot -Tsvg symbol-formula-graph-ch14.dot -o symbol-formula-graph-ch14.svg
```

**The other three graphs are too large/cyclic for `dot`'s layered ranking algorithm**
(the full manuscript graph alone is >1400 nodes; the Lean and combined graphs add 1016 Lean
declarations and 2751 `uses` edges — `dot` hangs printing `trouble in init_rank` diagnostics
on all three). Use `sfdp` instead (force-directed, no ranking pass, renders in a few seconds).
Plain default-option `sfdp` packs nodes tightly enough to look like an unreadable hairball at
this node count (this is what shipped 2026-07-17 morning and was reported unreadable) — pass
explicit overlap-removal, target-edge-length, and iteration-count options to spread it out:

```bash
sfdp -Goverlap=prism -Gsep="+20" -GK=2   -Gmaxiter=300 -Tsvg symbol-formula-graph.dot            -o symbol-formula-graph.svg
sfdp -Goverlap=prism -Gsep="+20" -GK=2   -Gmaxiter=300 -Tsvg manuscript-lean-crosswalk-graph.dot -o manuscript-lean-crosswalk-graph.svg
sfdp -Goverlap=prism -Gsep="+15" -GK=1.5 -Gmaxiter=300 -Tsvg lean-dependency-graph.dot           -o lean-dependency-graph.svg
```

`-Goverlap=prism` removes node overlaps (default sfdp overlap removal is weaker); `-GK` sets the
ideal edge length (higher = more spread, 2–2.5 works well at this density; the Lean-only graph
needs less since it has no giant symbol cluster); `-Gsep="+24"` adds extra margin around nodes
during overlap removal; `-Gmaxiter=300` gives the force-directed solver enough iterations to
settle at this size. This roughly quadruples the canvas area (e.g. the full manuscript graph
went from a ~2400×1900pt viewBox to ~10000×6000pt) — that is the point, not a bug; open the SVG
in a browser and zoom in rather than expecting to read it at fit-to-window scale. The other half
of the fix was removing redundant fixed edge labels (see "Graph semantics" above) — labels that
repeat the same text on every edge of a type add visual fog without adding information at this
node count, independent of layout algorithm.

These SVGs are reference artifacts for tracing reachability, not print figures — at this node
count they are illegible at print resolution and are not embedded in the manuscript PDF.

## Trace reachability (CLI)

From repo root, symbols reachable from `M_{A}` in ch14:

```bash
python3 - <<'PY'
import re
from pathlib import Path

dot = Path("metadata/symbol-census/graphs/symbol-formula-graph-ch14.dot").read_text()
edges = re.findall(r'"([^"]+)" -> "([^"]+)" \[.*label="(\w+)"', dot)
start = "sym:M_{A}"
seen = {start}
frontier = [start]
while frontier:
    n = frontier.pop()
    for a, b, lbl in edges:
        if a == n and b not in seen:
            seen.add(b)
            frontier.append(b)
            print(f"  {lbl}: {a} -> {b}")
print("Reachable nodes:", len(seen))
PY
```

Full-book reachability from any symbol: use `symbol-formula-graph.dot` and repeat; cross-chapter refs appear as `ghost:` nodes until you merge the full graph.

## Coverage limits

1. **Display math only:** symbols in bare `$...$` inline math are captured only when inside `\begin{equation}` / `align` / etc., or in prose lines with `\eqref`.
2. **Some chapters have zero display blocks** — they may still use heavy inline math not yet extracted. They now at least get `prose` nodes if they contain a `\ref{ch:...}`/`\ref{sec:...}`/`\eqref{eq:...}` (see point 8), so "no display equations" no longer means "invisible to the graph."
3. **Heuristic symbol parser:** `\mathrm{...}` subscripts normalized to `C_{raw}`; some false splits/merges remain. Edit `extract_symbols_from_math()` in `scripts/extract_symbol_formula_graph.py` to tune.
4. **Duplicate eq labels across chapters:** rare; ghost nodes mark missing targets.
5. **Lean `uses` edges are heuristic token matching, not Lean's real elaborated term graph:** `parse_lean_files()` scans each declaration's body text for other declared names as whole-word tokens. This catches direct proof-term calls (verified against `Certification.lean`/`Capability.lean` by hand) but will miss dependencies routed through typeclass instances/tactics that don't mention the name literally, and can't distinguish "uses in the type signature" from "uses in the proof." For an authoritative dependency graph, use Lean's `#print axioms <theorem>` (see `formal/README.md` "Build") — this script is for fast, coarse reachability across the whole spine, not a replacement for that.
6. **26 chapters have zero `\leanspine{}` anchors** (ch01, ch02, ch04, ch05, ch06, ch09, ch12, ch13, ch14, ch15, ch16, ch18, ch19, ch20, ch22, ch23, ch24, ch32, ch34, ch36, ch37, ch38, ch40, ch44, ch45, ch46) — every formula in those chapters is a genuine dead end in the combined graph, not an extraction artifact. Adding anchors there is a manuscript-side fix (see `metadata/TODO.md`), not a script-side one.
7. **5 of 68 `\leanspine{}` anchors don't resolve** (`P34A`, `P34K`, `P35M`, `P38H`, `inferential-ici` in ch07/ch35/ch39) — either not yet formalized under that name, or the short-id alias resolver (`resolve_lean_alias`) doesn't cover their naming pattern. See the "Lean spine coverage" section of `../symbol-formula-coverage.md` for the full per-anchor resolution table.
8. **`text-ref` edges are chapter/section-granularity, not equation-granularity:** a `\ref{sec:foo-ch15}` cross-reference resolves to `chref:ch15` (the whole chapter), not to the specific equation or paragraph the citing prose actually meant — the script has no way to know which formula within ch15 is intended without NLP over the surrounding sentence. Treat `text-ref` edges as "chapter X is textually relevant here," not "this exact formula depends on that exact formula." 9 of 536 occurrences don't resolve at all because they target `\label{sec:appm-*}` in appendix files outside `chapters/*.tex`, which this script doesn't parse.

## Relation to contribution audit

See [`../symbol-contribution-audit.md`](../symbol-contribution-audit.md) for *should we keep* judgments. This graph answers *where is it used* and *what does it reference*.
