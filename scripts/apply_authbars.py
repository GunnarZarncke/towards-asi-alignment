#!/usr/bin/env python3
"""Wrap section bodies in chapters/appendices with \\begin{authbar}{key} ... \\end{authbar}.

Skips: figures, epigraphs, existing authbar blocks.
Wraps: chapterthesis, epistemicstatus, leanbox bodies; each section/subsection body.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = sorted((ROOT / "chapters").glob("ch*.tex"))
APPENDICES = sorted((ROOT / "appendices").glob("app*.tex"))
WIRED_APPENDICES = {
    "appA-notation.tex",
    "appB-bridge-crosswalk.tex",
    "appC-institutional-translation.tex",
    "appM-institutional-histories.tex",
    "appD-worked-example.tex",
    "appE-glossary.tex",
    "appF-research-program.tex",
    "appG-lean-proof-spine.tex",
    "appN-experimental-evidence.tex",
}

GZ_AI_CHAPTERS = {1, 6, 7, 9}
SKIP_ENVS = {
    "figure",
    "figure*",
    "table",
    "table*",
    "longtable",
    "landscape",
    "sideways",
    "tikzpicture",
    "tikzpicture*",
    "picture",
    "picture*",
    "subfigure",
    "subfigure*",
    "authbar",
}
INPUTS_OUTSIDE_AUTHBAR = (
    "tables/",
)
WRAP_ENVS = {"chapterthesis", "epistemicstatus", "leanbox"}
EPISTEMIC_AUTH_KEY = "GZ+AI"
SUMMARY_SECTION = re.compile(r"^\\section\{Summary\}")
CHAPTER_REFS_SECTION = re.compile(r"^\\section\*\{Chapter References\}")
SECTION_RE = re.compile(r"^\\(section|subsection)(\*)?\{")
HEADER_TAIL_RE = re.compile(r"^\\(label|phantomsection)\{")
CHAPTER_RE = re.compile(r"^\\chapter(\*)?\{")


def chapter_auth_key(path: Path) -> str:
    m = re.search(r"ch(\d+)", path.name)
    if m and int(m.group(1)) in GZ_AI_CHAPTERS:
        return "GZ+AI"
    return "AI"


def appendix_auth_key(_path: Path) -> str:
    return "AI"


def is_comment_or_blank(line: str) -> bool:
    s = line.strip()
    return not s or s.startswith("%")


def is_header_tail(line: str) -> bool:
    s = line.strip()
    return bool(HEADER_TAIL_RE.match(s)) or s.startswith("%")


MACRO_DEF_RE = re.compile(
    r"^\\(newcommand|renewcommand|providecommand|DeclareRobustCommand|def)\*?"
)


def copy_brace_block(lines: list[str], start: int) -> tuple[list[str], int]:
    chunk = [lines[start]]
    depth = lines[start].count("{") - lines[start].count("}")
    i = start + 1
    while i < len(lines) and depth > 0:
        chunk.append(lines[i])
        depth += lines[i].count("{") - lines[i].count("}")
        i += 1
    return chunk, i


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines(keepends=True)


def write_lines(path: Path, lines: list[str]) -> None:
    path.write_text("".join(lines), encoding="utf-8")


def find_env_end(lines: list[str], start: int, env: str) -> int:
    """Return index of line with \\end{env} (same nesting level)."""
    depth = 1
    begin_pat = re.compile(rf"\\begin\{{{re.escape(env)}\}}")
    end_pat = re.compile(rf"\\end\{{{re.escape(env)}\}}")
    i = start + 1
    while i < len(lines):
        if begin_pat.search(lines[i]):
            depth += 1
        if end_pat.search(lines[i]):
            depth -= 1
            if depth == 0:
                return i
        i += 1
    raise ValueError(f"Unclosed environment {env} at line {start + 1}")


def copy_epigraph(lines: list[str], start: int) -> tuple[list[str], int]:
    """Copy a \\epigraph{...}{...} block starting at start."""
    chunk = [lines[start]]
    i = start + 1
    # epigraph usually spans multiple lines; copy until we have balanced outer call.
    text = lines[start]
    while i < len(lines) and text.count("{") > text.count("}"):
        chunk.append(lines[i])
        text += lines[i]
        i += 1
    return chunk, i


def process_file(path: Path, key: str) -> bool:
    lines = read_lines(path)
    if any("\\begin{authbar}" in ln for ln in lines):
        print(f"skip (already marked): {path.relative_to(ROOT)}")
        return False

    out: list[str] = []
    i = 0
    in_authbar = False
    seen_section = False
    pending_authbar_key: str | None = None

    def cancel_pending_authbar() -> None:
        nonlocal pending_authbar_key
        pending_authbar_key = None

    def close_authbar() -> None:
        nonlocal in_authbar
        if in_authbar:
            out.append("\\end{authbar}\n")
            in_authbar = False

    def open_authbar() -> None:
        open_authbar_with_key(key)

    def open_authbar_with_key(bar_key: str) -> None:
        nonlocal in_authbar, pending_authbar_key
        pending_authbar_key = None
        if not in_authbar:
            out.append(f"\\begin{{authbar}}{{{bar_key}}}\n")
            in_authbar = True

    def ensure_authbar_open() -> None:
        if pending_authbar_key is not None:
            open_authbar_with_key(pending_authbar_key)

    def emit_content(line: str) -> None:
        ensure_authbar_open()
        out.append(line)

    while i < len(lines):
        line = lines[i]

        if line.strip().startswith("\\begin{authbar}"):
            close_authbar()
            out.append(line)
            i += 1
            continue

        if line.strip().startswith("\\end{authbar}"):
            out.append(line)
            in_authbar = False
            i += 1
            continue

        if MACRO_DEF_RE.match(line.strip()):
            cancel_pending_authbar()
            close_authbar()
            chunk, i = copy_brace_block(lines, i)
            out.extend(chunk)
            continue

        if line.strip().startswith("\\input{"):
            for prefix in INPUTS_OUTSIDE_AUTHBAR:
                if prefix in line:
                    cancel_pending_authbar()
                    close_authbar()
                    break
            out.append(line)
            i += 1
            continue

        begin_m = re.search(r"\\begin\{([^}]+)\}", line)
        if begin_m:
            env = begin_m.group(1)
            if env in SKIP_ENVS:
                cancel_pending_authbar()
                close_authbar()
                end_i = find_env_end(lines, i, env)
                out.extend(lines[i : end_i + 1])
                i = end_i + 1
                continue
            if env in WRAP_ENVS:
                cancel_pending_authbar()
                close_authbar()
                end_i = find_env_end(lines, i, env)
                wrap_key = EPISTEMIC_AUTH_KEY if env == "epistemicstatus" else key
                open_authbar_with_key(wrap_key)
                out.extend(lines[i : end_i + 1])
                close_authbar()
                i = end_i + 1
                continue

        if line.strip().startswith("\\epigraph"):
            cancel_pending_authbar()
            close_authbar()
            chunk, i = copy_epigraph(lines, i)
            out.extend(chunk)
            continue

        sec_m = SECTION_RE.match(line.strip())
        if sec_m:
            seen_section = True
            cancel_pending_authbar()
            close_authbar()
            kind = sec_m.group(1)
            starred = sec_m.group(2)
            section_title = ""
            title_m = re.search(r"\{([^}]*)\}", line.strip())
            if title_m:
                section_title = title_m.group(1)
            body_key = key
            if SUMMARY_SECTION.match(line.strip()) or (
                starred and section_title == "Chapter References"
            ):
                body_key = "AI"
            needspace = "\\authbarsubneedspace\n" if kind == "subsection" else "\\authbarneedspace\n"
            out.append(needspace)
            out.append(line)
            i += 1
            while i < len(lines) and is_header_tail(lines[i]):
                out.append(lines[i])
                i += 1
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            pending_authbar_key = body_key
            continue

        if CHAPTER_RE.match(line.strip()) or line.strip().startswith("\\end{refsection}"):
            cancel_pending_authbar()
            close_authbar()
            out.append(line)
            i += 1
            continue

        if line.strip().startswith("\\begin{refsection}"):
            cancel_pending_authbar()
            close_authbar()
            out.append(line)
            i += 1
            continue

        # Chapter-level intro prose (appendices) before first section.
        if not seen_section and not is_comment_or_blank(line):
            if not in_authbar and not line.strip().startswith("\\"):
                open_authbar()
            elif not in_authbar and line.strip().startswith("\\") and not CHAPTER_RE.match(line.strip()):
                # e.g. \label after \chapter — stay outside authbar
                out.append(line)
                i += 1
                continue

        emit_content(line)
        i += 1

    cancel_pending_authbar()
    close_authbar()
    write_lines(path, out)
    print(f"marked: {path.relative_to(ROOT)} ({key})")
    return True


def main() -> int:
    changed = 0
    for path in CHAPTERS:
        if process_file(path, chapter_auth_key(path)):
            changed += 1
    for path in APPENDICES:
        if path.name not in WIRED_APPENDICES:
            continue
        if process_file(path, appendix_auth_key(path)):
            changed += 1
    print(f"Done. Updated {changed} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
