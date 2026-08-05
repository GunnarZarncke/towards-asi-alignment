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
import sys
import textwrap
from collections import defaultdict
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

# \symboldef / \symbolref{math} or [canonical-id]{math} — brace-balanced scan in helpers below.
SYMBOLDEF_CMD = "\\symboldef"
SYMBOLREF_CMD = "\\symbolref"

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
    "MI", "DL", "CCI", "Correctable", "leanspine", "symboldef", "symbolref",
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
    defined_symbols: set[str] = field(default_factory=set)
    used_symbols: set[str] = field(default_factory=set)
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


@dataclass
class SymbolDef:
    """One \\symboldef[canonical-id]{math} explicit definition site."""

    chapter: str
    line: int
    sym: str  # canonical symbol id (notation.md tokens)
    math_raw: str
    chapter_file: str

    @property
    def fid(self) -> str:
        return f"symdef:{self.chapter}:{self.line}"

    def as_formula(self) -> Formula:
        return Formula(
            fid=self.fid,
            chapter=self.chapter,
            chapter_file=self.chapter_file,
            line_start=self.line,
            line_end=self.line,
            env="symboldef",
            raw=self.math_raw[:200],
            symbols={self.sym},
            defined_symbols={self.sym},
            used_symbols=set(),
        )


@dataclass
class SymbolRef:
    """One \\symbolref[canonical-id]{math} explicit use site."""

    chapter: str
    line: int
    sym: str
    math_raw: str
    chapter_file: str

    @property
    def fid(self) -> str:
        return f"symref:{self.chapter}:{self.line}"

    def as_formula(self) -> Formula:
        return Formula(
            fid=self.fid,
            chapter=self.chapter,
            chapter_file=self.chapter_file,
            line_start=self.line,
            line_end=self.line,
            env="symbolref",
            raw=self.math_raw[:200],
            symbols={self.sym},
            defined_symbols=set(),
            used_symbols={self.sym},
        )


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


def _parse_braced_arg(text: str, open_brace: int) -> tuple[str, int] | None:
    """Return (inner, index after closing ``}``) when ``text[open_brace] == '{'``."""
    if open_brace >= len(text) or text[open_brace] != "{":
        return None
    depth = 0
    inner_start = open_brace + 1
    for i in range(open_brace, len(text)):
        if text[i] == "{":
            depth += 1
            if depth == 1:
                inner_start = i + 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[inner_start:i], i + 1
    return None


def _iter_symbol_markers(text: str, cmd: str) -> list[tuple[str | None, str, int]]:
    """Yield (optional canonical id, math inner, start index) for ``\\symboldef`` / ``\\symbolref``."""
    found: list[tuple[str | None, str, int]] = []
    i = 0
    while True:
        j = text.find(cmd, i)
        if j == -1:
            break
        k = j + len(cmd)
        explicit: str | None = None
        if k < len(text) and text[k] == "[":
            end = text.find("]", k)
            if end == -1:
                i = j + 1
                continue
            explicit = text[k + 1 : end]
            k = end + 1
        if k >= len(text) or text[k] != "{":
            i = j + 1
            continue
        parsed = _parse_braced_arg(text, k)
        if not parsed:
            i = j + 1
            continue
        inner, after = parsed
        found.append((explicit, inner, j))
        i = after
    return found


def _iter_symboldefs(text: str) -> list[tuple[str | None, str, int]]:
    return _iter_symbol_markers(text, SYMBOLDEF_CMD)


def _unwrap_symbol_marker(math: str, cmd: str) -> str:
    """Replace \\cmd[...]{inner} with inner for symbol extraction."""
    out: list[str] = []
    i = 0
    text = math
    while i < len(text):
        j = text.find(cmd, i)
        if j == -1:
            out.append(text[i:])
            break
        out.append(text[i:j])
        k = j + len(cmd)
        if k < len(text) and text[k] == "[":
            end = text.find("]", k)
            if end == -1:
                out.append(text[j])
                i = j + 1
                continue
            k = end + 1
        if k < len(text) and text[k] == "{":
            parsed = _parse_braced_arg(text, k)
            if parsed:
                inner, after = parsed
                out.append(inner)
                i = after
                continue
        out.append(text[j])
        i = j + 1
    return "".join(out)


def _unwrap_symbol_anchors(math: str) -> str:
    """Strip \\symboldef and \\symbolref wrappers before symbol extraction."""
    s = _unwrap_symbol_marker(math, SYMBOLDEF_CMD)
    return _unwrap_symbol_marker(s, SYMBOLREF_CMD)


def _unwrap_symboldef(math: str) -> str:
    """Replace \\symboldef[...]{inner} with inner for symbol extraction."""
    return _unwrap_symbol_anchors(math)


def canonical_symbol_id(explicit: str | None, math: str) -> str | None:
    """Resolve \\symboldef optional canonical id or infer from math."""
    if explicit is not None and explicit.strip():
        return normalize_sub(explicit.strip())

    syms = extract_symbols_from_math(_unwrap_symboldef(math))
    if not syms:
        return None

    for pref in ("RiskGap", "SelfControlGap", "ValueUpdateEnvelope", "Fit_E"):
        if pref in syms:
            return pref

    bare = {s for s in syms if "{" not in s and "_" not in s}
    if len(bare) == 1:
        return next(iter(bare))

    for base in ("CCI", "Control", "BIQ", "GLI", "ICI", "epsilon"):
        if base in syms:
            return base

    # Projection subscripts: CCI_{lambda} → CCI when vector/scalar family matches.
    for s in syms:
        m = re.match(r"^([A-Za-z]+)_\{([^}]+)\}$", s)
        if m and m.group(1) in ("CCI", "BIQ", "GLI", "ICI"):
            return m.group(1)

    return sorted(syms, key=lambda x: (len(x), x.lower()))[0]


