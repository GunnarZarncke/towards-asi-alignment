#!/usr/bin/env python3
"""One-shot migration: line-local G-/F-/N- IDs → global prefixed IDs."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (root-relative dir, old prefix pattern, new prefix)
LINE_RULES: list[tuple[str, str, str]] = [
    ("experiments/graded-lab-simulation", "G-", "GL-"),
    ("experiments/lab-simulation", "G-", "LS-"),
    ("experiments/goal-agent-simulation", "F-", "GA-"),
    ("experiments/embedded-simulation", "N-", "ES-"),
]

# Shared manuscript/docs files: apply all replacements (prefixes disambiguate)
SHARED_FILES = [
    "appendices/appN-experimental-evidence.tex",
    "metadata/experiments.yml",
    "metadata/claims-ledger.md",
    "docs/EXPERIMENTS.md",
    "docs/FINDING_IDS.md",
    "README.md",
    "experiments/README.md",
]

SHARED_DIRS = [
    "chapters",
]

TEXT_SUFFIXES = {".md", ".tex", ".yml", ".py", ".mjs", ".json"}


def replace_ids(text: str, old: str, new: str) -> str:
    # G-41 before G-4: sort numeric suffixes descending when old ends with -
    if old.endswith("-"):
        pat = re.compile(
            rf"(?<![A-Z]){re.escape(old)}(\d+[a-z]?)(?![0-9a-z])"
        )

        def sub(m: re.Match[str]) -> str:
            return f"{new}{m.group(1)}"

        return pat.sub(sub, text)
    return text


def iter_files(base: Path) -> list[Path]:
    if base.is_file():
        return [base]
    out: list[Path] = []
    for p in base.rglob("*"):
        if p.is_file() and p.suffix in TEXT_SUFFIXES:
            if "node_modules" in p.parts or ".git" in p.parts:
                continue
            out.append(p)
    return out


def migrate_tree(rel_dir: str, old: str, new: str) -> int:
    base = ROOT / rel_dir
    if not base.exists():
        return 0
    changed = 0
    for path in iter_files(base):
        text = path.read_text(encoding="utf-8")
        new_text = replace_ids(text, old, new)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed += 1
    return changed


def migrate_shared() -> int:
    changed = 0
    files = [ROOT / f for f in SHARED_FILES]
    for rel in SHARED_DIRS:
        files.extend(iter_files(ROOT / rel))
    for path in files:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        new_text = text
        # Only non-colliding prefixes in shared files (G- handled per-line above).
        new_text = replace_ids(new_text, "F-", "GA-")
        new_text = replace_ids(new_text, "N-", "ES-")
        new_text = new_text.replace("T-1", "TS-1").replace("T-2", "TS-2").replace("T-3", "TS-3")
        new_text = re.sub(r"\bE-(\d+[a-z]?)\b", r"ES-\1", new_text)
        new_text = re.sub(r"\bL-(\d+[a-z]?)\b", r"LS-\1", new_text)
        new_text = new_text.replace("finding:t-", "finding:ts-")
        new_text = new_text.replace("finding:e-", "finding:es-")
        new_text = new_text.replace("finding:l-", "finding:ls-")
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed += 1
    return changed


def main() -> int:
    total = 0
    for rel, old, new in LINE_RULES:
        n = migrate_tree(rel, old, new)
        print(f"{rel}: {old} → {new}: {n} files")
        total += n
    n = migrate_shared()
    print(f"shared manuscript/docs: {n} files")
    total += n
    print(f"total files changed: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
