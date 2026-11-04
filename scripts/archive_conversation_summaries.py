#!/usr/bin/env python3
"""Roll older session logs into archive/YYYY-MM/; rebuild slim INDEX.md.

Keeps ACTIVE_MAX newest **git-tracked** logs in the root folder. Does not delete logs.
Untracked logs are left in place and omitted from INDEX.md, so a committed index
cannot point at a file CI does not have.
For deletion of logs superseded by later sessions, use prune_superseded_conversation_logs.py.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "drafts" / "conversation-summaries"
ARCHIVE_DIR = LOG_DIR / "archive"
ACTIVE_MAX = 15
SKIP_NAMES = {"README.md", "INDEX.md", "HANDOFF.md", "RECOVERY.md"}


def log_date(name: str) -> str | None:
    m = re.match(r"(\d{4}-\d{2}-\d{2})-", name)
    return m.group(1) if m else None


def log_month(name: str) -> str | None:
    d = log_date(name)
    return d[:7] if d else None


def parse_log(path: Path) -> tuple[str, str]:
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
    if len(trigger) > 100:
        trigger = trigger[:97] + "..."
    return title, trigger


def move_to_archive(path: Path) -> None:
    month = log_month(path.name)
    if not month:
        raise ValueError(f"Cannot infer month for {path.name}")
    dest_dir = ARCHIVE_DIR / month
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / path.name
    if dest.exists():
        if path.exists():
            path.unlink()
        return
    shutil.move(str(path), str(dest))


def tracked_log_paths() -> set[str]:
    out = subprocess.run(
        ["git", "ls-files", "--", "drafts/conversation-summaries"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return set(out.stdout.splitlines())


def is_tracked(path: Path, tracked: set[str]) -> bool:
    return path.relative_to(ROOT).as_posix() in tracked


def write_month_index(month: str, tracked: set[str]) -> None:
    month_dir = ARCHIVE_DIR / month
    paths = sorted(
        (p for p in month_dir.glob("*.md") if is_tracked(p, tracked)),
        reverse=True,
    )
    lines = [
        f"# Archive index — {month}",
        "",
        f"{len(paths)} session logs. Full text in `archive/{month}/`.",
        "",
        "| Date | Topic | Log |",
        "|------|-------|-----|",
    ]
    for path in paths:
        date = log_date(path.name) or ""
        title, trigger = parse_log(path)
        topic = f"**{title}** — {trigger}" if trigger else title
        lines.append(f"| {date} | {topic} | [{path.name}]({month}/{path.name}) |")
    (ARCHIVE_DIR / f"{month}-INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_active_index(active: list[Path], tracked: set[str]) -> None:
    active.sort(key=lambda p: p.name, reverse=True)
    lines = [
        "# Conversation log index",
        "",
        "**Start here:** [HANDOFF.md](HANDOFF.md) (aggregated themes and open work).",
        "",
        f"**Recent sessions** ({len(active)} newest in this folder). Older: [archive/](archive/README.md).",
        "",
        "| Date | Topic | Log |",
        "|------|-------|-----|",
    ]
    for path in active:
        date = log_date(path.name) or ""
        title, trigger = parse_log(path)
        topic = f"**{title}** — {trigger}" if trigger else title
        lines.append(f"| {date} | {topic} | [{path.name}]({path.name}) |")

    months = sorted(
        {
            p.parent.name
            for p in ARCHIVE_DIR.glob("*/*.md")
            if is_tracked(p, tracked)
        },
        reverse=True,
    )
    lines.extend(["", "## Archive by month", ""])
    for month in months:
        n = sum(1 for p in (ARCHIVE_DIR / month).glob("*.md") if is_tracked(p, tracked))
        lines.append(f"- **{month}** ({n}): [{month}-INDEX.md](archive/{month}-INDEX.md)")

    lines.extend(
        [
            "",
            "## Maintenance",
            "",
            f"- Roll older logs: `python3 scripts/archive_conversation_summaries.py` (keeps {ACTIVE_MAX} tracked logs in root; untracked logs are omitted).",
            "- Prune superseded logs: `python3 scripts/prune_superseded_conversation_logs.py --apply`.",
            "- Rules: [README.md](README.md).",
            "",
        ]
    )
    (LOG_DIR / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    tracked = tracked_log_paths()
    root_logs = [
        p
        for p in LOG_DIR.glob("*.md")
        if p.name not in SKIP_NAMES and log_date(p.name) and is_tracked(p, tracked)
    ]
    root_logs.sort(key=lambda p: p.name, reverse=True)
    for path in root_logs[ACTIVE_MAX:]:
        move_to_archive(path)
        tracked.discard(path.relative_to(ROOT).as_posix())
        dest = ARCHIVE_DIR / (log_month(path.name) or "") / path.name
        tracked.add(dest.relative_to(ROOT).as_posix())
    active = sorted(
        (
            p
            for p in LOG_DIR.glob("2026-*.md")
            if p.name not in SKIP_NAMES and is_tracked(p, tracked)
        ),
        key=lambda p: p.name,
        reverse=True,
    )
    for month_dir in ARCHIVE_DIR.glob("20*"):
        if month_dir.is_dir():
            write_month_index(month_dir.name, tracked)
    write_active_index(active, tracked)
    archived = sum(1 for p in ARCHIVE_DIR.glob("*/*.md") if is_tracked(p, tracked))
    print(f"Active: {len(active)}; archived: {archived}")


if __name__ == "__main__":
    main()
