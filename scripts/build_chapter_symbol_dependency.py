#!/usr/bin/env python3
"""Chapter-level prerequisite DAG from equation-chain symbols and informal concepts.

Modes:
  symbol   — bridge symbols only (eq-chain); ``chapter-symbol-dependency.*``
  informal — curated concept prerequisites; ``chapter-informal-dependency.*``
  combined — both layers, transitively thinned; ``chapter-reading-dependency.*``

Informal edges live in ``metadata/concept-graph/chapter-informal-edges.yml``.

Also invoked at the end of ``extract_symbol_formula_graph.py``.

Usage:
  python3 scripts/build_chapter_symbol_dependency.py
  python3 scripts/build_chapter_symbol_dependency.py --mode combined
  python3 scripts/build_chapter_symbol_dependency.py --mode informal --rankdir LR
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
INFORMAL_YML = OUT_DIR / "chapter-informal-edges.yml"

sys.path.insert(0, str(ROOT / "scripts"))
from extract_symbol_formula_graph import (  # noqa: E402
    _compute_eq_chain_core,
    _formula_defines_sym,
    _formula_order_key,
    dot_label,
    parse_chapter,
    parse_symboldefs,
    parse_symbolrefs,
)

CH_NUM = re.compile(r"^ch(\d+)$")
MODES = ("symbol", "informal", "combined")


@dataclass
class ReadingDepEdge:
    provider: str
    consumer: str
    kind: str  # "symbol" | "informal"
    tags: set[str] = field(default_factory=set)
    use_sites: int = 0


def load_chapter_titles() -> dict[str, str]:
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


def chapters_in_book_order(titles: dict[str, str]) -> list[str]:
    return sorted(titles.keys(), key=ch_sort_key)


def transitive_reduction(edges: set[tuple[str, str]]) -> set[tuple[str, str]]:
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
    edges: dict[tuple[str, str], ReadingDepEdge],
) -> dict[tuple[str, str], ReadingDepEdge]:
    kept = transitive_reduction(set(edges.keys()))
    return {k: edges[k] for k in kept}


def merge_edge_dicts(
    *layers: dict[tuple[str, str], ReadingDepEdge],
) -> dict[tuple[str, str], ReadingDepEdge]:
    """Merge edge maps; on duplicate (prov, cons) keys union tags and kinds."""
    merged: dict[tuple[str, str], ReadingDepEdge] = {}
    for layer in layers:
        for key, edge in layer.items():
            if key not in merged:
                merged[key] = ReadingDepEdge(
                    provider=edge.provider,
                    consumer=edge.consumer,
                    kind=edge.kind,
                    tags=set(edge.tags),
                    use_sites=edge.use_sites,
                )
                continue
            cur = merged[key]
            if cur.kind != edge.kind:
                cur.kind = "mixed"
            cur.tags.update(edge.tags)
            cur.use_sites += edge.use_sites
    return merged


def compute_symbol_dependencies(core) -> dict[tuple[str, str], ReadingDepEdge]:
    edges: dict[tuple[str, str], ReadingDepEdge] = {}
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
                edges[key] = ReadingDepEdge(
                    provider=def_ch, consumer=use_ch, kind="symbol"
                )
            edges[key].tags.add(sym)
            edges[key].use_sites += 1
    return edges


def load_informal_edges(
    path: Path = INFORMAL_YML,
) -> dict[tuple[str, str], ReadingDepEdge]:
    if not path.exists():
        return {}
    try:
        import yaml
    except ImportError as exc:
        raise SystemExit("PyYAML required: pip install pyyaml") from exc

    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    edges: dict[tuple[str, str], ReadingDepEdge] = {}
    for item in raw.get("edges") or []:
        prov = item.get("provider")
        cons = item.get("consumer")
        if not prov or not cons:
            continue
        concepts = item.get("concepts") or []
        key = (prov, cons)
        if key not in edges:
            edges[key] = ReadingDepEdge(provider=prov, consumer=cons, kind="informal")
        edges[key].tags.update(str(c) for c in concepts)
    return edges


def symbol_chapters(edges: dict[tuple[str, str], ReadingDepEdge]) -> set[str]:
    return {ch for pair in edges for ch in pair}


def chapters_without_symbol_edges(titles: dict[str, str]) -> set[str]:
    paths = sorted((ROOT / "chapters").glob("ch*.tex"))
    all_formulas: list = []
    for p in paths:
        all_formulas.extend(parse_chapter(p))
    core = _compute_eq_chain_core(
        all_formulas, parse_symboldefs(paths), parse_symbolrefs(paths)
    )
    sym_edges = compute_symbol_dependencies(core)
    in_sym = symbol_chapters(sym_edges)
    return {ch for ch in titles if ch not in in_sym}


def topological_layers(
    chapters: set[str], edges: dict[tuple[str, str], ReadingDepEdge]
) -> tuple[list[list[str]], list[tuple[str, str]]]:
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
            layers.append(sorted(remaining, key=ch_sort_key))
            break
        layers.append(ready)
        for ch in ready:
            remaining.discard(ch)
            for nxt in adj.get(ch, ()):
                in_deg[nxt] -= 1

    cycles: list[tuple[str, str]] = []
    for (a, b) in edges:
        if (b, a) in edges:
            pair = (a, b) if ch_sort_key(a) < ch_sort_key(b) else (b, a)
            if pair not in cycles:
                cycles.append(pair)
    return layers, cycles


def chapters_missing_from_graph(
    titles: dict[str, str],
    edges: dict[tuple[str, str], ReadingDepEdge],
) -> list[str]:
    """Chapters with no incident edge in the graph."""
    touched: set[str] = set()
    for prov, cons in edges:
        touched.add(prov)
        touched.add(cons)
    return sorted(
        [ch for ch in titles if ch not in touched],
        key=ch_sort_key,
    )


def build_dependency_dot(
    edges: dict[tuple[str, str], ReadingDepEdge],
    titles: dict[str, str],
    *,
    rankdir: str = "TB",
    mode: str = "symbol",
    show_all_chapters: bool = False,
) -> str:
    if show_all_chapters:
        chapters = set(titles.keys())
    else:
        chapters = {ch for pair in edges for ch in pair}

    orient = "vertical" if rankdir.upper() == "TB" else "horizontal"
    ranksep = "1.0" if rankdir.upper() == "TB" else "1.4"
    labels = {
        "symbol": "symbol def/use chains",
        "informal": "informal concept prerequisites",
        "combined": "symbols + informal concepts",
    }

    lines = [
        "digraph ChapterReadingDependency {",
        f'  graph [rankdir={rankdir.upper()}, fontsize=10, overlap=prism, '
        f'sep="+20", ranksep={ranksep}, nodesep=0.5,',
        f'    label="Chapter prerequisites ({labels.get(mode, mode)}, {orient})", labelloc=t];',
        '  node [shape=box, style=filled, fontname=Helvetica, fontsize=9];',
        '  edge [fontname=Helvetica, fontsize=8];',
        "",
    ]

    no_sym = chapters_without_symbol_edges(titles) if mode == "combined" else set()

    for ch in sorted(chapters, key=ch_sort_key):
        title = titles.get(ch, ch)
        slug = title[:36] + "…" if len(title) > 36 else title
        num = ch[2:] if ch.startswith("ch") else ch
        if mode == "combined" and ch in no_sym:
            color = "#bfdbfe"
            border = "#1d4ed8"
        else:
            color = "#fed7aa"
            border = "#92400e"
        lines.append(
            f'  "unit:{ch}" [label="{dot_label(f"Ch {num}\n{slug}")}", '
            f'fillcolor="{color}", color="{border}"];'
        )

    lines.append("")
    sym_style = 'color="#2563eb"'
    inf_style = 'color="#16a34a", style=dashed'
    mix_style = 'color="#7c3aed", style="dashed,bold"'

    for (prov, cons), edge in sorted(
        edges.items(), key=lambda x: (ch_sort_key(x[0][0]), ch_sort_key(x[0][1]))
    ):
        preview = ", ".join(sorted(edge.tags)[:4])
        if len(edge.tags) > 4:
            preview += f", +{len(edge.tags) - 4}"
        if edge.kind == "symbol":
            label = f"{len(edge.tags)} sym"
            estyle = sym_style
        elif edge.kind == "informal":
            label = f"{len(edge.tags)} concept"
            estyle = inf_style
        else:
            label = f"mixed ({len(edge.tags)})"
            estyle = mix_style
        if preview:
            label += f"\n{preview}"
        lines.append(
            f'  "unit:{prov}" -> "unit:{cons}" [label="{dot_label(label)}", {estyle}];'
        )

    sym_n = sum(1 for e in edges.values() if e.kind == "symbol")
    inf_n = sum(1 for e in edges.values() if e.kind == "informal")
    mix_n = sum(1 for e in edges.values() if e.kind == "mixed")
    lines.append("")
    lines.append(
        f"  // ({len(chapters)} chapters, {len(edges)} edges: "
        f"{sym_n} symbol, {inf_n} informal, {mix_n} mixed)"
    )
    lines.append("}")
    return "\n".join(lines)


def build_dependency_md(
    edges: dict[tuple[str, str], ReadingDepEdge],
    titles: dict[str, str],
    *,
    mode: str,
    no_symbol: set[str] | None = None,
) -> str:
    chapters = {ch for pair in edges for ch in pair}
    layers, cycles = topological_layers(chapters, edges)
    missing = chapters_missing_from_graph(titles, edges)
    no_symbol = no_symbol or chapters_without_symbol_edges(titles)

    titles_map = {
        "symbol": "Chapter symbol-prerequisite DAG",
        "informal": "Chapter informal-concept prerequisite DAG",
        "combined": "Chapter reading-prerequisite DAG (symbols + informal)",
    }
    sources = {
        "symbol": "equation-chain bridge symbols",
        "informal": "`chapter-informal-edges.yml`",
        "combined": "equation-chain bridge symbols + `chapter-informal-edges.yml`",
    }

    lines = [
        f"# {titles_map.get(mode, 'Chapter dependency DAG')}",
        "",
        f"Generated by `scripts/build_chapter_symbol_dependency.py --mode {mode}` from {sources.get(mode, mode)}.",
        "",
        "## Semantics",
        "",
    ]

    if mode in ("symbol", "combined"):
        lines.extend(
            [
                "- **Symbol edge** `A → B`: chapter **B** uses a bridge symbol whose home is **A**.",
                "- Forward symbol refs (use before def in PDF order) are excluded.",
            ]
        )
    if mode in ("informal", "combined"):
        lines.extend(
            [
                "- **Informal edge** `A → B`: chapter **A** introduces concepts **B** assumes in prose or display math",
                "  (curated in `chapter-informal-edges.yml`; no cross-chapter bridge symbol required).",
            ]
        )
    if mode == "combined":
        lines.append(
            "- Blue nodes: chapters with symbol-bridge edges; light-blue nodes: informal-only participants."
        )
    lines.extend(
        [
            "- **Transitive edges removed** on the merged relation before layout.",
            "",
            f"**Summary:** {len(chapters)} chapters in graph, {len(edges)} directed edges, "
            f"{len(cycles)} mutual pairs, {len(missing)} chapters with no edges.",
            "",
        ]
    )

    if no_symbol and mode == "combined":
        nos = sorted(no_symbol, key=ch_sort_key)
        lines.extend(
            [
                "## No-symbol chapters (informal layer)",
                "",
                "These chapters do not participate in cross-chapter bridge symbols; informal edges carry their prerequisites:",
                "",
            ]
        )
        for ch in nos:
            outs = sorted(
                [cons for (prov, cons) in edges if prov == ch],
                key=ch_sort_key,
            )
            lines.append(
                f"- **{ch}** ({titles.get(ch, '?')}) → {', '.join(outs) if outs else '—'}"
            )
        lines.append("")

    if missing:
        lines.extend(
            [
                "## Chapters still missing from graph",
                "",
                "No incoming or outgoing edge — add informal edges or symbol bridges:",
                "",
            ]
        )
        for ch in missing:
            lines.append(f"- **{ch}** ({titles.get(ch, '?')})")
        lines.append("")
    else:
        lines.extend(
            [
                "## Chapters still missing from graph",
                "",
                "- None — all manuscript chapters appear in at least one edge.",
                "",
            ]
        )

    lines.extend(
        [
            "## Topological layers",
            "",
            "Each layer can be read in any order internally; read layer *n* before layer *n+1*.",
            "",
        ]
    )
    for i, layer in enumerate(layers, 1):
        parts = [f"**{ch}** ({titles.get(ch, '?')})" for ch in layer]
        lines.append(f"{i}. " + "; ".join(parts))

    lines.extend(["", "## Edges (provider → consumer)", ""])
    if mode == "combined":
        lines.append("| Provider | Consumer | Kind | Tags |")
        lines.append("|----------|----------|------|------|")
        for (prov, cons), edge in sorted(
            edges.items(), key=lambda x: (ch_sort_key(x[0][0]), ch_sort_key(x[0][1]))
        ):
            tags = ", ".join(sorted(edge.tags))
            lines.append(f"| {prov} | {cons} | {edge.kind} | {tags} |")
    elif mode == "informal":
        lines.append("| Provider | Consumer | Concepts |")
        lines.append("|----------|----------|----------|")
        for (prov, cons), edge in sorted(
            edges.items(), key=lambda x: (ch_sort_key(x[0][0]), ch_sort_key(x[0][1]))
        ):
            tags = ", ".join(sorted(edge.tags))
            lines.append(f"| {prov} | {cons} | {tags} |")
    else:
        lines.append("| Provider | Consumer | Symbols | Use sites |")
        lines.append("|----------|----------|---------|-----------|")
        for (prov, cons), edge in sorted(
            edges.items(), key=lambda x: (ch_sort_key(x[0][0]), ch_sort_key(x[0][1]))
        ):
            tags = ", ".join(sorted(edge.tags))
            lines.append(f"| {prov} | {cons} | {tags} | {edge.use_sites} |")

    lines.extend(
        [
            "",
            "## Coherent reading paths",
            "",
            "1. **Book order (ch01→ch48):** default narrative.",
            "2. **Layers (above):** minimize undefined symbols and informal concept jumps.",
            "3. **Prose cite DAG:** `section-reference-graph-units.dot`.",
            "",
            f"Regenerate: `python3 scripts/build_chapter_symbol_dependency.py --mode {mode}`",
            "",
        ]
    )
    return "\n".join(lines)


def build_edges_for_mode(mode: str) -> dict[tuple[str, str], ReadingDepEdge]:
    paths = sorted((ROOT / "chapters").glob("ch*.tex"))
    all_formulas: list = []
    for p in paths:
        all_formulas.extend(parse_chapter(p))
    core = _compute_eq_chain_core(
        all_formulas, parse_symboldefs(paths), parse_symbolrefs(paths)
    )
    sym = compute_symbol_dependencies(core)
    inf = load_informal_edges()

    if mode == "symbol":
        raw = sym
    elif mode == "informal":
        raw = inf
    else:
        raw = merge_edge_dicts(sym, inf)
    return remove_transitive_edges(raw)


def output_stems(mode: str) -> tuple[str, str]:
    if mode == "symbol":
        return "chapter-symbol-dependency", "chapter-symbol-dependency"
    if mode == "informal":
        return "chapter-informal-dependency", "chapter-informal-dependency"
    return "chapter-reading-dependency", "chapter-reading-dependency"


def build_from_manuscript(
    *,
    rankdir: str = "TB",
    mode: str = "symbol",
) -> tuple[Path, Path]:
    titles = load_chapter_titles()
    edges = build_edges_for_mode(mode)
    dot_stem, md_stem = output_stems(mode)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    dot_path = OUT_DIR / f"{dot_stem}.dot"
    md_path = OUT_DIR / f"{md_stem}.md"
    dot_path.write_text(
        build_dependency_dot(
            edges,
            titles,
            rankdir=rankdir,
            mode=mode,
            show_all_chapters=(mode == "combined"),
        ),
        encoding="utf-8",
    )
    md_path.write_text(
        build_dependency_md(edges, titles, mode=mode),
        encoding="utf-8",
    )
    return dot_path, md_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=MODES,
        default="symbol",
        help="symbol (eq-chain only), informal (YAML concepts), combined (both)",
    )
    parser.add_argument(
        "--rankdir",
        choices=("TB", "LR"),
        default="TB",
        help="Graph layout direction (default TB = scroll-friendly)",
    )
    parser.add_argument(
        "--all-modes",
        action="store_true",
        help="Write symbol, informal, and combined outputs",
    )
    args = parser.parse_args()

    modes = MODES if args.all_modes else (args.mode,)
    last: tuple[Path, Path] | None = None
    for mode in modes:
        last = build_from_manuscript(rankdir=args.rankdir, mode=mode)
        print(f"Wrote {last[0]}")
        print(f"Wrote {last[1]}")

    if args.all_modes and last:
        titles = load_chapter_titles()
        combined = build_edges_for_mode("combined")
        missing = chapters_missing_from_graph(titles, combined)
        print(
            f"Combined: {len({c for p in combined for c in p})} chapters, "
            f"{len(combined)} edges, {len(missing)} missing"
        )
        if missing:
            print("Missing:", ", ".join(missing))


if __name__ == "__main__":
    main()