def parse_symboldefs(chapters: list[Path]) -> list[SymbolDef]:
    """Collect \\symboldef[canonical-id]{math} anchors from manuscript chapters."""
    defs: list[SymbolDef] = []
    for path in chapters:
        ch = chapter_id(path)
        text = strip_comments(path.read_text(encoding="utf-8", errors="replace"))
        for idx, line in enumerate(text.splitlines(), 1):
            for explicit, math_raw, _pos in _iter_symboldefs(line):
                sym = canonical_symbol_id(explicit, math_raw)
                if not sym:
                    continue
                defs.append(
                    SymbolDef(
                        chapter=ch,
                        line=idx,
                        sym=sym,
                        math_raw=math_raw.strip(),
                        chapter_file=path.name,
                    )
                )
    return defs


def parse_symbolrefs(chapters: list[Path]) -> list[SymbolRef]:
    """Collect \\symbolref[canonical-id]{math} use anchors from manuscript chapters."""
    refs: list[SymbolRef] = []
    for path in chapters:
        ch = chapter_id(path)
        text = strip_comments(path.read_text(encoding="utf-8", errors="replace"))
        for idx, line in enumerate(text.splitlines(), 1):
            for explicit, math_raw, _pos in _iter_symbol_markers(line, SYMBOLREF_CMD):
                sym = canonical_symbol_id(explicit, math_raw)
                if not sym:
                    continue
                refs.append(
                    SymbolRef(
                        chapter=ch,
                        line=idx,
                        sym=sym,
                        math_raw=math_raw.strip(),
                        chapter_file=path.name,
                    )
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


def normalize_chain_sym_id(sym: str) -> str:
    """Unify ``\\symboldef`` ids with extractor tokens (e.g. ``D_{G}`` → ``D_G``)."""
    sym = sym.strip()
    m = re.match(r"^([A-Za-z]+)_\{([^}]+)\}$", sym)
    if m:
        return f"{m.group(1)}_{normalize_sub(m.group(2))}"
    return sym


def _strip_math_env(block: str) -> str:
    s = block
    s = re.sub(r"\\begin\{[^}]+\}", "", s)
    s = re.sub(r"\\end\{[^}]+\}", "", s)
    s = re.sub(r"\\label\{[^}]+\}", "", s)
    s = re.sub(r"\\tag\{[^}]+\}", "", s)
    return s


def _split_depth0(s: str, sep: str) -> list[str]:
    parts: list[str] = []
    depth = 0
    start = 0
    for i, c in enumerate(s):
        if c == "{":
            depth += 1
        elif c == "}":
            depth = max(0, depth - 1)
        elif c == sep and depth == 0:
            parts.append(s[start:i])
            start = i + 1
    parts.append(s[start:])
    return parts


def _split_first_def_relation(line: str) -> tuple[str, str] | None:
    """Split on first top-level definitional relation (``=``, ``\\coloneqq``, etc.)."""
    depth = 0
    i = 0
    relations = ("\\coloneqq", "\\approx", "\\geq", "\\leq", "=")
    while i < len(line):
        c = line[i]
        if c == "{":
            depth += 1
            i += 1
            continue
        if c == "}":
            depth = max(0, depth - 1)
            i += 1
            continue
        if depth == 0:
            for token in relations:
                if line.startswith(token, i):
                    return line[:i].strip(), line[i + len(token) :].strip()
        i += 1
    return None


def _split_first_equals(line: str) -> tuple[str, str] | None:
    """Backward-compatible wrapper."""
    return _split_first_def_relation(line)


def _tuple_list_defined(rhs: str) -> set[str]:
    """Symbols in RHS of ``X = (a, b, c)`` or ``X = \\left(a, b, c\\right)``."""
    rhs = rhs.strip().rstrip(".")
    inner: str | None = None
    m = re.match(r"\\left\((.*)\\right\)\s*\.?$", rhs, re.DOTALL)
    if m:
        inner = m.group(1)
    elif rhs.startswith("("):
        depth = 0
        close = -1
        for i, c in enumerate(rhs):
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
                if depth == 0:
                    close = i
                    break
        if close == len(rhs.rstrip()) - 1:
            inner = rhs[1:close]
    if inner is None:
        return set()
    out: set[str] = set()
    for part in _split_depth0(inner, ","):
        part = part.strip()
        if part:
            out.update(extract_symbols_from_math(part))
    return out


def _symboldef_canonical_ids(fragment: str) -> set[str]:
    """Canonical ids from ``\\symboldef[...]{...}`` in a math fragment."""
    ids: set[str] = set()
    for explicit, math_raw, _pos in _iter_symboldefs(fragment):
        cid = canonical_symbol_id(explicit, math_raw)
        if cid:
            ids.add(normalize_chain_sym_id(cid))
    return ids


def _apply_symboldef_lhs_overrides(line_defined: set[str], lhs: str) -> set[str]:
    """Prefer ``\\symboldef`` canonical ids on the LHS over heuristic subscript tokens."""
    symdef_ids = _symboldef_canonical_ids(lhs)
    if not symdef_ids:
        return line_defined
    out = line_defined | symdef_ids
    for sid in symdef_ids:
        if "_" in sid:
            out.discard(sid.split("_", 1)[1])
        base = sid.split("_", 1)[0]
        out = {s for s in out if not (s != sid and s.startswith(f"{base}_"))}
    return out


def _symbolref_canonical_ids(fragment: str) -> set[str]:
    """Canonical ids from ``\\symbolref[...]{...}`` in a math fragment."""
    ids: set[str] = set()
    for explicit, math_raw, _pos in _iter_symbol_markers(fragment, SYMBOLREF_CMD):
        cid = canonical_symbol_id(explicit, math_raw)
        if cid:
            ids.add(normalize_chain_sym_id(cid))
    return ids


def split_defined_used_symbols(block: str) -> tuple[set[str], set[str]]:
    """Split display-math symbols into defined (LHS of ``='') vs used (RHS / no ``='')."""
    body = _strip_math_env(block)
    body = re.sub(r"\s*\n\s*", " ", body)
    defined: set[str] = set()
    used: set[str] = set()

    for segment in re.split(r"\\\\", body):
        segment = segment.strip().rstrip(",")
        if not segment:
            continue

        if "&" in segment:
            parts = _split_depth0(segment, "&")
            lhs = parts[0].strip()
            rhs = parts[-1].strip() if len(parts) > 1 else ""
            if rhs.startswith("="):
                rhs = rhs[1:].strip()
        else:
            eq_parts = _split_first_def_relation(segment)
            if eq_parts is None:
                used.update(extract_symbols_from_math(segment))
                continue
            lhs, rhs = eq_parts

        line_defined = extract_symbols_from_math(lhs) if lhs else set()
        line_defined = _apply_symboldef_lhs_overrides(line_defined, lhs)
        line_used = extract_symbols_from_math(rhs) if rhs else set()
        if rhs:
            line_defined |= _tuple_list_defined(rhs)

        defined |= line_defined
        used |= line_used - line_defined

    return defined, used


def extract_symbols_from_math(math: str, _depth: int = 0) -> set[str]:
    """Heuristic symbol extraction from LaTeX math."""
    math = _unwrap_symboldef(math)
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

    # Font-wrapped identifiers with sub/superscript: \mathbb{B}_{race} → B_{race};
    # \mathcal{C}_t → mathcal_C_{t} (distinct from bare correction C_t).
    font_sub_spans: list[tuple[int, int]] = []
    for m in re.finditer(
        r"\\(mathrm|operatorname|mathcal|mathfrak|mathbb)\{([A-Za-z])\}"
        r"(?:_\{(?:\\(?:mathrm|text)\{)?([^}]+)\}?(?:\})?"
        r"|_\{([^}]+)\}"
        r"|_([A-Za-z0-9]+)"
        r"|\^\{(?:\\(?:mathrm|text)\{)?([^}]+)\}?(?:\})?"
        r"|\^\{([^}]+)\}"
        r"|\^([A-Za-z0-9]))",
        math,
    ):
        font = m.group(1)
        base = m.group(2)
        sub = m.group(3) or m.group(4) or m.group(5)
        sup = m.group(6) or m.group(7) or m.group(8)
        if sub:
            sid = f"{base}_{{{normalize_sub(sub)}}}"
            if font in ("mathcal", "mathfrak"):
                sid = f"{font}_{sid}"
            syms.add(sid)
        elif sup:
            sid = f"{base}^{{{normalize_sub(sup)}}}"
            if font in ("mathcal", "mathfrak"):
                sid = f"{font}_{sid}"
            syms.add(sid)
        font_sub_spans.append((m.start(), m.end()))

    # Standalone \mathrm{...} / \mathcal{...} names (skip if sub/sup handled above)
    for m in re.finditer(
        r"\\(?:mathrm|operatorname|mathcal|mathfrak|mathbb)\{([^}]+)\}",
        math,
    ):
        if any(s <= m.start() < e for s, e in font_sub_spans):
            continue
        name = normalize_sub(m.group(1))
        if name and name not in SKIP_CMDS:
            syms.add(name)

    # Book-specific compound symbols (metadata/notation.md)
    if re.search(r"\\mu_E\b", math):
        syms.add("mu_E")
    if re.search(r"\\mathrm\{Fit\}_E", math) or re.search(r"\\Fit_E\b", math):
        syms.add("Fit_E")
    if re.search(r"\\kappa_\{\\(?:mathrm|text)\{sel\}\}", math):
        syms.add("kappa_sel")

    # Greek letter + subscript: \epsilon_B, \epsilon_{\Phi}, \epsilon_\Phi
    greek_pat = "|".join(sorted(GREEK, key=len, reverse=True))
    for m in re.finditer(
        rf"\\({greek_pat})(?:_\{{([^}}]+)\}}|_([A-Za-z0-9]+))",
        math,
    ):
        greek = m.group(1)
        sub = normalize_sub(m.group(2) or m.group(3))
        syms.add(f"{greek}_{{{sub}}}")
    for m in re.finditer(rf"\\({greek_pat})_\\([A-Za-z]+)", math):
        syms.add(f"{m.group(1)}_{{{m.group(2)}}}")

    # Bare command symbols
    for m in re.finditer(r"\\([A-Za-z]+)", math):
        cmd = m.group(1)
        end = m.end()
        if cmd in GREEK:
            if cmd == "mu" and re.search(r"\\mu_E\b", math):
                continue
            if end < len(math) and math[end] == "_":
                continue
            syms.add(cmd)
        elif cmd in ("CCI", "GLI", "DL", "MI", "Phi", "Gamma", "Delta", "Fit"):
            if cmd == "Delta":
                continue  # handled above
            if cmd == "Fit" and re.search(r"\\mathrm\{Fit\}_E", math):
                continue
            syms.add(cmd)

    # Subscripted identifiers (base must not be tail of a \command name)
    for m in re.finditer(
        r"(?<![A-Za-z])([A-Za-z])_\{(?:\\(?:mathrm|text)\{)?([^}]+)\}?(?:\})?"
        r"|(?<![A-Za-z])([A-Za-z])_\{([^}]+)\}"
        r"|(?<![A-Za-z])([A-Za-z])_([A-Za-z0-9]+)",
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
        defined, used = split_defined_used_symbols(block)
        used |= _symbolref_canonical_ids(block)
        syms = defined | used

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
                defined_symbols=defined,
                used_symbols=used,
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
    """Escape for single-line Graphviz attributes (no line breaks)."""
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def dot_label(s: str) -> str:
    """Escape a multi-line Graphviz node label (newlines render as line breaks)."""
    if not s:
        return ""
    return "\\n".join(
        line.replace("\\", "\\\\").replace('"', '\\"') for line in s.split("\n")
    )


def _eq_chain_eq_label(f: Formula) -> str:
    if f.env == "symboldef":
        sym = next(iter(f.defined_symbols), "?")
        ch_num = f.chapter.replace("ch", "")
        return f"{sym} (def anchor)\nch{ch_num} · L{f.line_start}\n{f.fid}"
    if f.env == "symbolref":
        sym = next(iter(f.used_symbols), "?")
        ch_num = f.chapter.replace("ch", "")
        return f"{sym} (use anchor)\nch{ch_num} · L{f.line_start}\n{f.fid}"
    slug = f.fid[3:] if f.fid.startswith("eq:") else f.fid
    ch_num = f.chapter.replace("ch", "")
    return f"{slug}\nch{ch_num} · L{f.line_start}\n{f.fid}"


def _eq_chain_sym_label(sym: str, core: EqChainCore) -> str:
    order = core.first_def_order.get(sym)
    if not order:
        return sym
    _ch, line, fid = order
    if fid.startswith("symdef:"):
        slug = fid
    elif fid.startswith("eq:"):
        slug = fid[3:]
    else:
        slug = fid
    ch_num = _ch.replace("ch", "")
    return f"{sym}\ndef {slug}\nch{ch_num} · L{line}"


def _eq_chain_chapter_label(ch: str, core: EqChainCore, anchor_fid: str | None) -> str:
    num = ch.replace("ch", "")
    if not anchor_fid or anchor_fid not in core.by_fid:
        return f"ch{num}"
    f = core.by_fid[anchor_fid]
    if anchor_fid.startswith("eq:"):
        slug = anchor_fid[3:]
    else:
        slug = anchor_fid
    return f"ch{num}\nanchor {slug}\nL{f.line_start} · {f.chapter_file}"


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


def emit_prose_eq_ref_edges(
    lines: list[str],
    all_formulas: list[Formula],
    known_fids: set[str],
) -> None:
    """Restore ``\\eqref{eq:...}`` edges from prose (not emitted on labeled eq nodes).

    Uses one ``eqcite:chNN`` hub per citing chapter — same aggregation as the old
    ``chcite → eq`` spokes, without re-adding chapter/section ``\\ref`` hairballs.
    """
    labeled = [f for f in all_formulas if f.fid.startswith("eq:")]
    prose_eq = collect_prose_eq_refs(all_formulas, labeled)
    if not prose_eq:
        return

    lines.append("  // Prose equation refs (\\\\eqref / \\\\ref{eq:...}; aggregated per citing chapter)")
    emitted_hubs: set[str] = set()
    for src in sorted(prose_eq, key=lambda c: int(c[2:]) if c[2:].isdigit() else 999):
        hub = f"eqcite:{src}"
        if hub not in emitted_hubs:
            lines.append(
                f'  "{hub}" [shape=folder, style=filled, fillcolor="#ecfdf5", '
                f'color="#047857", label="{src}\\neqref"];'
            )
            emitted_hubs.add(hub)
        for ref in sorted(prose_eq[src]):
            if ref in known_fids:
                lines.append(f'  "{hub}" -> "{ref}" [{LOW_WEIGHT_EQREF_ATTRS}];')
            else:
                ghost = f"ghost:{ref}"
                if ghost not in known_fids:
                    lines.append(
                        f'  "{ghost}" [shape=octagon, style=dashed, fillcolor="#fee2e2", '
                        f'label="{dot_escape(ref)}\\n(external)"];'
                    )
                    known_fids.add(ghost)
                lines.append(f'  "{hub}" -> "{ghost}" [color="#dc2626", style=dashed];')


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


READING_ORDER_RANK_ATTRS = "style=invis, weight=1, constraint=true"
SYMBOL_SPINE_ATTRS = "color=#2c5282, penwidth=1.0, weight=80, constraint=true"
LOW_WEIGHT_EQREF_ATTRS = "color=#059669, style=dashed, penwidth=0.6, weight=0.5, constraint=false"
EQ_CHAIN_SYM_COOCCUR_ATTRS = (
    'color="#94a3b8", style=dashed, dir=both, constraint=false, penwidth=1.0'
)
EQ_CHAIN_GRAPH_SEP = "+24"  # node margin for dot overlap=prism (was +20; +20% hspace Aug 2026)
EQ_CHAIN_GRAPH_RANKSEP = "1.4"  # rankdir=LR: horizontal space between ranks
EQ_CHAIN_GRAPH_NODESEP = "0.45"  # rankdir=LR: vertical space within a rank
EQ_CHAIN_GRAPH_RANKSEP_TB = "1.2"  # rankdir=TB: vertical space between ranks
EQ_CHAIN_GRAPH_NODESEP_TB = "0.55"  # rankdir=TB: horizontal space within a rank


def _eq_chain_graph_attrs(rankdir: str) -> str:
    """Graphviz ``graph [...]`` attribute string for eq-chain layout."""
    if rankdir.upper() == "TB":
        return (
            f'  graph [rankdir=TB, fontsize=10, overlap=prism, sep="{EQ_CHAIN_GRAPH_SEP}", '
            f"ranksep={EQ_CHAIN_GRAPH_RANKSEP_TB}, nodesep={EQ_CHAIN_GRAPH_NODESEP_TB},"
        )
    return (
        f'  graph [rankdir=LR, fontsize=10, overlap=prism, sep="{EQ_CHAIN_GRAPH_SEP}", '
        f"ranksep={EQ_CHAIN_GRAPH_RANKSEP}, nodesep={EQ_CHAIN_GRAPH_NODESEP},"
    )


def _anchor_covered_by_kept_eq(
    anchor_fid: str, core: "EqChainCore"
) -> bool:
    """True when a symdef/symref line sits inside a kept labeled equation block."""
    if anchor_fid not in core.by_fid:
        return False
    anchor = core.by_fid[anchor_fid]
    if anchor.env not in ("symboldef", "symbolref"):
        return False
    for fid in core.kept_eqs:
        if not fid.startswith("eq:"):
            continue
        f = core.by_fid[fid]
        if f.chapter != anchor.chapter:
            continue
        if f.line_start <= anchor.line_start <= f.line_end:
            return True
    return False


def _record_sym_eq(
    bucket: dict[str, set[str]], sym: str, fid: str
) -> None:
    bucket[normalize_chain_sym_id(sym)].add(fid)


def _formula_defines_sym(f: Formula, sym: str) -> bool:
    norm = normalize_chain_sym_id(sym)
    return norm in {normalize_chain_sym_id(s) for s in f.defined_symbols}


def _formula_uses_sym(f: Formula, sym: str) -> bool:
    norm = normalize_chain_sym_id(sym)
    return norm in {normalize_chain_sym_id(s) for s in f.used_symbols}


EQ_CHAIN_SYM_TO_EQ_ATTRS = 'color="#2563eb", penwidth=1.2, weight=80, constraint=true'
EQ_CHAIN_EQ_DEF_SYM_ATTRS = 'color="#7c3aed", penwidth=1.2, weight=80, constraint=true'
EQ_CHAIN_CH_DEF_EQ_ATTRS = (
    'color="#b45309", penwidth=1.2, weight=80, constraint=true'
)
EQ_CHAIN_SPINE_ATTRS = "style=invis, weight=60, constraint=true"


def _formula_order_key(f: Formula) -> tuple[str, int, str]:
    return (f.chapter, f.line_start, f.fid)


@dataclass
class EqChainCore:
    chain_syms: set[str]
    kept_eqs: set[str]
    sym_def_eqs: dict[str, set[str]]
    sym_use_eqs: dict[str, set[str]]
    first_def_order: dict[str, tuple[str, int, str]]
    first_def_chapter: dict[str, str]
    by_fid: dict[str, Formula]


def _compute_eq_chain_core(
    all_formulas: list[Formula],
    symbol_defs: list[SymbolDef] | None = None,
    symbol_refs: list[SymbolRef] | None = None,
) -> EqChainCore:
    labeled = [f for f in all_formulas if f.fid.startswith("eq:")]
    by_fid = {f.fid: f for f in labeled}
    for sd in symbol_defs or []:
        by_fid[sd.fid] = sd.as_formula()
    for sr in symbol_refs or []:
        by_fid[sr.fid] = sr.as_formula()
    ordered = sorted(labeled, key=_formula_order_key)

    sym_def_eqs: dict[str, set[str]] = defaultdict(set)
    sym_use_eqs: dict[str, set[str]] = defaultdict(set)
    for f in labeled:
        for sym in f.defined_symbols:
            _record_sym_eq(sym_def_eqs, sym, f.fid)
        for sym in f.used_symbols:
            _record_sym_eq(sym_use_eqs, sym, f.fid)
    for sd in symbol_defs or []:
        _record_sym_eq(sym_def_eqs, sd.sym, sd.fid)
    for sr in symbol_refs or []:
        _record_sym_eq(sym_use_eqs, sr.sym, sr.fid)

    first_def_order: dict[str, tuple[str, int, str]] = {}
    first_def_chapter: dict[str, str] = {}
    def_events: list[tuple[str, int, str, str]] = []
    for f in ordered:
        for sym in f.defined_symbols:
            def_events.append((f.chapter, f.line_start, f.fid, normalize_chain_sym_id(sym)))
    for sd in symbol_defs or []:
        def_events.append((sd.chapter, sd.line, sd.fid, normalize_chain_sym_id(sd.sym)))
    for ch, line, fid, sym in sorted(def_events, key=lambda e: (e[0], e[1], e[2])):
        if sym not in first_def_order:
            first_def_order[sym] = (ch, line, fid)
            first_def_chapter[sym] = ch

    chain_syms: set[str] = set()
    for sym in sym_def_eqs:
        use_eqs = sym_use_eqs.get(sym, set())
        if not use_eqs:
            continue
        for use_fid in use_eqs:
            use_f = by_fid[use_fid]
            if _formula_defines_sym(use_f, sym):
                continue
            if sym not in first_def_order:
                continue
            if _formula_order_key(use_f) <= first_def_order[sym]:
                continue
            chain_syms.add(sym)
            break

    kept_eqs: set[str] = set()
    for sym in chain_syms:
        kept_eqs |= sym_def_eqs[sym]
        kept_eqs |= {
            e for e in sym_use_eqs[sym] if _formula_uses_sym(by_fid[e], sym)
        }

    return EqChainCore(
        chain_syms=chain_syms,
        kept_eqs=kept_eqs,
        sym_def_eqs=sym_def_eqs,
        sym_use_eqs=sym_use_eqs,
        first_def_order=first_def_order,
        first_def_chapter=first_def_chapter,
        by_fid=by_fid,
    )


def _append_eq_chain_nodes_edges(
    lines: list[str], core: EqChainCore, *, include_cooccur: bool = False
) -> tuple[int, int, int, int]:
    """Emit eq/sym nodes, def/use edges, spine, and optional sym co-occurrence edges."""
    visible_fids: set[str] = set()
    for fid in sorted(core.kept_eqs, key=lambda e: _formula_order_key(core.by_fid[e])):
        if fid.startswith(("symdef:", "symref:")) and _anchor_covered_by_kept_eq(
            fid, core
        ):
            continue
        visible_fids.add(fid)
        f = core.by_fid[fid]
        if f.env == "symboldef":
            node_attrs = 'shape=note, style=filled, fillcolor="#fef3c7"'
        elif f.env == "symbolref":
            node_attrs = 'shape=note, style=filled, fillcolor="#e0f2fe"'
        else:
            node_attrs = 'shape=box, style=filled, fillcolor="#d1fae5"'
        lines.append(
            f'  "{fid}" [{node_attrs}, '
            f'label="{dot_label(_eq_chain_eq_label(f))}"];'
        )

    for sym in sorted(core.chain_syms, key=lambda s: s.lower()):
        lines.append(
            f'  "sym:{sym}" [shape=ellipse, style=filled, fillcolor="#dbeafe", '
            f'label="{dot_label(_eq_chain_sym_label(sym, core))}"];'
        )

    lines.append("")
    lines.append("  // eq|symdef → sym (definition on LHS, tuple intro, or \\symboldef)")
    n_def = 0
    for sym in sorted(core.chain_syms, key=lambda s: s.lower()):
        for fid in sorted(core.sym_def_eqs[sym] & core.kept_eqs):
            if fid not in visible_fids:
                continue
            lines.append(f'  "{fid}" -> "sym:{sym}" [{EQ_CHAIN_EQ_DEF_SYM_ATTRS}];')
            n_def += 1

    lines.append("")
    lines.append("  // sym → eq|symref (use on RHS or \\symbolref, after first definition)")
    n_use = 0
    for sym in sorted(core.chain_syms, key=lambda s: s.lower()):
        for fid in sorted(core.sym_use_eqs[sym] & core.kept_eqs):
            if fid not in visible_fids:
                continue
            use_f = core.by_fid[fid]
            if _formula_defines_sym(use_f, sym):
                continue
            if sym not in core.first_def_order:
                continue
            if _formula_order_key(use_f) <= core.first_def_order[sym]:
                continue
            lines.append(f'  "sym:{sym}" -> "{fid}" [{EQ_CHAIN_SYM_TO_EQ_ATTRS}];')
            n_use += 1

    by_ch: dict[str, list[Formula]] = defaultdict(list)
    for fid in visible_fids:
        f = core.by_fid[fid]
        if f.env in ("symboldef", "symbolref") or not fid.startswith("eq:"):
            continue
        by_ch[f.chapter].append(f)
    lines.append("")
    lines.append("  // Within-chapter equation line-order (invis layout spine)")
    n_spine = 0
    for ch in sorted(by_ch):
        eqs = sorted(by_ch[ch], key=lambda f: f.line_start)
        for a, b in zip(eqs, eqs[1:]):
            lines.append(f'  "{a.fid}" -> "{b.fid}" [{EQ_CHAIN_SPINE_ATTRS}];')
            n_spine += 1

    n_co = 0
    if include_cooccur:
        lines.append("")
        lines.append("  // sym↔sym co-occurrence in the same kept labeled equation")
        for fid in sorted(visible_fids):
            if not fid.startswith("eq:"):
                continue
            f = core.by_fid[fid]
            present = sorted(
                {
                    normalize_chain_sym_id(s)
                    for s in f.defined_symbols | f.used_symbols
                    if normalize_chain_sym_id(s) in core.chain_syms
                },
                key=str.lower,
            )
            for i, a in enumerate(present):
                for b in present[i + 1 :]:
                    lines.append(
                        f'  "sym:{a}" -> "sym:{b}" [{EQ_CHAIN_SYM_COOCCUR_ATTRS}];'
                    )
                    n_co += 1
    return n_def, n_use, n_spine, n_co


def _visible_eq_chain_fid(fid: str, core: EqChainCore) -> bool:
    if fid not in core.kept_eqs:
        return False
    if fid.startswith(("symdef:", "symref:")) and _anchor_covered_by_kept_eq(
        fid, core
    ):
        return False
    return True


def _resolve_chapter_anchor(anchor: str, ch: str, core: EqChainCore) -> str:
    """Prefer labeled eq over symdef/symref when anchor sits inside that eq."""
    if not anchor.startswith(("symdef:", "symref:")):
        return anchor
    if not _anchor_covered_by_kept_eq(anchor, core):
        return anchor
    anchor_f = core.by_fid[anchor]
    for fid in sorted(core.kept_eqs):
        if not fid.startswith("eq:"):
            continue
        f = core.by_fid[fid]
        if f.chapter != ch:
            continue
        if f.line_start <= anchor_f.line_start <= f.line_end:
            return fid
    return anchor


def _chapter_anchor_eq(core: EqChainCore, ch: str) -> str | None:
    """Earliest kept def site (eq or symdef) in ``ch`` that first-defines a bridge symbol."""
    best_fid: str | None = None
    best_key: tuple[str, int, str] | None = None
    for sym in core.chain_syms:
        if core.first_def_chapter.get(sym) != ch:
            continue
        key = core.first_def_order[sym]
        fid = key[2]
        if fid not in core.kept_eqs:
            continue
        if best_key is None or key < best_key:
            best_key = key
            best_fid = fid
    return best_fid


def build_eq_chain_dot(
    all_formulas: list[Formula],
    symbol_defs: list[SymbolDef] | None = None,
    symbol_refs: list[SymbolRef] | None = None,
    *,
    include_cooccur: bool = False,
    rankdir: str = "LR",
) -> str:
    """Minimal eq→sym→eq chain graph: definitions (LHS) vs uses (RHS).

    Purple eq|symdef→sym: equation defines the symbol (LHS of ``='' or tuple
    component), or an explicit ``\\symboldef`` anchor.
    Blue sym→eq|symref: symbol is used in a later equation (RHS only) or
    ``\\symbolref`` site.
    """
    core = _compute_eq_chain_core(all_formulas, symbol_defs, symbol_refs)
    orient = "vertical" if rankdir.upper() == "TB" else "horizontal"
    lines = [
        "digraph EquationChainGraph {",
        _eq_chain_graph_attrs(rankdir),
        f'    label="Equation chains ({orient}; eq|symdef→sym defines, sym→eq|symref uses)", labelloc=t];',
        "  node [fontname=Helvetica, fontsize=9];",
        "  edge [fontname=Helvetica, fontsize=8];",
        "",
    ]
    n_def, n_use, n_spine, n_co = _append_eq_chain_nodes_edges(
        lines, core, include_cooccur=include_cooccur
    )
    co_note = f", {n_co} co-occur edges" if include_cooccur else ""
    lines.append(
        f"  // ({len(core.kept_eqs)} eq nodes, {len(core.chain_syms)} bridge symbols, "
        f"{n_def} def, {n_use} use, {n_spine} spine{co_note})"
    )
    lines.append("}")
    return "\n".join(lines)


def build_eq_chain_chapters_dot(
    all_formulas: list[Formula],
    symbol_defs: list[SymbolDef] | None = None,
    symbol_refs: list[SymbolRef] | None = None,
    *,
    include_cooccur: bool = False,
    rankdir: str = "LR",
) -> str:
    """Eq-chain graph plus one chapter→equation link per defining chapter.

    Each ``unit:chNN`` connects to the earliest kept def site in that chapter that
    first-defines a bridge symbol (constraining layout). Symbol defs remain
    eq|symdef→sym; uses include ``\\symbolref`` sites; no chapter→symbol fan-out.
    """
    core = _compute_eq_chain_core(all_formulas, symbol_defs, symbol_refs)
    def_chapters = {core.first_def_chapter[sym] for sym in core.chain_syms}
    ch_anchors: dict[str, str] = {}
    for ch in def_chapters:
        anchor = _chapter_anchor_eq(core, ch)
        if anchor:
            ch_anchors[ch] = anchor

    orient = "vertical" if rankdir.upper() == "TB" else "horizontal"
    lines = [
        "digraph EquationChainGraphWithChapters {",
        _eq_chain_graph_attrs(rankdir),
        f'    label="Equation chains + chapter→first-def eq ({orient})", labelloc=t];',
        "  node [fontname=Helvetica, fontsize=9];",
        "  edge [fontname=Helvetica, fontsize=8];",
        "",
    ]

    for ch in sorted(ch_anchors, key=lambda c: int(c[2:]) if c[2:].isdigit() else 999):
        lines.append(
            f'  "unit:{ch}" [shape=folder, style=filled, fillcolor="#fef3c7", '
            f'label="{dot_label(_eq_chain_chapter_label(ch, core, ch_anchors.get(ch)))}"];'
        )

    n_def, n_use, n_spine, n_co = _append_eq_chain_nodes_edges(
        lines, core, include_cooccur=include_cooccur
    )

    lines.append("")
    lines.append("  // unit:chNN → earliest first-def site in chapter (eq or symdef)")
    n_ch = 0
    for ch in sorted(ch_anchors, key=lambda c: int(c[2:]) if c[2:].isdigit() else 999):
        anchor = _resolve_chapter_anchor(ch_anchors[ch], ch, core)
        lines.append(f'  "unit:{ch}" -> "{anchor}" [{EQ_CHAIN_CH_DEF_EQ_ATTRS}];')
        n_ch += 1

    co_note = f", {n_co} co-occur" if include_cooccur else ""
    lines.append(
        f"  // ({len(ch_anchors)} chapter nodes, {len(core.kept_eqs)} eq, "
        f"{len(core.chain_syms)} bridge symbols, {n_ch} ch→eq, "
        f"{n_def} eq→sym, {n_use} sym→eq, {n_spine} spine{co_note})"
    )
    lines.append("}")
    return "\n".join(lines)


def build_dot(
    all_formulas: list[Formula],
    chapter_filter: str | None = None,
    ch_owner: dict[str, str] | None = None,
    sec_owner: dict[str, str] | None = None,
    detailed: bool = False,
    *,
    sym_spine_layout: bool = True,
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

    lines.append("  // Symbol → formula (primary layout spine: sym→eq→sym→eq chains)")
    if sym_spine_layout:
        for f in visible:
            for sym in sorted(f.symbols):
                lines.append(f'  "sym:{sym}" -> "{f.fid}" [{SYMBOL_SPINE_ATTRS}];')
    else:
        lines.append('  edge [penwidth=0.4, arrowsize=0.4];')
        for f in visible:
            for sym in sorted(f.symbols):
                lines.append(f'  "sym:{sym}" -> "{f.fid}" [color="#2c528266"];')
        lines.append('  edge [penwidth=1.0, arrowsize=1.0];')

    lines.append("  // Formula references formula (labeled eq blocks; medium weight)")
    for f in visible:
        for ref in sorted(f.refs):
            if ref in known_fids:
                lines.append(
                    f'  "{f.fid}" -> "{ref}" [color="#059669", weight=2, constraint=true];'
                )
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

    # Prose \\eqref{eq:...} (dominant style) — restored after chcite removal; section/ch
    # prose refs stay in metadata/concept-graph/section-reference-graph.dot.
    if not detailed:
        emit_prose_eq_ref_edges(lines, all_formulas, known_fids)

    # Chapter/section prose refs live in metadata/concept-graph/section-reference-graph.dot
    if detailed and ch_owner is not None and sec_owner is not None:
        emit_text_ref_edges(lines, all_formulas, ch_owner, sec_owner)

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
    if not detailed:
        emit_prose_eq_ref_edges(lines, all_formulas, known_fids)

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

    # Section/chapter prose refs: see metadata/concept-graph/ (not duplicated here).
    if detailed and ch_owner is not None and sec_owner is not None:
        emit_text_ref_edges(lines, all_formulas, ch_owner, sec_owner)

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
            "Chapter/section prose citations are **not** edges in the symbol→formula graph",
            "(they produced unreadable per-line `chNN:prose:LINE` hairballs). They are",
            "aggregated in `metadata/concept-graph/section-reference-graph.dot` via",
            "`scripts/build_section_reference_graph.py` — one edge per citing section →",
            "target `sec:`/`ch:` label. The symbol graph keeps green `ref` edges for",
            "`\\eqref{eq:...}` only.",
            "",
            f"- `\\ref{{ch:...}}` / `\\ref{{sec:...}}` occurrences in manuscript: {text_ref_count}",
            f"- Resolved to a known chapter (legacy count): {resolved}",
            f"- Unresolved (label not found in parsed sources): {len(unresolved_refs)}",
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
    parser.add_argument(
        "--no-sym-spine-layout",
        action="store_true",
        help="Use faint sym→eq edges (old style) instead of high-weight layout spine",
    )
    parser.add_argument(
        "--cooccur",
        action="store_true",
        help="Emit dashed sym↔sym co-occurrence edges in eq-chain graphs (off by default)",
    )
    args = parser.parse_args()
    sym_spine = not args.no_sym_spine_layout

    paths = sorted(CHAPTERS_DIR.glob("ch*.tex"))
    all_formulas: list[Formula] = []
    ch_owner: dict[str, str] = {}
    sec_owner: dict[str, str] = {}
    for p in paths:
        all_formulas.extend(parse_chapter(p, ch_owner=ch_owner, sec_owner=sec_owner))

    symbol_defs = parse_symboldefs(paths)
    print(f"  {len(symbol_defs)} \\symboldef{{}} definition anchors in manuscript")
    symbol_refs = parse_symbolrefs(paths)
    print(f"  {len(symbol_refs)} \\symbolref{{}} use anchors in manuscript")

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
            sym_spine_layout=sym_spine,
        )
    else:
        dot = build_dot(
            all_formulas,
            ch_owner=ch_owner,
            sec_owner=sec_owner,
            sym_spine_layout=sym_spine,
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(dot, encoding="utf-8")

    eq_chain_path = args.out.with_name("equation-chain-graph.dot")
    eq_chain_path.write_text(
        build_eq_chain_dot(
            all_formulas,
            symbol_defs,
            symbol_refs,
            include_cooccur=args.cooccur,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {eq_chain_path}")

    eq_chain_ch_path = args.out.with_name("equation-chain-graph-chapters.dot")
    eq_chain_ch_path.write_text(
        build_eq_chain_chapters_dot(
            all_formulas,
            symbol_defs,
            symbol_refs,
            include_cooccur=args.cooccur,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {eq_chain_ch_path}")

    eq_chain_vert_path = args.out.with_name("equation-chain-graph-vertical.dot")
    eq_chain_vert_path.write_text(
        build_eq_chain_dot(
            all_formulas,
            symbol_defs,
            symbol_refs,
            include_cooccur=args.cooccur,
            rankdir="TB",
        ),
        encoding="utf-8",
    )
    print(f"Wrote {eq_chain_vert_path}")

    eq_chain_ch_vert_path = args.out.with_name(
        "equation-chain-graph-chapters-vertical.dot"
    )
    eq_chain_ch_vert_path.write_text(
        build_eq_chain_chapters_dot(
            all_formulas,
            symbol_defs,
            symbol_refs,
            include_cooccur=args.cooccur,
            rankdir="TB",
        ),
        encoding="utf-8",
    )
    print(f"Wrote {eq_chain_ch_vert_path}")

    if args.detailed and not args.chapter:
        detailed_path = args.out.with_name("symbol-formula-graph-detailed.dot")
        detailed_path.write_text(
            build_dot(
                all_formulas,
                ch_owner=ch_owner,
                sec_owner=sec_owner,
                detailed=True,
                sym_spine_layout=sym_spine,
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
        ch14_dot = build_dot(
            all_formulas,
            chapter_filter="ch14",
            ch_owner=ch_owner,
            sec_owner=sec_owner,
            sym_spine_layout=sym_spine,
        )
        ch14_path = args.out.with_name("symbol-formula-graph-ch14.dot")
        ch14_path.write_text(ch14_dot, encoding="utf-8")
        print(f"Wrote {ch14_path}")

    visible_count = len(graph_formula_nodes(all_formulas, detailed=False))
    print(f"Wrote {args.out} ({visible_count} labeled-eq nodes in reachability graph; {len(all_formulas)} parsed total)")
    print(f"Wrote {args.coverage}")

    # Chapter prerequisite DAG (symbol def/use → reading paths)
    try:
        from build_chapter_symbol_dependency import build_from_manuscript

        dep_dot, dep_md = build_from_manuscript(rankdir="TB")
        print(f"Wrote {dep_dot}")
        print(f"Wrote {dep_md}")
    except Exception as exc:  # pragma: no cover
        print(f"Warning: chapter symbol dependency graph skipped: {exc}", file=sys.stderr)


if __name__ == "__main__":
    main()
