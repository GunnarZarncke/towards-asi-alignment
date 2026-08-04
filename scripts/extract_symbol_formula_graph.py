#!/usr/bin/env python3
"""Extract symbol→formula and formula→formula edges from manuscript chapters.

Outputs Graphviz DOT for reachability analysis. Regenerates the symbol census
in `metadata/symbol-census/` (see that folder's README.md for the full picture:
contribution audit, coverage tables, and rendered graphs).

Usage:
  python3 scripts/extract_symbol_formula_graph.py
  python3 scripts/extract_symbol_formula_graph.py --out metadata/symbol-census/graphs/symbol-formula-graph.dot
"""

from __future__ import annotations

import argparse
import re
import textwrap
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS_DIR = ROOT / "chapters"
LEAN_DIR = ROOT / "formal" / "AlignmentProofSpine"

# \leanspine{kind}{node-id}{gloss} — manuscript ↔ Lean crosswalk anchor.
# kind ∈ {proof, counterexample, bridge}
LEANSPINE = re.compile(
    r"\\leanspine\{(proof|counterexample|bridge)\}\{([^}]+)\}\{([^}]*)\}"
)

LEAN_IMPORT = re.compile(r"^import\s+([A-Za-z0-9_.]+)")
LEAN_DECL_KEYWORDS = (
    "theorem", "lemma", "def", "noncomputable def", "abbrev",
    "structure", "axiom", "inductive", "instance",
)
LEAN_DECL_START = re.compile(
    r"^(?:noncomputable\s+)?(theorem|lemma|def|abbrev|structure|axiom|inductive|instance)\s+"
    r"([A-Za-z_][A-Za-z0-9_.']*)"
)

# Math environment delimiters
ENV_START = re.compile(
    r"\\begin\{(equation\*?|align\*?|gather\*?|multline\*?|eqnarray\*?)\}"
)
ENV_END = re.compile(r"\\end\{(equation\*?|align\*?|gather\*?|multline\*?|eqnarray\*?)\}")
LABEL_EQ = re.compile(r"\\label\{(eq:[^}]+)\}")
LABEL_CH = re.compile(r"\\label\{(ch:[^}]+)\}")
LABEL_SEC = re.compile(r"\\label\{(sec:[^}]+)\}")
EQREF = re.compile(r"\\(?:eqref|ref)\{(eq:[^}]+)\}")

# Cross-references at chapter/section granularity, e.g. "Chapter~\ref{ch:foo}"
# or "Section~\ref{sec:bar-ch15}". These are the manuscript's dominant citation
# style (far more common than \eqref{eq:...}) but were previously invisible to
# the graph: a human reading "this reuses X from Chapter 11" can see the
# dependency, but no \eqref exists to record it. TEXTREF makes them explicit
# edges (see build_dot's "text-ref" edges) instead of leaving them only
# inferrable by reading prose.
TEXTREF = re.compile(r"\\ref\{(ch:[^}]+|sec:[^}]+)\}")

# Skip LaTeX commands that are not symbols
SKIP_CMDS = {
    "mathrm", "text", "operatorname", "mathcal", "mathfrak", "mathbb",
    "mathbf", "mathit", "boldsymbol", "left", "right", "mid", "cdot",
    "times", "leq", "geq", "neq", "approx", "equiv", "propto", "sim",
    "in", "notin", "forall", "exists", "partial", "nabla", "infty",
    "arg", "max", "min", "log", "exp", "Pr", "mathbb", "mathrm",
    "MI", "DL", "CCI", "GLI", "Correctable", "leanspine",
    "label", "ref", "eqref", "autocite", "cite", "emph", "textbf",
    "begin", "end", "frac", "sqrt", "sum", "prod", "int", "lim",
    "to", "mapsto", "longrightarrow", "rightarrow", "Rightarrow",
    "quad", "qquad", "text", "hat", "tilde", "bar", "vec", "dot",
    "ddot", "prime", "circ", "ldots", "cdots", "vdots", "ddots",
    "leftarrow", "longleftrightarrow", "leftrightarrow", "uparrow",
    "downarrow", "Big", "big", "Bigg", "bigg", "displaystyle",
    "scriptstyle", "ensuremath", "not", "neg", "land", "lor",
    "subseteq", "supseteq", "subset", "supset", "cup", "cap",
    "setminus", "emptyset", "varnothing", "pm", "mp", "cdot",
    "ldots", "dots", "mathrm", "operatorname", "underbrace", "overbrace",
    "substack", "aligned", "array", "cases", "matrix", "pmatrix",
    "bmatrix", "vmatrix", "small", "footnotesize", "normalsize",
    "large", "Large", "hfill", "hspace", "vspace", "newline",
    "linebreak", "noindent", "indent", "item", "paragraph",
}

# Greek letters as symbols when standalone
GREEK = set(
    "alpha beta gamma delta epsilon varepsilon zeta eta theta vartheta "
    "iota kappa lambda mu nu xi pi varpi rho varrho sigma varsigma "
    "tau upsilon phi varphi chi psi omega Gamma Delta Theta Lambda "
    "Xi Pi Sigma Upsilon Phi Psi Omega".split()
)

# Common subscript words → canonical symbol names
SUBWORD = re.compile(
    r"^([A-Za-z\\]+)_\{(?:\\(?:mathrm|text)\{)?([^}]+)\}?(?:\})?$"
)


@dataclass
class Formula:
    fid: str  # eq:... or chNN:line:LLL
    chapter: str  # ch14
    chapter_file: str
    line_start: int
    line_end: int
    env: str
    raw: str
    symbols: set[str] = field(default_factory=set)
    refs: set[str] = field(default_factory=set)
    text_refs: set[str] = field(default_factory=set)  # \ref{ch:...} / \ref{sec:...}


@dataclass
class LeanDecl:
    name: str  # dotted Lean identifier, e.g. MarkovBlanketBIQProfile.biq_le_capacity_sum
    kind: str  # theorem/lemma/def/structure/axiom/inductive/instance
    file: str  # relative to formal/AlignmentProofSpine/
    line_start: int
    line_end: int
    body: str
    uses: set[str] = field(default_factory=set)  # other Lean decl names referenced


@dataclass
class LeanSpineRef:
    """One \\leanspine{kind}{node}{gloss} anchor in the manuscript."""

    chapter: str
    line: int
    kind: str  # proof/counterexample/bridge
    node: str  # Lean node id (underscores unescaped)
    gloss: str


