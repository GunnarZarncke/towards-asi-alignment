#!/usr/bin/env python3
"""Check (and optionally fix) relative Markdown links inside the repository.

Scans tracked ``*.md`` files (excluding attic folders, archived session logs, and
``node_modules``) for ``[text](target)`` links whose target is a relative path
that does not exist. External URLs, anchors-only links, ``mailto:``, ``~/`` and
absolute paths are ignored. Anchors (``#...``) are stripped before checking.

Gitignored targets are checked **after** ``make generate`` (symbol census and
concept-graph outputs). Only gitignored paths that ``make check`` deliberately
does not build (``dist/pdf/``, toy-simulation ``results/`` JSON) are skipped.

    python3 scripts/check_markdown_links.py            # report, exit 1 on failures
    python3 scripts/check_markdown_links.py --fix      # rewrite links whose basename
                                                        # resolves to exactly one file
    python3 scripts/check_markdown_links.py --all      # include attic/archive folders

Fixing is conservative: a broken target is rewritten only when its basename
matches exactly one file in the repository. Everything else is reported.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote, unquote

ROOT = Path(__file__).resolve().parent.parent
LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "#", "~/", "/", "file:")
SKIP_DIRS = {"node_modules", ".lake", ".git", ".venv", ".venv-test", "dist"}
# Markdown whose relative links are site routes, not repo paths.
SITE_ROUTED = ("metadata/concepts/bodies/", "site/src/content/")
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
HISTORICAL_DIRS = ("attic", "conversation-summaries/archive")
# Gitignored outputs produced by scripts/generate_manuscript_tex.sh before this check runs.
GENERATED_IN_CHECK_PREFIXES = ("metadata/concept-graph/", "metadata/symbol-census/")
# Gitignored paths outside make check scope (see scripts/check.sh — no PDF, no sim runs).
LINK_CHECK_EXEMPT_PREFIXES = ("dist/pdf/", "experiments/toy-simulation/results/")


def is_gitignored(rel: str) -> bool:
    return (
        subprocess.run(
            ["git", "check-ignore", "-q", "--", rel],
            cwd=ROOT,
            capture_output=True,
        ).returncode
        == 0
    )


def is_exempt_gitignored_target(rel: str) -> bool:
    """Skip link check for gitignored artifacts make check does not generate."""
    if not is_gitignored(rel):
        return False
    if rel.startswith(GENERATED_IN_CHECK_PREFIXES):
        return False  # must exist after generate
    return rel.startswith(LINK_CHECK_EXEMPT_PREFIXES)


def tracked_markdown(include_all: bool) -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files", "--", "*.md"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.splitlines()
    files = []
    for rel in out:
        parts = rel.split("/")
        if any(p in SKIP_DIRS for p in parts):
            continue
        if not include_all and (
            "attic" in parts or "conversation-summaries/archive" in rel
        ):
            continue
        if rel.startswith(SITE_ROUTED):
            continue
        # Dated session logs are records, not instructions; only the hub files are checked.
        if rel.startswith("drafts/conversation-summaries/") and re.match(r"\d{4}-\d{2}-\d{2}-", Path(rel).name):
            continue
        if (ROOT / rel).exists():  # tracked but deleted/moved in the working tree
            files.append(ROOT / rel)
    return files


def basename_index() -> tuple[dict[str, list[Path]], list[str], set[str]]:
    """Return (basename -> tracked files, all tracked paths, all tracked directories)."""
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True)
    idx: dict[str, list[Path]] = defaultdict(list)
    paths: list[str] = []
    dirs: set[str] = set()
    for rel in out.stdout.splitlines():
        p = Path(rel)
        idx[p.name].append(p)
        paths.append(rel)
        for parent in p.parents:
            if str(parent) != ".":
                dirs.add(str(parent))
    return idx, paths, dirs


def resolve_by_suffix(clean: str, paths: list[str], dirs: set[str]) -> str | None:
    """Resolve a broken relative target by the longest unique path suffix.

    ``../../reference/field-agendas/data/bridges.yml`` written from the wrong depth
    still names the file uniquely by its suffix ``reference/field-agendas/data/bridges.yml``.
    Directory targets (trailing slash) are matched against tracked directories.
    """
    suffix = re.sub(r"^(\.\./|\./)+", "", clean).rstrip("/")
    if not suffix:
        return None
    pool = dirs if clean.endswith("/") else set(paths)
    hits = [c for c in pool if c == suffix or c.endswith("/" + suffix)]
    if len(hits) == 1:
        return hits[0] + ("/" if clean.endswith("/") else "")
    return None


def check_file(
    path: Path, idx: dict[str, list[Path]], paths: list[str], dirs: set[str], fix: bool
) -> tuple[list[str], int]:
    text = path.read_text(encoding="utf-8")
    problems: list[str] = []
    fixed = 0
    lines = text.split("\n")
    new_lines = []
    for lineno, line in enumerate(lines, 1):
        def repl(m: re.Match) -> str:
            nonlocal fixed
            target = m.group(1)
            if target.startswith(SKIP_PREFIXES) or "://" in target:
                return m.group(0)
            clean = unquote(target.split("#", 1)[0])
            if not clean or UUID_RE.match(clean):
                return m.group(0)
            resolved = (path.parent / clean).resolve()
            try:
                rel_to = str(resolved.relative_to(ROOT))
            except ValueError:
                return m.group(0)  # points outside the repository (sibling repo); not checked
            if is_exempt_gitignored_target(rel_to):
                return m.group(0)  # outside make check scope; see LINK_CHECK_EXEMPT_PREFIXES
            if resolved.exists():
                return m.group(0)
            candidates = idx.get(Path(clean).name, [])
            new_target: str | None = None
            if len(candidates) == 1 and not clean.endswith("/"):
                new_target = str(candidates[0])
            else:
                new_target = resolve_by_suffix(clean, paths, dirs)
            if fix and new_target:
                new_rel = os.path.relpath(ROOT / new_target, path.parent)
                if new_target.endswith("/"):
                    new_rel += "/"
                anchor = target.split("#", 1)[1] if "#" in target else ""
                fixed += 1
                return m.group(0).replace(target, quote(new_rel, safe="/.-_~()") + ("#" + anchor if anchor else ""))
            hint = ""
            if len(candidates) > 1:
                hint = f" (ambiguous: {', '.join(str(c) for c in candidates[:4])})"
            elif not candidates:
                hint = " (no file with that name)"
            problems.append(f"{path.relative_to(ROOT)}:{lineno}: {target}{hint}")
            return m.group(0)

        new_lines.append(LINK_RE.sub(repl, line))
    if fix and fixed:
        path.write_text("\n".join(new_lines), encoding="utf-8")
    return problems, fixed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix", action="store_true", help="rewrite uniquely resolvable links")
    ap.add_argument("--all", action="store_true", help="include attic and archived logs")
    args = ap.parse_args()
    idx, paths, dirs = basename_index()
    problems: list[str] = []
    fixed_total = 0
    for f in tracked_markdown(args.all):
        p, n = check_file(f, idx, paths, dirs, args.fix)
        problems.extend(p)
        fixed_total += n
    if args.fix:
        print(f"fixed {fixed_total} link(s)")
    for line in problems:
        print(line)
    if problems:
        print(f"{len(problems)} broken relative link(s)")
        return 1
    print("Markdown link check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
