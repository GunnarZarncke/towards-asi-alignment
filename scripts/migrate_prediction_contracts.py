#!/usr/bin/env python3
"""One-off migrator: split legacy predictionbox content into four contract environments."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "appendices/appP-bridge-predictions.tex"

DEFAULT_CHOICES = (
    r"\textbf{Choices.} YES, NO, and OTHER as defined in this appendix's reading rules."
)
MARKET20_CHOICES = (
    r"\textbf{Choices.} YES and OTHER as defined in this appendix's reading rules."
)

RESOLUTION_MARKERS = (
    r"\\textbf\{YES requires\}|"
    r"\\textbf\{The challenge qualifies\}|"
    r"\\textbf\{The tournament conditions\}|"
    r"\\textbf\{A registered stack is a qualifying attempt if\}|"
    r"\\textbf\{The performance bars are met if\}|"
    r"\\textbf\{What a stack is\}|"
    r"\\textbf\{Case labels\}|"
    r"\\textbf\{Terms\}"
)


def split_at_resolution(text: str) -> tuple[str, str]:
    m = re.search(RESOLUTION_MARKERS, text)
    if not m:
        return text.strip(), ""
    return text[: m.start()].strip(), text[m.start() :].strip()


def split_resolution_output(resolution: str) -> tuple[str, str]:
    m = re.search(r"\\textbf\{Output\.\}", resolution)
    if not m:
        return resolution.strip(), ""
    return resolution[: m.start()].strip(), resolution[m.start() :].strip()


def parse_front(front: str) -> tuple[str, str, str]:
    resolve_m = re.search(
        r"(\\textbf\{Resolve by\.\}[^\n]*(?:\n(?!\\textbf)[^\n]*)*)", front
    )
    if not resolve_m:
        raise ValueError("missing Resolve by")
    resolve_by = resolve_m.group(1).strip()
    rest = front[resolve_m.end() :].strip()
    rest = re.sub(r"^\\textbf\{In plain terms\.\}\s*", "", rest)
    rest = re.sub(r"Parts \d+ .*?posted with it\.\s*", "", rest)
    q_m = re.search(r"\\textbf\{Question\.\}\s*", rest)
    if not q_m:
        raise ValueError("missing Question")
    after_q = rest[q_m.end() :].strip()
    # Question is first paragraph(s) until blank line + non-question content
    q_parts = []
    bg_parts = []
    mode = "q"
    for block in re.split(r"\n\n+", after_q):
        if mode == "q" and (
            block.startswith("\\textbf{")
            or block.startswith("\\paragraph{")
            or re.match(r"^(An |The |Before |Qualifying |A |Example |Positive |Hidden |Attackers |Whether |Every |It |Registration |Deployment |Stack |Failure |Attacks )", block)
        ):
            mode = "bg"
        if mode == "q":
            q_parts.append(block)
        else:
            bg_parts.append(block)
    question = "\\textbf{Question.}\n" + "\n\n".join(q_parts)
    background = "\n\n".join(bg_parts).strip()
    return resolve_by, question, background


def migrate_box_inner(inner: str, choices: str) -> str:
    front, resolution_block = split_at_resolution(inner)
    front = re.sub(r"\\paragraph\{[^}]+\}\.\s*", "", front)
    resolve_by, question, background = parse_front(front)
    resolution, output = split_resolution_output(resolution_block)
    parts = [
        "\\begin{predictionbox}[TITLE]",
        resolve_by,
        "",
        question,
        "",
        choices,
        "\\end{predictionbox}",
    ]
    if background:
        parts.extend(["", "\\begin{predictionbackground}", background, "\\end{predictionbackground}"])
    if resolution or output:
        body = resolution
        if output:
            body = (body + "\n\n" + output).strip() if body else output
        parts.extend(["", "\\begin{predictionresolution}", body, "\\end{predictionresolution}"])
    return "\n".join(parts)


def migrate_market_section(section: str, n: int) -> str:
    if "\\begin{predictionbackground}" in section:
        return section

    auth = re.search(r"\\begin\{authbar\}\{([^}]+)\}", section)
    if not auth:
        return section
    auth_key = auth.group(1)

    intro_m = re.search(
        r"\\begin\{authbar\}\{[^}]+\}\s*(.*?)\s*\\begin\{predictionbox\}",
        section,
        re.S,
    )
    intro = intro_m.group(1).strip() if intro_m else ""

    boxes = re.findall(
        r"\\begin\{predictionbox\}(?:\[([^\]]*)\])?([\s\S]*?)\\end\{predictionbox\}",
        section,
    )
    if not boxes:
        return section
    title = boxes[0][0] or f"Market {n}."
    merged = "\n\n".join(b[1] for b in boxes)

    last_end = section.rindex("\\end{predictionbox}") + len("\\end{predictionbox}")
    tail = section[last_end:].strip()
    tail = re.sub(r"^\\end\{authbar\}\s*", "", tail)
    fine_extra = ""
    closest = tail
    if "Closest existing work" in tail:
        idx = tail.index("Closest existing work")
        fine_extra = tail[:idx].strip()
        closest = tail[idx:].strip()

    choices = MARKET20_CHOICES if n == 20 else DEFAULT_CHOICES
    block = migrate_box_inner(merged, choices).replace("[TITLE]", title)
    if fine_extra:
        block += (
            "\n\n\\begin{predictionfineprint}\n"
            + fine_extra
            + "\n\\end{predictionfineprint}"
        )

    out = f"\\begin{{authbar}}{{{auth_key}}}\n{intro}\n\\end{{authbar}}\n{block}\n"
    if closest:
        out += f"\\begin{{authbar}}{{{auth_key}}}\n{closest}\n\\end{{authbar}}\n"
    return out


def migrate_common(section: str) -> str:
    if "\\begin{predictionbackground}" in section:
        return section
    boxes = re.findall(
        r"\\begin\{predictionbox\}(?:\[([^\]]*)\])?([\s\S]*?)\\end\{predictionbox\}",
        section,
    )
    merged = "\n\n".join(b[1] for b in boxes)
    m1, merged = re.split(r"\\paragraph\{Per-instance certificate\.\}", merged, maxsplit=1)
    m2, m3 = re.split(r"\\paragraph\{Listing question\.\}", merged, maxsplit=1)
    resolution = m1.strip()
    background = ("\\paragraph{Per-instance certificate.}\n" + m2.strip()).strip()
    fine = ("\\paragraph{Listing question.}\n" + m3.strip()).strip()
    fine = fine.replace(
        "Copy the box's Question line as a multiple-choice item with the outcomes that line lists.",
        "Copy each market's Question line and Choices from its front box as a multiple-choice item with the outcomes that line lists.",
    )

    tail_m = re.search(
        r"\\paragraph\{Shared glossary.*?\\end\{authbar\}",
        section,
        re.S,
    )
    tail = tail_m.group(0) if tail_m else ""

    return (
        "\\begin{authbar}{AI}\n\\end{authbar}\n"
        "\\begin{predictionbox}[Common qualification]\n"
        "Rules that apply to every market before a qualifying attempt is scored.\n"
        "\\end{predictionbox}\n\n"
        "\\begin{predictionresolution}\n"
        f"{resolution}\n"
        "\\end{predictionresolution}\n\n"
        "\\begin{predictionbackground}\n"
        f"{background}\n"
        "\\end{predictionbackground}\n\n"
        "\\begin{predictionfineprint}\n"
        f"{fine}\n"
        "\\end{predictionfineprint}\n\n"
        f"{tail}\n"
    )


def main() -> None:
    text = TEX.read_text()
    # Common rules
    common_m = re.search(
        r"(\\section\{Rules that apply to every market\}[\s\S]*?)\\authbarneedspace\n\\section\{How a market",
        text,
    )
    if common_m:
        text = (
            text[: common_m.start(1)]
            + migrate_common(common_m.group(1))
            + text[common_m.end(1) :]
        )

    for n in range(1, 22):
        if n in (19, 20):
            continue
        pat = (
            rf"(\\subsection{{Market {n}\.[\s\S]*?)"
            rf"(?=\\authbarneedspace\n\\subsection{{|\\authbarneedspace\n\\section{{)"
        )
        m = re.search(pat, text)
        if not m:
            print(f"warning: market {n} not found", file=sys.stderr)
            continue
        new_sec = migrate_market_section(m.group(1), n)
        text = text[: m.start(1)] + new_sec + text[m.end(1) :]

    TEX.write_text(text)
    print("migrated", TEX)


if __name__ == "__main__":
    main()