def strip_lean_comments(text: str) -> str:
    """Strip Lean `--` line comments and `/- ... -/` (incl. `/-- ... -/` doc)
    block comments. Doc comments routinely name other theorems in prose
    (e.g. "folded into CCI in Lean"), which would otherwise create spurious
    dependency edges (and cycles) that have nothing to do with the actual
    proof term.
    """
    out = []
    i = 0
    n = len(text)
    depth = 0
    while i < n:
        if text[i : i + 2] == "/-":
            depth += 1
            i += 2
            continue
        if depth > 0 and text[i : i + 2] == "-/":
            depth -= 1
            i += 2
            continue
        if depth > 0:
            if text[i] == "\n":
                out.append("\n")
            i += 1
            continue
        if text[i : i + 2] == "--":
            j = text.find("\n", i)
            if j == -1:
                break
            i = j
            continue
        out.append(text[i])
        i += 1
    return "".join(out)


def parse_lean_files(lean_dir: Path) -> tuple[list[LeanDecl], dict[str, set[str]]]:
    """Parse all .lean files under lean_dir for top-level declarations and imports.

    Dependency edges between declarations are found heuristically: for each
    declaration body, scan for other known declaration names as whole-word
    tokens (this catches direct proof-term calls like
    `MarkovBlanketBIQProfile.biq_le_capacity_sum := P10_biq_upper_bound ...`).
    """
    paths = sorted(lean_dir.rglob("*.lean"))
    file_imports: dict[str, set[str]] = {}
    raw_decls: list[tuple[str, str, str, int, int, str]] = []  # name,kind,file,start,end,body

    for path in paths:
        rel = str(path.relative_to(lean_dir.parent.parent))  # formal/...
        text = strip_lean_comments(path.read_text(encoding="utf-8", errors="replace"))
        lines = text.splitlines()

        imports: set[str] = set()
        for line in lines:
            m = LEAN_IMPORT.match(line.strip())
            if m:
                imports.add(m.group(1))
        file_imports[rel] = imports

        i = 0
        n = len(lines)
        while i < n:
            line = lines[i]
            m = LEAN_DECL_START.match(line.strip())
            if not m:
                i += 1
                continue
            kind = m.group(1)
            name = m.group(2)
            start = i + 1
            body_lines = [line]
            i += 1
            # consume until next top-level decl / 'end' / 'namespace' at col 0, or EOF
            while i < n:
                nxt = lines[i]
                stripped = nxt.strip()
                if (
                    LEAN_DECL_START.match(stripped)
                    or stripped.startswith("namespace ")
                    or stripped.startswith("end ")
                    or stripped == "end"
                    or stripped.startswith("import ")
                    or stripped.startswith("/-!")
                ):
                    break
                body_lines.append(nxt)
                i += 1
            end = i
            body = "\n".join(body_lines)
            raw_decls.append((name, kind, rel, start, end, body))

    known_names = {d[0] for d in raw_decls}
    # also register unqualified suffix (after last dot) for looser matching
    suffix_map: dict[str, list[str]] = {}
    for name in known_names:
        suffix_map.setdefault(name.rsplit(".", 1)[-1], []).append(name)

    decls: list[LeanDecl] = []
    for name, kind, rel, start, end, body in raw_decls:
        uses: set[str] = set()
        # strip the declaration's own signature line to avoid trivial self-match
        for other in known_names:
            if other == name:
                continue
            if re.search(rf"(?<![A-Za-z0-9_.']){re.escape(other)}(?![A-Za-z0-9_.'])", body):
                uses.add(other)
        decls.append(
            LeanDecl(
                name=name, kind=kind, file=rel, line_start=start, line_end=end,
                body=body[:400], uses=uses,
            )
        )

    return decls, file_imports


RANGE_SPLIT = re.compile(r"^(.*?)--(.*)$")


def expand_leanspine_node(node: str) -> list[str]:
    """Expand a manuscript range like 'MB7a--MB7d' or 'P05--P09' into individual
    node ids. Falls back to a single-element list if it isn't a recognized range.
    """
    m = RANGE_SPLIT.match(node)
    if not m:
        return [node]
    start, end = m.group(1), m.group(2)
    # trailing letter range: MB7a--MB7d
    lm = re.match(r"^(.*?)([a-z])$", start)
    rm = re.match(r"^(.*?)([a-z])$", end)
    if lm and rm and lm.group(1) == rm.group(1):
        prefix = lm.group(1)
        lo, hi = ord(lm.group(2)), ord(rm.group(2))
        if lo <= hi:
            return [f"{prefix}{chr(c)}" for c in range(lo, hi + 1)]
    # trailing digit range: P05--P09 / MB1--MB9
    lm = re.match(r"^([A-Za-z]+)(\d+)$", start)
    rm = re.match(r"^([A-Za-z]+)(\d+)$", end)
    if lm and rm and lm.group(1) == rm.group(1):
        prefix = lm.group(1)
        width = len(lm.group(2))
        lo, hi = int(lm.group(2)), int(rm.group(2))
        if lo <= hi:
            return [f"{prefix}{i:0{width}d}" for i in range(lo, hi + 1)]
    return [start, end]


def parse_leanspine_refs(chapters: list[Path]) -> list[LeanSpineRef]:
    refs: list[LeanSpineRef] = []
    for path in chapters:
        ch = chapter_id(path)
        text = strip_comments(path.read_text(encoding="utf-8", errors="replace"))
        for idx, line in enumerate(text.splitlines(), 1):
            for m in LEANSPINE.finditer(line):
                kind, node_raw, gloss = m.groups()
                node = node_raw.replace("\\_", "_").replace("\\", "")
                for expanded in expand_leanspine_node(node):
                    refs.append(
                        LeanSpineRef(chapter=ch, line=idx, kind=kind, node=expanded, gloss=gloss)
                    )
    return refs


def resolve_lean_alias(node: str, known_names: set[str]) -> str | None:
    """Resolve a short proof-spine id (P13, MB8, ...) to the actual Lean
    declaration name (P10_biq_upper_bound, MB1_estimator_soundness, ...) via
    exact match, then shortest-name prefix match (name == node or
    name.startswith(node + '_')).
    """
    if node in known_names:
        return node
    candidates = sorted(
        (n for n in known_names if n.startswith(node + "_") or n.startswith(node)),
        key=len,
    )
    return candidates[0] if candidates else None


def chapter_id(path: Path) -> str:
    m = re.match(r"ch(\d+)", path.stem)
    return f"ch{m.group(1)}" if m else path.stem


def strip_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        # remove full-line comments
        if line.strip().startswith("%"):
            continue
        # remove trailing comments (avoid \\)
        out = []
        i = 0
        while i < len(line):
            if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
                break
            out.append(line[i])
            i += 1
        lines.append("".join(out))
    return "\n".join(lines)


