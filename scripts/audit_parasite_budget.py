#!/usr/bin/env python3
"""§3.8 correction-parasite budget from session-log Done bullets.

Counts Done bullets tagged content: vs bookkeeping: (AGENTS.md §4.6). Bullets
without either tag are reported as unlabeled and excluded from the weekly share.

Stop (frozen 2026-11-02):
  BOOKKEEPING_MAX_SHARE = 0.40
  CONSECUTIVE_WEEKS = 3
  When bookkeeping share exceeds the max for three consecutive ISO weeks with
  at least one labeled bullet, exit 1.

Exit 0: stop not armed.
Exit 1: stop armed.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_DIRS = (
    ROOT / "drafts/conversation-summaries",
    ROOT / "drafts/conversation-summaries/archive",
)
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
DONE_BULLET = re.compile(r"^- (content|bookkeeping):\s", re.I)
BOOKKEEPING_MAX_SHARE = 0.40
CONSECUTIVE_WEEKS = 3
OUT_DIR = ROOT / "drafts/project/self-audit"


def iso_week(d: date) -> str:
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def log_date(path: Path) -> date | None:
    m = DATE_RE.search(path.name)
    if not m:
        return None
    return datetime.strptime(m.group(1), "%Y-%m-%d").date()


def parse_log(path: Path) -> tuple[int, int, int]:
    text = path.read_text(encoding="utf-8", errors="replace")
    in_done = False
    content = bookkeeping = unlabeled = 0
    for line in text.splitlines():
        if line.startswith("## Done"):
            in_done = True
            continue
        if in_done and line.startswith("## "):
            break
        if not in_done or not line.startswith("- "):
            continue
        m = DONE_BULLET.match(line)
        if m:
            if m.group(1).lower() == "content":
                content += 1
            else:
                bookkeeping += 1
        else:
            unlabeled += 1
    return content, bookkeeping, unlabeled


def collect_weeks() -> dict[str, dict]:
    weeks: dict[str, dict] = defaultdict(
        lambda: {"content": 0, "bookkeeping": 0, "unlabeled": 0, "logs": 0}
    )
    for base in LOG_DIRS:
        if not base.is_dir():
            continue
        for path in base.rglob("*.md"):
            if path.name in ("HANDOFF.md", "INDEX.md", "README.md", "RECOVERY.md"):
                continue
            d = log_date(path)
            if d is None:
                continue
            w = iso_week(d)
            c, b, u = parse_log(path)
            if c + b + u == 0:
                continue
            weeks[w]["content"] += c
            weeks[w]["bookkeeping"] += b
            weeks[w]["unlabeled"] += u
            weeks[w]["logs"] += 1
    return dict(weeks)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weeks", type=int, default=8, help="how many recent ISO weeks to print")
    parser.add_argument("--out", type=Path, default=None, help="optional CSV path")
    args = parser.parse_args()

    weeks = collect_weeks()
    ordered = sorted(weeks.keys())[-args.weeks :]

    rows = []
    for w in ordered:
        d = weeks[w]
        labeled = d["content"] + d["bookkeeping"]
        share = (d["bookkeeping"] / labeled) if labeled else None
        rows.append({**d, "week": w, "labeled": labeled, "bookkeeping_share": share})

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    out_path = args.out or (OUT_DIR / f"parasite-budget-{ts[:10]}.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "week",
                "logs",
                "content",
                "bookkeeping",
                "unlabeled",
                "labeled",
                "bookkeeping_share",
            ],
        )
        w.writeheader()
        for row in rows:
            w.writerow(
                {
                    "week": row["week"],
                    "logs": row["logs"],
                    "content": row["content"],
                    "bookkeeping": row["bookkeeping"],
                    "unlabeled": row["unlabeled"],
                    "labeled": row["labeled"],
                    "bookkeeping_share": (
                        f"{row['bookkeeping_share']:.4f}" if row["bookkeeping_share"] is not None else ""
                    ),
                }
            )
        f.write(f"# generated_at,{ts}\n")
        f.write(f"# bookkeeping_max_share,{BOOKKEEPING_MAX_SHARE}\n")
        f.write(f"# consecutive_weeks,{CONSECUTIVE_WEEKS}\n")

    print(f"wrote {out_path.relative_to(ROOT)}")
    print(f"threshold bookkeeping > {BOOKKEEPING_MAX_SHARE:.0%} for {CONSECUTIVE_WEEKS} consecutive weeks")
    for row in rows:
        sh = row["bookkeeping_share"]
        shs = f"{sh:.1%}" if sh is not None else "n/a"
        print(
            f"  {row['week']}  logs {row['logs']:3}  "
            f"content {row['content']:4}  bookkeeping {row['bookkeeping']:4}  "
            f"unlabeled {row['unlabeled']:4}  share {shs}"
        )

    streak = 0
    for w in sorted(weeks.keys(), reverse=True):
        d = weeks[w]
        labeled = d["content"] + d["bookkeeping"]
        if labeled == 0:
            break
        share = d["bookkeeping"] / labeled
        if share > BOOKKEEPING_MAX_SHARE:
            streak += 1
        else:
            break
        if streak >= CONSECUTIVE_WEEKS:
            print(
                f"STOP: bookkeeping share above {BOOKKEEPING_MAX_SHARE:.0%} "
                f"for {CONSECUTIVE_WEEKS} consecutive weeks (through {w})."
            )
            return 1

    print("PASS: parasite stop not armed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
