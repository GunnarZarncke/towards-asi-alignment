#!/usr/bin/env python3
"""Redacted monthly prompt digest. Raw prompts stay in gitignored telemetry/."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def first_eight_words(prompt: str) -> str:
    words = prompt.split()
    return " ".join(words[:8])


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--month", required=True, metavar="YYYY-MM")
    args = p.parse_args()
    year, month = args.month.split("-")
    prompt_dir = ROOT / "telemetry" / "prompts"
    rows = []
    if prompt_dir.exists():
        for path in sorted(prompt_dir.glob("*.jsonl")):
            if not path.name.startswith(f"{year}-{month}"):
                continue
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    rows.append(json.loads(line))
    by_session: dict[str, list] = defaultdict(list)
    for r in rows:
        by_session[r.get("session", "")].append(r)
    out = ROOT / "drafts/project/self-audit/prompts" / f"{args.month}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# Prompt digest {args.month}",
        "",
        f"Sessions: {len(by_session)}. Prompts: {len(rows)}.",
        "Full prompt text is not included unless the author adds it after export.",
        "",
    ]
    for session, items in sorted(by_session.items()):
        lines.append(f"## `{session}`")
        lines.append(f"Count: {len(items)}")
        for r in items:
            pid = r.get("prompt_id") or ""
            eight = first_eight_words(r.get("prompt") or "")
            kind = r.get("kind") or "unclassified"
            lines.append(f"- `{pid}` ({kind}) {eight}")
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