def normalize_sub(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\\mathrm\{([^}]+)\}", r"\1", s)
    s = re.sub(r"\\text\{([^}]+)\}", r"\1", s)
    return s.replace(" ", "").replace("/", "-")


def extract_symbols_from_math(math: str, _depth: int = 0) -> set[str]:
    """Heuristic symbol extraction from LaTeX math."""
    syms: set[str] = set()
    if _depth > 3:
        return syms

    # Compound time deltas: \Delta t_{\mathrm{corr}}
    for m in re.finditer(
        r"\\Delta\s*t_\{(?:\\(?:mathrm|text)\{)?([^}]+)\}?(?:\})?",
        math,
    ):
        syms.add(f"Delta_t_{{{normalize_sub(m.group(1))}}}")

    # Compound Delta C, Delta K patterns
    for m in re.finditer(
        r"\\Delta\s*([A-Za-z])_\{(?:\\(?:mathrm|text)\{)?([^}]+)\}?(?:\})?"
        r"|\\Delta\s*([A-Za-z])_\{([^}]+)\}",
        math,
    ):
        base = m.group(1) or m.group(3)
        sub = m.group(2) or m.group(4)
        if base and sub:
            syms.add(f"Delta_{base}_{{{normalize_sub(sub)}}}")

    for m in re.finditer(r"\\Delta\s*([A-Za-z])\b", math):
        syms.add(f"Delta_{m.group(1)}")

    # d/dt patterns on named quantities
    for m in re.finditer(
        r"\\frac\{d\s*([A-Za-z])_\{(?:\\(?:mathrm|text)\{)?([^}]+)\}?(?:\})?\}\{dt\}"
        r"|\\frac\{d\s*([A-Za-z])\}\{dt\}",
        math,
    ):
        if m.group(1):
            syms.add(f"d{m.group(1)}_{{{normalize_sub(m.group(2))}}}/dt")
        elif m.group(3):
            syms.add(f"d{m.group(3)}/dt")

    for m in re.finditer(
        r"\\frac\{d\^\{2\}\s*([A-Za-z])_\{(?:\\(?:mathrm|text)\{)?([^}]+)\}?(?:\})?\}\{dt\^\{2\}\}"
        r"|\\frac\{d\^\{2\}\s*([A-Za-z])\}\{dt\^\{2\}\}",
        math,
    ):
        if m.group(1):
            syms.add(f"d2_{m.group(1)}_{{{normalize_sub(m.group(2))}}}/dt2")
        elif m.group(3):
            syms.add(f"d2_{m.group(3)}/dt2")

    # \MI(...) → generic + inner tokens
    for m in re.finditer(r"\\MI\s*\(([^)]*)\)", math):
        syms.add("MI(·;·)")
        for part in re.split(r"[;,]", m.group(1)):
            part = part.strip()
            if part:
                syms.update(extract_symbols_from_math(part, _depth + 1))

    # \mathrm{Control}(A), \mathrm{CCI}(A), etc.
    for m in re.finditer(
        r"\\(?:mathrm|operatorname)\{([^}]+)\}\s*\(([^)]*)\)",
        math,
    ):
        name = normalize_sub(m.group(1))
        if name:
            syms.add(name)

    # Standalone \mathrm{...} / \mathcal{...} names
    for m in re.finditer(
        r"\\(?:mathrm|operatorname|mathcal|mathfrak|mathbb)\{([^}]+)\}",
        math,
    ):
        name = normalize_sub(m.group(1))
        if name and name not in SKIP_CMDS:
            syms.add(name)

    # Bare command symbols
    for m in re.finditer(r"\\([A-Za-z]+)", math):
        cmd = m.group(1)
        if cmd in GREEK:
            syms.add(cmd)
        elif cmd in ("CCI", "GLI", "DL", "MI", "Phi", "Gamma", "Delta"):
            if cmd == "Delta":
                continue  # handled above
            syms.add(cmd)

    # Subscripted identifiers
    for m in re.finditer(
        r"([A-Za-z])_\{(?:\\(?:mathrm|text)\{)?([^}]+)\}?(?:\})?"
        r"|([A-Za-z])_\{([^}]+)\}"
        r"|([A-Za-z])_([A-Za-z0-9]+)",
        math,
    ):
        base = m.group(1) or m.group(3) or m.group(5)
        sub = m.group(2) or m.group(4) or m.group(6)
        if base and sub:
            sub_n = normalize_sub(sub)
            # Skip if already captured as Delta_t_{...}
            tok = f"{base}_{{{sub_n}}}"
            if tok not in syms:
                syms.add(tok)

    # Superscripts
    for m in re.finditer(
        r"([A-Za-z])_\{([^}]+)\}\^\{([^}]+)\}"
        r"|([A-Za-z])\^\{([^}]+)\}"
        r"|([A-Za-z])\^([A-Za-z0-9])",
        math,
    ):
        if m.group(1):
            syms.add(f"{m.group(1)}_{{{normalize_sub(m.group(2))}}}^{{{normalize_sub(m.group(3))}}}")
        else:
            base = m.group(4) or m.group(6)
            sup = m.group(5) or m.group(7)
            if base and sup:
                syms.add(f"{base}^{{{normalize_sub(sup)}}}")

    # Multi-letter identifiers
    for m in re.finditer(
        r"(?<![A-Za-z])([A-Z][a-z]+(?:[A-Z][a-z]+)+)(?![A-Za-z])", math
    ):
        syms.add(m.group(1))

    if "RiskGap" in math:
        syms.add("RiskGap")
    if "SelfControlGap" in math:
        syms.add("SelfControlGap")
    if "ValueUpdateEnvelope" in math:
        syms.add("ValueUpdateEnvelope")

    noise = {
        "text", "mathrm", "operatorname", "mathcal", "mid", "left", "right",
        "cdot", "times", "label", "ref", "eqref", "bundle", "corr", "harm",
        "ctrl", "pred", "manip", "certified", "irreversible", "world", "raw",
        "trans", "value", "social", "succ", "self", "power", "proxy",
    }
    # Drop bare subscript words that duplicate C_{world} etc.
    syms -= noise

    return syms


