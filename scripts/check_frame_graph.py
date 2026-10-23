#!/usr/bin/env python3
"""Check the alignment-frame relation DOT graphs against the Lean registries.

Compares drafts/alignment-frames-relations{,-b,-c}.dot with
formal/AlignmentProofSpine/FrameRelations.lean (compose slots, red-edge
registry), FrameMorphisms.lean (specialize / project / encode registry), and
FrameLimits.lean (limit / strengthens registry).

Stop rule: a failure means a graph edge and the Lean registry disagree. Fix
whichever side is wrong (DOT label/colour, or the Lean table plus its proof)
before syncing the lens map to the site. Do not silence the check by adding
an edge to only one side.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRAFTS = ROOT / "drafts"
LEAN = ROOT / "formal" / "AlignmentProofSpine"

GREEN = "#2E7D32"
RED = "#B00020"
EDGE_RE = re.compile(r"^\s*(\w+)\s*->\s*(\w+)\s*\[(.*)\];?\s*$")
KIND_BY_VERB = {"specializes": "specialize", "projects": "project", "encodes": "encode",
                "limit": "limit", "strengthens": "strengthen"}
MORPHISM_KINDS = {"specialize", "project", "encode"}
LIMIT_KINDS = {"limit", "strengthen"}


def dot_edges(path: Path) -> list[tuple[str, str, str]]:
    """(src, tgt, kind) for visible edges; kind is green/red or a KIND_BY_VERB value."""
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = EDGE_RE.match(line)
        if not m or "invis" in m.group(3):
            continue
        src, tgt, attrs = m.groups()
        label = re.search(r'label="([^"\\]*)', attrs)
        verb = label.group(1).split()[0] if label and label.group(1).split() else ""
        if RED in attrs:
            kind = "red"
        elif GREEN in attrs:
            kind = "green"
        else:
            kind = KIND_BY_VERB.get(verb, "other")
        out.append((src, tgt, kind))
    return out


def lean_compose_slots(text: str) -> set[tuple[str, str]]:
    def table(name: str) -> dict[str, str]:
        block = text.split(f"def ComposeSlot.{name} : ComposeSlot → FrameNode", 1)[1]
        block = block.split("\n\n", 1)[0]
        return dict(re.findall(r"\|\s*\.(\w+)\s*=>\s*\.(\w+)", block))

    src, tgt = table("src"), table("tgt")
    return {(src[k], tgt[k]) for k in src}


def lean_incompat(text: str) -> set[frozenset[str]]:
    block = text.split("def incompatWitnesses", 1)[1].split("def incompatibleDeriv", 1)[0]
    return {frozenset(p) for p in re.findall(r"src := \.(\w+), tgt := \.(\w+)", block)}


def lean_morphisms(text: str, name: str) -> set[tuple[str, str, str]]:
    block = text.split(f"def {name}", 1)[1].split("\ndef ", 1)[0]
    return set(re.findall(r"src := \.(\w+), tgt := \.(\w+), kind := \.(\w+)", block))


def main() -> int:
    rel = (LEAN / "FrameRelations.lean").read_text(encoding="utf-8")
    mor = (LEAN / "FrameMorphisms.lean").read_text(encoding="utf-8")
    compose = lean_compose_slots(rel)
    incompat = lean_incompat(rel)
    morph_a = lean_morphisms(mor, "morphismRegistryA")
    morph_b = morph_a | lean_morphisms(mor, "morphismRegistryBExtra")
    lim = (LEAN / "FrameLimits.lean").read_text(encoding="utf-8")
    limits = lean_morphisms(lim, "limitEdges")
    errors: list[str] = []

    def compare(label: str, dot: set, lean: set) -> None:
        for e in sorted(dot - lean, key=str):
            errors.append(f"{label}: in DOT, not in Lean: {e}")
        for e in sorted(lean - dot, key=str):
            errors.append(f"{label}: in Lean, not in DOT: {e}")

    variants = {"a": "alignment-frames-relations.dot", "b": "alignment-frames-relations-b.dot",
                "c": "alignment-frames-relations-c.dot"}
    edges = {v: dot_edges(DRAFTS / f) for v, f in variants.items()}

    compare("c compose", {(s, t) for s, t, k in edges["c"] if k == "green"}, compose)
    compare("c incompatible", {frozenset((s, t)) for s, t, k in edges["c"] if k == "red"}, incompat)
    for v in ("a", "b"):
        reds = {frozenset((s, t)) for s, t, k in edges[v] if k == "red"}
        for e in sorted(reds - incompat, key=str):
            errors.append(f"{v} incompatible: red edge without Lean proof: {tuple(sorted(e))}")
    for v, lean in (("a", morph_a), ("b", morph_b)):
        dot = {(s, t, k) for s, t, k in edges[v] if k in MORPHISM_KINDS}
        compare(f"{v} morphisms", dot, lean)
        dot = {(s, t, k) for s, t, k in edges[v] if k in LIMIT_KINDS}
        compare(f"{v} limit/strengthens", dot, limits)

    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        print(f"Frame graph check failed: {len(errors)} mismatch(es).", file=sys.stderr)
        return 1
    print(f"Frame graph check passed ({len(compose)} compose, {len(incompat)} incompatible, "
          f"{len(morph_b)} morphism, {len(limits)} limit/strengthens edges match Lean).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
