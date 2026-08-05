#!/usr/bin/env python3
"""Build a section-level manuscript reference DAG and validate glossary definitional homes.

Replaces the noisy per-line prose reference nodes in the symbol-formula graph with
aggregated section→section (and section→chapter) edges derived from \\ref{sec:...}
and \\ref{ch:...}. Also records \\eqref{eq:...} / \\ref{eq:...} as section→equation
edges (green) with an equation line-order spine within each chapter.

Outputs:
  metadata/concept-graph/section-reference-graph.dot
  metadata/concept-graph/glossary-section-audit.md

Usage:
  python3 scripts/build_section_reference_graph.py
  python3 scripts/build_section_reference_graph.py --check
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML required: pip install pyyaml") from exc

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "metadata" / "concept-graph"
CONCEPTS_YML = ROOT / "metadata" / "concepts.yml"
TEX_GLOBS = ("chapters/ch*.tex", "appendices/app*.tex")

LABEL_ANY = re.compile(r"\\label\{([^}]+)\}")
LABEL_SEC = re.compile(r"\\label\{(sec:[^}]+)\}")
LABEL_CH = re.compile(r"\\label\{(ch:[^}]+)\}")
LABEL_EQ = re.compile(r"\\label\{(eq:[^}]+)\}")
TEXTREF = re.compile(r"\\ref\{(ch:[^}]+|sec:[^}]+)\}")
EQREF = re.compile(r"\\(?:eqref|ref)\{(eq:[^}]+)\}")
DEF_START = re.compile(r"\\begin\{definition\}(?:\[([^\]]*)\])?")
CHAPTER_NUM = re.compile(r"^ch(\d+)")
CH_HINT = re.compile(r"\*\*ch(\d+)\*\*")
EQ_HINT = re.compile(r"`?(eq:[\w-]+)`?")
SEC_HINT = re.compile(r"\b(sec:[\w-]+)\b")


@dataclass
class SectionInfo:
    label: str
    chapter: str  # ch07
    chapter_file: str
    line: int
    definitions: list[str] = field(default_factory=list)


@dataclass
class ParsedManuscript:
    ch_owner: dict[str, str]  # ch:label -> ch07
    sec_owner: dict[str, str]  # sec:label -> ch07
    ch_label_by_num: dict[str, str]  # "07" -> ch:finding-boundary
    ch_num_by_label: dict[str, str]  # ch:finding-boundary -> "07"
    eq_owner: dict[str, str]  # eq:label -> sec:label | ch:label
    eq_line: dict[str, int]  # eq:label -> defining line in file
    eq_chapter: dict[str, str]  # eq:label -> ch07
    sections: dict[str, SectionInfo]
    edges: set[tuple[str, str]]  # (source_node, target_node)
    eq_edges: set[tuple[str, str]]  # eq/section → eq:… (\\eqref)
    unresolved_refs: set[str]


def strip_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if line.strip().startswith("%"):
            continue
        out = []
        i = 0
        while i < len(line):
            if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
                break
            out.append(line[i])
            i += 1
        lines.append("".join(out))
    return "\n".join(lines)


def chapter_id(path: Path) -> str:
    m = CHAPTER_NUM.search(path.stem)
    return f"ch{m.group(1)}" if m else path.stem


APP_ID = re.compile(r"^app([A-Z])")


def unit_id(chapter_field: str) -> str:
    """Stable unit node id for a chapter file (``ch07`` or ``appB-bridge-crosswalk``)."""
    return f"unit:{chapter_field}"


def normalize_cite_from(cite_from: str, ch_owner: dict[str, str]) -> str:
    """Map chapter-level cite anchors to ``unit:…`` (never emit ``ch:`` in the DAG)."""
    if cite_from.startswith("sec:"):
        return cite_from
    if cite_from.startswith("ch:") and cite_from in ch_owner:
        return unit_id(ch_owner[cite_from])
    return cite_from


def resolve_ref_target(ref: str, ch_owner: dict[str, str], sec_owner: dict[str, str]) -> str | None:
    """Resolve ``\\ref{…}`` to a graph node id (``sec:…`` or ``unit:…``)."""
    if ref.startswith("ch:"):
        if ref not in ch_owner:
            return None
        return unit_id(ch_owner[ref])
    if ref.startswith("sec:"):
        if ref not in sec_owner:
            return None
        return ref
    return None


def parse_manuscript() -> ParsedManuscript:
    ch_owner: dict[str, str] = {}
    sec_owner: dict[str, str] = {}
    ch_label_by_num: dict[str, str] = {}
    ch_num_by_label: dict[str, str] = {}
    eq_owner: dict[str, str] = {}
    eq_line: dict[str, int] = {}
    eq_chapter: dict[str, str] = {}
    sections: dict[str, SectionInfo] = {}
    edges: set[tuple[str, str]] = set()
    eq_edges: set[tuple[str, str]] = set()
    unresolved: set[str] = set()

    paths = sorted(p for g in TEX_GLOBS for p in ROOT.glob(g))

    # Pass 1: labels, sections, definitions, equation homes
    file_lines: list[tuple[Path, str, list[str]]] = []
    for path in paths:
        ch = chapter_id(path)
        text = strip_comments(path.read_text(encoding="utf-8", errors="replace"))
        lines = text.splitlines()
        file_lines.append((path, ch, lines))

        chapter_label: str | None = None
        current_sec: str | None = None

        for idx, line in enumerate(lines, 1):
            for m in LABEL_CH.finditer(line):
                chapter_label = m.group(1)
                ch_owner[chapter_label] = ch
                num = CHAPTER_NUM.search(path.stem)
                if num:
                    ch_label_by_num[num.group(1)] = chapter_label
                    ch_num_by_label[chapter_label] = num.group(1)

            for m in LABEL_SEC.finditer(line):
                sec = m.group(1)
                current_sec = sec
                sec_owner[sec] = ch
                if sec not in sections:
                    sections[sec] = SectionInfo(
                        label=sec, chapter=ch, chapter_file=path.name, line=idx
                    )

            for m in LABEL_ANY.finditer(line):
                label = m.group(1)
                if label.startswith("eq:"):
                    home = current_sec or chapter_label
                    if home:
                        eq_owner[label] = home
                        eq_line[label] = idx
                        eq_chapter[label] = ch

            if DEF_START.search(line):
                title = DEF_START.search(line).group(1) or ""
                home = current_sec or chapter_label
                if home and home.startswith("sec:"):
                    sections.setdefault(
                        home,
                        SectionInfo(label=home, chapter=ch, chapter_file=path.name, line=idx),
                    ).definitions.append(title.strip())

    # Pass 2: cross-references (all labels known)
    for _path, _ch, lines in file_lines:
        current_sec: str | None = None
        chapter_label: str | None = None
        for line in lines:
            m_ch = LABEL_CH.search(line)
            if m_ch:
                chapter_label = m_ch.group(1)
            m_sec = LABEL_SEC.search(line)
            if m_sec:
                current_sec = m_sec.group(1)

            cite_from = current_sec or chapter_label
            if not cite_from:
                continue
            src = normalize_cite_from(cite_from, ch_owner)
            for ref in TEXTREF.findall(line):
                tgt = resolve_ref_target(ref, ch_owner, sec_owner)
                if tgt is None:
                    unresolved.add(ref)
                    continue
                edges.add((src, tgt))

            for ref in EQREF.findall(line):
                if ref not in eq_owner:
                    unresolved.add(ref)
                    continue
                src = normalize_cite_from(cite_from, ch_owner)
                eq_edges.add((src, ref))

    return ParsedManuscript(
        ch_owner=ch_owner,
        sec_owner=sec_owner,
        ch_label_by_num=ch_label_by_num,
        ch_num_by_label=ch_num_by_label,
        eq_owner=eq_owner,
        eq_line=eq_line,
        eq_chapter=eq_chapter,
        sections=sections,
        edges=edges,
        eq_edges=eq_edges,
        unresolved_refs=unresolved,
    )


def load_glossary_entries() -> list[dict]:
    data = yaml.safe_load(CONCEPTS_YML.read_text(encoding="utf-8"))
    entries: list[dict] = []
    for row in data.get("concepts", []):
        book_labels = list(row.get("bookLabels") or [])
        slug = row["slug"]
        for gt in row.get("glossaryTerms") or []:
            entries.append(
                {
                    "term": gt["term"],
                    "definition": gt.get("definition", ""),
                    "slug": slug,
                    "bookLabels": book_labels,
                    "kind": "glossaryTerm",
                }
            )
        if row.get("kind") == "glossary":
            entries.append(
                {
                    "term": row.get("term") or row.get("title", slug),
                    "definition": row.get("summary", ""),
                    "slug": slug,
                    "bookLabels": book_labels,
                    "kind": "glossary",
                }
            )
    return entries


def resolve_glossary_home(entry: dict, ms: ParsedManuscript) -> dict:
    """Return validation record for one glossary entry."""
    term = entry["term"]
    definition = entry.get("definition", "")
    labels = list(entry.get("bookLabels") or [])

    # Hints from definition prose (most specific first)
    def_secs = SEC_HINT.findall(definition)
    def_eqs = EQ_HINT.findall(definition)
    def_ch_nums = CH_HINT.findall(definition)

    for sec in def_secs:
        if sec.startswith("sec:") and sec in ms.sec_owner and sec not in labels:
            labels.insert(0, sec)
    for eq in def_eqs:
        home = ms.eq_owner.get(eq)
        if home and home not in labels:
            labels.insert(0, home)
    for num in def_ch_nums:
        ch_label = ms.ch_label_by_num.get(num.zfill(2) if len(num) == 1 else num)
        if not ch_label:
            ch_label = ms.ch_label_by_num.get(num)
        if ch_label and ch_label not in labels:
            labels.append(ch_label)

    resolved_secs = [lb for lb in labels if lb.startswith("sec:") and lb in ms.sec_owner]

    # Term-specific section: definition title match, then term mention in section text
    if resolved_secs or def_ch_nums or [lb for lb in labels if lb.startswith("ch:")]:
        ch_nums = def_ch_nums or []
        if not ch_nums:
            for lb in labels:
                if lb.startswith("ch:"):
                    ch_nums = [ms.ch_num_by_label.get(lb, "")]
                    break
        for ch_num in ch_nums:
            ch_num = ch_num.zfill(2) if len(ch_num) == 1 else ch_num
            ch_id = f"ch{ch_num}"
            for sec, info in ms.sections.items():
                if info.chapter != ch_id:
                    continue
                if any(term.lower() in d.lower() for d in info.definitions):
                    return {
                        "term": term,
                        "slug": entry["slug"],
                        "status": "inferred",
                        "home": sec,
                        "chapter": info.chapter,
                        "source": f"definition block in {sec}",
                        "labels": labels,
                    }

    if def_eqs:
        for eq in def_eqs:
            home = ms.eq_owner.get(eq)
            if home and home.startswith("sec:"):
                return {
                    "term": term,
                    "slug": entry["slug"],
                    "status": "inferred",
                    "home": home,
                    "chapter": ms.sec_owner[home],
                    "source": f"equation {eq}",
                    "labels": labels,
                }

    if resolved_secs:
        # Prefer section whose slug/id matches term keywords (e.g. minimal-model for deployment leverage)
        term_tokens = set(re.findall(r"[a-z]{4,}", term.lower()))
        best = resolved_secs[0]
        best_score = -1
        for sec in resolved_secs:
            sec_tokens = set(re.findall(r"[a-z]{4,}", sec.lower()))
            score = len(term_tokens & sec_tokens)
            if score > best_score:
                best_score = score
                best = sec
        home = best
        return {
            "term": term,
            "slug": entry["slug"],
            "status": "ok" if home in (entry.get("bookLabels") or []) else "inferred",
            "home": home,
            "chapter": ms.sec_owner[home],
            "source": "sec label",
            "labels": labels,
        }

    resolved_chs = [lb for lb in labels if lb.startswith("ch:") and lb in ms.ch_owner]

    if resolved_chs:
        ch_label = resolved_chs[0]
        ch_num = ms.ch_num_by_label.get(ch_label, "")
        for sec, info in ms.sections.items():
            if info.chapter != f"ch{ch_num}":
                continue
            if any(term.lower() in d.lower() for d in info.definitions):
                return {
                    "term": term,
                    "slug": entry["slug"],
                    "status": "inferred",
                    "home": sec,
                    "chapter": info.chapter,
                    "source": f"definition in {sec}",
                    "labels": labels,
                }
        return {
            "term": term,
            "slug": entry["slug"],
            "status": "chapter-only",
            "home": ch_label,
            "chapter": ms.ch_owner[ch_label],
            "source": "chapter label only — no sec: anchor",
            "labels": labels,
        }

    return {
        "term": term,
        "slug": entry["slug"],
        "status": "missing",
        "home": None,
        "chapter": None,
        "source": "no resolvable bookLabels or definition hint",
        "labels": labels,
    }


def dot_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def unit_sort_key(unit: str) -> tuple:
    """Sort chapters before appendices, numerically within chapters."""
    body = unit.removeprefix("unit:")
    m = CHAPTER_NUM.match(body)
    if m:
        return (0, int(m.group(1)))
    m = APP_ID.match(body)
    if m:
        return (1, m.group(1))
    return (2, body)


def unit_display_label(chapter_field: str, ch_label: str | None) -> str:
    m = CHAPTER_NUM.match(chapter_field)
    if m:
        num = m.group(1)
        suffix = f"\\n{ch_label[3:]}" if ch_label else ""
        return f"Ch {num}{suffix}"
    m = APP_ID.match(chapter_field)
    if m:
        slug = chapter_field.split("-", 1)[-1].replace("-", " ") if "-" in chapter_field else chapter_field
        return f"App {m.group(1)}\\n{slug}"
    return chapter_field.replace("-", "\\n")


def eq_manuscript_order(eq: str, ms: ParsedManuscript) -> tuple[int, int, str]:
    ch = ms.eq_chapter.get(eq, "ch999")
    num = int(ch[2:]) if ch[2:].isdigit() else 999
    return (num, ms.eq_line.get(eq, 0), eq)


def node_manuscript_order(node: str, ms: ParsedManuscript) -> tuple[int, int, str]:
    """Sort key: chapter number, line in file, label (for stable tie-break)."""
    if node.startswith("unit:"):
        sk = unit_sort_key(node.removeprefix("unit:"))
        if sk[0] == 0:
            return (sk[1], 0, node)
        if sk[0] == 1:
            return (1000 + ord(sk[1]), 0, node)
        return (2000, 0, node)
    if node.startswith("sec:"):
        ch = ms.sec_owner.get(node, "ch999")
        num = int(ch[2:]) if ch[2:].isdigit() else 999
        info = ms.sections.get(node)
        line = info.line if info else 0
        return (num, line, node)
    if node.startswith("eq:"):
        return eq_manuscript_order(node, ms)
    return (9999, 0, node)


def is_back_reference(src: str, tgt: str, ms: ParsedManuscript) -> bool:
    """True when *tgt* is defined earlier in the manuscript than *src* (normal citation)."""
    if src.startswith("eq:") and tgt.startswith("eq:"):
        return eq_manuscript_order(src, ms) > eq_manuscript_order(tgt, ms)
    return node_manuscript_order(src, ms) > node_manuscript_order(tgt, ms)


def eq_ref_edge_attrs() -> str:
    return 'color="#059669", style=solid, penwidth=1.0, weight=1.5, constraint=false'


def reading_order_rank_pair(src: str, tgt: str, ms: ParsedManuscript) -> tuple[str, str] | None:
    """Manuscript-order pair (left, right) for ``rankdir=LR`` — earlier node first."""
    if src == tgt:
        return None
    if is_back_reference(src, tgt, ms):
        return tgt, src
    return src, tgt


def cross_ref_edge_attrs(src: str, tgt: str, ms: ParsedManuscript) -> str:
    """Visible citation edge — shows cite direction; never constrains ``dot`` ranks."""
    if is_back_reference(src, tgt, ms):
        return 'color="#d97706", style=dashed, penwidth=0.8, weight=0.5, constraint=false'
    return 'color="#ea580c", style=solid, penwidth=1.2, weight=2, constraint=false'


READING_ORDER_RANK_ATTRS = "style=invis, weight=1, constraint=true"
SECTION_LINE_SPINE_ATTRS = "style=invis, weight=80, constraint=true"


def transitive_reduction(edges: set[tuple[str, str]] | list[tuple[str, str]]) -> set[tuple[str, str]]:
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


def back_ref_edge_set(
    edges: set[tuple[str, str]] | list[tuple[str, str]], ms: ParsedManuscript
) -> set[tuple[str, str]]:
    return {(s, t) for s, t in edges if is_back_reference(s, t, ms)}


def layout_back_ref_edges(
    edges: set[tuple[str, str]] | list[tuple[str, str]],
    ms: ParsedManuscript,
    *,
    thin_transitive: bool,
) -> set[tuple[str, str]]:
    """Back-reference cite edges used for rank layout (optionally transitively thinned)."""
    back = back_ref_edge_set(edges, ms)
    if thin_transitive:
        back = transitive_reduction(back)
    return back


def sections_in_line_order(
    unit: str, unit_to_secs: dict[str, list[str]], ms: ParsedManuscript
) -> list[str]:
    secs = unit_to_secs.get(unit, [])
    return sorted(secs, key=lambda s: (ms.sections[s].line if s in ms.sections else 0, s))


def emitted_eq_spine_pairs(
    unit: str,
    unit_to_secs: dict[str, list[str]],
    content_nodes: set[str],
    ms: ParsedManuscript,
) -> list[tuple[str, str]]:
    """Consecutive labeled equations in this unit, in line order."""
    eqs = [
        eq
        for eq, ch in ms.eq_chapter.items()
        if ch == unit and eq in content_nodes
    ]
    eqs.sort(key=lambda e: eq_manuscript_order(e, ms))
    return list(zip(eqs, eqs[1:]))


def emitted_section_spine_pairs(
    unit: str,
    unit_to_secs: dict[str, list[str]],
    content_nodes: set[str],
    ms: ParsedManuscript,
) -> list[tuple[str, str]]:
    """Consecutive xref/glossary sections in this unit, in manuscript line order."""
    secs = [s for s in sections_in_line_order(unit, unit_to_secs, ms) if s in content_nodes]
    return list(zip(secs, secs[1:]))


def eq_home_node(eq: str, ms: ParsedManuscript, ch_owner: dict[str, str]) -> str | None:
    home = ms.eq_owner.get(eq)
    if not home:
        return None
    if home.startswith("sec:"):
        return home
    if home.startswith("ch:") and home in ch_owner:
        return unit_id(ch_owner[home])
    return None


def append_back_ref_rank_edges(
    lines: list[str],
    edges: set[tuple[str, str]] | list[tuple[str, str]],
    content_nodes: set[str],
    ms: ParsedManuscript,
    *,
    comment: str,
    thin_transitive: bool = True,
) -> int:
    rank_edges: set[tuple[str, str]] = set()
    layout_edges = layout_back_ref_edges(edges, ms, thin_transitive=thin_transitive)
    for src, tgt in layout_edges:
        if src not in content_nodes or tgt not in content_nodes:
            continue
        pair = reading_order_rank_pair(src, tgt, ms)
        if pair:
            rank_edges.add(pair)
    thin_note = " transitively thinned" if thin_transitive else ""
    lines.append(f"  // {comment}{thin_note}")
    for left, right in sorted(rank_edges):
        lines.append(f'  "{left}" -> "{right}" [{READING_ORDER_RANK_ATTRS}];')
    lines.append(f"  // ({len(rank_edges)} rank edges from {len(layout_edges)} back-ref cites)")
    lines.append("")
    return len(rank_edges)


def unit_field_from_node(node: str, ms: ParsedManuscript) -> str | None:
    if node.startswith("unit:"):
        return node.removeprefix("unit:")
    if node.startswith("sec:"):
        return ms.sec_owner.get(node)
    return None


def unit_outgoing_ref_count(unit: str, ms: ParsedManuscript, outgoing: dict[str, set[str]]) -> int:
    uid = unit_id(unit)
    n = len(outgoing.get(uid, set()))
    for src, tgts in outgoing.items():
        if src.startswith("sec:") and ms.sec_owner.get(src) == unit:
            n += len(tgts)
    return n


def classify_terminal(node: str, ms: ParsedManuscript, outgoing: dict[str, set[str]], incoming: dict[str, set[str]]) -> str:
    """Heuristic class for nodes with no outgoing cross-refs."""
    if node.startswith("unit:"):
        unit = node.removeprefix("unit:")
        if unit_outgoing_ref_count(unit, ms, outgoing) > 0:
            return "unit sink (receives cites; sections inside cite out)"
        return "unit sink (no outgoing cites from this file)"
    if "wwctv" in node:
        return "WWCTV falsifier block (cited, does not cite out)"
    if node.startswith("sec:app"):
        return "appendix index / crosswalk anchor"
    if "summary" in node or "conclusion" in node:
        return "summary section (leaf by design)"
    if len(incoming[node]) <= 1:
        return "leaf section (low in-degree)"
    return "leaf section (cited, no labeled outward \\ref)"


def build_terminal_audit_md(ms: ParsedManuscript) -> str:
    outgoing: dict[str, set[str]] = defaultdict(set)
    incoming: dict[str, set[str]] = defaultdict(set)
    for src, tgt in ms.edges:
        outgoing[src].add(tgt)
        incoming[tgt].add(src)
    all_nodes = set(outgoing) | set(incoming)
    terminals = sorted(n for n in all_nodes if not outgoing[n])

    back = sum(1 for s, t in ms.edges if is_back_reference(s, t, ms))
    fwd = len(ms.edges) - back

    by_class: dict[str, list[str]] = defaultdict(list)
    for n in terminals:
        by_class[classify_terminal(n, ms, outgoing, incoming)].append(n)

    lines = [
        "# Section graph — terminal & back-reference audit",
        "",
        "Generated by `scripts/build_section_reference_graph.py`.",
        "",
        "## Cross-ref edge direction (manuscript order)",
        "",
        f"- Total cross-ref edges: {len(ms.edges)}",
        f"- **Back references** (cite earlier material): {back}",
        f"- Forward references (cite later material): {fwd}",
        "",
        "**Layout (DOT):** visible cite edges are always `constraint=false`. **Chapters are not",
        "chained in reading order** — inter-chapter placement uses invisible earlier→later",
        "rank edges on **back refs only** (reversed vs the cite arrow). **Within each chapter**,",
        "consecutive emitted sections follow an invisible line-order spine (by `.tex` position).",
        "Forward cites are visible but do not constrain layout.",
        "",
        "Back references are expected in a book (later chapters cite earlier definitions).",
        "",
        "## Terminal nodes (no outgoing `\\ref{ch:}` / `\\ref{sec:}`)",
        "",
        f"Count: {len(terminals)} of {len(all_nodes)} cross-ref nodes.",
        "",
        "| Class | Count |",
        "|-------|------:|",
    ]
    for cls in sorted(by_class, key=lambda c: -len(by_class[c])):
        lines.append(f"| {cls} | {len(by_class[cls])} |")
    lines.extend(["", "## Sample terminals (inspected)", ""])
    lines.append("| Node | In | Class | Note |")
    lines.append("|------|---:|-------|------|")

    sample_order = [
        "unit:ch16", "unit:ch25", "unit:ch31", "unit:ch34", "unit:ch07",
        "sec:bundle-bearer-map", "sec:appk-adversarial", "sec:wwctv-transport-types",
        "sec:basin-guarantees-ch33", "sec:bundle-tradeoff-geometry",
        "unit:ch12", "sec:summary-low-dim",
    ]
    notes = {
        "unit:ch16": "Was `ch:value-bundle-model` hub; now unit receives chapter-level cites",
        "unit:ch25": "Was `ch:correction-causal-channel`; sections inside still cite out",
        "unit:ch31": "Was `ch:conserved-properties`",
        "unit:ch34": "Was `ch:selection-environment`",
        "unit:ch07": "Was `ch:finding-boundary`",
        "sec:bundle-bearer-map": "Bridge paragraph; 1 cite from App G",
        "sec:appk-adversarial": "App D forward-pointer target for App K",
        "sec:wwctv-transport-types": "WWCTV falsifier block",
        "sec:basin-guarantees-ch33": "Guarantee-type definition leaf",
        "sec:bundle-tradeoff-geometry": "Local geometry block; 1 cite",
        "unit:ch12": "Unit sink if preamble-only cites absent",
        "sec:summary-low-dim": "Chapter summary section",
    }
    for n in sample_order:
        if n not in terminals:
            continue
        cls = classify_terminal(n, ms, outgoing, incoming)
        lines.append(f"| `{n}` | {len(incoming[n])} | {cls} | {notes.get(n, '')} |")

    # Top terminals by in-degree
    lines.extend(["", "## Top terminal nodes by in-degree", ""])
    lines.append("| Node | In | Out | Class |")
    lines.append("|------|---:|----:|-------|")
    for n in sorted(terminals, key=lambda x: -len(incoming[x]))[:25]:
        lines.append(
            f"| `{n}` | {len(incoming[n])} | {len(outgoing[n])} | "
            f"{classify_terminal(n, ms, outgoing, incoming)} |"
        )

    lines.extend([
        "",
        "## Graph model",
        "",
        "- ``\\ref{ch:…}`` targets map to **`unit:chNN`** (chapter/appendix file), not ``ch:`` labels.",
        "- ``\\ref{sec:…}`` stays section-granular.",
        "- **Unit nodes as terminals** are citation sinks: the file is cited as a whole while",
        "  outgoing deps live on ``sec:`` nodes inside the same unit.",
        "",
    ])
    return "\n".join(lines)


def xref_and_glossary_nodes(ms: ParsedManuscript, glossary_homes: dict[str, list[str]]) -> set[str]:
    """Nodes that participate in cross-refs, eqrefs, or glossary definitions."""
    nodes: set[str] = set()
    for src, tgt in ms.edges:
        nodes.add(src)
        nodes.add(tgt)
    for src, tgt in ms.eq_edges:
        nodes.add(src)
        nodes.add(tgt)
    for home in glossary_homes:
        if home.startswith("sec:") or home.startswith("unit:"):
            nodes.add(home)
    return nodes


def eq_nodes_in_graph(ms: ParsedManuscript, content_nodes: set[str]) -> set[str]:
    return {n for n in content_nodes if n.startswith("eq:")}


def manuscript_spine_pairs(units: list[str]) -> list[tuple[str, str]]:
    """Consecutive chapter/appendix units in reading order (layout spine only)."""
    pairs: list[tuple[str, str]] = []
    ordered = [u for u in units]
    for a, b in zip(ordered, ordered[1:]):
        pairs.append((unit_id(a), unit_id(b)))
    return pairs


def aggregate_unit_cross_refs(ms: ParsedManuscript) -> set[tuple[str, str]]:
    """Collapse section-level ``\\ref`` edges to unit→unit (inter-unit only)."""
    unit_edges: set[tuple[str, str]] = set()
    for src, tgt in ms.edges:
        src_unit = unit_field_from_node(src, ms)
        tgt_unit = unit_field_from_node(tgt, ms)
        if not src_unit or not tgt_unit:
            continue
        su, tu = unit_id(src_unit), unit_id(tgt_unit)
        if su != tu:
            unit_edges.add((su, tu))
    return unit_edges


def build_dot(ms: ParsedManuscript, glossary_homes: dict[str, list[str]], *, thin_transitive: bool = True) -> str:
    """Flat graph: book → unit (chapter/appendix) → sections/ch labels; cross-refs separate."""
    # Group content by manuscript unit (one tex file)
    unit_to_secs: dict[str, list[str]] = defaultdict(list)
    for sec, info in ms.sections.items():
        unit_to_secs[info.chapter].append(sec)
    for u in unit_to_secs:
        unit_to_secs[u] = sections_in_line_order(u, unit_to_secs, ms)

    ch_label_by_unit: dict[str, str] = {}
    for ch_label, ch_field in ms.ch_owner.items():
        ch_label_by_unit[ch_field] = ch_label

    units = sorted(
        set(unit_to_secs) | set(ch_label_by_unit),
        key=unit_sort_key,
    )

    # Section nodes: cross-ref participants + glossary homes only (not all 1300+ sections)
    xref_nodes = xref_and_glossary_nodes(ms, glossary_homes)
    ref_targets = {t for _, t in ms.edges}
    ref_sources = {s for s, _ in ms.edges}

    content_nodes: set[str] = set(xref_nodes)
    for u in units:
        content_nodes.add(unit_id(u))

    lines = [
        "digraph SectionReferenceGraph {",
        '  graph [rankdir=LR, fontsize=10, overlap=prism, sep="+25",',
        '    label="Manuscript section reference DAG\\\\n(gray: unit→sec spine; orange: \\\\ref; ranks from cites)", labelloc=t];',
        "  node [fontname=Helvetica, fontsize=9];",
        "  edge [fontname=Helvetica, fontsize=8];",
        "",
        '  "book:manuscript" [shape=doublecircle, style=filled, fillcolor="#1e293b",',
        '    fontcolor=white, label="Book", width=1.2, height=1.2];',
        "",
    ]

    # Unit nodes (chapters + appendices)
    for u in units:
        uid = unit_id(u)
        ch_label = ch_label_by_unit.get(u)
        label = unit_display_label(u, ch_label)
        n_secs = len(unit_to_secs.get(u, []))
        n_xref_secs = sum(1 for s in unit_to_secs.get(u, []) if s in content_nodes)
        cited = uid in ref_targets
        cites = uid in ref_sources
        color = "#fed7aa" if cited else "#fff7ed"
        pen = "2.0" if cited else "1.5"
        badge = []
        if cited:
            badge.append(f"{sum(1 for s,t in ms.edges if t==uid)} in")
        if cites:
            badge.append(f"{sum(1 for s,t in ms.edges if s==uid)} out")
        badge_s = ("\\n" + ", ".join(badge)) if badge else ""
        lines.append(
            f'  "{uid}" [shape=folder, style=filled, fillcolor="{color}", color="#92400e", '
            f'label="{dot_escape(label)}\\n({n_xref_secs}/{n_secs} sec){badge_s}", penwidth={pen}];'
        )
    lines.append("")

    # Section nodes: cross-ref participants + glossary homes only
    for node in sorted(content_nodes):
        terms = glossary_homes.get(node, [])
        gloss_note = ""
        if terms:
            gloss_note = "\\n" + ", ".join(terms[:2])
            if len(terms) > 2:
                gloss_note += ", …"

        if node.startswith("sec:"):
            short = node[4:].replace("-", "\\n")
            color = "#dbeafe" if terms else "#fef3c7"
            in_refs = node in xref_nodes
            style = '"filled,bold"' if in_refs else "filled"
            lines.append(
                f'  "{node}" [shape=box, style={style}, fillcolor="{color}", '
                f'label="{dot_escape(short)}{gloss_note}"];'
            )
        elif node.startswith("unit:"):
            pass  # already emitted above
        elif node.startswith("ch:"):
            lines.append(
                f'  "{node}" [shape=note, style=filled, fillcolor="#ffedd5", '
                f'label="{dot_escape(node[3:] + gloss_note)}"];'
            )
        elif node.startswith("eq:"):
            short = node[3:].replace("-", "\\n")
            lines.append(
                f'  "{node}" [shape=hexagon, style=filled, fillcolor="#d1fae5", '
                f'label="{dot_escape(short)}"];'
            )
    lines.append("")

    # Optional ch: label nodes (structural only, not cross-ref endpoints)
    for u in units:
        ch_label = ch_label_by_unit.get(u)
        if ch_label and ch_label in content_nodes and ch_label not in xref_nodes:
            lines.append(
                f'  "{ch_label}" [shape=note, style=filled, fillcolor="#ffedd5", '
                f'label="{dot_escape(ch_label[3:])}"];'
            )

    # Structural hierarchy: book → first unit; rest follow reading-order spine
    lines.append("  // Structural: book → first unit (weak anchor; no linear chapter spine)")
    if units:
        lines.append(
            f'  "book:manuscript" -> "{unit_id(units[0])}" [color="#64748b", penwidth=2, weight=10, constraint=false];'
        )
    lines.append("")

    lines.append("  // Structural: unit → first section; line-order spine within unit")
    for u in units:
        uid = unit_id(u)
        ch_label = ch_label_by_unit.get(u)
        if ch_label and ch_label in content_nodes:
            lines.append(
                f'  "{uid}" -> "{ch_label}" [color="#94a3b8", penwidth=1.2, weight=40, constraint=false];'
            )
        emitted = [s for s in unit_to_secs.get(u, []) if s in content_nodes]
        if emitted:
            lines.append(
                f'  "{uid}" -> "{emitted[0]}" [color="#94a3b8", penwidth=1.0, weight=40];'
            )
        for a, b in emitted_section_spine_pairs(u, unit_to_secs, content_nodes, ms):
            lines.append(f'  "{a}" -> "{b}" [{SECTION_LINE_SPINE_ATTRS}];')
        for eq in sorted(
            (eq for eq, ch in ms.eq_chapter.items() if ch == u and eq in content_nodes),
            key=lambda e: eq_manuscript_order(e, ms),
        ):
            home = eq_home_node(eq, ms, ms.ch_owner)
            if home and home in content_nodes:
                lines.append(
                    f'  "{home}" -> "{eq}" [color="#6ee7b7", penwidth=0.8, weight=20, constraint=false];'
                )
        for a, b in emitted_eq_spine_pairs(u, unit_to_secs, content_nodes, ms):
            lines.append(f'  "{a}" -> "{b}" [{SECTION_LINE_SPINE_ATTRS}];')
    lines.append("")

    lines.append("  // Cross-references (visible; constraint=false — cite direction only)")
    n_back = 0
    for src, tgt in sorted(ms.edges):
        if src not in content_nodes or tgt not in content_nodes:
            continue
        if is_back_reference(src, tgt, ms):
            n_back += 1
        attrs = cross_ref_edge_attrs(src, tgt, ms)
        lines.append(f'  "{src}" -> "{tgt}" [{attrs}];')
    lines.append(f"  // ({n_back} back-ref sec/ch cites, {len(ms.edges) - n_back} forward)")
    lines.append("")

    lines.append("  // Equation references (\\\\eqref / \\\\ref{eq:...}; green)")
    n_eq_back = 0
    for src, tgt in sorted(ms.eq_edges):
        if src not in content_nodes or tgt not in content_nodes:
            continue
        if is_back_reference(src, tgt, ms):
            n_eq_back += 1
        lines.append(f'  "{src}" -> "{tgt}" [{eq_ref_edge_attrs()}];')
    lines.append(f"  // ({n_eq_back} back-ref eq cites, {len(ms.eq_edges) - n_eq_back} forward)")
    lines.append("")

    all_rank_edges = set(ms.edges) | set(ms.eq_edges)
    append_back_ref_rank_edges(
        lines,
        all_rank_edges,
        content_nodes,
        ms,
        comment="Reading-order ranks (invis earlier→later; back-ref cites reversed vs arrow)",
        thin_transitive=thin_transitive,
    )

    lines.append("}")
    return "\n".join(lines)


def build_unit_dot(ms: ParsedManuscript, *, thin_transitive: bool = True) -> str:
    """Chapter/appendix-level overview: one node per unit, aggregated cross-refs, reading-order spine."""
    unit_to_secs: dict[str, list[str]] = defaultdict(list)
    for sec, info in ms.sections.items():
        unit_to_secs[info.chapter].append(sec)
    for u in unit_to_secs:
        unit_to_secs[u] = sections_in_line_order(u, unit_to_secs, ms)

    ch_label_by_unit: dict[str, str] = {}
    for ch_label, ch_field in ms.ch_owner.items():
        ch_label_by_unit[ch_field] = ch_label

    units = sorted(
        set(unit_to_secs) | set(ch_label_by_unit),
        key=unit_sort_key,
    )
    unit_edges = aggregate_unit_cross_refs(ms)
    ref_targets = {t for _, t in ms.edges}
    ref_sources = {s for s, _ in ms.edges}

    lines = [
        "digraph SectionReferenceUnits {",
        '  graph [rankdir=LR, fontsize=11, overlap=prism, sep="+30",',
        '    label="Manuscript unit reference graph\\\\n(citation-driven ranks; dashed = reading-order hint)", labelloc=t];',
        "  node [fontname=Helvetica, fontsize=10, shape=folder, style=filled];",
        "  edge [fontname=Helvetica, fontsize=8];",
        "",
        '  "book:manuscript" [shape=doublecircle, style=filled, fillcolor="#1e293b",',
        '    fontcolor=white, label="Book", width=1.2, height=1.2];',
        "",
    ]

    for u in units:
        uid = unit_id(u)
        ch_label = ch_label_by_unit.get(u)
        label = unit_display_label(u, ch_label)
        n_secs = len(unit_to_secs.get(u, []))
        cited = uid in ref_targets
        cites = uid in ref_sources
        color = "#fed7aa" if cited else "#fff7ed"
        badge = []
        if cited:
            badge.append(f"{sum(1 for s, t in ms.edges if t == uid)} in")
        if cites:
            badge.append(f"{sum(1 for s, t in ms.edges if s == uid)} out")
        badge_s = ("\\n" + ", ".join(badge)) if badge else ""
        lines.append(
            f'  "{uid}" [fillcolor="{color}", color="#92400e", '
            f'label="{dot_escape(label)}\\n({n_secs} sec){badge_s}"];'
        )
    lines.append("")

    lines.append("  // Reading-order hint only (non-constraining — layout from cite ranks below)")
    for a, b in manuscript_spine_pairs(units):
        lines.append(
            f'  "{a}" -> "{b}" [color="#94a3b8", style=dashed, penwidth=0.6, weight=0, constraint=false];'
        )
    lines.append("")

    layout_back = layout_back_ref_edges(unit_edges, ms, thin_transitive=thin_transitive)
    visible_back = layout_back if thin_transitive else back_ref_edge_set(unit_edges, ms)

    lines.append("  // Aggregated cross-references (visible; low weight, non-constraining)")
    n_back_vis = 0
    for src, tgt in sorted(unit_edges):
        if is_back_reference(src, tgt, ms):
            if thin_transitive and (src, tgt) not in visible_back:
                continue
            n_back_vis += 1
        attrs = cross_ref_edge_attrs(src, tgt, ms)
        lines.append(f'  "{src}" -> "{tgt}" [{attrs}];')
    lines.append(
        f"  // ({n_back_vis} back-ref unit cites shown, "
        f"{len(unit_edges) - n_back_vis} forward; "
        f"{len(layout_back)} back cites drive ranks)"
    )
    lines.append("")
    unit_nodes = {unit_id(u) for u in units}
    append_back_ref_rank_edges(
        lines,
        unit_edges,
        unit_nodes,
        ms,
        comment="Unit ranks from back-ref cites (invis earlier→later; reversed vs arrow)",
        thin_transitive=thin_transitive,
    )

    lines.append("  // book → first unit (weak anchor only)")
    if units:
        lines.append(
            f'  "book:manuscript" -> "{unit_id(units[0])}" [color="#64748b", penwidth=1.5, weight=10, constraint=false];'
        )

    lines.append("}")
    return "\n".join(lines)


def build_audit_md(ms: ParsedManuscript, validations: list[dict]) -> str:
    ok = [v for v in validations if v["status"] == "ok"]
    inferred = [v for v in validations if v["status"] == "inferred"]
    ch_only = [v for v in validations if v["status"] == "chapter-only"]
    missing = [v for v in validations if v["status"] == "missing"]

    lines = [
        "# Glossary section audit",
        "",
        "Generated by `scripts/build_section_reference_graph.py`. Validates that each",
        "site glossary entry (`metadata/concepts.yml`) resolves to a manuscript",
        "`sec:` label (preferred) or `ch:` label (acceptable with warning). Definitions",
        "(`\\begin{definition}`) within a section inherit that section as their home.",
        "",
        "## Summary",
        "",
        f"| Status | Count |",
        f"|--------|------:|",
        f"| `ok` (explicit `sec:`) | {len(ok)} |",
        f"| `inferred` (eq/definition/ch hint → section) | {len(inferred)} |",
        f"| `chapter-only` (needs `sec:` in bookLabels) | {len(ch_only)} |",
        f"| `missing` | {len(missing)} |",
        "",
        f"Manuscript: {len(ms.sections)} section labels, {len(ms.edges)} sec/ch ref edges, "
        f"{len(ms.eq_edges)} equation ref edges, "
        f"{len(ms.unresolved_refs)} unresolved `\\ref{{...}}` / `\\eqref{{...}}` targets.",
        "",
    ]

    def table(title: str, rows: list[dict]) -> None:
        if not rows:
            return
        lines.extend([f"## {title}", ""])
        lines.append("| Term | Card | Home | Source |")
        lines.append("|------|------|------|--------|")
        for v in sorted(rows, key=lambda r: r["term"].lower()):
            home = v.get("home") or "—"
            lines.append(
                f"| {v['term']} | `{v['slug']}` | `{home}` | {v['source']} |"
            )
        lines.append("")

    table("OK — explicit section anchor", ok)
    table("Inferred — section resolved from definition/equation", inferred)
    table("Chapter-only — add `sec:` to bookLabels", ch_only)
    table("Missing — no resolvable anchor", missing)

    if ms.unresolved_refs:
        lines.extend(["## Unresolved manuscript refs", ""])
        for u in sorted(ms.unresolved_refs):
            lines.append(f"- `{u}`")
        lines.append("")

    lines.extend(
        [
            "## Recommended bookLabels fixes",
            "",
            "Add the narrowest `sec:` label from the Home column to `bookLabels` on the",
            "card slug shown, then re-run this script.",
            "",
        ]
    )
    for v in inferred + ch_only:
        if v.get("home") and v["home"].startswith("sec:"):
            lines.append(f"- `{v['slug']}` → add `{v['home']}` for *{v['term']}*")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if audit report or dot would change",
    )
    parser.add_argument(
        "--no-thin-transitive",
        action="store_true",
        help="Keep all back-ref rank edges (no transitive reduction; unit graph gets very dense)",
    )
    args = parser.parse_args()
    thin_transitive = not args.no_thin_transitive

    ms = parse_manuscript()
    entries = load_glossary_entries()
    validations = [resolve_glossary_home(e, ms) for e in entries]

    glossary_homes: dict[str, list[str]] = defaultdict(list)
    for v in validations:
        if v.get("home"):
            home = v["home"]
            if home.startswith("ch:") and home in ms.ch_owner:
                home = unit_id(ms.ch_owner[home])
            glossary_homes[home].append(v["term"])
    gloss_map = {k: v for k, v in glossary_homes.items()}

    dot = build_dot(ms, gloss_map, thin_transitive=thin_transitive)
    unit_dot = build_unit_dot(ms, thin_transitive=thin_transitive)
    audit = build_audit_md(ms, validations)
    terminal_audit = build_terminal_audit_md(ms)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    dot_path = OUT_DIR / "section-reference-graph.dot"
    unit_dot_path = OUT_DIR / "section-reference-graph-units.dot"
    audit_path = OUT_DIR / "glossary-section-audit.md"
    terminal_path = OUT_DIR / "terminal-backref-audit.md"

    if args.check:
        changed = False
        for path, content in (
            (dot_path, dot),
            (unit_dot_path, unit_dot),
            (audit_path, audit),
            (terminal_path, terminal_audit),
        ):
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                changed = True
        if changed:
            print("section reference graph out of date — run scripts/build_section_reference_graph.py")
            return 1
        print("section reference graph up to date")
        return 0

    dot_path.write_text(dot, encoding="utf-8")
    unit_dot_path.write_text(unit_dot, encoding="utf-8")
    audit_path.write_text(audit, encoding="utf-8")
    terminal_path.write_text(terminal_audit, encoding="utf-8")

    missing = sum(1 for v in validations if v["status"] == "missing")
    ch_only = sum(1 for v in validations if v["status"] == "chapter-only")
    n_unit_edges = len(aggregate_unit_cross_refs(ms))
    n_units = len(set(ms.sec_owner.values()) | set(ms.ch_owner.values()))
    print(f"Wrote {dot_path} ({len(ms.edges)} sec/ch edges, {len(ms.eq_edges)} eq edges, {len(ms.sections)} section labels)")
    print(f"Wrote {unit_dot_path} ({n_unit_edges} inter-unit edges, {n_units} units)")
    print(f"Wrote {audit_path} ({len(validations)} glossary entries; {ch_only} chapter-only, {missing} missing)")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