def parse_chapter(
    path: Path,
    ch_owner: dict[str, str] | None = None,
    sec_owner: dict[str, str] | None = None,
) -> list[Formula]:
    """Parse one chapter file.

    `ch_owner` and `sec_owner`, if given, are mutated in place to map
    `ch:label` / `sec:label` -> the chapter id that defines that label (via
    `\\label{...}`), so that `\\ref{ch:...}` / `\\ref{sec:...}` found anywhere
    in the manuscript can later be resolved to a target chapter.
    """
    text = strip_comments(path.read_text(encoding="utf-8", errors="replace"))
    lines = text.splitlines()
    ch = chapter_id(path)
    formulas: list[Formula] = []

    if ch_owner is not None:
        for line in lines:
            for label in LABEL_CH.findall(line):
                ch_owner[label] = ch
    if sec_owner is not None:
        for line in lines:
            for label in LABEL_SEC.findall(line):
                sec_owner[label] = ch

    i = 0
    while i < len(lines):
        m_start = ENV_START.search(lines[i])
        if not m_start:
            i += 1
            continue
        env = m_start.group(1)
        start_line = i + 1
        block_lines = [lines[i]]
        i += 1
        depth = 1
        while i < len(lines) and depth > 0:
            if ENV_START.search(lines[i]):
                depth += 1
            if ENV_END.search(lines[i]):
                depth -= 1
            block_lines.append(lines[i])
            i += 1
        end_line = i
        block = "\n".join(block_lines)

        label_m = LABEL_EQ.search(block)
        if label_m:
            fid = label_m.group(1)
        else:
            fid = f"{ch}:unlabeled:{start_line}"

        refs = set(EQREF.findall(block))
        text_refs = set(TEXTREF.findall(block))
        syms = extract_symbols_from_math(block)

        formulas.append(
            Formula(
                fid=fid,
                chapter=ch,
                chapter_file=path.name,
                line_start=start_line,
                line_end=end_line,
                env=env,
                raw=block[:500],
                symbols=syms,
                refs=refs,
                text_refs=text_refs,
            )
        )

    # Also scan prose for \eqref / \ref{eq:...} (formula->formula edges) and
    # \ref{ch:...} / \ref{sec:...} (text-only cross-references, formerly
    # invisible to the graph) outside math blocks.
    for idx, line in enumerate(lines, 1):
        line_eq_refs = EQREF.findall(line)
        line_text_refs = TEXTREF.findall(line)
        if not line_eq_refs and not line_text_refs:
            continue
        prose_fid = f"{ch}:prose:{idx}"
        existing = next((f for f in formulas if f.fid == prose_fid), None)
        if not existing:
            formulas.append(
                Formula(
                    fid=prose_fid,
                    chapter=ch,
                    chapter_file=path.name,
                    line_start=idx,
                    line_end=idx,
                    env="prose",
                    raw=line.strip()[:200],
                    symbols=extract_symbols_from_math(line),
                    refs=set(line_eq_refs),
                    text_refs=set(line_text_refs),
                )
            )
        else:
            existing.refs.update(line_eq_refs)
            existing.text_refs.update(line_text_refs)

    return formulas


def dot_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def resolve_text_ref(ref: str, ch_owner: dict[str, str], sec_owner: dict[str, str]) -> str | None:
    """Resolve a \\ref{ch:...} or \\ref{sec:...} target to the chapter id that
    defines the corresponding \\label. Section labels resolve to their owning
    chapter (we do not model a separate node per section)."""
    if ref.startswith("ch:"):
        return ch_owner.get(ref)
    if ref.startswith("sec:"):
        return sec_owner.get(ref)
    return None


def graph_formula_nodes(all_formulas: list[Formula], detailed: bool) -> list[Formula]:
    """Formulas to emit as visible nodes in the reachability graph.

    Default (``detailed=False``): labeled display equations only (``eq:...``).
    The parser also creates ~400 ``chNN:unlabeled:LINE`` nodes (every
    unlabeled ``equation``/``align`` block) and ~430 ``chNN:prose:LINE`` nodes
    (one per line containing ``\\ref``/``\\eqref``). Emitting all of those
    made the SVG an unreadable hairball once text-ref edges were added — the
    reachability graph keeps the 166 labeled anchors and aggregates prose-level
    refs at chapter granularity instead.

    ``detailed=True`` retains every parsed node for line-level debugging.
    """
    if detailed:
        return all_formulas
    return [f for f in all_formulas if f.fid.startswith("eq:")]


def collect_chapter_text_ref_pairs(
    all_formulas: list[Formula],
    ch_owner: dict[str, str],
    sec_owner: dict[str, str],
) -> tuple[dict[str, set[str]], dict[str, set[str]], set[str]]:
    """Aggregate ``\\ref{ch:...}``/``\\ref{sec:...}`` by citing chapter.

    Returns ``(ch_to_ch, ch_to_unresolved, chapters_with_cites)`` where
    ``ch_to_ch[source][target]`` is the set of resolved target chapter ids
    cited from ``source``, and ``ch_to_unresolved[source]`` is unresolved ref
    labels.
    """
    ch_to_ch: dict[str, set[str]] = {}
    ch_to_unresolved: dict[str, set[str]] = {}
    chapters_with_cites: set[str] = set()
    for f in all_formulas:
        if not f.text_refs:
            continue
        chapters_with_cites.add(f.chapter)
        for ref in f.text_refs:
            target_ch = resolve_text_ref(ref, ch_owner, sec_owner)
            if target_ch is None:
                ch_to_unresolved.setdefault(f.chapter, set()).add(ref)
            else:
                ch_to_ch.setdefault(f.chapter, set()).add(target_ch)
    return ch_to_ch, ch_to_unresolved, chapters_with_cites


def collect_prose_eq_refs(
    all_formulas: list[Formula],
    labeled: list[Formula],
) -> dict[str, set[str]]:
    """Eq refs appearing only on prose/unlabeled lines (not on labeled eq nodes)."""
    labeled_refs: dict[str, set[str]] = {}
    for f in labeled:
        labeled_refs.setdefault(f.chapter, set()).update(f.refs)
    prose_refs: dict[str, set[str]] = {}
    for f in all_formulas:
        if f.fid.startswith("eq:"):
            continue
        for ref in f.refs:
            if ref not in labeled_refs.get(f.chapter, set()):
                prose_refs.setdefault(f.chapter, set()).add(ref)
    return prose_refs


