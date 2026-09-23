#!/usr/bin/env python3
"""Generate a chapter stub from title and label."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from init_scaffold import chapter_stub  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a chapter stub .tex file")
    parser.add_argument("filename", help="e.g. ch01-wrong-object")
    parser.add_argument("title", help="Chapter title")
    parser.add_argument("label", help="Short label for \\label{ch:...}")
    args = parser.parse_args()

    path = ROOT / "chapters" / f"{args.filename}.tex"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(chapter_stub(args.filename, args.title, args.label), encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
