#!/usr/bin/env python3
"""Extract bridge positions and edges from mb-bridge-dependencies-v2.dot via graphviz."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEMO_DIR = SCRIPT_DIR.parent
REPO_ROOT = DEMO_DIR.parents[1]
DOT_PATH = REPO_ROOT / "reference" / "field-agendas" / "graphs" / "mb-bridge-dependencies-v2.dot"
OUT_PATH = DEMO_DIR / "data" / "bridge-layout.json"

LIVE = [
    "MB1", "MB2", "MB3", "MB4", "MB4a", "MB5", "MB6",
    "MB7", "MB7d", "MB9", "MB10", "MB11",
]

COLLAPSE = {
    "MB6a": "MB6",
    "MB6b": "MB6",
    "MB7a": "MB7",
    "MB7b": "MB7",
    "MB7c": "MB7",
}

SKIP_NODES = {"MB8"}


def collapse_id(node: str) -> str | None:
    if node in SKIP_NODES:
        return None
    if node in COLLAPSE:
        return COLLAPSE[node]
    if node in LIVE:
        return node
    return None


def run_dot_plain(dot_path: Path) -> str:
    try:
        proc = subprocess.run(
            ["dot", "-Tplain", str(dot_path)],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        sys.exit("graphviz `dot` not found — install graphviz to regenerate bridge-layout.json")
    return proc.stdout


def parse_plain(text: str) -> tuple[float, dict[str, tuple[float, float]], list[tuple[str, str, str, bool]]]:
    graph_h = 18.0
    raw_nodes: dict[str, tuple[float, float]] = {}
    raw_edges: list[tuple[str, str, str, bool]] = []

    for line in text.splitlines():
        if line.startswith("graph "):
            parts = line.split()
            if len(parts) >= 4:
                graph_h = float(parts[3])
            continue
        if line.startswith("node "):
            parts = line.split()
            if len(parts) < 4:
                continue
            name, x, y = parts[1], float(parts[2]), float(parts[3])
            raw_nodes[name] = (x, y)
            continue
        if line.startswith("edge "):
            parts = line.split()
            if len(parts) < 3:
                continue
            a, b = parts[1], parts[2]
            color = "#CC3333"
            dashed = False
            if " dashed " in line or line.rstrip().endswith("dashed"):
                dashed = True
            m = re.search(r"(#[0-9A-Fa-f]{6})\s*$", line)
            if m:
                color = m.group(1)
            raw_edges.append((a, b, color, dashed))

    return graph_h, raw_nodes, raw_edges


def aggregate_positions(
    graph_h: float,
    raw_nodes: dict[str, tuple[float, float]],
) -> dict[str, dict[str, float]]:
    buckets: dict[str, list[tuple[float, float]]] = {k: [] for k in LIVE}
    for name, (x, y) in raw_nodes.items():
        key = collapse_id(name)
        if key:
            buckets[key].append((x, y))

    scale = 22.0
    positions: dict[str, dict[str, float]] = {}
    xs: list[float] = []
    ys: list[float] = []

    for key in LIVE:
        pts = buckets.get(key) or []
        if not pts:
            continue
        gx = sum(p[0] for p in pts) / len(pts)
        gy = sum(p[1] for p in pts) / len(pts)
        cx = gx * scale
        cy = (graph_h - gy) * scale
        positions[key] = {"x": cx, "y": cy}
        xs.append(cx)
        ys.append(cy)

    if xs and ys:
        mx = sum(xs) / len(xs)
        my = sum(ys) / len(ys)
        for key in positions:
            positions[key]["x"] -= mx
            positions[key]["y"] -= my

    return positions


def apply_layout_tweaks(positions: dict[str, dict[str, float]]) -> dict[str, dict[str, float]]:
    """Manual spacing pass after Graphviz — keeps field-overview topology, evens columns."""
    p = {k: dict(v) for k, v in positions.items()}

    mb7_y = -75.0
    mb10_y = 145.0
    col_left = -150.0
    step = (mb10_y - mb7_y) / 3.0  # MB2 → MB3 → MB5 → MB10

    p["MB7"] = {"x": -45.0, "y": mb7_y}
    p["MB2"] = {"x": col_left, "y": mb7_y}
    p["MB3"] = {"x": col_left, "y": mb7_y + step}
    p["MB5"] = {"x": col_left, "y": mb7_y + 2 * step}
    p["MB10"] = {"x": col_left, "y": mb10_y}

    mb3_y = mb7_y + step
    mb5_y = mb7_y + 2 * step
    mb4a_y = (mb3_y + mb5_y) / 2.0  # vertically between MB3 and MB5
    row_mid_y = mb7_y + 2.5 * step  # between MB5 and MB10
    p["MB4"] = {"x": 130.0, "y": row_mid_y}
    p["MB4a"] = {"x": (130.0 + -45.0) / 2.0, "y": mb4a_y}
    p["MB9"] = {"x": -45.0, "y": row_mid_y}
    p["MB6"] = {"x": 130.0, "y": mb7_y}
    p["MB7d"] = {"x": (-45.0 + col_left) / 2.0, "y": (mb3_y + mb5_y) / 2.0}

    p["MB11"] = {"x": -5.0, "y": mb10_y + step}
    p["MB1"] = {"x": -5.0, "y": -155.0}

    return p


def aggregate_edges(raw_edges: list[tuple[str, str, str, bool]]) -> list[dict]:
    seen: set[tuple[str, str]] = set()
    out: list[dict] = []
    for a, b, color, dashed in raw_edges:
        if dashed:
            continue
        ca, cb = collapse_id(a), collapse_id(b)
        if not ca or not cb or ca == cb:
            continue
        key = (ca, cb)
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "from": ca,
            "to": cb,
            "color": color,
            "assembly": color.lower() == "#333333",
        })
    return out


def main() -> None:
    plain = run_dot_plain(DOT_PATH)
    graph_h, raw_nodes, raw_edges = parse_plain(plain)
    payload = {
        "source": str(DOT_PATH.relative_to(REPO_ROOT)),
        "positions": apply_layout_tweaks(aggregate_positions(graph_h, raw_nodes)),
        "edges": aggregate_edges(raw_edges),
    }
    OUT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_PATH} ({len(payload['positions'])} nodes, {len(payload['edges'])} edges)")


if __name__ == "__main__":
    main()