def emit_aggregated_text_ref_edges(
    lines: list[str],
    all_formulas: list[Formula],
    ch_owner: dict[str, str],
    sec_owner: dict[str, str],
    known_fids: set[str],
) -> None:
    """Chapter-level text-ref and prose-eq-ref edges (reachability graph).

    One ``chcite:chNN`` hub per citing chapter instead of hundreds of
    ``chNN:prose:LINE`` spokes.
    """
    ch_to_ch, ch_to_unresolved, cite_chapters = collect_chapter_text_ref_pairs(
        all_formulas, ch_owner, sec_owner
    )
    labeled = [f for f in all_formulas if f.fid.startswith("eq:")]
    prose_eq = collect_prose_eq_refs(all_formulas, labeled)
    cite_chapters |= set(prose_eq)

    if not cite_chapters:
        return

    lines.append("  // Chapter-level citations (aggregated from prose/section \\\\ref lines)")
    emitted_chref: set[str] = set()
    emitted_chcite: set[str] = set()

    for src in sorted(cite_chapters, key=lambda c: int(c[2:]) if c[2:].isdigit() else 999):
        hub = f"chcite:{src}"
        if hub not in emitted_chcite:
            lines.append(
                f'  "{hub}" [shape=folder, style=filled, fillcolor="#fff7ed", '
                f'color="#92400e", label="{src}\\ncites"];'
            )
            emitted_chcite.add(hub)

        for tgt in sorted(ch_to_ch.get(src, set()), key=lambda c: int(c[2:]) if c[2:].isdigit() else 999):
            node = f"chref:{tgt}"
            if node not in emitted_chref:
                lines.append(
                    f'  "{node}" [shape=cds, style=filled, fillcolor="#fef3c7", '
                    f'color="#92400e", label="{tgt}"];'
                )
                emitted_chref.add(node)
            lines.append(f'  "{hub}" -> "{node}" [color="#d97706", style=dashed];')

        for ref in sorted(ch_to_unresolved.get(src, set())):
            node = f"textref:{ref}"
            if node not in emitted_chref:
                lines.append(
                    f'  "{node}" [shape=octagon, style=dashed, fillcolor="#fee2e2", '
                    f'label="{dot_escape(ref)}\\n(unresolved)"];'
                )
                emitted_chref.add(node)
            lines.append(f'  "{hub}" -> "{node}" [color="#d97706", style=dashed];')

        for ref in sorted(prose_eq.get(src, set())):
            if ref in known_fids:
                lines.append(f'  "{hub}" -> "{ref}" [color="#059669", style=dashed];')
            else:
                ghost = f"ghost:{ref}"
                if ghost not in known_fids:
                    lines.append(
                        f'  "{ghost}" [shape=octagon, style=dashed, fillcolor="#fee2e2", '
                        f'label="{dot_escape(ref)}\\n(external)"];'
                    )
                    known_fids.add(ghost)
                lines.append(f'  "{hub}" -> "{ghost}" [color="#dc2626", style=dashed];')


def emit_text_ref_edges(
    lines: list[str],
    all_formulas: list[Formula],
    ch_owner: dict[str, str],
    sec_owner: dict[str, str],
) -> None:
    """Append chapter/section text-reference nodes and edges to `lines` in
    place. These capture cross-references stated only in prose (e.g.
    "Chapter~\\ref{ch:foo}", "Section~\\ref{sec:bar-ch15}") that are the
    manuscript's dominant citation style but were previously invisible to the
    graph: no \\eqref exists for them, so no edge was ever recorded even
    though a human reader can see the dependency by reading the sentence.
    """
    emitted_chref: set[str] = set()
    lines.append("  // Text-only cross-reference (\\ref{ch:...} / \\ref{sec:...}, not \\eqref)")
    for f in all_formulas:
        for ref in sorted(f.text_refs):
            target_ch = resolve_text_ref(ref, ch_owner, sec_owner)
            if target_ch is None:
                node = f"textref:{ref}"
                if node not in emitted_chref:
                    lines.append(
                        f'  "{node}" [shape=octagon, style=dashed, fillcolor="#fee2e2", '
                        f'label="{dot_escape(ref)}\\n(unresolved)"];'
                    )
                    emitted_chref.add(node)
                lines.append(
                    f'  "{f.fid}" -> "{node}" [color="#d97706", style=dashed];'
                )
                continue
            node = f"chref:{target_ch}"
            if node not in emitted_chref:
                lines.append(
                    f'  "{node}" [shape=cds, style=filled, fillcolor="#fef3c7", '
                    f'color="#92400e", label="{target_ch}"];'
                )
                emitted_chref.add(node)
            # Only label the edge when it carries information beyond the edge
            # style itself (a specific sec: id) — a generic "text-ref" label
            # on every one of these edges would just be more label fog.
            if ref.startswith("sec:"):
                lines.append(
                    f'  "{f.fid}" -> "{node}" [color="#d97706", style=dashed, '
                    f'label="{dot_escape(ref)}", fontsize=6];'
                )
            else:
                lines.append(f'  "{f.fid}" -> "{node}" [color="#d97706", style=dashed];')


def build_dot(
    all_formulas: list[Formula],
    chapter_filter: str | None = None,
    ch_owner: dict[str, str] | None = None,
    sec_owner: dict[str, str] | None = None,
    detailed: bool = False,
) -> str:
    visible = graph_formula_nodes(all_formulas, detailed)
    if chapter_filter:
        visible = [f for f in visible if f.chapter == chapter_filter]

    graph_label = "Manuscript symbol→formula reachability"
    if detailed:
        graph_label += " (detailed: all unlabeled+prose nodes)"
    if chapter_filter:
        graph_label += f" ({chapter_filter})"

    lines = [
        "digraph SymbolFormulaGraph {",
        f'  graph [rankdir=LR, fontsize=10, label="{graph_label}", labelloc=t];',
        "  node [fontname=Helvetica];",
        "  edge [fontname=Helvetica, fontsize=8];",
        "",
    ]

    chapters = sorted({f.chapter for f in visible})

    # Per-chapter subgraphs
    for ch in chapters:
        ch_formulas = [f for f in visible if f.chapter == ch]
        lines.append(f"  subgraph cluster_{ch} {{")
        lines.append(f'    label="{ch}"; style=dashed; color="#92400e";')
        lines.append(f'    "{ch}_anchor" [shape=point, width=0.01, label=""];')
        for f in ch_formulas:
            if f.env == "prose":
                shape, color = "note", "#f3f4f6"
            elif ":unlabeled:" in f.fid:
                shape, color = "component", "#ede9fe"
            else:
                shape, color = "box", "#d1fae5"
            # Reachability graph: show eq label only, not internal id noise
            if f.fid.startswith("eq:"):
                label = f.fid[3:].replace("-", "\\n")
            else:
                label = f.fid.replace(":", "\\n")
                if ":unlabeled:" in f.fid:
                    label += f"\\nL{f.line_start}"
            lines.append(
                f'    "{f.fid}" [shape={shape}, style=filled, fillcolor="{color}", '
                f'label="{dot_escape(label)}"];'
            )
            lines.append(f'    "{ch}_anchor" -> "{f.fid}" [style=invis];')
        lines.append("  }")
        lines.append("")

    all_syms: set[str] = set()
    for f in visible:
        all_syms |= f.symbols

    lines.append("  subgraph cluster_symbols {")
    lines.append('    label="Symbols"; style=dotted; color="#2c5282";')
    for sym in sorted(all_syms, key=lambda s: s.lower()):
        sid = f"sym:{sym}"
        lines.append(
            f'    "{sid}" [shape=ellipse, style=filled, fillcolor="#e8f4fc", '
            f'label="{dot_escape(sym)}"];'
        )
    lines.append("  }")
    lines.append("")

    known_fids = {f.fid for f in visible}

    lines.append("  // Symbol used in formula (thinned: this is the highest-count, least-traced edge type)")
    lines.append('  edge [penwidth=0.4, arrowsize=0.4];')
    for f in visible:
        for sym in sorted(f.symbols):
            lines.append(f'  "sym:{sym}" -> "{f.fid}" [color="#2c528266"];')
    lines.append('  edge [penwidth=1.0, arrowsize=1.0];')

    lines.append("  // Formula references formula")
    for f in visible:
        for ref in sorted(f.refs):
            if ref in known_fids:
                lines.append(f'  "{f.fid}" -> "{ref}" [color="#059669"];')
            else:
                ghost = f"ghost:{ref}"
                if ghost not in known_fids:
                    lines.append(
                        f'  "{ghost}" [shape=octagon, style=dashed, fillcolor="#fee2e2", '
                        f'label="{dot_escape(ref)}\\n(external)"];'
                    )
                    known_fids.add(ghost)
                lines.append(
                    f'  "{f.fid}" -> "{ghost}" [color="#dc2626", style=dashed];'
                )

    if ch_owner is not None and sec_owner is not None:
        if detailed:
            emit_text_ref_edges(lines, all_formulas, ch_owner, sec_owner)
        else:
            emit_aggregated_text_ref_edges(
                lines, all_formulas, ch_owner, sec_owner, known_fids
            )

    lines.append("}")
    return "\n".join(lines)


