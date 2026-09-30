#!/usr/bin/env python3
"""Close authbar environments before \\wikiq and reopen after (same key)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKIQ_RE = re.compile(r"\\wikiq\{")
BEGIN_RE = re.compile(r"^\\begin\{authbar\}\{([^}]+)\}\s*$")
END_RE = re.compile(r"^\\end\{authbar\}\s*$")


def split_authbars(text: str) -> str:
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    in_authbar = False
    authbar_key: str | None = None

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        begin = BEGIN_RE.match(stripped)
        if begin:
            in_authbar = True
            authbar_key = begin.group(1)
            out.append(line)
            i += 1
            continue

        if END_RE.match(stripped):
            in_authbar = False
            authbar_key = None
            out.append(line)
            i += 1
            continue

        if in_authbar and WIKIQ_RE.search(line):
            if not (out and END_RE.match(out[-1].strip())):
                out.append("\\end{authbar}\n")
            out.append(line)
            i += 1
            while i < len(lines) and WIKIQ_RE.search(lines[i]):
                out.append(lines[i])
                i += 1
            if i < len(lines) and END_RE.match(lines[i].strip()):
                i += 1
            if i < len(lines) and not END_RE.match(lines[i].strip()) and authbar_key:
                out.append(f"\\begin{{authbar}}{{{authbar_key}}}\n")
                in_authbar = True
            else:
                in_authbar = False
            continue

        out.append(line)
        i += 1

    return "".join(out)


def main() -> None:
    changed = 0
    for path in sorted((ROOT / "chapters").glob("ch*.tex")):
        text = path.read_text(encoding="utf-8")
        if not WIKIQ_RE.search(text):
            continue
        updated = split_authbars(text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"updated {path.relative_to(ROOT)}")
    print(f"Done ({changed} files).")


if __name__ == "__main__":
    main()
