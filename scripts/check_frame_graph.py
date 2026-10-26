#!/usr/bin/env python3
"""Check the alignment-frame relation DOT graphs against the Lean registries.

Compares drafts/alignment-frames-relations{,-b,-c}.dot with
formal/AlignmentProofSpine/FrameRelations.lean (compose slots, red-edge
registry), FrameMorphisms.lean (specialize / project / encode registry),
FrameLimits.lean (limit / strengthens registry), and FrameHistoryState.lean
(red edges on nodes outside graph c).

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
ORANGE = "#E8590C"
# Incompatibility class (Lean `IncompatClass`) by colour and line style.
RED_STYLE_CLASS = {"dotted": "representability", "dashed": "choiceConflict", "": "rigidity"}
EDGE_RE = re.compile(r"^\s*(\w+)\s*->\s*(\w+)\s*\[(.*)\];?\s*$")
KIND_BY_VERB = {"specializes": "specialize", "projects": "project", "encodes": "encode",
                "limit": "limit", "strengthens": "strengthen"}
MORPHISM_KINDS = {"specialize", "project", "encode"}
LIMIT_KINDS = {"limit", "strengthen"}
# Layout-only DOT nodes (not FrameNode); rigidity edges may route through them.
LAYOUT_NODES = frozenset({"state_corr_gap"})


def dot_edges(path: Path) -> list[tuple[str, str, str]]:
    """(src, tgt, kind) for visible edges; kind is green, an incompatibility
    class (red/orange edges), or a KIND_BY_VERB value."""
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = EDGE_RE.match(line)
        if not m or "invis" in m.group(3):
            continue
        src, tgt, attrs = m.groups()
        label = re.search(r'label="([^"\\]*)', attrs)
        verb = label.group(1).split()[0] if label and label.group(1).split() else ""
        style = re.search(r"style=(\w+)", attrs)
        if RED in attrs:
            kind = RED_STYLE_CLASS.get(style.group(1) if style else "", "unknown")
        elif ORANGE in attrs:
            kind = "sharedResource"
        elif GREEN in attrs:
            kind = "green"
        else:
            kind = KIND_BY_VERB.get(verb, "other")
        out.append((src, tgt, kind))
    return out


def incompat_endpoint_pairs(
    edges: list[tuple[str, str, str]], incompat_classes: set[str]
) -> set[frozenset[str]]:
    """Red/orange endpoint pairs, collapsing layout stubs (e.g. state–gap–correction)."""
    reds = [(s, t) for s, t, k in edges if k in incompat_classes]
    red_set = {frozenset(p) for p in reds}
    if frozenset(("state", "state_corr_gap")) in red_set and frozenset(
        ("state_corr_gap", "correction")
    ) in red_set:
        collapsed = {frozenset((s, t)) for s, t in reds if s not in LAYOUT_NODES and t not in LAYOUT_NODES}
        collapsed.add(frozenset(("state", "correction")))
        return collapsed
    return red_set


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


def lean_incompat_classes(inc: str, hst: str) -> dict[frozenset[str], str]:
    """Red-edge endpoints → `IncompatClass`, via each entry's kind and `IncompatKind.cls`."""
    cls_block = inc.split("def IncompatKind.cls", 1)[1].split("\n\n", 1)[0]
    cls = dict(re.findall(r"\|\s*\.(\w+)\s*=>\s*\.(\w+)", cls_block))
    reg = inc.split("def provedIncompat", 1)[1].split("theorem", 1)[0]
    entries = re.findall(r"⟨\.(\w+), \.(\w+), \.(\w+),", reg)
    ext = hst.split("def incompatExt", 1)[1]
    entries += re.findall(r"src := \.(\w+), tgt := \.(\w+), kind := \.(\w+)", ext)
    return {frozenset((a, b)): cls[k] for a, b, k in entries}


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
    hst = (LEAN / "FrameHistoryState.lean").read_text(encoding="utf-8")
    incompat_ext = {frozenset(p) for p in re.findall(
        r"src := \.(\w+), tgt := \.(\w+)", hst.split("def incompatExt", 1)[1])}
    inc = (LEAN / "FrameIncompatibility.lean").read_text(encoding="utf-8")
    classes = lean_incompat_classes(inc, hst)
    incompat_classes = set(classes.values())
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
    for v, es in edges.items():
        for s_, t_, k in es:
            if s_ in LAYOUT_NODES or t_ in LAYOUT_NODES:
                continue
            pair = frozenset((s_, t_))
            if k in incompat_classes | {"unknown"} and classes.get(pair) != k:
                errors.append(f"{v} incompatible: {s_}–{t_} drawn as {k}, Lean class "
                              f"{classes.get(pair)}")
    compare(
        "c incompatible",
        incompat_endpoint_pairs(edges["c"], incompat_classes),
        incompat,
    )
    for v in ("a", "b"):
        reds = incompat_endpoint_pairs(edges[v], incompat_classes)
        for e in sorted(reds - incompat - incompat_ext, key=str):
            errors.append(f"{v} incompatible: red edge without Lean proof: {tuple(sorted(e))}")
        for e in sorted(incompat_ext - reds, key=str):
            errors.append(f"{v} incompatible: in Lean incompatExt, not in DOT: {tuple(sorted(e))}")
    for v, lean in (("a", morph_a), ("b", morph_b)):
        dot = {(s, t, k) for s, t, k in edges[v] if k in MORPHISM_KINDS}
        compare(f"{v} morphisms", dot, lean)
        dot = {(s, t, k) for s, t, k in edges[v] if k in LIMIT_KINDS}
        compare(f"{v} limit/strengthens", dot, limits)

    # Every implemented map names a declaration that exists in the Frame modules.
    dec = (LEAN / "FrameDecision.lean").read_text(encoding="utf-8")
    frame_src = "\n".join(f.read_text(encoding="utf-8") for f in LEAN.glob("Frame*.lean"))
    impls = re.findall(r'\("([^"]+)", "([^"]+)"\)', dec.split("def mapImpls", 1)[1].split("theorem", 1)[0])
    mor_ids = set(re.findall(r'mapId := "([^"]+)"', mor))
    for map_id, decl in impls:
        if map_id not in mor_ids:
            errors.append(f"mapImpls: {map_id} is not a registered mapId")
        if not re.search(rf"^(?:theorem|def|abbrev) {re.escape(decl)}\b", frame_src, re.M):
            errors.append(f"mapImpls: declaration {decl} not found")

    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        print(f"Frame graph check failed: {len(errors)} mismatch(es).", file=sys.stderr)
        return 1
    print(f"Frame graph check passed ({len(compose)} compose, {len(incompat) + len(incompat_ext)} incompatible, "
          f"{len(morph_b)} morphism ({len(impls)} with map functions), {len(limits)} limit/strengthens "
          f"edges match Lean).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
