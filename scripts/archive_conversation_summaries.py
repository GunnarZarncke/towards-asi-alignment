#!/usr/bin/env python3
"""Archive old conversation logs and rebuild a slim INDEX.md.

Moves logs dated before ACTIVE_CUTOFF into archive/YYYY-MM/.
Generates one-line compressed indexes per archive month.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "drafts" / "conversation-summaries"
ARCHIVE_DIR = LOG_DIR / "archive"
ACTIVE_CUTOFF = "2026-07-20"  # inclusive in active root
SKIP_NAMES = {"README.md", "INDEX.md"}


def log_date(name: str) -> str | None:
    m = re.match(r"(\d{4}-\d{2}-\d{2})-", name)
    return m.group(1) if m else None


def log_month(name: str) -> str | None:
    d = log_date(name)
    return d[:7] if d else None


def parse_log(path: Path) -> tuple[str, str]:
    """Return (title, trigger_one_liner)."""
    text = path.read_text(encoding="utf-8", errors="replace")
    title = path.stem
    m = re.match(r"^#\s+\d{4}-\d{2}-\d{2}\s+—\s+(.+)$", text, re.MULTILINE)
    if m:
        title = m.group(1).strip()
    trigger = ""
    if "## Trigger" in text:
        block = text.split("## Trigger", 1)[1].split("\n## ", 1)[0]
        for line in block.strip().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                trigger = line
                break
    if len(trigger) > 120:
        trigger = trigger[:117] + "..."
    return title, trigger


def move_to_archive(path: Path) -> Path:
    month = log_month(path.name)
    if not month:
        raise ValueError(f"Cannot infer month for {path.name}")
    dest_dir = ARCHIVE_DIR / month
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / path.name
    if dest.exists():
        return dest
    shutil.move(str(path), str(dest))
    return dest


def write_month_index(month: str, entries: list[tuple[str, str, str]]) -> None:
    """entries: (date, filename, one_line_summary) newest first."""
    out = ARCHIVE_DIR / f"{month}-INDEX.md"
    lines = [
        f"# Archive index — {month}",
        "",
        f"Compressed index for {len(entries)} sessions archived from the active log folder.",
        "Full logs live in `archive/{}/`. Search with `rg` or git history.".format(month),
        "",
        "| Date | Topic | Log |",
        "|------|-------|-----|",
    ]
    for date, fname, summary in entries:
        title, trigger = parse_log(ARCHIVE_DIR / month / fname)
        topic = title if title != fname else fname.replace(f"{date}-", "").replace("-", " ")
        blurb = trigger or summary
        if len(blurb) > 100:
            blurb = blurb[:97] + "..."
        lines.append(
            f"| {date} | {topic} — {blurb} | [{fname}]({month}/{fname}) |"
        )
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_active_index(active_files: list[Path]) -> None:
    active_files.sort(key=lambda p: p.name, reverse=True)
    lines = [
        "# Conversation log index",
        "",
        "Agent handoff record. **Read the top row first**, then skim `metadata/book.yml`.",
        "",
        f"Logs before **{ACTIVE_CUTOFF}** are in [`archive/`](archive/README.md) with monthly compressed indexes.",
        "",
        "## Recent sessions",
        "",
        "| Date | Topic | Log |",
        "|------|-------|-----|",
    ]
    for path in active_files:
        date = log_date(path.name) or "????-??-??"
        title, trigger = parse_log(path)
        topic = title
        if trigger:
            topic = f"**{title}** — {trigger}"
        elif not topic or topic == path.stem:
            topic = path.stem.replace(f"{date}-", "").replace("-", " ")
        lines.append(f"| {date} | {topic} | [{path.name}]({path.name}) |")

    archived_months = sorted(
        {p.parent.name for p in ARCHIVE_DIR.glob("*/*.md")},
        reverse=True,
    )
    lines.extend(["", "## Archive (older sessions)", ""])
    for month in archived_months:
        count = len(list((ARCHIVE_DIR / month).glob("*.md")))
        lines.append(
            f"- **{month}** ({count} logs): [{month}-INDEX.md](archive/{month}-INDEX.md)"
        )
    lines.extend(
        [
            "",
            "## Maintenance",
            "",
            f"- Active cutoff: `{ACTIVE_CUTOFF}` (move older logs with `python3 scripts/archive_conversation_summaries.py`).",
            "- Template and rules: [README.md](README.md).",
            "",
        ]
    )
    (LOG_DIR / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    to_archive: list[Path] = []
    active: list[Path] = []

    for path in sorted(LOG_DIR.glob("*.md")):
        if path.name in SKIP_NAMES:
            continue
        date = log_date(path.name)
        if not date:
            continue
        if date < ACTIVE_CUTOFF:
            to_archive.append(path)
        else:
            active.append(path)

    for path in to_archive:
        move_to_archive(path)

    by_month: dict[str, list[tuple[str, str, str]]] = {}
    for month_dir in sorted(ARCHIVE_DIR.glob("20*")):
        if not month_dir.is_dir():
            continue
        month = month_dir.name
        entries = []
        for path in sorted(month_dir.glob("*.md"), reverse=True):
            date = log_date(path.name) or ""
            entries.append((date, path.name, ""))
        if entries:
            by_month[month] = entries

    for month, entries in by_month.items():
        write_month_index(month, entries)

    write_active_index(active)
    print(
        f"Archived {len(to_archive)} logs; {len(active)} active; "
        f"{len(by_month)} archive months indexed."
    )


if __name__ == "__main__":
    main()
