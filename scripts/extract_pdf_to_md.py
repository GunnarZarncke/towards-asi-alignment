#!/usr/bin/env python3
"""Extract context PDFs to markdown with formulas preserved as LaTeX."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import fitz

UNICODE_TO_LATEX = {
    "α": r"\alpha",
    "β": r"\beta",
    "γ": r"\gamma",
    "δ": r"\delta",
    "ε": r"\epsilon",
    "ζ": r"\zeta",
    "η": r"\eta",
    "θ": r"\theta",
    "ι": r"\iota",
    "κ": r"\kappa",
    "λ": r"\lambda",
    "μ": r"\mu",
    "ν": r"\nu",
    "ξ": r"\xi",
    "π": r"\pi",
    "ρ": r"\rho",
    "σ": r"\sigma",
    "τ": r"\tau",
    "υ": r"\upsilon",
    "φ": r"\phi",
    "χ": r"\chi",
    "ψ": r"\psi",
    "ω": r"\omega",
    "Γ": r"\Gamma",
    "Δ": r"\Delta",
    "Θ": r"\Theta",
    "Λ": r"\Lambda",
    "Ξ": r"\Xi",
    "Π": r"\Pi",
    "Σ": r"\Sigma",
    "Φ": r"\Phi",
    "Ψ": r"\Psi",
    "Ω": r"\Omega",
    "∂": r"\partial",
    "∇": r"\nabla",
    "∑": r"\sum",
    "∏": r"\prod",
    "∫": r"\int",
    "√": r"\sqrt",
    "∞": r"\infty",
    "≈": r"\approx",
    "≠": r"\neq",
    "≤": r"\leq",
    "≥": r"\geq",
    "±": r"\pm",
    "×": r"\times",
    "÷": r"\div",
    "∈": r"\in",
    "∉": r"\notin",
    "⊂": r"\subset",
    "⊃": r"\supset",
    "∪": r"\cup",
    "∩": r"\cap",
    "→": r"\to",
    "←": r"\leftarrow",
    "↔": r"\leftrightarrow",
    "⇒": r"\Rightarrow",
    "⇔": r"\Leftrightarrow",
    "∀": r"\forall",
    "∃": r"\exists",
    "∧": r"\land",
    "∨": r"\lor",
    "¬": r"\neg",
    "⊕": r"\oplus",
    "⊗": r"\otimes",
    "⟨": r"\langle",
    "⟩": r"\rangle",
    "ϕ": r"\phi",
}

MATH_CHARS = set(UNICODE_TO_LATEX) | set("=_<>+-*/^\\{}[]()0123456789")
SECTION_RE = re.compile(r"^([IVXLC]+\.\s+[A-Z].{3,80})$")
NUMBERED_RE = re.compile(r"^(\d+\.\s+[A-Z].{3,120})$")


def clean_text(text: str) -> str:
    text = text.replace("\x00", "")
    text = re.sub(r"[\x01-\x08\x0b\x0c\x0e-\x1f]", "", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def slugify(name: str) -> str:
    stem = Path(name).stem.lower()
    stem = re.sub(r"[^a-z0-9]+", "-", stem)
    return stem.strip("-")


def to_latex(text: str) -> str:
    out = text
    for uni, latex in UNICODE_TO_LATEX.items():
        out = out.replace(uni, latex)
    return out


def is_display_equation(line: str) -> bool:
    s = line.strip()
    if len(s) < 3 or len(s) > 220:
        return False
    if s.endswith(".") and not any(c in s for c in "=<>≤≥"):
        return False
    math_count = sum(1 for c in s if c in MATH_CHARS)
    greek_count = sum(1 for c in s if c in UNICODE_TO_LATEX)
    if greek_count >= 1 and math_count >= 2:
        return True
    if math_count / max(len(s), 1) > 0.35 and any(op in s for op in ("=", "≤", "≥", "→", "∂", "∑", "∫")):
        return True
    if re.fullmatch(r"\(?\d+\)?", s):
        return True
    return False


def format_line(line: str) -> str:
    stripped = line.strip()
    if not stripped:
        return ""

    if SECTION_RE.match(stripped):
        return f"## {stripped}"

    if NUMBERED_RE.match(stripped):
        return f"### {stripped}"

    if is_display_equation(stripped):
        return f"$$\n{to_latex(stripped)}\n$$"

    converted = to_latex(stripped)
    if converted != stripped:
        return converted
    return stripped


def join_broken_equations(lines: list[str]) -> list[str]:
    """Merge consecutive short math fragments split across PDF lines."""
    out: list[str] = []
    buf: list[str] = []

    def flush() -> None:
        nonlocal buf
        if not buf:
            return
        merged = " ".join(part.strip() for part in buf)
        out.append(format_line(merged))
        buf = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            flush()
            out.append("")
            continue

        if buf:
            buf.append(stripped)
            joined = " ".join(buf)
            if is_display_equation(joined) or len(joined) > 100:
                flush()
            elif len(buf) > 4:
                flush()
            continue

        if is_display_equation(stripped) and len(stripped) < 40:
            buf = [stripped]
        else:
            out.append(format_line(stripped))

    flush()
    return out


def page_to_markdown(text: str) -> str:
    lines = [ln.rstrip() for ln in text.splitlines()]
    formatted = join_broken_equations(lines)
    paragraphs: list[str] = []
    current: list[str] = []

    for line in formatted:
        if not line:
            if current:
                paragraphs.append("\n".join(current))
                current = []
            continue
        if line.startswith("## ") or line.startswith("### ") or line.startswith("$$"):
            if current:
                paragraphs.append("\n".join(current))
                current = []
            paragraphs.append(line)
        else:
            current.append(line)

    if current:
        paragraphs.append("\n".join(current))

    return "\n\n".join(paragraphs)


def extract_pdf(pdf_path: Path, out_dir: Path) -> Path:
    doc = fitz.open(pdf_path)
    page_chunks: list[str] = []
    for page in doc:
        raw = page.get_text("text")
        page_chunks.append(page_to_markdown(raw))

    content = "\n\n---\n\n".join(page_chunks)
    out_path = out_dir / f"{slugify(pdf_path.name)}.md"
    header = (
        f"# Extract: {pdf_path.name}\n\n"
        f"**Source PDF:** `context/{pdf_path.name}`  \n"
        f"**Extract:** `context/extracts/{out_path.name}`  \n"
        f"**Pages:** {len(doc)}  \n"
        f"**Note:** Auto-extracted for agent/manuscript use. Display equations use `$$...$$`; "
        f"Unicode math symbols are converted to LaTeX where possible.\n"
    )
    out_path.write_text(clean_text(header + "\n" + content), encoding="utf-8")
    doc.close()
    return out_path


def main(argv: list[str]) -> int:
    root = Path(__file__).resolve().parents[1]
    context_dir = root / "context"
    out_dir = context_dir / "extracts"
    out_dir.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(context_dir.glob("*.pdf"))
    if not pdfs:
        print("No PDFs found in context/", file=sys.stderr)
        return 1

    for pdf in pdfs:
        out = extract_pdf(pdf, out_dir)
        print(out.relative_to(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
