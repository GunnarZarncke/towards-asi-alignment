#!/usr/bin/env python3
"""Generate a markdown report of manuscript statistics."""

from __future__ import annotations

import argparse
import math
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STRIP_RE = re.compile(r"\\[a-zA-Z@]+(\[[^\]]*\])?(\{[^}]*\})?|[{}%]|\\.")
INPUT_RE = re.compile(r"\\input\{([^}]+)\}")
ADDBIB_RE = re.compile(r"\\addbibresource\{([^}]+)\}")
INCLUDEGRAPHICS_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
CITE_RE = re.compile(
    r"\\(?:parencite|textcite|cite|autocite|footcite|Cite|Parencite|Textcite|Autocite|Footcite)\{([^}]+)\}"
)
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
CHAPTER_TOC_RE = re.compile(
    r"\\contentsline \{chapter\}\{(?:\\chapternumberline \{(\d+)\})?([^}]*)\}\{([^}]+)\}\{([^}]+)\}"
)
APPENDIX_TOC_RE = re.compile(
    r"\\contentsline \{appendix\}\{\\chapternumberline \{([A-Z])\}([^}]*)\}\{(\d+)\}"
)
PDF_PAGES_RE = re.compile(r"Output written on .* \((\d+) pages,")
BIB_KEY_RE = re.compile(r"@\w+\{([^,\s]+),", re.MULTILINE)

MATH_ENV_RE = re.compile(
    r"\\begin\{(?:equation\*?|align\*?|gather\*?|multline\*?|split|eqnarray\*?|flalign\*?)\}"
)
DISPLAY_MATH_RE = re.compile(r"\\\[")

LEAN_DECL_LINE_RE = re.compile(
    r"^\s*(theorem|lemma|def|abbrev|structure|class|instance|inductive|axiom)\b"
)
SPINE_P_THEOREM_RE = re.compile(r"^\s*(?:theorem|lemma)\s+(P\d+[a-zA-Z]*)")
SPINE_MB_AXIOM_RE = re.compile(r"^\s*axiom\s+(MB\d+[a-zA-Z]*)")
LEANSPINE_RE = re.compile(r"\\leanspine\{")
LEANSPINE_NODE_RE = re.compile(r"\\leanspine\{[^}]+\}\{([^}]+)\}")
SORRY_RE = re.compile(r"\bsorry\b|\badmit\b")

FRONTMATTER_FILES = [
    "frontmatter/titlepage.tex",
    "frontmatter/dedication.tex",
    "frontmatter/acknowledgements.tex",
    "frontmatter/preface.tex",
    "frontmatter/introduction.tex",
    "frontmatter/executive-overview.tex",
    "frontmatter/current-status.tex",
]

FRONTMATTER_TOC_TITLES = {
    "dedication.tex": "Dedication",
    "acknowledgements.tex": "Acknowledgements",
    "preface.tex": "Preface",
    "introduction.tex": "Introduction",
    "executive-overview.tex": "Executive Overview",
    "current-status.tex": "Current Status",
}

def discover_appendix_files() -> list[str]:
    return sorted(str(p.relative_to(ROOT)) for p in (ROOT / "appendices").glob("app*.tex"))


@dataclass
class BookFileInventory:
    tex_files: set[str] = field(default_factory=set)
    bib_files: set[str] = field(default_factory=set)
    figure_files: set[str] = field(default_factory=set)

    @property
    def pdf_total(self) -> int:
        return len(self.tex_files) + len(self.bib_files) + len(self.figure_files)

    def tex_by_category(self) -> dict[str, list[str]]:
        buckets: dict[str, list[str]] = {
            "Root": [],
            "Parts": [],
            "Chapters": [],
            "Frontmatter": [],
            "Appendices": [],
            "Metadata": [],
            "Tables": [],
            "References (TeX)": [],
            "Other TeX": [],
        }
        for rel in sorted(self.tex_files):
            if rel == "book.tex":
                buckets["Root"].append(rel)
            elif rel.startswith("parts/"):
                buckets["Parts"].append(rel)
            elif rel.startswith("chapters/"):
                buckets["Chapters"].append(rel)
            elif rel.startswith("frontmatter/"):
                buckets["Frontmatter"].append(rel)
            elif rel.startswith("appendices/"):
                buckets["Appendices"].append(rel)
            elif rel.startswith("metadata/"):
                buckets["Metadata"].append(rel)
            elif rel.startswith("tables/"):
                buckets["Tables"].append(rel)
            elif rel.startswith("references/"):
                buckets["References (TeX)"].append(rel)
            else:
                buckets["Other TeX"].append(rel)
        return {name: paths for name, paths in buckets.items() if paths}


def resolve_tex_input(ref: str) -> Path | None:
    ref = ref.strip()
    if not ref:
        return None
    candidates = [ROOT / ref]
    if not ref.endswith(".tex"):
        candidates.insert(0, ROOT / f"{ref}.tex")
    for path in candidates:
        if path.is_file():
            return path
    return None


