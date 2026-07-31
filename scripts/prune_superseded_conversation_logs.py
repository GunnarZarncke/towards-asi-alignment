#!/usr/bin/env python3
"""Remove session logs superseded by a later conversation (not by code landing).

Writes one-line entries to RECOVERY.md for deleted files. Keeps HANDOFF.md and
all logs that are not explicitly superseded by a later session log.

Criteria (conservative):
  1. Manual pairs (older, newer) where the later log is the handoff-final word.
  2. Auto: newer log cites older filename AND contains 'superseded' near that cite.
  3. Auto: newer log is a line-closure ('line stopped' / 'line closed') and cites older ET-* logs.

Does NOT delete logs merely because work landed in the repo (chapter drafts, etc.).
"""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "drafts" / "conversation-summaries"
ARCHIVE_DIR = LOG_DIR / "archive"
SKIP = {"README.md", "INDEX.md", "HANDOFF.md", "RECOVERY.md"}
LOG_NAME = re.compile(r"^(2026-\d{2}-\d{2}-[a-z0-9-]+\.md)$")
LOG_REF = re.compile(r"(2026-\d{2}-\d{2}-[a-z0-9-]+\.md)")

# (older, newer) — newer must exist and be strictly later by filename.
MANUAL_SUPERSESSIONS: list[tuple[str, str]] = [
    ("2026-07-25-tier-b-field-news-partial.md", "2026-07-25-field-news-tier-ab.md"),
    ("2026-07-25-tier-a-field-news.md", "2026-07-25-field-news-tier-ab.md"),
    ("2026-07-20-et1-colosseum-sc-battery.md", "2026-07-24-et1-lockstep-fsm-root-cause.md"),
    ("2026-07-23-et1-colosseum-sc-claude-positive-control.md", "2026-07-24-et1-lockstep-fsm-root-cause.md"),
    ("2026-07-23-et1-colosseum-attack-simple.md", "2026-07-24-et1-lockstep-fsm-root-cause.md"),
    ("2026-07-23-et2-cil-adapter-build.md", "2026-07-25-et2-cil-live-smoke-null.md"),
    ("2026-07-06-lab-simulation-freeze-review.md", "2026-07-06-lab-simulation-handles-freeze.md"),
    ("2026-07-06-lab-simulation-d3-ecology-notes.md", "2026-07-06-lab-simulation-post-freeze-consolidation.md"),
    ("2026-07-06-lab-simulation-d4-d1-comms-file-channel.md", "2026-07-06-lab-simulation-post-freeze-consolidation.md"),
    ("2026-07-05-lab-simulation-phase2-5.md", "2026-07-06-lab-simulation-freeze-review.md"),
    ("2026-07-18-graded-lab-plan-v4-v0-v1-v2-implementation.md", "2026-07-18-graded-lab-v4-1-freeze-r-mb9-r-mb7d.md"),
]


def collect_logs() -> dict[str, Path]:
    out: dict[str, Path] = {}
    for path in LOG_DIR.rglob("*.md"):
        if path.name in SKIP or path.name.endswith("-INDEX.md"):
            continue
        if path.name == "README.md" and "archive" in path.parts:
            continue
        if LOG_NAME.match(path.name):
            out[path.name] = path
    return out


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


def auto_superseded(logs: dict[str, Path]) -> set[str]:
    delete: set[str] = set()
    names = sorted(logs.keys())
    for newer in names:
        text = logs[newer].read_text(encoding="utf-8", errors="replace")
        head = text[:4000]
        closure = bool(
            re.search(r"line stopped|line closed|conclusion:", head, re.I)
        )
        for older in LOG_REF.findall(head):
            if older == newer or older not in logs:
                continue
            if newer <= older:
                continue
            window = ""
            idx = head.find(older)
            if idx >= 0:
                window = head[max(0, idx - 120) : idx + len(older) + 120]
            if re.search(r"superseded", window, re.I):
                delete.add(older)
            elif closure and "et1" in older and "et1" in newer:
                delete.add(older)
    return delete


def validate_pairs(logs: dict[str, Path]) -> set[str]:
    delete: set[str] = set()
    for older, newer in MANUAL_SUPERSESSIONS:
        if older not in logs:
            continue
        if newer not in logs:
            print(f"warn: newer missing for manual pair {older} -> {newer}")
            continue
        delete.add(older)
    return delete


def append_recovery(entries: list[tuple[str, str, str]], prune_date: str) -> None:
    path = LOG_DIR / "RECOVERY.md"
    if path.exists() and "Pruned session logs" in path.read_text(encoding="utf-8"):
        existing = path.read_text(encoding="utf-8")
    else:
        existing = (
            "# Pruned session logs (recovery index)\n\n"
            "One line per log removed because a **later session log** superseded it "
            "(not because the work landed in code alone). "
            "Full text: `git log -- drafts/conversation-summaries/` or "
            "`git show <commit>:<path>`.\n\n"
        )
    block = [f"## Prune run {prune_date}", ""]
    for fname, title, summary in sorted(entries, reverse=True):
        blurb = f" — {summary}" if summary else ""
        block.append(f"- `{fname}` **{title}**{blurb} (superseded; see later session in git)")
    block.append("")
    path.write_text(existing.rstrip() + "\n\n" + "\n".join(block) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Delete files (default: dry run)")
    args = parser.parse_args()

    logs = collect_logs()
    to_delete = validate_pairs(logs) | auto_superseded(logs)

    print(f"Logs on disk: {len(logs)}")
    print(f"Superseded (candidates to prune): {len(to_delete)}")
    for name in sorted(to_delete):
        print(f"  {name}")

    if not args.apply:
        print("\nDry run. Pass --apply to delete and append RECOVERY.md.")
        return

    entries: list[tuple[str, str, str]] = []
    for name in sorted(to_delete):
        path = logs[name]
        title, summary = parse_one_liner(path)
        entries.append((name, title, summary))
        path.unlink()

    append_recovery(entries, date.today().isoformat())
    print(f"Deleted {len(entries)} superseded logs; updated RECOVERY.md.")


if __name__ == "__main__":
    main()
