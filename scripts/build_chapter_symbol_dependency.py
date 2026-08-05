#!/usr/bin/env python3
"""Chapter-level prerequisite DAG from equation-chain bridge symbols.

Aggregates cross-chapter def→use edges from the eq-chain core: if chapter B uses a
bridge symbol first defined in chapter A (after A in manuscript order), then
**read A before B** for formal symbol continuity.

Outputs (under metadata/concept-graph/):
  chapter-symbol-dependency.dot   — provider→consumer, rankdir=TB (scroll-friendly)
  chapter-symbol-dependency.md    — topo layers, sample reading paths, edge table

Also invoked at the end of extract_symbol_formula_graph.py.

Usage:
  python3 scripts/build_chapter_symbol_dependency.py
  python3 scripts/build_chapter_symbol_dependency.py --rankdir LR
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "metadata" / "concept-graph"
BOOK_YML = ROOT / "metadata" / "book.yml"
CHAPTERS_GLOB = "chapters/ch*.tex"

# Import eq-chain machinery from the symbol extractor.
sys.path.insert(0, str(ROOT / "scripts"))
from extract_symbol_formula_graph import (  # noqa: E402
    _compute_eq_chain_core,
    _formula_defines_sym,
    _formula_order_key,
    _formula_uses_sym,
    chapter_id,
    dot_label,
    parse_chapter,
    parse_symboldefs,
    parse_symbolrefs,
)

CH_NUM = re.compile(r"^ch(\d+)$")


@dataclass
class ChapterDepEdge:
    provider: str  # defines symbols
    consumer: str  # uses them later
    symbols: set[str] = field(default_factory=set)
    use_sites: int = 0


def load_chapter_titles() -> dict[str, str]:
    """Parse ``metadata/book.yml`` chapter titles without requiring PyYAML."""
    titles: dict[str, str] = {}
    if not BOOK_YML.exists():
        return titles
    current: str | None = None
    for line in BOOK_YML.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s+(ch\d+):\s*$", line)
        if m:
            current = m.group(1)
            continue
        m = re.match(r'^\s+title:\s*"(.+)"\s*$', line)
        if m and current:
            titles[current] = m.group(1)
            current = None
    return titles


def ch_sort_key(ch: str) -> tuple[int, str]:
    m = CH_NUM.match(ch)
    return (int(m.group(1)), ch) if m else (9999, ch)


def transitive_reduction(edges: set[tuple[str, str]]) -> set[tuple[str, str]]:
    """Drop ``a→c`` when some ``a→…→c`` path exists without the direct edge."""
    edge_set = set(edges)
    out: dict[str, set[str]] = defaultdict(set)
    for a, b in edge_set:
        out[a].add(b)
    reduced: set[tuple[str, str]] = set()
    for a, b in sorted(edge_set):
        out[a].discard(b)
        seen = {a}
        stack = list(out[a])
        reachable = False
        while stack:
            n = stack.pop()
            if n == b:
                reachable = True
                break
            if n in seen:
                continue
            seen.add(n)
            stack.extend(out[n])
        out[a].add(b)
        if not reachable:
            reduced.add((a, b))
    return reduced


def remove_transitive_edges(
    edges: dict[tuple[str, str], ChapterDepEdge],
) -> dict[tuple[str, str], ChapterDepEdge]:
    """Keep only cover edges — drop provider→consumer when a longer path exists."""
    kept = transitive_reduction(set(edges.keys()))
    return {k: edges[k] for k in kept}


def compute_chapter_symbol_dependencies(core) -> dict[tuple[str, str], ChapterDepEdge]:
    """Build aggregated provider→consumer edges from eq-chain bridge symbols."""
    edges: dict[tuple[str, str], ChapterDepEdge] = {}

    for sym in core.chain_syms:
        if sym not in core.first_def_order:
            continue
        def_ch = core.first_def_chapter[sym]
        def_order = core.first_def_order[sym]

        for use_fid in core.sym_use_eqs.get(sym, ()):
            if use_fid not in core.kept_eqs:
                continue
            use_f = core.by_fid[use_fid]
            if _formula_defines_sym(use_f, sym):
                continue
            if _formula_order_key(use_f) <= def_order:
                continue
            use_ch = use_f.chapter
            if use_ch == def_ch:
                continue

            key = (def_ch, use_ch)
            if key not in edges:
                edges[key] = ChapterDepEdge(provider=def_ch, consumer=use_ch)
            edges[key].symbols.add(sym)
            edges[key].use_sites += 1

    return edges


def chapters_in_book_order(titles: dict[str, str]) -> list[str]:
    return sorted(titles.keys(), key=ch_sort_key)


def topological_layers(
    chapters: set[str], edges: dict[tuple[str, str], ChapterDepEdge]
) -> tuple[list[list[str]], list[tuple[str, str]]]:
    """Layer chapters for reading order (providers before consumers). Returns cycles."""
    adj: dict[str, set[str]] = defaultdict(set)
    in_deg: dict[str, int] = {ch: 0 for ch in chapters}
    for (prov, cons), _edge in edges.items():
        if cons not in adj[prov]:
            adj[prov].add(cons)
            in_deg[cons] = in_deg.get(cons, 0) + 1
        if prov not in in_deg:
            in_deg[prov] = in_deg.get(prov, 0)

    layers: list[list[str]] = []
    remaining = set(chapters)
    while remaining:
        ready = sorted(
            [ch for ch in remaining if in_deg.get(ch, 0) == 0],
            key=ch_sort_key,
        )
        if not ready:
            # Cycle — report remaining as one layer
            layers.append(sorted(remaining, key=ch_sort_key))
            break
        layers.append(ready)
        for ch in ready:
            remaining.discard(ch)
            for nxt in adj.get(ch, ()):
                in_deg[nxt] -= 1

    # Detect cycle pairs for markdown
    cycles: list[tuple[str, str]] = []
    for (a, b) in edges:
        if (b, a) in edges:
            pair = (a, b) if ch_sort_key(a) < ch_sort_key(b) else (b, a)
            if pair not in cycles:
                cycles.append(pair)
    return layers, cycles


def build_chapter_symbol_dependency_dot(
    edges: dict[tuple[str, str], ChapterDepEdge],
    titles: dict[str, str],
    *,
    rankdir: str = "TB",
) -> str:
    chapters = {ch for pair in edges for ch in pair}
    orient = "vertical" if rankdir.upper() == "TB" else "horizontal"
    ranksep = "1.0" if rankdir.upper() == "TB" else "1.4"
    nodesep = "0.5"

    lines = [
        "digraph ChapterSymbolDependency {",
        f'  graph [rankdir={rankdir.upper()}, fontsize=10, overlap=prism, '
        f'sep="+20", ranksep={ranksep}, nodesep={nodesep},',
        f'    label="Chapter prerequisites from symbol def/use chains ({orient})", labelloc=t];',
        "  node [shape=box, style=filled, fillcolor=\"#fed7aa\", color=\"#92400e\", "
        'fontname=Helvetica, fontsize=9];',
        '  edge [fontname=Helvetica, fontsize=8, color="#2563eb"];',
        "",
    ]

    for ch in sorted(chapters, key=ch_sort_key):
        title = titles.get(ch, ch)
        slug = title[:36] + "…" if len(title) > 36 else title
        num = ch[2:] if ch.startswith("ch") else ch
        lines.append(
            f'  "unit:{ch}" [label="{dot_label(f"Ch {num}\\n{slug}")}"];'
        )

    lines.append("")
    for (prov, cons), edge in sorted(edges.items(), key=lambda x: (ch_sort_key(x[0][0]), ch_sort_key(x[0][1]))):
        sym_preview = ", ".join(sorted(edge.symbols)[:4])
        if len(edge.symbols) > 4:
            sym_preview += f", +{len(edge.symbols) - 4}"
        label = f"{len(edge.symbols)} sym"
        if sym_preview:
            label += f"\\n{sym_preview}"
        lines.append(
            f'  "unit:{prov}" -> "unit:{cons}" [label="{dot_label(label)}"];'
        )

    lines.append("")
    lines.append(f"  // ({len(chapters)} chapters, {len(edges)} dependency edges)")
    lines.append("}")
    return "\n".join(lines)


def build_chapter_symbol_dependency_md(
    edges: dict[tuple[str, str], ChapterDepEdge],
    titles: dict[str, str],
) -> str:
    chapters = {ch for pair in edges for ch in pair}
    book_order = [ch for ch in chapters_in_book_order(titles) if ch in chapters]
    layers, cycles = topological_layers(chapters, edges)

    lines = [
        "# Chapter symbol-prerequisite DAG",
        "",
        "Generated by `scripts/build_chapter_symbol_dependency.py` from **equation-chain**",
        "bridge symbols (`metadata/symbol-census/graphs/equation-chain-graph*.dot`).",
        "",
        "## Semantics",
        "",
        "- **Node:** manuscript chapter that participates in at least one cross-chapter bridge symbol.",
        "- **Edge** `A → B`: chapter **B** uses (after first definition) a bridge symbol whose canonical",
        "  home is chapter **A** — read **A before B** for formal symbol continuity.",
        "- This is **not** the same as prose `\\ref{ch:…}` cites (see",
        "  `section-reference-graph-units.dot`). Prose cites reflect narrative pointers;",
        "  this graph reflects **defined-then-used** math symbols.",
        "- Forward references (use before def in PDF order) are **excluded** — same rule as the eq-chain graph.",
        "- **Transitive edges removed:** if `A → B` and `B → C` (or longer paths), direct `A → C` is dropped.",
        "",
        f"**Summary:** {len(chapters)} chapters, {len(edges)} directed edges, {len(cycles)} mutual pairs.",
        "",
        "## Topological layers (symbol-min reading order)",
        "",
        "Each layer can be read in any order internally; read layer *n* before layer *n+1*.",
        "",
    ]

    for i, layer in enumerate(layers, 1):
        parts = [f"**{ch}** ({titles.get(ch, '?')})" for ch in layer]
        lines.append(f"{i}. " + "; ".join(parts))

    lines.extend(
        [
            "",
            "## PDF order vs symbol prerequisites",
            "",
            "Chapters that appear **early in the book** but depend (symbolically) on **later** chapters",
            "are forward references in this graph — read the later chapter first if you follow symbols strictly:",
            "",
        ]
    )

    forward_jumps = []
    book_idx = {ch: i for i, ch in enumerate(chapters_in_book_order(titles))}
    for (prov, cons), edge in sorted(edges.items(), key=lambda x: ch_sort_key(x[0][1])):
        if book_idx.get(prov, 0) > book_idx.get(cons, 0):
            syms = ", ".join(sorted(edge.symbols)[:6])
            forward_jumps.append(
                f"- **{cons}** (PDF ch{cons[2:]}) uses symbols from **{prov}** (PDF ch{prov[2:]}) — e.g. {syms}"
            )
    if forward_jumps:
        lines.extend(forward_jumps)
    else:
        lines.append("- None among current bridge edges.")

    if cycles:
        lines.extend(["", "## Mutual dependency pairs (cycles)", ""])
        for a, b in cycles:
            lines.append(
                f"- **{a}** ↔ **{b}** — no strict order; read both before chapters that depend on either."
            )

    lines.extend(["", "## Edges (provider → consumer)", ""])
    lines.append("| Provider | Consumer | Symbols | Use sites |")
    lines.append("|----------|----------|---------|-----------|")
    for (prov, cons), edge in sorted(
        edges.items(), key=lambda x: (ch_sort_key(x[0][0]), ch_sort_key(x[0][1]))
    ):
        syms = ", ".join(sorted(edge.symbols))
        lines.append(f"| {prov} | {cons} | {syms} | {edge.use_sites} |")

    lines.extend(
        [
            "",
            "## Coherent reading paths",
            "",
            "1. **Book order (ch01→ch48):** default manuscript; tolerate forward `\\symbolref` or brief",
            "   `\\ref{ch:…}` pointers.",
            "2. **Symbol layers (above):** minimize undefined bridge symbols when reading display math.",
            "3. **Prose cite DAG:** `section-reference-graph-units.dot` — chapter `\\ref{ch:…}` structure.",
            "",
            "Regenerate: `python3 scripts/build_chapter_symbol_dependency.py`",
            "",
        ]
    )
    return "\n".join(lines)


def build_from_manuscript(*, rankdir: str = "TB") -> tuple[Path, Path]:
    paths = sorted((ROOT / "chapters").glob("ch*.tex"))
    all_formulas: list = []
    for p in paths:
        all_formulas.extend(parse_chapter(p))
    symbol_defs = parse_symboldefs(paths)
    symbol_refs = parse_symbolrefs(paths)
    core = _compute_eq_chain_core(all_formulas, symbol_defs, symbol_refs)
    edges = remove_transitive_edges(compute_chapter_symbol_dependencies(core))
    titles = load_chapter_titles()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    dot_path = OUT_DIR / "chapter-symbol-dependency.dot"
    md_path = OUT_DIR / "chapter-symbol-dependency.md"
    dot_path.write_text(
        build_chapter_symbol_dependency_dot(edges, titles, rankdir=rankdir),
        encoding="utf-8",
    )
    md_path.write_text(build_chapter_symbol_dependency_md(edges, titles), encoding="utf-8")
    return dot_path, md_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--rankdir",
        choices=("TB", "LR"),
        default="TB",
        help="Graph layout direction (default TB = scroll-friendly)",
    )
    args = parser.parse_args()
    dot_path, md_path = build_from_manuscript(rankdir=args.rankdir)
    print(f"Wrote {dot_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
