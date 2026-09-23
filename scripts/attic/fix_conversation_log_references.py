#!/usr/bin/env python3
"""Point broken RECOVERY.md session links at real log paths (root or archive/)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "drafts" / "conversation-summaries"
SKIP = {"README.md", "INDEX.md", "HANDOFF.md", "RECOVERY.md"}

BROKEN = re.compile(
    r"(?:`drafts/conversation-summaries/)?"
    r"(?:RECOVERY\.md` \(session `(2026-\d{2}-\d{2}-[a-z0-9-]+\.md)`\)|"
    r"`drafts/conversation-summaries/RECOVERY\.md` \(session `(2026-\d{2}-\d{2}-[a-z0-9-]+\.md)`\))"
)


def index_logs() -> dict[str, Path]:
    out: dict[str, Path] = {}
    for path in LOG_DIR.rglob("2026-*.md"):
        if path.name in SKIP:
            continue
        out[path.name] = path.relative_to(ROOT)
    return out


def rel_link(path: Path) -> str:
    return f"`{path.as_posix()}`"


def fix_text(text: str, logs: dict[str, Path]) -> tuple[str, int]:
    n = 0

    def sub_broken(m: re.Match[str]) -> str:
        nonlocal n
        fname = m.group(1)
        if fname in logs:
            n += 1
            return rel_link(logs[fname])
        return m.group(0)

    text = BROKEN.sub(sub_broken, text)

    # Fix doubled malformed links from an earlier bad pass.
    doubled = re.compile(
        r"\[`drafts/conversation-summaries/RECOVERY\.md` \(session `(2026-\d{2}-\d{2}-[a-z0-9-]+\.md)`\)\]"
        r"\(\.\./\.\./`drafts/conversation-summaries/RECOVERY\.md` \(session `\1`\)\)"
    )

    def sub_doubled(m: re.Match[str]) -> str:
        nonlocal n
        fname = m.group(1)
        if fname in logs:
            n += 1
            p = logs[fname]
            return f"[{p.name}](../../{p.as_posix()})"
        return m.group(0)

    text = doubled.sub(sub_doubled, text)
    return text, n


def main() -> None:
    logs = index_logs()
    total = 0
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in {".md", ".tex", ".yml"}:
            continue
        if "node_modules" in path.parts or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if "RECOVERY.md" not in text and "session `" not in text:
            continue
        new_text, n = fix_text(text, logs)
        if n:
            path.write_text(new_text, encoding="utf-8")
            print(f"{path.relative_to(ROOT)}: {n} fixes")
            total += n
    print(f"Total fixes: {total}")


if __name__ == "__main__":
    main()