def build_lean_dot(decls: list[LeanDecl], file_imports: dict[str, set[str]]) -> str:
    lines = [
        "digraph LeanDependencyGraph {",
        '  graph [rankdir=LR, fontsize=10, label="Lean spine: declaration-level dependencies (parsed from formal/AlignmentProofSpine/*.lean)", labelloc=t];',
        "  node [fontname=Helvetica];",
        "  edge [fontname=Helvetica, fontsize=8];",
        "",
    ]

    kind_color = {
        "theorem": "#d1fae5",
        "lemma": "#d1fae5",
        "def": "#e0e7ff",
        "structure": "#fef3c7",
        "axiom": "#fee2e2",
        "inductive": "#fce7f3",
        "instance": "#e0e7ff",
    }

    by_file: dict[str, list[LeanDecl]] = {}
    for d in decls:
        by_file.setdefault(d.file, []).append(d)

    for f, ds in sorted(by_file.items()):
        cluster = re.sub(r"[^A-Za-z0-9]", "_", f)
        lines.append(f"  subgraph cluster_{cluster} {{")
        lines.append(f'    label="{f}"; style=dashed; color="#374151";')
        for d in ds:
            color = kind_color.get(d.kind, "#f3f4f6")
            is_bridge = d.name.startswith("MB") or bool(re.match(r"MB\d+", d.name))
            shape = "octagon" if (d.kind == "axiom" and is_bridge) else "box"
            lines.append(
                f'    "lean:{d.name}" [shape={shape}, style=filled, fillcolor="{color}", '
                f'label="{dot_escape(d.name)}\\n({d.kind})\\nL{d.line_start}"];'
            )
        lines.append("  }")
    lines.append("")

    # Unlabeled: 2751 `uses` edges all carrying the identical fixed label
    # rendered as a dense fog of repeated text at this node count; color
    # already identifies the edge type (see graphs/README.md legend).
    lines.append("  // Declaration uses declaration (proof-term / signature reference)")
    for d in decls:
        for used in sorted(d.uses):
            lines.append(f'  "lean:{d.name}" -> "lean:{used}" [color="#059669"];')

    lines.append("}")
    return "\n".join(lines)