def resolve_figure_path(ref: str) -> Path | None:
    ref = ref.strip()
    if not ref:
        return None
    path = Path(ref)
    if path.is_absolute():
        candidates = [path]
    else:
        candidates = [ROOT / ref]
    stem = candidates[0]
    if stem.suffix:
        candidates = [stem]
    else:
        candidates = [stem.with_suffix(ext) for ext in (".png", ".pdf", ".jpg", ".jpeg", ".svg", ".eps")]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def discover_book_file_inventory() -> BookFileInventory:
    inventory = BookFileInventory()
    stack = [ROOT / "book.tex"]
    while stack:
        path = stack.pop()
        rel = str(path.relative_to(ROOT))
        if rel in inventory.tex_files:
            continue
        inventory.tex_files.add(rel)
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in INPUT_RE.finditer(text):
            child = resolve_tex_input(match.group(1))
            if child is not None:
                stack.append(child)

    book_text = (ROOT / "book.tex").read_text(encoding="utf-8", errors="replace")
    for match in ADDBIB_RE.finditer(book_text):
        bib_rel = match.group(1).strip()
        if (ROOT / bib_rel).is_file():
            inventory.bib_files.add(bib_rel)

    for rel in inventory.tex_files:
        text = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
        for match in INCLUDEGRAPHICS_RE.finditer(text):
            fig_path = resolve_figure_path(match.group(1))
            if fig_path is not None:
                inventory.figure_files.add(str(fig_path.relative_to(ROOT)))

    return inventory


def roman_to_int(value: str) -> int | None:
    value = value.strip().lower()
    if not value:
        return None
    if value.isdigit():
        return int(value)
    numerals = {"i": 1, "v": 5, "x": 10, "l": 50, "c": 100, "d": 500, "m": 1000}
    total = 0
    prev = 0
    for ch in reversed(value):
        if ch not in numerals:
            return None
        current = numerals[ch]
        if current < prev:
            total -= current
        else:
            total += current
            prev = current
    return total


def count_words(text: str) -> int:
    text = re.sub(r"%.*", "", text)
    text = STRIP_RE.sub(" ", text)
    return len(text.split())


def approx_llm_tokens(text: str) -> int:
    """Approximate LLM token count using the common UTF-8 bytes / 4 heuristic."""
    return math.ceil(len(text.encode("utf-8")) / 4)


def count_plain_words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE))


def count_lines(text: str) -> int:
    return text.count("\n") + (0 if text.endswith("\n") or not text else 1)


def count_non_empty_lines(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip())


def count_tex_loc(text: str) -> tuple[int, int, int]:
    """Return (total_lines, loc_non_blank, code_loc_excl_comment_only)."""
    total = count_lines(text)
    loc = 0
    code_loc = 0
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not stripped:
            continue
        loc += 1
        if strip_tex_comment(raw_line):
            code_loc += 1
    return total, loc, code_loc


def strip_tex_comment(line: str) -> str:
    out: list[str] = []
    for i, ch in enumerate(line):
        if ch == "%" and (i == 0 or line[i - 1] != "\\"):
            break
        out.append(ch)
    return "".join(out).strip()


def count_lean_loc(text: str) -> tuple[int, int, int]:
    """Return (total_lines, loc_non_blank, code_loc_excl_comment_only)."""
    total = count_lines(text)
    loc = 0
    code_loc = 0
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not stripped:
            continue
        loc += 1
        code_part = stripped.split("--", 1)[0].strip()
        if code_part and not (code_part.startswith("/-") and code_part.endswith("-/")):
            code_loc += 1
    return total, loc, code_loc


@dataclass
class FileStats:
    path: str
    group: str
    title: str = ""
    words: int = 0
    lines: int = 0
    loc: int = 0
    code_loc: int = 0
    pages: int | None = None
    page_start: str | None = None
    citations: int = 0
    cite_keys: set[str] = field(default_factory=set)
    labels: int = 0
    label_keys: set[str] = field(default_factory=set)
    formulas: int = 0
    figures: int = 0
    tables: int = 0
    sections: int = 0
    subsections: int = 0
    todos: int = 0
    includegraphics: int = 0


@dataclass
class LeanModuleStats:
    path: str
    lines: int = 0
    loc: int = 0
    code_loc: int = 0
    theorems: int = 0
    lemmas: int = 0
    defs: int = 0
    abbrevs: int = 0
    structures: int = 0
    classes: int = 0
    instances: int = 0
    inductives: int = 0
    axioms: int = 0
    spine_p_ids: set[str] = field(default_factory=set)
    spine_mb_ids: set[str] = field(default_factory=set)
    spine_p_theorems: int = 0
    other_theorems: int = 0
    sorry_admit: int = 0


@dataclass
class SourceExtractStats:
    path: str
    words: int = 0
    approx_tokens: int = 0
    chars: int = 0
    lines: int = 0


def discover_source_extracts() -> list[Path]:
    extracts_dir = ROOT / "context" / "extracts"
    if not extracts_dir.exists():
        return []
    return sorted(extracts_dir.glob("*.md"))


