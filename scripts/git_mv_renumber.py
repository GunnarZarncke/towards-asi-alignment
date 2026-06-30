#!/usr/bin/env python3
"""Restore HEAD paths, git mv renames via temp names, restore working-tree content."""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKUP = ROOT / ".renumber-content-backup"
TMP_PREFIX = "__renumber_tmp__"

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

APPENDIX_MAP: dict[str, str] = {
    "appBridge-crosswalk": "appB-bridge-crosswalk",
    "appJ-institutional-translation": "appC-institutional-translation",
    "appK-worked-example": "appD-worked-example",
    "appF-glossary": "appE-glossary",
    "appH-research-program": "appF-research-program",
    "appI-lean-proof-spine": "appG-lean-proof-spine",
    "appB-worked-example-agent-boundary": "appH-boundary-worked-example",
    "appC-value-bundle-inference": "appI-value-bundle-inference",
    "appD-correction-channel-audit": "appJ-correction-channel-audit",
    "appE-assumptions": "appL-assumptions",
    "appG-safety-case-template": "appK-safety-case-template",
}


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)


def chapter_moves() -> list[tuple[Path, Path]]:
    moves: list[tuple[Path, Path]] = []
    for old_path in subprocess.check_output(
        ["git", "ls-files", "chapters/ch*.tex"], text=True, cwd=ROOT
    ).splitlines():
        old_name = Path(old_path).name
        m = re.match(r"(ch\d+b?)-(.+\.tex)$", old_name)
        if not m:
            continue
        old_id, slug = m.groups()
        new_id = CHAPTER_ID_MAP.get(old_id)
        if new_id is None:
            continue
        moves.append(
            (
                ROOT / "chapters" / f"{old_id}-{slug}",
                ROOT / "chapters" / f"{new_id}-{slug}",
            )
        )
    return moves


def appendix_moves() -> list[tuple[Path, Path]]:
    return [
        (ROOT / "appendices" / f"{old}.tex", ROOT / "appendices" / f"{new}.tex")
        for old, new in APPENDIX_MAP.items()
    ]


def backup_tree() -> None:
    if BACKUP.exists():
        shutil.rmtree(BACKUP)
    for sub in ("chapters", "appendices"):
        src = ROOT / sub
        if src.exists():
            shutil.copytree(src, BACKUP / sub)
    print(f"Backed up to {BACKUP}")


def restore_head_tree() -> None:
    for sub in ("chapters", "appendices"):
        run(["git", "clean", "-fd", sub])
    run(["git", "checkout", "HEAD", "--", "chapters/", "appendices/"])


def git_mv_via_tmp(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(src)
    if dst.exists():
        raise FileExistsError(f"destination exists: {dst}")
    tmp = src.with_name(TMP_PREFIX + src.name)
    if tmp.exists():
        raise FileExistsError(tmp)
    run(["git", "mv", str(src.relative_to(ROOT)), str(tmp.relative_to(ROOT))])
    run(["git", "mv", str(tmp.relative_to(ROOT)), str(dst.relative_to(ROOT))])


def apply_renames(moves: list[tuple[Path, Path]]) -> None:
    for src, dst in moves:
        git_mv_via_tmp(src, dst)


def restore_content(moves: list[tuple[Path, Path]]) -> None:
    for _src, dst in moves:
        rel = dst.relative_to(ROOT)
        backup_file = BACKUP / rel
        if backup_file.is_file():
            shutil.copy2(backup_file, dst)
            print(f"restored content {rel}")


def restore_unchanged_modified() -> None:
    move_dst = {dst for _s, dst in chapter_moves()} | {dst for _s, dst in appendix_moves()}
    for sub in ("chapters", "appendices"):
        for path in (BACKUP / sub).rglob("*.tex"):
            rel = path.relative_to(BACKUP)
            target = ROOT / rel
            if target in move_dst:
                continue
            if not target.exists():
                continue
            if path.read_bytes() != target.read_bytes():
                shutil.copy2(path, target)
                print(f"restored modified {rel}")


def main() -> None:
    chapter = chapter_moves()
    appendix = appendix_moves()
    print(f"{len(chapter)} chapter renames, {len(appendix)} appendix renames")

    if not BACKUP.exists():
        raise SystemExit(f"Missing backup at {BACKUP}; run backup_tree() first.")

    restore_head_tree()
    apply_renames(chapter)
    apply_renames(appendix)
    restore_content(chapter)
    restore_content(appendix)
    restore_unchanged_modified()
    print("Done. Review with: git diff --stat --find-renames=50%")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "backup-only":
        backup_tree()
    else:
        main()
