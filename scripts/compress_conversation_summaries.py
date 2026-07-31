#!/usr/bin/env python3
"""Compress conversation logs: RECOVERY one-liners + delete full log files.

Reads all session logs under drafts/conversation-summaries/, writes
RECOVERY.md (one line per log for git recovery), optionally deletes files.
HANDOFF.md is maintained manually (aggregated themes); this script does not overwrite it.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "drafts" / "conversation-summaries"
ARCHIVE_DIR = LOG_DIR / "archive"
SKIP = {"README.md", "INDEX.md", "HANDOFF.md", "RECOVERY.md"}


def log_date(name: str) -> str:
    m = re.match(r"(\d{4}-\d{2}-\d{2})-", name)
    return m.group(1) if m else "0000-00-00"


def parse_one_liner(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    title = path.stem
    m = re.match(r"^#\s+\d{4}-\d{2}-\d{2}\s+—\s+(.+)$", text, re.MULTILINE)
    if m:
        title = m.group(1).strip()
    summary = ""
    for section in ("## Done", "## Trigger", "## Decisions"):
        if section in text:
            block = text.split(section, 1)[1].split("\n## ", 1)[0]
            for line in block.strip().splitlines():
                line = line.strip().lstrip("-").strip()
                if line and not line.startswith("#"):
                    summary = line
                    break
        if summary:
            break
    if len(summary) > 140:
        summary = summary[:137] + "..."
    return title, summary


def collect_logs() -> list[tuple[str, Path]]:
    found: list[tuple[str, Path]] = []
    for path in LOG_DIR.glob("*.md"):
        if path.name in SKIP or not log_date(path.name):
            continue
        found.append((path.name, path))
    for path in ARCHIVE_DIR.glob("*/*.md"):
        if path.name.endswith("-INDEX.md") or path.name == "README.md":
            continue
        if log_date(path.name):
            found.append((path.name, path))
    found.sort(key=lambda x: x[0], reverse=True)
    return found


def git_path(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_recovery(entries: list[tuple[str, Path, str, str]]) -> None:
    lines = [
        "# Conversation log recovery index",
        "",
        "One line per deleted session log. Full text: `git log -- drafts/conversation-summaries/` "
        "or `git show <commit>:<path>`.",
        "",
        f"Total: **{len(entries)}** sessions (compressed {__import__('datetime').date.today().isoformat()}).",
        "",
    ]
    current_month = ""
    for fname, path, title, summary in entries:
        month = fname[:7]
        if month != current_month:
            lines.extend([f"## {month}", ""])
            current_month = month
        rel = git_path(path)
        blurb = f" — {summary}" if summary else ""
        lines.append(f"- `{fname}` **{title}**{blurb}")
    lines.append("")
    (LOG_DIR / "RECOVERY.md").write_text("\n".join(lines), encoding="utf-8")


def write_index() -> None:
    text = """# Conversation summaries

**Start here:** [HANDOFF.md](HANDOFF.md) — aggregated open work, recent themes, and where durable state lives.

| File | Role |
|------|------|
| [HANDOFF.md](HANDOFF.md) | Agent resume doc (themes, open items, pointers) |
| [RECOVERY.md](RECOVERY.md) | One-line index of all past sessions (git recovery) |
| [README.md](README.md) | Format and maintenance rules |

Durable task state: `metadata/TODO.md`, `metadata/book.yml`, experiment `FINDINGS.md` / `TODO.md` — not this folder.

New sessions: append a bullet to **HANDOFF.md** (Open / Recently shipped); add one line to **RECOVERY.md** only if retiring a standalone log file.
"""
    (LOG_DIR / "INDEX.md").write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Delete individual log files after writing RECOVERY.md",
    )
    args = parser.parse_args()

    logs = collect_logs()
    entries: list[tuple[str, Path, str, str]] = []
    for fname, path in logs:
        title, summary = parse_one_liner(path)
        entries.append((fname, path, title, summary))

    write_recovery(entries)
    write_index()

    deleted = 0
    if args.delete:
        for _, path in logs:
            path.unlink()
            deleted += 1
        for month_dir in list(ARCHIVE_DIR.glob("20*")):
            if month_dir.is_dir() and not any(month_dir.iterdir()):
                month_dir.rmdir()
        for stale in ARCHIVE_DIR.glob("*-INDEX.md"):
            stale.unlink()

    print(f"RECOVERY.md: {len(entries)} entries; deleted {deleted} files.")


if __name__ == "__main__":
    main()