def analyze_source_extract(path: Path) -> SourceExtractStats:
    text = path.read_text(encoding="utf-8", errors="replace")
    return SourceExtractStats(
        path=str(path.relative_to(ROOT)),
        words=count_plain_words(text),
        approx_tokens=approx_llm_tokens(text),
        chars=len(text),
        lines=count_lines(text),
    )


def sum_plain_text_stats(paths: list[Path]) -> tuple[int, int, int]:
    words = 0
    approx_tokens = 0
    chars = 0
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        words += count_plain_words(text)
        approx_tokens += approx_llm_tokens(text)
        chars += len(text)
    return words, approx_tokens, chars


def analyze_lean(path: Path) -> LeanModuleStats:
    text = path.read_text(encoding="utf-8", errors="replace")
    stats = LeanModuleStats(path=str(path.relative_to(ROOT)))
    stats.lines, stats.loc, stats.code_loc = count_lean_loc(text)

    for raw_line in text.splitlines():
        line = raw_line.split("--", 1)[0]
        if not line.strip():
            continue

        if SORRY_RE.search(line):
            stats.sorry_admit += 1

        decl = LEAN_DECL_LINE_RE.match(line)
        if decl:
            kind = decl.group(1)
            if kind == "theorem":
                stats.theorems += 1
                p_match = SPINE_P_THEOREM_RE.match(line)
                if p_match:
                    stats.spine_p_theorems += 1
                    stats.spine_p_ids.add(p_match.group(1))
                else:
                    stats.other_theorems += 1
            elif kind == "lemma":
                stats.lemmas += 1
                p_match = SPINE_P_THEOREM_RE.match(line)
                if p_match:
                    stats.spine_p_theorems += 1
                    stats.spine_p_ids.add(p_match.group(1))
            elif kind == "def":
                stats.defs += 1
            elif kind == "abbrev":
                stats.abbrevs += 1
            elif kind == "structure":
                stats.structures += 1
            elif kind == "class":
                stats.classes += 1
            elif kind == "instance":
                stats.instances += 1
            elif kind == "inductive":
                stats.inductives += 1
            elif kind == "axiom":
                stats.axioms += 1
                mb_match = SPINE_MB_AXIOM_RE.match(line)
                if mb_match:
                    stats.spine_mb_ids.add(mb_match.group(1))

    return stats


def discover_lean_files() -> list[Path]:
    formal = ROOT / "formal"
    if not formal.exists():
        return []
    files = sorted(formal.rglob("*.lean"))
    return [p for p in files if ".lake" not in p.parts]


def count_leanspine_refs() -> tuple[int, set[str], dict[str, int]]:
    total = 0
    nodes: set[str] = set()
    per_chapter: dict[str, int] = {}
    for tex in ROOT.rglob("*.tex"):
        if ".venv" in tex.parts:
            continue
        text = tex.read_text(encoding="utf-8", errors="replace")
        refs = LEANSPINE_RE.findall(text)
        if not refs:
            continue
        count = len(refs)
        total += count
        rel = str(tex.relative_to(ROOT))
        if rel.startswith("chapters/"):
            per_chapter[rel] = count
        for node in LEANSPINE_NODE_RE.findall(text):
            nodes.add(node.strip())
    return total, nodes, dict(sorted(per_chapter.items()))


def sum_lean_stats(items: list[LeanModuleStats]) -> dict[str, int]:
    return {
        "lines": sum(s.lines for s in items),
        "loc": sum(s.loc for s in items),
        "code_loc": sum(s.code_loc for s in items),
        "theorems": sum(s.theorems for s in items),
        "lemmas": sum(s.lemmas for s in items),
        "defs": sum(s.defs for s in items),
        "abbrevs": sum(s.abbrevs for s in items),
        "structures": sum(s.structures for s in items),
        "classes": sum(s.classes for s in items),
        "instances": sum(s.instances for s in items),
        "inductives": sum(s.inductives for s in items),
        "axioms": sum(s.axioms for s in items),
        "spine_p_theorems": sum(s.spine_p_theorems for s in items),
        "other_theorems": sum(s.other_theorems for s in items),
        "sorry_admit": sum(s.sorry_admit for s in items),
    }


