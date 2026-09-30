#!/usr/bin/env python3
"""One-shot chapter and appendix renumbering to align filenames with print order."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Old YAML/file id → new id (ch01–ch19 unchanged).
CHAPTER_ID_MAP: dict[str, str] = {
    "ch19b": "ch20",
    "ch20": "ch21",
    "ch21": "ch22",
    "ch22": "ch23",
    "ch23": "ch24",
    "ch24": "ch25",
    "ch25": "ch26",
    "ch25b": "ch27",
    "ch26": "ch28",
    "ch27": "ch29",
    "ch28": "ch30",
    "ch29": "ch31",
    "ch30": "ch32",
    "ch31": "ch33",
    "ch32": "ch34",
    "ch33": "ch35",
    "ch34": "ch36",
    "ch35": "ch37",
    "ch35b": "ch38",
    "ch36": "ch39",
    "ch37": "ch40",
    "ch38": "ch41",
    "ch39": "ch42",
    "ch39b": "ch43",
    "ch40": "ch44",
    "ch41": "ch45",
    "ch42": "ch46",
    "ch43": "ch47",
    "ch44": "ch48",
}

# Old printed chapter number (sequential before renumber) → new number.
# Used for prose like "Chapter 40" where the number matched old print order.
PRINTED_CHAPTER_MAP: dict[int, int] = {i: i for i in range(1, 20)}
PRINTED_CHAPTER_MAP.update(
    {
        20: 20,  # was ch19b
        21: 21,
        22: 22,
        23: 23,
        24: 24,
        25: 25,
        26: 26,
        27: 27,  # was ch25b
        28: 28,
        29: 29,
        30: 30,
        31: 31,
        32: 32,
        33: 33,
        34: 34,
        35: 35,
        36: 36,
        37: 37,
        38: 38,  # was ch35b
        39: 39,
        40: 40,
        41: 41,
        42: 42,
        43: 43,  # was ch39b
        44: 44,
        45: 45,
        46: 46,
        47: 47,
        48: 48,
    }
)

# Filename-based chapter number in prose/docs (old file id number) → new print number.
FILENAME_NUM_TO_PRINT: dict[int, int] = {i: i for i in range(1, 20)}
for old_id, new_id in CHAPTER_ID_MAP.items():
    old_num = int(re.match(r"ch(\d+)", old_id).group(1))
    new_num = int(re.match(r"ch(\d+)", new_id).group(1))
    FILENAME_NUM_TO_PRINT[old_num] = new_num

APPENDIX_RENAMES: list[tuple[str, str]] = [
    ("appBridge-crosswalk", "appB-bridge-crosswalk"),
    ("appJ-institutional-translation", "appC-institutional-translation"),
    ("appK-worked-example", "appD-worked-example"),
    ("appF-glossary", "appE-glossary"),
    ("appH-research-program", "appF-research-program"),
    ("appI-lean-proof-spine", "appG-lean-proof-spine"),
    ("appB-worked-example-agent-boundary", "appH-boundary-worked-example"),
    ("appC-value-bundle-inference", "appI-value-bundle-inference"),
    ("appD-correction-channel-audit", "appJ-correction-channel-audit"),
    ("appE-assumptions", "appL-assumptions"),
    ("appG-safety-case-template", "appK-safety-case-template"),
]

TEXT_GLOBS = (
    "*.md",
    "*.tex",
    "*.yml",
    "*.py",
    "*.lean",
    "*.txt",
)
SKIP_DIRS = {
    ".git",
    ".lake",
    "dist",
    "node_modules",
    "__pycache__",
    ".biber-par-cache",
}


def chapter_files() -> dict[Path, Path]:
    chapters_dir = ROOT / "chapters"
    mapping: dict[Path, Path] = {}
    for path in sorted(chapters_dir.glob("ch*.tex")):
        match = re.match(r"(ch\d+b?)-(.+\.tex)$", path.name)
        if not match:
            raise ValueError(f"Unexpected chapter filename: {path.name}")
        old_prefix, slug = match.groups()
        new_prefix = CHAPTER_ID_MAP.get(old_prefix, old_prefix)
        mapping[path] = chapters_dir / f"{new_prefix}-{slug}"
    return mapping


def rename_via_temp(moves: dict[Path, Path]) -> None:
    temp: dict[Path, Path] = {}
    for src in moves:
        tmp = src.with_name(f"__renumber_tmp__{src.name}")
        if tmp.exists():
            raise FileExistsError(tmp)
        temp[src] = tmp
    for src, tmp in temp.items():
        src.rename(tmp)
    for src, dst in moves.items():
        tmp = temp[src]
        if dst.exists():
            raise FileExistsError(dst)
        tmp.rename(dst)


def replace_in_text(text: str) -> str:
    # Longest ids first so ch19b is not partially matched as ch19.
    for old_id in sorted(CHAPTER_ID_MAP, key=len, reverse=True):
        new_id = CHAPTER_ID_MAP[old_id]
        text = text.replace(old_id, new_id)

    for old_slug, new_slug in APPENDIX_RENAMES:
        text = text.replace(f"appendices/{old_slug}", f"appendices/{new_slug}")
        text = text.replace(old_slug, new_slug)

    return text


def rewrite_book_yml() -> None:
    path = ROOT / "metadata" / "book.yml"
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    out: list[str] = []
    in_chapters = False
    chapter_blocks: dict[str, list[str]] = {}
    current: str | None = None

    for line in lines:
        if line == "chapters:":
            in_chapters = True
            continue
        if line == "parts:":
            in_chapters = False
            break
        if not in_chapters:
            out.append(line)
            continue
        key_match = re.match(r"^  (ch\d+b?):\s*$", line)
        if key_match:
            current = key_match.group(1)
            chapter_blocks[current] = []
            continue
        if current is not None:
            chapter_blocks[current].append(line)

    # Drop temporary notes about b-suffix insertions.
    cleaned_blocks: dict[str, list[str]] = {}
    for cid, block in chapter_blocks.items():
        cleaned: list[str] = []
        skip_note = False
        for line in block:
            if line.strip().startswith("note:") and "temporary" in line.lower():
                skip_note = True
                continue
            if skip_note and line.startswith("    "):
                continue
            skip_note = False
            cleaned.append(line)
        cleaned_blocks[cid] = cleaned

    new_order = [f"ch{n:02d}" for n in range(1, 10)] + [f"ch{n}" for n in range(10, 49)]

    id_to_block: dict[str, list[str]] = {}
    for old_id, new_id in CHAPTER_ID_MAP.items():
        id_to_block[new_id] = cleaned_blocks.pop(old_id)
    for cid in [f"ch{n:02d}" for n in range(1, 10)] + [f"ch{n}" for n in range(10, 20)]:
        id_to_block[cid] = cleaned_blocks.pop(cid)
    if cleaned_blocks:
        raise ValueError(f"Unmapped chapter blocks: {sorted(cleaned_blocks)}")

    chapter_section = ["chapters:"]
    for cid in new_order:
        chapter_section.append(f"  {cid}:")
        chapter_section.extend(id_to_block[cid])

    parts_section = text.split("parts:", 1)[1]
    parts_section = replace_in_text(parts_section)
    path.write_text("\n".join(out + chapter_section + ["", "parts:" + parts_section]), encoding="utf-8")


def patch_generate_tables() -> None:
    path = ROOT / "scripts" / "generate_tables.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        '    match = re.match(r"(ch\\d+b?)", slug)',
        '    match = re.match(r"(ch\\d+)", slug)',
    )
    text = text.replace(
        """def chapter_display_id(chapter_id: str) -> str:
    match = re.fullmatch(r"ch(\\d+)([a-z]?)", chapter_id)
    if not match:
        raise ValueError(f"Cannot display chapter id: {chapter_id}")
    number, suffix = match.groups()
    return f"{int(number)}{suffix}"