def build_combined_dot(
    all_formulas: list[Formula],
    decls: list[LeanDecl],
    leanspine_refs: list[LeanSpineRef],
    ch_owner: dict[str, str] | None = None,
    sec_owner: dict[str, str] | None = None,
    detailed: bool = False,
) -> str:
    visible = graph_formula_nodes(all_formulas, detailed)
    lines = [
        "digraph ManuscriptLeanCrosswalk {",
        '  graph [rankdir=LR, fontsize=10, label="Symbol -> formula -> \\\\leanspine -> Lean declaration reachability", labelloc=t];',
        "  node [fontname=Helvetica];",
        "  edge [fontname=Helvetica, fontsize=8];",
        "",
    ]

    known_fids = {f.fid for f in visible}
    known_lean = {d.name for d in decls}

    all_syms: set[str] = set()
    for f in visible:
        all_syms |= f.symbols

    lines.append("  subgraph cluster_symbols {")
    lines.append('    label="Symbols"; style=dotted; color="#2c5282";')
    for sym in sorted(all_syms, key=lambda s: s.lower()):
        lines.append(
            f'    "sym:{sym}" [shape=ellipse, style=filled, fillcolor="#e8f4fc", '
            f'label="{dot_escape(sym)}"];'
        )
    lines.append("  }")
    lines.append("")

    lines.append("  subgraph cluster_manuscript {")
    lines.append('    label="Manuscript formulas (labeled eq only)"; style=dashed; color="#92400e";')
    for f in visible:
        shape, color = "box", "#d1fae5"
        label = f.fid[3:].replace("-", "\\n") if f.fid.startswith("eq:") else f.fid.replace(":", "\\n")
        lines.append(
            f'    "{f.fid}" [shape={shape}, style=filled, fillcolor="{color}", '
            f'label="{dot_escape(label)}"];'
        )
    lines.append("  }")
    lines.append("")

    lines.append("  subgraph cluster_leanspine {")
    lines.append('    label="\\\\leanspine anchors"; style=dotted; color="#7c3aed";')
    for r in leanspine_refs:
        aid = f"leanspine:{r.chapter}:{r.line}"
        lines.append(
            f'    "{aid}" [shape=diamond, style=filled, fillcolor="#ede9fe", '
            f'label="{r.chapter}\\nL{r.line}\\n({r.kind})"];'
        )
    lines.append("  }")
    lines.append("")

    lines.append("  subgraph cluster_lean {")
    lines.append('    label="Lean declarations"; style=solid; color="#374151";')
    for d in decls:
        is_bridge = bool(re.match(r"MB\d+", d.name))
        shape = "octagon" if (d.kind == "axiom" and is_bridge) else "box"
        color = "#fee2e2" if is_bridge else "#e0e7ff"
        lines.append(
            f'    "lean:{d.name}" [shape={shape}, style=filled, fillcolor="{color}", '
            f'label="{dot_escape(d.name)}\\n({d.kind})"];'
        )
    lines.append("  }")
    lines.append("")

    lines.append("  // Symbol -> formula (thinned/unlabeled: highest-count, least-traced edge type)")
    lines.append('  edge [penwidth=0.4, arrowsize=0.4];')
    for f in visible:
        for sym in sorted(f.symbols):
            lines.append(f'  "sym:{sym}" -> "{f.fid}" [color="#2c528266"];')
    lines.append('  edge [penwidth=1.0, arrowsize=1.0];')

    lines.append("  // Formula -> formula")
    for f in visible:
        for ref in sorted(f.refs):
            if ref in known_fids:
                lines.append(f'  "{f.fid}" -> "{ref}" [color="#059669"];')

    lines.append("  // Manuscript formula -> leanspine anchor (nearest labeled eq before anchor line)")
    for r in leanspine_refs:
        aid = f"leanspine:{r.chapter}:{r.line}"
        candidates = [
            f for f in visible
            if f.chapter == r.chapter and f.line_start <= r.line
        ]
        if candidates:
            nearest = max(candidates, key=lambda f: f.line_start)
            lines.append(f'  "{nearest.fid}" -> "{aid}" [color="#7c3aed", style=dotted, label="near"];')
        lines.append(f'  "{r.chapter}" [shape=box, style=filled, fillcolor="#fef3c7", color="#92400e", label="{r.chapter}"];')
        lines.append(f'  "{r.chapter}" -> "{aid}" [color="#92400e", label="chapter"];')

    lines.append("  // leanspine anchor -> Lean declaration (crosswalk edge; resolves short")
    lines.append("  // proof-spine ids like P13/MB8 to their full Lean declaration name)")
    for r in leanspine_refs:
        aid = f"leanspine:{r.chapter}:{r.line}"
        resolved = resolve_lean_alias(r.node, known_lean)
        target_name = resolved if resolved else r.node
        target = f"lean:{target_name}"
        if not resolved:
            lines.append(
                f'  "{target}" [shape=octagon, style=dashed, fillcolor="#fee2e2", '
                f'label="{dot_escape(r.node)}\\n(unresolved)"];'
            )
        lines.append(f'  "{aid}" -> "{target}" [color="#7c3aed", label="{r.kind}"];')

    lines.append("  // Lean declaration -> Lean declaration (deep dependency chain)")
    for d in decls:
        for used in sorted(d.uses):
            lines.append(f'  "lean:{d.name}" -> "lean:{used}" [color="#059669"];')

    if ch_owner is not None and sec_owner is not None:
        if detailed:
            emit_text_ref_edges(lines, all_formulas, ch_owner, sec_owner)
        else:
            emit_aggregated_text_ref_edges(
                lines, all_formulas, ch_owner, sec_owner, known_fids
            )

    lines.append("}")
    return "\n".join(lines)