def analyze_tex(path: Path, group: str, title: str = "") -> FileStats:
    text = path.read_text(encoding="utf-8", errors="replace")
    stats = FileStats(path=str(path.relative_to(ROOT)), group=group, title=title)
    stats.words = count_words(text)
    stats.lines, stats.loc, stats.code_loc = count_tex_loc(text)

    for match in CITE_RE.finditer(text):
        stats.citations += 1
        for key in match.group(1).split(","):
            key = key.strip()
            if key:
                stats.cite_keys.add(key)

    for match in LABEL_RE.finditer(text):
        stats.labels += 1
        stats.label_keys.add(match.group(1))

    stats.formulas = len(MATH_ENV_RE.findall(text)) + len(DISPLAY_MATH_RE.findall(text))
    stats.figures = len(re.findall(r"\\begin\{figure\*?\}", text))
    stats.tables = len(re.findall(r"\\begin\{table\*?\}", text))
    stats.sections = len(re.findall(r"\\section\{", text))
    stats.subsections = len(re.findall(r"\\subsection\{", text))
    stats.includegraphics = len(re.findall(r"\\includegraphics", text))
    stats.todos = len(re.findall(r"\\todo\b|%\s*TODO\b|\bTODO:", text, flags=re.IGNORECASE))

    if not stats.title:
        chapter_match = re.search(r"\\chapter\{([^}]+)\}", text)
        if chapter_match:
            stats.title = re.sub(r"\\[^ ]+\s*", "", chapter_match.group(1)).strip()
        else:
            stats.title = path.stem

    return stats


def discover_chapter_files() -> list[str]:
    paths: list[str] = []
    for part in sorted((ROOT / "parts").glob("part*.tex")):
        for match in INPUT_RE.finditer(part.read_text(encoding="utf-8", errors="replace")):
            rel = match.group(1)
            if rel.startswith("chapters/"):
                paths.append(f"{rel}.tex" if not rel.endswith(".tex") else rel)
    return paths


@dataclass
class TocEntry:
    kind: str
    number: str | None
    title: str
    page_label: str
    page_int: int | None


def parse_toc() -> list[TocEntry]:
    toc_path = ROOT / "book.toc"
    if not toc_path.exists():
        return []

    entries: list[TocEntry] = []
    for line in toc_path.read_text(encoding="utf-8", errors="replace").splitlines():
        appendix_match = APPENDIX_TOC_RE.search(line)
        if appendix_match:
            letter, title, page = appendix_match.groups()
            entries.append(
                TocEntry(
                    kind="appendix",
                    number=letter,
                    title=title.strip(),
                    page_label=page,
                    page_int=int(page),
                )
            )
            continue

        chapter_match = CHAPTER_TOC_RE.search(line)
        if not chapter_match:
            continue
        number, title, page_label, _anchor = chapter_match.groups()
        title = re.sub(r"\\[^ ]+\s*", "", title).strip()
        entries.append(
            TocEntry(
                kind="chapter" if number else "frontmatter",
                number=number,
                title=title,
                page_label=page_label,
                page_int=roman_to_int(page_label),
            )
        )
    return entries


def assign_page_spans(entries: list[TocEntry]) -> dict[tuple[str, str | None], int]:
    """Return (kind, number-or-title) -> page span."""
    spans: dict[tuple[str, str | None], int] = {}
    for idx, entry in enumerate(entries):
        if entry.page_int is None:
            continue
        next_page: int | None = None
        for later in entries[idx + 1 :]:
            if later.page_int is not None and later.page_int > entry.page_int:
                next_page = later.page_int
                break
        if next_page is None:
            log_path = ROOT / "book.log"
            if log_path.exists():
                log_match = PDF_PAGES_RE.search(log_path.read_text(encoding="utf-8", errors="replace"))
                if log_match:
                    next_page = int(log_match.group(1)) + 1
        if next_page is None:
            continue
        key = (entry.kind, entry.number or entry.title)
        spans[key] = max(next_page - entry.page_int, 1)
    return spans


def load_bibliography_stats() -> tuple[int, dict[str, int]]:
    per_file: dict[str, int] = {}
    keys: set[str] = set()
    for bib in sorted((ROOT / "references").glob("*.bib")):
        file_keys = BIB_KEY_RE.findall(bib.read_text(encoding="utf-8", errors="replace"))
        per_file[bib.name] = len(file_keys)
        keys.update(file_keys)
    return len(keys), per_file


def pdf_page_count() -> int | None:
    log_path = ROOT / "book.log"
    if not log_path.exists():
        return None
    match = PDF_PAGES_RE.search(log_path.read_text(encoding="utf-8", errors="replace"))
    return int(match.group(1)) if match else None


def fmt_int(value: int | None) -> str:
    return "—" if value is None else f"{value:,}"


def normalize_title(title: str) -> str:
    return re.sub(r"\s+", " ", title).strip()


def sum_stats(items: list[FileStats]) -> dict[str, int]:
    return {
        "words": sum(s.words for s in items),
        "lines": sum(s.lines for s in items),
        "loc": sum(s.loc for s in items),
        "code_loc": sum(s.code_loc for s in items),
        "pages": sum(s.pages or 0 for s in items if s.pages is not None),
        "citations": sum(s.citations for s in items),
        "labels": sum(s.labels for s in items),
        "formulas": sum(s.formulas for s in items),
        "figures": sum(s.figures for s in items),
        "tables": sum(s.tables for s in items),
        "sections": sum(s.sections for s in items),
        "subsections": sum(s.subsections for s in items),
        "todos": sum(s.todos for s in items),
    }


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def sort_spine_p_id(node_id: str) -> tuple[int, str]:
    match = re.match(r"P(\d+)", node_id)
    if match:
        return int(match.group(1)), node_id
    return 999, node_id