""",
        """def chapter_display_id(entry: ChapterEntry) -> str:
    return str(entry.order)
""",
    )
    text = text.replace(
        "chapter_display_id(entry.chapter_id)",
        "chapter_display_id(entry)",
    )
    path.write_text(text, encoding="utf-8")


def update_text_files() -> None:
    for pattern in TEXT_GLOBS:
        for path in ROOT.rglob(pattern):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if path.name.startswith("__renumber_tmp__"):
                continue
            if path.relative_to(ROOT).parts[0] == "scripts" and path.name == "renumber_manuscript.py":
                continue
            try:
                original = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            updated = replace_in_text(original)
            if updated != original:
                path.write_text(updated, encoding="utf-8")


def main() -> None:
    chapter_moves = chapter_files()
    if chapter_moves:
        rename_via_temp(chapter_moves)
        print(f"Renamed {len(chapter_moves)} chapter files.")

    appendix_moves = {
        ROOT / "appendices" / f"{old}.tex": ROOT / "appendices" / f"{new}.tex"
        for old, new in APPENDIX_RENAMES
    }
    rename_via_temp(appendix_moves)
    print(f"Renamed {len(appendix_moves)} appendix files.")

    rewrite_book_yml()
    print("Rewrote metadata/book.yml.")

    patch_generate_tables()
    print("Patched scripts/generate_tables.py.")

    update_text_files()
    print("Updated text references across repo.")


if __name__ == "__main__":
    main()