def build_coverage_md(
    all_formulas: list[Formula],
    decls: list[LeanDecl] | None = None,
    leanspine_refs: list[LeanSpineRef] | None = None,
    ch_owner: dict[str, str] | None = None,
    sec_owner: dict[str, str] | None = None,
) -> str:
    by_ch: dict[str, list[Formula]] = {}
    for f in all_formulas:
        by_ch.setdefault(f.chapter, []).append(f)

    sym_to_formulas: dict[str, list[str]] = {}
    for f in all_formulas:
        for s in f.symbols:
            sym_to_formulas.setdefault(s, []).append(f.fid)

    lines = [
        "# Symbol–Formula Coverage (generated)",
        "",
        f"Generated by `scripts/extract_symbol_formula_graph.py`.",
        f"Graphviz: `metadata/symbol-census/graphs/symbol-formula-graph.dot`",
        "",
        "## Summary",
        "",
        f"- Chapters: {len(by_ch)}",
        f"- Formulas (labeled + unlabeled + prose refs): {len(all_formulas)}",
        f"- Unique symbols extracted: {len(sym_to_formulas)}",
        "",
        "## Per-chapter formula count",
        "",
        "| Chapter | Formulas | Labeled | Symbols |",
        "|---------|----------|---------|---------|",
    ]
    for ch in sorted(by_ch, key=lambda c: int(c[2:]) if c[2:].isdigit() else 999):
        fs = by_ch[ch]
        labeled = sum(1 for f in fs if f.fid.startswith("eq:"))
        syms = len({s for f in fs for s in f.symbols})
        lines.append(f"| {ch} | {len(fs)} | {labeled} | {syms} |")

    lines.extend(["", "## Per-chapter symbol → formula map", ""])
    for ch in sorted(by_ch, key=lambda c: int(c[2:]) if c[2:].isdigit() else 999):
        fs = by_ch[ch]
        ch_syms: dict[str, set[str]] = {}
        for f in fs:
            for s in f.symbols:
                ch_syms.setdefault(s, set()).add(f.fid)
        lines.append(f"### {ch} ({by_ch[ch][0].chapter_file})")
        lines.append("")
        lines.append("| Symbol | Formulas |")
        lines.append("|--------|----------|")
        for sym in sorted(ch_syms, key=lambda s: s.lower()):
            fids = ", ".join(f"`{x}`" for x in sorted(ch_syms[sym]))
            lines.append(f"| `{sym}` | {fids} |")
        lines.append("")

    if decls is not None and leanspine_refs is not None:
        by_ch_leanspine: dict[str, list[LeanSpineRef]] = {}
        for r in leanspine_refs:
            by_ch_leanspine.setdefault(r.chapter, []).append(r)

        known_lean = {d.name for d in decls}
        unresolved = sorted({
            r.node for r in leanspine_refs
            if resolve_lean_alias(r.node, known_lean) is None
        })
        chapters_with_leanspine = set(by_ch_leanspine)
        chapters_without_leanspine = sorted(
            set(by_ch) - chapters_with_leanspine,
            key=lambda c: int(c[2:]) if c[2:].isdigit() else 999,
        )

        lines.extend([
            "## Lean spine coverage",
            "",
            f"- Lean declarations parsed: {len(decls)} (from `formal/AlignmentProofSpine/**/*.lean`)",
            f"- `\\leanspine{{}}` crosswalk anchors in manuscript: {len(leanspine_refs)}",
            f"- Chapters with at least one `\\leanspine{{}}` anchor: {len(chapters_with_leanspine)}",
            f"- Chapters with **no** `\\leanspine{{}}` anchor: {len(chapters_without_leanspine)} "
            f"({', '.join(chapters_without_leanspine)})",
            f"- `\\leanspine{{}}` nodes that do not resolve to a parsed Lean declaration: {len(unresolved)}",
            "",
        ])
        if unresolved:
            lines.append("Unresolved leanspine targets (name mismatch, or declared via a macro/field the parser " \
                          "does not expand — check manually):")
            lines.append("")
            for u in unresolved:
                lines.append(f"- `{u}`")
            lines.append("")

        lines.extend(["### `\\leanspine{}` anchors by chapter", "", "| Chapter | Line | Kind | Lean node | Resolves to |", "|---|---|---|---|---|"])
        for r in sorted(leanspine_refs, key=lambda r: (int(r.chapter[2:]) if r.chapter[2:].isdigit() else 999, r.line)):
            resolved = resolve_lean_alias(r.node, known_lean)
            resolved_s = f"`{resolved}`" if resolved else "**unresolved**"
            lines.append(f"| {r.chapter} | {r.line} | {r.kind} | `{r.node}` | {resolved_s} |")
        lines.append("")

    if ch_owner is not None and sec_owner is not None:
        text_ref_count = sum(len(f.text_refs) for f in all_formulas)
        resolved = 0
        unresolved_refs: set[str] = set()
        for f in all_formulas:
            for ref in f.text_refs:
                if resolve_text_ref(ref, ch_owner, sec_owner) is not None:
                    resolved += 1
                else:
                    unresolved_refs.add(ref)
        lines.extend([
            "## Text cross-references (`\\ref{ch:...}` / `\\ref{sec:...}`, not `\\eqref`)",
            "",
            "The manuscript's dominant citation style is chapter/section-level prose "
            "(e.g. \"Chapter~\\ref{ch:foo}\", \"Section~\\ref{sec:bar-ch15}\"), not "
            "per-equation `\\eqref`. These are now extracted as `text-ref` edges "
            "(dashed amber: `chcite:chNN` hub → `chref:chMM` target in the default "
            "reachability graph; per-line `chNN:prose:LINE` nodes only in "
            "`symbol-formula-graph-detailed.dot` with `--detailed`) in addition to the "
            "green `ref` edges for `\\eqref{eq:...}`.",
            "",
            f"- `\\ref{{ch:...}}` / `\\ref{{sec:...}}` occurrences found: {text_ref_count}",
            f"- Resolved to a known chapter: {resolved}",
            f"- Unresolved (label not found in any parsed chapter): {len(unresolved_refs)}",
            "",
        ])
        if unresolved_refs:
            lines.append("Unresolved text-ref targets:")
            lines.append("")
            for u in sorted(unresolved_refs):
                lines.append(f"- `{u}`")
            lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "metadata" / "symbol-census" / "graphs" / "symbol-formula-graph.dot",
    )
    parser.add_argument(
        "--coverage",
        type=Path,
        default=ROOT / "metadata" / "symbol-census" / "symbol-formula-coverage.md",
    )
    parser.add_argument(
        "--chapter",
        type=str,
        default=None,
        help="Emit subgraph for one chapter only (e.g. ch14)",
    )
    parser.add_argument(
        "--detailed",
        action="store_true",
        help="Also emit symbol-formula-graph-detailed.dot with every unlabeled/prose node",
    )
    args = parser.parse_args()

    paths = sorted(CHAPTERS_DIR.glob("ch*.tex"))
    all_formulas: list[Formula] = []
    ch_owner: dict[str, str] = {}
    sec_owner: dict[str, str] = {}
    for p in paths:
        all_formulas.extend(parse_chapter(p, ch_owner=ch_owner, sec_owner=sec_owner))

    # Full graph uses all formulas; resolve refs globally
    full_fids = {f.fid for f in all_formulas}
    for f in all_formulas:
        for ref in list(f.refs):
            if ref not in full_fids:
                pass  # ghost nodes added in build_dot

    if args.chapter:
        dot = build_dot(
            all_formulas,
            chapter_filter=args.chapter,
            ch_owner=ch_owner,
            sec_owner=sec_owner,
        )
    else:
        dot = build_dot(all_formulas, ch_owner=ch_owner, sec_owner=sec_owner)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(dot, encoding="utf-8")

    if args.detailed and not args.chapter:
        detailed_path = args.out.with_name("symbol-formula-graph-detailed.dot")
        detailed_path.write_text(
            build_dot(
                all_formulas,
                ch_owner=ch_owner,
                sec_owner=sec_owner,
                detailed=True,
            ),
            encoding="utf-8",
        )
        print(f"Wrote {detailed_path}")

    # Lean spine layer: parses formal/AlignmentProofSpine/**/*.lean for
    # declaration-level dependencies, and chapters/*.tex for \leanspine{}
    # crosswalk anchors. Without this, symbols/formulas only chain through
    # \eqref/\ref{eq:...} (rare — the manuscript mostly cross-references at
    # chapter/section granularity), so chains look artificially short and no
    # Lean node ever appears, even though Lean's import/proof-term graph is
    # far deeper.
    print("Parsing Lean spine...")
    decls, file_imports = parse_lean_files(LEAN_DIR)
    leanspine_refs = parse_leanspine_refs(paths)
    print(f"  {len(decls)} Lean declarations across {len(file_imports)} files")
    print(f"  {len(leanspine_refs)} \\leanspine{{}} crosswalk anchors in manuscript")

    lean_dot = build_lean_dot(decls, file_imports)
    lean_path = args.out.with_name("lean-dependency-graph.dot")
    lean_path.write_text(lean_dot, encoding="utf-8")
    print(f"Wrote {lean_path}")

    combined_dot = build_combined_dot(all_formulas, decls, leanspine_refs, ch_owner=ch_owner, sec_owner=sec_owner)
    combined_path = args.out.with_name("manuscript-lean-crosswalk-graph.dot")
    combined_path.write_text(combined_dot, encoding="utf-8")
    print(f"Wrote {combined_path}")

    md = build_coverage_md(all_formulas, decls, leanspine_refs, ch_owner=ch_owner, sec_owner=sec_owner)
    args.coverage.write_text(md, encoding="utf-8")

    # Chapter-filtered companion graph
    if not args.chapter:
        ch14_dot = build_dot(all_formulas, chapter_filter="ch14", ch_owner=ch_owner, sec_owner=sec_owner)
        ch14_path = args.out.with_name("symbol-formula-graph-ch14.dot")
        ch14_path.write_text(ch14_dot, encoding="utf-8")
        print(f"Wrote {ch14_path}")

    visible_count = len(graph_formula_nodes(all_formulas, detailed=False))
    print(f"Wrote {args.out} ({visible_count} labeled-eq nodes in reachability graph; {len(all_formulas)} parsed total)")
    print(f"Wrote {args.coverage}")


if __name__ == "__main__":
    main()
