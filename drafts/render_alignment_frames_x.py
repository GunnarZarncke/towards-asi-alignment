#!/usr/bin/env python3
"""Build variant x from the default alignment-frames graph (a), preserving its layout.

Graphviz `dot` recomputes layout when the graph changes. `style=invis` only suppresses
drawing. To keep **a**'s geometry while hiding the correction-inconsistent cluster:

  1. Regenerate x.dot from alignment-frames-relations.dot (invis nodes/edges).
  2. Render alignment-frames-relations.svg from the default dot.
  3. Hide the same nodes/edges in that SVG → alignment-frames-relations-x.svg.

Do not run plain `dot` on x.dot expecting the same layout as the main graph.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

DRAFTS = Path(__file__).resolve().parent
MAIN_DOT = DRAFTS / "alignment-frames-relations.dot"
MAIN_SVG = DRAFTS / "alignment-frames-relations.svg"
X_DOT = DRAFTS / "alignment-frames-relations-x.dot"
X_SVG = DRAFTS / "alignment-frames-relations-x.svg"

# Frames inconsistent with or only tethered to the correction-centered cluster.
OMIT_NODES = frozenset(
    {
        "state",
        "robust",
        "ai_power",
        "weighted_scalar",
        "hist",
        "dist",
        "quant",
        "cev",
    }
)

CLUSTER_ROOT = "correction"

X_HEADER = """// Relations among alignment frames (variant x: correction-centered cluster; omitted nodes/edges invis).
// Same node set and layout as alignment-frames-relations.dot (default graph a).
// SVG: python3 drafts/render_alignment_frames_x.py — do not use plain `dot` on this file for layout.
// Read with drafts/alignment-frames-relations.md.
// Arrow direction is part of the legend. Do not read every arrow as "implies".
"""

X_GRAPH_LABEL = (
    "Alignment frames (variant x): correction-centered cluster\\n"
    "Same layout as default graph · Omitted nodes and edges use invis · "
    "Solid specializes · Dashed projects · Dotted encodes · Bold isomorphic summand · "
    "Orange limit · Purple stronger quantifier · Green composable · Red incompatible"
)


def parse_edges(dot: str) -> list[tuple[str, str]]:
    edges: list[tuple[str, str]] = []
    for line in dot.splitlines():
        m = re.match(r"^\s+(\w+)\s+->\s+(\w+)", line)
        if m:
            edges.append((m.group(1), m.group(2)))
    return edges


def parse_node_ids(dot: str) -> frozenset[str]:
    skip = {"graph", "node", "edge", "subgraph"}
    ids: set[str] = set()
    for line in dot.splitlines():
        m = re.match(r"^\s+(\w+)\s+\[", line)
        if m and m.group(1) not in skip and not m.group(1).startswith("cluster_"):
            ids.add(m.group(1))
    return frozenset(ids)


def hide_nodes_for_cluster(dot: str) -> frozenset[str]:
    """Omitted frames plus visible nodes with no path to CLUSTER_ROOT (omit layout-only invis edges)."""
    omit = set(OMIT_NODES)
    edges = parse_edges(dot)
    layout_only: set[tuple[str, str]] = set()
    for line in dot.splitlines():
        if "style=invis" in line.replace(" ", ""):
            m = re.match(r"^\s+(\w+)\s+->\s+(\w+)", line)
            if m:
                layout_only.add((m.group(1), m.group(2)))

    adj: dict[str, set[str]] = {}
    for a, b in edges:
        if (a, b) in layout_only:
            continue
        if a in omit or b in omit:
            continue
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)

    seen = {CLUSTER_ROOT}
    stack = [CLUSTER_ROOT]
    while stack:
        n = stack.pop()
        for nb in adj.get(n, ()):
            if nb not in seen:
                seen.add(nb)
                stack.append(nb)

    for n in parse_node_ids(dot):
        if n not in omit and n not in seen:
            omit.add(n)
    return frozenset(omit)


def read_main_dot_body() -> str:
    text = MAIN_DOT.read_text()
    m = re.search(r"^digraph \w+ \{\s*", text, re.MULTILINE)
    if not m:
        raise ValueError(f"no digraph in {MAIN_DOT}")
    body = text[m.end() :]
    if not body.rstrip().endswith("}"):
        raise ValueError("unexpected main dot shape")
    return body


def patch_graph_label(body: str) -> str:
    return re.sub(
        r'label="[^"]*"',
        f'label="{X_GRAPH_LABEL}"',
        body,
        count=1,
    )


def invis_node_block(block: str, node_id: str) -> str:
    if 'style="invis"' in block or "style=invis" in block:
        return block
    return re.sub(
        rf"^(\s+{re.escape(node_id)}\s+\[)",
        r'\1style="invis", ',
        block,
        count=1,
        flags=re.MULTILINE,
    )


def invis_edge_block(block: str) -> str:
    keep_dir_none = "dir=none" in block
    if keep_dir_none:
        return re.sub(r"\[[^\]]*\]", "[style=invis, dir=none]", block, count=1)
    return re.sub(r"\[[^\]]*\]", "[style=invis]", block, count=1)


def build_x_dot(hide: frozenset[str]) -> str:
    body = patch_graph_label(read_main_dot_body())
    lines = body.splitlines(keepends=True)
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        nm = re.match(r"^(\s+)(\w+)\s+\[", line)
        if nm and nm.group(2) in hide:
            block = line
            while not block.rstrip().endswith("];") and i + 1 < len(lines):
                i += 1
                block += lines[i]
            out.append(invis_node_block(block, nm.group(2)))
            i += 1
            continue

        em = re.match(r"^\s+(\w+)\s+->\s+(\w+)", line)
        if em and (em.group(1) in hide or em.group(2) in hide):
            block = line
            while not block.rstrip().endswith("];") and i + 1 < len(lines):
                i += 1
                block += lines[i]
            out.append(invis_edge_block(block))
            i += 1
            continue

        out.append(line)
        i += 1

    return X_HEADER + "digraph AlignmentFrameRelationsX {\n" + "".join(out)


def ensure_main_svg() -> str:
    subprocess.run(
        ["dot", "-Tsvg", "-o", str(MAIN_SVG), str(MAIN_DOT)],
        check=True,
    )
    return MAIN_SVG.read_text()


def decode_edge_comment(comment: str) -> tuple[str, str] | None:
    s = comment.replace("&#45;", "-").replace("&gt;", ">").strip()
    m = re.match(r"(\w+)->(\w+)", s)
    if m:
        return m.group(1), m.group(2)
    return None


def hide_in_svg(svg: str, hide: frozenset[str]) -> str:
    def hide_node(m: re.Match[str]) -> str:
        block = m.group(0)
        title = re.search(r"<title>([^<]+)</title>", block)
        if title and title.group(1) in hide:
            return re.sub(
                r'<g id="(node\d+)"',
                r'<g id="\1" style="opacity:0"',
                block,
                count=1,
            )
        return block

    svg = re.sub(
        r'<g id="node\d+" class="node">.*?</g>\n',
        hide_node,
        svg,
        flags=re.DOTALL,
    )

    def hide_edge(m: re.Match[str]) -> str:
        block = m.group(0)
        title = re.search(r"<title>([^<]+)</title>", block)
        if not title:
            return block
        endpoints = decode_edge_comment(title.group(1))
        if endpoints and (endpoints[0] in hide or endpoints[1] in hide):
            return ""
        return block

    return re.sub(
        r'<g id="edge\d+" class="edge">.*?</g>\n',
        hide_edge,
        svg,
        flags=re.DOTALL,
    )


def patch_svg_title(svg: str) -> str:
    return re.sub(
        r"<title>Alignment frames: specialization[^<]*</title>",
        "<title>Alignment frames (variant x): correction-centered cluster</title>",
        svg,
        count=1,
    )


def main() -> int:
    main_text = MAIN_DOT.read_text()
    hide = hide_nodes_for_cluster(main_text)
    extra = sorted(hide - OMIT_NODES)
    if extra:
        print(f"also hiding disconnected from {CLUSTER_ROOT}: {extra}", file=sys.stderr)

    x_dot = build_x_dot(hide)
    X_DOT.write_text(x_dot)

    svg = hide_in_svg(ensure_main_svg(), hide)
    svg = patch_svg_title(svg)
    X_SVG.write_text(svg)
    print(f"wrote {X_DOT}")
    print(f"wrote {X_SVG} (layout from {MAIN_SVG})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
