# Symbol–formula graph (Graphviz)

Machine-generated coverage of manuscript symbols and the formulas they appear in, plus the Lean proof-spine dependency graph and the combined manuscript↔Lean crosswalk. Part of the [symbol census](../README.md) — see that file for how this fits with the contribution audit and coverage tables.

## Regenerate

Run from the repo root:

```bash
python3 scripts/extract_symbol_formula_graph.py
# single chapter:
python3 scripts/extract_symbol_formula_graph.py --chapter ch14 --out metadata/symbol-census/graphs/symbol-formula-graph-ch14.dot
```

## Outputs

| File | Description |
|------|-------------|
| `symbol-formula-graph.dot` | Full book graph (1004 formula/prose nodes, 741 symbols, incl. 536 chapter/section text-ref edges) — manuscript only |
| `symbol-formula-graph-ch14.dot` | ch14-only subgraph |
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

## Text-only cross-references are now edges too

The first two passes only turned `\eqref{eq:...}` / `\ref{eq:...}` into edges. But the
manuscript's dominant citation style is chapter/section-level prose — "Chapter~\ref{ch:foo}",
"Section~\ref{sec:bar-ch15}" — which outnumbers per-equation refs by roughly 8:1 (536 `ch:`/`sec:`
refs vs ~70 `eq:` refs). A human reading "this reuses the boundary-information competence
functional from Chapter 11" can see the dependency; the old parser couldn't, because no
`\eqref` existed to record it. The extractor now also parses `\label{ch:...}` / `\label{sec:...}`
(to know which chapter owns each label) and `\ref{ch:...}` / `\ref{sec:...}` anywhere in the
text, and resolves each to the chapter it targets (`resolve_text_ref()` in the script). This
adds a `chref:chNN` node per referenced chapter and a dashed amber `text-ref` edge from the
citing formula/prose line to it (edge label carries the specific `sec:...` id when the ref was
section-level, so you can still tell *which* section was meant, not just which chapter).
524 of 536 occurrences resolve; the 9 unresolved ones point at appendix labels
(`sec:appm-*`) that live outside `chapters/*.tex` and so aren't in the parsed label set — see
the "Text cross-references" section of `../symbol-formula-coverage.md` for the full list.

## Graph semantics

**Node types**

| Shape | ID pattern | Meaning |
|-------|------------|---------|
| Ellipse | `sym:C_{raw}` | Extracted symbol |
| Box (green) | `eq:alignment-margin` | Labeled display equation |
| Box (purple) | `ch14:unlabeled:177` | Unlabeled `equation`/`align` block + line |
| Note (gray) | `ch14:prose:394` | Prose line containing `\eqref`/`\ref` (equation-level) or `\ref{ch:...}`/`\ref{sec:...}` (chapter/section-level) |
| Octagon (dashed, red) | `ghost:eq:cci-ch26` | Referenced equation defined elsewhere |
| CDS/tab (amber) | `chref:ch11` | Target of a chapter/section text-ref (see below) |
| Octagon (dashed, red) | `textref:sec:appm-constraint-inheritance` | Text-ref target that doesn't resolve to any parsed `\label` |

**Edge types**

| Color | Label | Direction | Meaning |
|-------|-------|-----------|---------|
| Blue | `in` | symbol → formula | Symbol appears in that formula block |
| Green | `ref` | formula → formula | `\eqref` / `\ref{eq:...}` dependency |
| Amber (dashed) | `text-ref` or `sec:...` | formula/prose → `chref:chNN` | `\ref{ch:...}` / `\ref{sec:...}` cross-reference — chapter/section-granularity prose citation, not a per-equation dependency |

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
(anchor → Lean node), green `uses` edge (Lean declaration → Lean declaration it references in
its body/proof term). Full chain example (verified in the generated graph): `ch25:prose:321` → `leanspine:ch25:322` (`proof`, node `P13`) → `lean:P13_risk_gap_bounded_by_cci_slack` → `lean:RiskGap` / `lean:CCI` / `lean:Control` — now traceable end to end instead of stopping at the equation label.

## Render

All four graphs are pre-rendered as `.svg` in this folder (open directly in a browser — they
are large, so use the browser's zoom/pan or Graphviz's SVG pan-zoom rather than expecting a
single screen-sized view). To regenerate after editing chapters or `formal/`:

```bash
# ch14 subgraph only (small, ~350 lines): dot's layered ranking works fine
dot -Tsvg symbol-formula-graph-ch14.dot -o symbol-formula-graph-ch14.svg
```

**The other three graphs are too large/cyclic for `dot`'s layered ranking algorithm**
(the full manuscript graph alone is >1400 nodes; the Lean and combined graphs add 1016 Lean
declarations and 2751 `uses` edges — `dot` hangs printing `trouble in init_rank` diagnostics
on all three). Use `sfdp` instead (force-directed, no ranking pass, renders in a few seconds):

```bash
sfdp -Tsvg symbol-formula-graph.dot -o symbol-formula-graph.svg
sfdp -Tsvg lean-dependency-graph.dot -o lean-dependency-graph.svg
sfdp -Tsvg manuscript-lean-crosswalk-graph.dot -o manuscript-lean-crosswalk-graph.svg
```

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