def sort_spine_mb_id(node_id: str) -> tuple[str, str]:
    return node_id, node_id


def build_report() -> str:
    toc_entries = parse_toc()
    page_spans = assign_page_spans(toc_entries)

    numbered_chapters = [e for e in toc_entries if e.kind == "chapter" and e.number]
    numbered_chapters_by_title = {
        normalize_title(e.title): e for e in numbered_chapters
    }
    frontmatter_toc = [e for e in toc_entries if e.kind == "frontmatter"]
    appendix_toc = [e for e in toc_entries if e.kind == "appendix"]

    frontmatter_stats: list[FileStats] = []
    for rel in FRONTMATTER_FILES:
        path = ROOT / rel
        if not path.exists():
            continue
        title = FRONTMATTER_TOC_TITLES.get(path.name, path.stem)
        stats = analyze_tex(path, group="frontmatter", title=title)
        span = page_spans.get(("frontmatter", title))
        if span is not None:
            stats.pages = span
            for entry in frontmatter_toc:
                if entry.title == title:
                    stats.page_start = entry.page_label
                    break
        frontmatter_stats.append(stats)

    chapter_stats: list[FileStats] = []
    chapter_files = discover_chapter_files()
    for rel in chapter_files:
        path = ROOT / rel
        stats = analyze_tex(path, group="chapter")
        toc_entry = numbered_chapters_by_title.get(normalize_title(stats.title))
        if toc_entry:
            span = page_spans.get(("chapter", toc_entry.number))
            if span is not None:
                stats.pages = span
                stats.page_start = toc_entry.page_label
        chapter_stats.append(stats)

    appendix_stats: list[FileStats] = []
    for idx, rel in enumerate(discover_appendix_files()):
        path = ROOT / rel
        stats = analyze_tex(path, group="appendix")
        if idx < len(appendix_toc):
            toc_entry = appendix_toc[idx]
            stats.title = toc_entry.title or stats.title
            span = page_spans.get(("appendix", toc_entry.number))
            if span is not None:
                stats.pages = span
                stats.page_start = toc_entry.page_label
        appendix_stats.append(stats)

    metadata_stats: list[FileStats] = []
    for path in sorted((ROOT / "metadata").glob("*.tex")):
        metadata_stats.append(analyze_tex(path, group="metadata", title=path.name))

    tables_stats: list[FileStats] = []
    for path in sorted((ROOT / "tables").glob("*.tex")):
        tables_stats.append(analyze_tex(path, group="tables", title=path.name))

    all_body = frontmatter_stats + chapter_stats + appendix_stats
    all_tex = all_body + metadata_stats + tables_stats

    cited_keys: set[str] = set()
    all_labels: set[str] = set()
    for stats in all_tex:
        cited_keys.update(stats.cite_keys)
        all_labels.update(stats.label_keys)

    bib_total, bib_per_file = load_bibliography_stats()
    totals = sum_stats(all_body)
    grand = sum_stats(all_tex)

    lean_modules = [analyze_lean(p) for p in discover_lean_files()]
    lean_totals = sum_lean_stats(lean_modules)
    all_p_ids: set[str] = set()
    all_mb_ids: set[str] = set()
    for mod in lean_modules:
        all_p_ids.update(mod.spine_p_ids)
        all_mb_ids.update(mod.spine_mb_ids)
    leanspine_total, leanspine_nodes, leanspine_by_chapter = count_leanspine_refs()
    file_inventory = discover_book_file_inventory()
    tex_categories = file_inventory.tex_by_category()
    book_text_rels = sorted(file_inventory.tex_files | file_inventory.bib_files | {m.path for m in lean_modules})
    book_text_paths = [ROOT / rel for rel in book_text_rels]
    book_text_words, book_text_tokens, book_text_chars = sum_plain_text_stats(book_text_paths)
    source_extracts = [analyze_source_extract(p) for p in discover_source_extracts()]
    source_extract_words = sum(s.words for s in source_extracts)
    source_extract_tokens = sum(s.approx_tokens for s in source_extracts)
    source_extract_chars = sum(s.chars for s in source_extracts)
    combined_text_files = len(book_text_paths) + len(source_extracts)
    combined_text_words = book_text_words + source_extract_words
    combined_text_tokens = book_text_tokens + source_extract_tokens
    combined_text_chars = book_text_chars + source_extract_chars

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    pdf_pages = pdf_page_count()
    page_source = "book.toc (+ book.log for PDF total)" if toc_entries else "not built (no book.toc)"

    lines: list[str] = [
        "# Book statistics",
        "",
        f"Generated: {generated}",
        "",
        "## Summary",
        "",
        f"- **PDF pages** (built): {fmt_int(pdf_pages)}",
        f"- **Page spans** source: {page_source}",
        f"- **Frontmatter files**: {len(frontmatter_stats)}",
        f"- **Chapters**: {len(chapter_stats)}",
        f"- **Appendices**: {len(appendix_stats)}",
        f"- **Contributing files (PDF build)**: {file_inventory.pdf_total:,} "
        f"({len(file_inventory.tex_files):,} TeX, {len(file_inventory.bib_files):,} `.bib`, "
        f"{len(file_inventory.figure_files):,} figures)",
        f"- **All book sources (PDF + Lean)**: {file_inventory.pdf_total + len(lean_modules):,} files",
        f"- **Body words** (frontmatter + chapters + appendices): {totals['words']:,}",
        f"- **All counted TeX words** (+ metadata/tables): {grand['words']:,}",
        f"- **Book text sources, no `context/`** (TeX + `.bib` + Lean): {len(book_text_paths):,} files, "
        f"{book_text_words:,} words, ~{book_text_tokens:,} LLM tokens",
        f"- **Context source extracts only** (`context/extracts/*.md`): {len(source_extracts):,} files, "
        f"{source_extract_words:,} words, ~{source_extract_tokens:,} LLM tokens",
        f"- **Book text sources + context extracts**: {combined_text_files:,} files, "
        f"{combined_text_words:,} words, ~{combined_text_tokens:,} LLM tokens",
        f"- **TeX LOC (body)**: {totals['code_loc']:,} code lines "
        f"({totals['loc']:,} non-blank, {totals['lines']:,} total)",
        f"- **TeX LOC (all counted)**: {grand['code_loc']:,} code lines "
        f"({grand['loc']:,} non-blank, {grand['lines']:,} total)",
        f"- **Body PDF pages** (sum of TOC spans): {totals['pages']:,}" if totals["pages"] else "- **Body PDF pages**: — (build PDF to populate book.toc)",
        f"- **Unique citation keys used**: {len(cited_keys):,}",
        f"- **Bibliography entries** (all `.bib` files): {bib_total:,}",
        f"- **Uncited bibliography entries**: {max(bib_total - len(cited_keys), 0):,}",
        f"- **Unique anchors** (`\\label{{...}}`): {len(all_labels):,}",
        f"- **Display math blocks**: {totals['formulas']:,}",
        f"- **Figures / tables**: {totals['figures']:,} / {totals['tables']:,}",
        f"- **Sections / subsections**: {totals['sections']:,} / {totals['subsections']:,}",
        f"- **TODO markers**: {totals['todos']:,}",
        f"- **Lean modules**: {len(lean_modules):,}",
        f"- **Lean LOC**: {lean_totals['code_loc']:,} code lines "
        f"({lean_totals['loc']:,} non-blank, {lean_totals['lines']:,} total)",
        f"- **Lean spine P nodes** (unique `P*` IDs): {len(all_p_ids):,} ({lean_totals['spine_p_theorems']:,} named theorems/lemmas)",
        f"- **Lean spine MB bridges** (unique `MB*` axioms): {len(all_mb_ids):,}",
        f"- **Lean declarations**: {lean_totals['theorems']:,} theorems, {lean_totals['lemmas']:,} lemmas, "
        f"{lean_totals['defs']:,} defs, {lean_totals['structures']:,} structures, {lean_totals['axioms']:,} axioms",
        f"- **\\leanspine cross-refs** in manuscript: {leanspine_total:,} ({len(leanspine_nodes):,} distinct node IDs cited)",
        "",
        "## Source material extracts",
        "",
        "Markdown extracts in `context/extracts/` are the book-local readable copies of source PDFs.",
        "Token counts are approximate LLM-token estimates using `ceil(UTF-8 bytes / 4)`, not a model-specific tokenizer.",
        f"Combined text-source total including book sources and context extracts: {combined_text_files:,} files, "
        f"{combined_text_words:,} words, ~{combined_text_tokens:,} LLM tokens.",
        "",
        render_table(
            ["File", "Words", "Approx. tokens", "Chars", "Lines"],
            [
                [
                    s.path,
                    fmt_int(s.words),
                    fmt_int(s.approx_tokens),
                    fmt_int(s.chars),
                    fmt_int(s.lines),
                ]
                for s in source_extracts
            ]
            + [
                [
                    "**Total**",
                    f"**{source_extract_words:,}**",
                    f"**~{source_extract_tokens:,}**",
                    f"**{source_extract_chars:,}**",
                    f"**{sum(s.lines for s in source_extracts):,}**",
                ]
            ],
        ),
        "",
        "## Contributing files",
        "",
        "Files reached from `book.tex` via `\\input`, `\\addbibresource`, and `\\includegraphics`.",
        "",
        render_table(
            ["Category", "Files"],
            [[name, str(len(paths))] for name, paths in tex_categories.items()]
            + [["Bibliography (`.bib`)", str(len(file_inventory.bib_files))]]
            + [["Figures", str(len(file_inventory.figure_files))]]
            + [["**PDF build total**", f"**{file_inventory.pdf_total:,}**"]]
            + [["Lean spine (`.lean`, not in PDF)", str(len(lean_modules))]]
            + [["**All book sources**", f"**{file_inventory.pdf_total + len(lean_modules):,}**"]],
        ),
        "",
        "## TeX LOC",
        "",
        render_table(
            ["Scope", "Files", "Total", "LOC", "Code"],
            [
                ["Frontmatter", str(len(frontmatter_stats)), *[fmt_int(sum_stats(frontmatter_stats)[k]) for k in ("lines", "loc", "code_loc")]],
                ["Chapters", str(len(chapter_stats)), *[fmt_int(sum_stats(chapter_stats)[k]) for k in ("lines", "loc", "code_loc")]],
                ["Appendices", str(len(appendix_stats)), *[fmt_int(sum_stats(appendix_stats)[k]) for k in ("lines", "loc", "code_loc")]],
                ["Metadata", str(len(metadata_stats)), *[fmt_int(sum_stats(metadata_stats)[k]) for k in ("lines", "loc", "code_loc")]],
                ["Tables", str(len(tables_stats)), *[fmt_int(sum_stats(tables_stats)[k]) for k in ("lines", "loc", "code_loc")]],
                [
                    "**Body**",
                    str(len(all_body)),
                    f"**{totals['lines']:,}**",
                    f"**{totals['loc']:,}**",
                    f"**{totals['code_loc']:,}**",
                ],
                [
                    "**All counted**",
                    str(len(all_tex)),
                    f"**{grand['lines']:,}**",
                    f"**{grand['loc']:,}**",
                    f"**{grand['code_loc']:,}**",
                ],
            ],
        ),
        "",
        "## Frontmatter",
        "",
        render_table(
            ["File", "Words", "Total", "LOC", "Code", "Pages", "Cites", "Labels", "Formulas", "TODOs"],
            [
                [
                    s.path,
                    fmt_int(s.words),
                    fmt_int(s.lines),
                    fmt_int(s.loc),
                    fmt_int(s.code_loc),
                    fmt_int(s.pages),
                    fmt_int(s.citations),
                    fmt_int(s.labels),
                    fmt_int(s.formulas),
                    fmt_int(s.todos),
                ]
                for s in frontmatter_stats
            ]
            + [
                [
                    "**Subtotal**",
                    f"**{sum_stats(frontmatter_stats)['words']:,}**",
                    f"**{sum_stats(frontmatter_stats)['lines']:,}**",
                    f"**{sum_stats(frontmatter_stats)['loc']:,}**",
                    f"**{sum_stats(frontmatter_stats)['code_loc']:,}**",
                    f"**{sum_stats(frontmatter_stats)['pages']:,}**" if sum_stats(frontmatter_stats)["pages"] else "**—**",
                    f"**{sum_stats(frontmatter_stats)['citations']:,}**",
                    f"**{sum_stats(frontmatter_stats)['labels']:,}**",
                    f"**{sum_stats(frontmatter_stats)['formulas']:,}**",
                    f"**{sum_stats(frontmatter_stats)['todos']:,}**",
                ]
            ],
        ),
        "",
        "## Chapters",
        "",
        render_table(
            ["#", "File", "Title", "Words", "Total", "LOC", "Code", "Pages", "Cites", "Labels", "Formulas", "Secs", "TODOs"],
            [
                [
                    str(idx + 1),
                    s.path,
                    s.title[:60] + ("…" if len(s.title) > 60 else ""),
                    fmt_int(s.words),
                    fmt_int(s.lines),
                    fmt_int(s.loc),
                    fmt_int(s.code_loc),
                    fmt_int(s.pages),
                    fmt_int(s.citations),
                    fmt_int(s.labels),
                    fmt_int(s.formulas),
                    fmt_int(s.sections),
                    fmt_int(s.todos),
                ]
                for idx, s in enumerate(chapter_stats)
            ]
            + [
                [
                    "",
                    "**Subtotal**",
                    "",
                    f"**{sum_stats(chapter_stats)['words']:,}**",
                    f"**{sum_stats(chapter_stats)['lines']:,}**",
                    f"**{sum_stats(chapter_stats)['loc']:,}**",
                    f"**{sum_stats(chapter_stats)['code_loc']:,}**",
                    f"**{sum_stats(chapter_stats)['pages']:,}**" if sum_stats(chapter_stats)["pages"] else "**—**",
                    f"**{sum_stats(chapter_stats)['citations']:,}**",
                    f"**{sum_stats(chapter_stats)['labels']:,}**",
                    f"**{sum_stats(chapter_stats)['formulas']:,}**",
                    f"**{sum_stats(chapter_stats)['sections']:,}**",
                    f"**{sum_stats(chapter_stats)['todos']:,}**",
                ]
            ],
        ),
        "",
        "## Appendices",
        "",
        render_table(
            ["File", "Title", "Words", "Total", "LOC", "Code", "Pages", "Cites", "Labels", "Formulas"],
            [
                [
                    s.path,
                    s.title[:50] + ("…" if len(s.title) > 50 else ""),
                    fmt_int(s.words),
                    fmt_int(s.lines),
                    fmt_int(s.loc),
                    fmt_int(s.code_loc),
                    fmt_int(s.pages),
                    fmt_int(s.citations),
                    fmt_int(s.labels),
                    fmt_int(s.formulas),
                ]
                for s in appendix_stats
            ]
            + [
                [
                    "**Subtotal**",
                    "",
                    f"**{sum_stats(appendix_stats)['words']:,}**",
                    f"**{sum_stats(appendix_stats)['lines']:,}**",
                    f"**{sum_stats(appendix_stats)['loc']:,}**",
                    f"**{sum_stats(appendix_stats)['code_loc']:,}**",
                    f"**{sum_stats(appendix_stats)['pages']:,}**" if sum_stats(appendix_stats)["pages"] else "**—**",
                    f"**{sum_stats(appendix_stats)['citations']:,}**",
                    f"**{sum_stats(appendix_stats)['labels']:,}**",
                    f"**{sum_stats(appendix_stats)['formulas']:,}**",
                ]
            ],
        ),
        "",
        "## Bibliography",
        "",
        render_table(
            ["File", "Entries"],
            [[name, str(count)] for name, count in sorted(bib_per_file.items())]
            + [["**Total unique keys**", f"**{bib_total:,}**"]],
        ),
        "",
        "## Lean proof spine",
        "",
        render_table(
            [
                "Module",
                "Total",
                "LOC",
                "Code",
                "Thms",
                "Lems",
                "Defs",
                "Struct",
                "Axioms",
                "P*",
                "MB*",
            ],
            [
                [
                    s.path,
                    fmt_int(s.lines),
                    fmt_int(s.loc),
                    fmt_int(s.code_loc),
                    fmt_int(s.theorems),
                    fmt_int(s.lemmas),
                    fmt_int(s.defs + s.abbrevs),
                    fmt_int(s.structures),
                    fmt_int(s.axioms),
                    fmt_int(len(s.spine_p_ids)),
                    fmt_int(len(s.spine_mb_ids)),
                ]
                for s in lean_modules
            ]
            + [
                [
                    "**Subtotal**",
                    f"**{lean_totals['lines']:,}**",
                    f"**{lean_totals['loc']:,}**",
                    f"**{lean_totals['code_loc']:,}**",
                    f"**{lean_totals['theorems']:,}**",
                    f"**{lean_totals['lemmas']:,}**",
                    f"**{lean_totals['defs'] + lean_totals['abbrevs']:,}**",
                    f"**{lean_totals['structures']:,}**",
                    f"**{lean_totals['axioms']:,}**",
                    f"**{len(all_p_ids):,}**",
                    f"**{len(all_mb_ids):,}**",
                ]
            ],
        ),
        "",
        "### Spine node inventory",
        "",
        f"- **P nodes** ({len(all_p_ids)}): {', '.join(sorted(all_p_ids, key=sort_spine_p_id))}",
        f"- **MB bridges** ({len(all_mb_ids)}): {', '.join(sorted(all_mb_ids, key=sort_spine_mb_id))}",
        "",
    ]

    if leanspine_by_chapter:
        lines.extend(
            [
                "### \\leanspine cross-refs by chapter",
                "",
                render_table(
                    ["Chapter file", "Refs"],
                    [[path, str(count)] for path, count in leanspine_by_chapter.items()]
                    + [["**Total**", f"**{leanspine_total:,}**"]],
                ),
                "",
            ]
        )

    lines.extend(
        [
        "## Notes",
        "",
        "- **Words**: LaTeX commands and comments stripped; approximate prose count.",
        "- **TeX LOC**: **Code** = non-blank lines excluding comment-only (`%`, respecting `\\%`); **LOC** = all non-blank lines.",
        "- **Contributing files**: Transitive closure from `book.tex`; figures only if the path resolves on disk.",
        "- **Pages**: Per-unit spans from `book.toc` when present; run `./build.sh` first for accurate values.",
        "- **Formulas**: Counts `equation`, `align`, `gather`, `multline`, and `\\[` environments (not inline `$...$`).",
        "- **Cites**: Counts `\\autocite`, `\\cite`, `\\parencite`, `\\textcite`, `\\footcite` invocations.",
        "- **Labels**: Counts `\\label{...}` anchors (includes chapters, sections, figures, equations).",
        "- **Lean P\\***: Unique proof-spine node IDs from `theorem`/`lemma` names (`P01`, `P22a`, `P36R`, …).",
        "- **Lean MB\\***: Explicit bridge axioms (`MB1`–`MB9`, including split `MB6a`/`MB6b`, `MB7a`–`MB7d`).",
        "- **Lean LOC**: **Code** = non-blank lines excluding comment-only (`--` and single-line `/- -/`); **LOC** = all non-blank lines.",
        "- **Lean counts**: Line-anchored declarations; multi-line signatures count at the opening line only.",
        "",
        ]
    )

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate book statistics markdown report.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=ROOT / "metadata" / "book-stats.md",
        help="Output markdown path (default: metadata/book-stats.md)",
    )
    args = parser.parse_args()

    report = build_report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"Wrote {args.output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
