#!/usr/bin/env python3
"""Check (and optionally fix) relative Markdown links inside the repository.

Scans tracked ``*.md`` files (excluding attic folders, archived session logs, and
``node_modules``) for ``[text](target)`` links whose target is a relative path
that does not exist. External URLs, anchors-only links, ``mailto:``, ``~/`` and
absolute paths are ignored. Anchors (``#...``) are stripped before checking.

Gitignored targets are checked **after** ``make generate`` (symbol census and
concept-graph outputs). Only gitignored paths that ``make check`` deliberately
does not build (``dist/pdf/``, toy-simulation ``results/`` JSON, the local
``data/lesswrong/`` corpus) are skipped.

Link targets must be **git-tracked** (``git ls-files``), not merely present in
the working tree, except the draft-to-draft case below. Untracked local files
must not make a link pass while CI (clean checkout) fails. Gitignored outputs
under ``GENERATED_IN_CHECK_PREFIXES`` are valid only when they exist on disk
after ``make generate``.

Stop rules (this is a gate):

- A broken link whose source and resolved target are both under ``drafts/``
  is printed and does **not** fail. That is ordinary draft debt.
- Any other broken link fails, unless ``scripts/markdown-link-baseline.txt``
  lists ``source<TAB>target`` (target as written, anchor stripped).
- A baseline line whose link is no longer broken fails, so the file shrinks
  when the link is fixed.
- A baselined link fails anyway when this run's diff adds or edits its line.
  The diff is ``HEAD^`` on a clean checkout (needs fetch-depth ≥ 2 in CI),
  ``HEAD`` when the worktree is dirty, and the staged diff for ``--staged``.

    python3 scripts/check_markdown_links.py            # report; exit 1 on a blocking miss
    python3 scripts/check_markdown_links.py --staged   # staged diff only (pre-commit)
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
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, unquote

ROOT = Path(__file__).resolve().parent.parent
BASELINE_PATH = ROOT / "scripts" / "markdown-link-baseline.txt"
LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "#", "~/", "/", "file:")
SKIP_DIRS = {"node_modules", ".lake", ".git", ".venv", ".venv-test", "dist"}
# Markdown whose relative links are site routes, not repo paths.
SITE_ROUTED = ("metadata/concepts/bodies/", "site/src/content/")
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
HISTORICAL_DIRS = ("attic", "conversation-summaries/archive")
# Gitignored outputs produced by scripts/generate_manuscript_tex.sh before this check runs.
GENERATED_IN_CHECK_PREFIXES = ("metadata/concept-graph/", "metadata/symbol-census/")
# Gitignored paths outside make check scope (see scripts/check.sh — no PDF, no sim runs,
# no third-party LessWrong dump).
LINK_CHECK_EXEMPT_PREFIXES = (
    "dist/pdf/",
    "experiments/toy-simulation/results/",
    "data/lesswrong/",
)


@dataclass(frozen=True)
class BrokenLink:
    source: str
    lineno: int
    target: str
    clean: str
    resolved: str
    hint: str

    @property
    def key(self) -> str:
        return f"{self.source}\t{self.clean}"

    @property
    def draft_to_draft(self) -> bool:
        return self.source.startswith("drafts/") and (
            self.resolved == "drafts" or self.resolved.startswith("drafts/")
        )


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


def dir_has_tracked_content(dir_rel: str, tracked: set[str], dirs: set[str]) -> bool:
    d = dir_rel.rstrip("/")
    if not d:
        return False
    if d in dirs:
        return True
    prefix = d + "/"
    return any(p.startswith(prefix) for p in tracked)


def is_valid_link_target(
    rel_to: str,
    clean: str,
    resolved: Path,
    tracked: set[str],
    dirs: set[str],
) -> bool:
    """True when the target is valid for CI and local make check alike."""
    if is_exempt_gitignored_target(rel_to):
        return True
    if rel_to in tracked:
        return True
    if (
        resolved.exists()
        and is_gitignored(rel_to)
        and rel_to.startswith(GENERATED_IN_CHECK_PREFIXES)
    ):
        return True
    is_dir_link = clean.endswith("/") or clean in (".", "./")
    if is_dir_link and dir_has_tracked_content(rel_to, tracked, dirs):
        return True
    return False


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


def load_baseline(text: str) -> set[str]:
    """Parse ``source<TAB>target`` lines. Comments and blank lines are ignored."""
    keys: set[str] = set()
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "\t" not in line:
            raise SystemExit(
                f"{BASELINE_PATH.relative_to(ROOT)}:{lineno}: expected source<TAB>target"
            )
        source, target = line.split("\t", 1)
        source = source.strip()
        target = target.strip()
        if not source or not target:
            raise SystemExit(
                f"{BASELINE_PATH.relative_to(ROOT)}:{lineno}: empty source or target"
            )
        keys.add(f"{source}\t{target}")
    return keys


def read_baseline_text(staged: bool) -> str:
    rel = BASELINE_PATH.relative_to(ROOT).as_posix()
    if staged:
        got = subprocess.run(
            ["git", "show", f":{rel}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if got.returncode == 0:
            return got.stdout
    if BASELINE_PATH.exists():
        return BASELINE_PATH.read_text(encoding="utf-8")
    return ""


def link_cleans(text: str) -> set[str]:
    found: set[str] = set()
    for match in LINK_RE.finditer(text):
        target = match.group(1)
        if target.startswith(SKIP_PREFIXES) or "://" in target:
            continue
        clean = unquote(target.split("#", 1)[0])
        if clean and not UUID_RE.match(clean):
            found.add(clean)
    return found


def classify_target(
    path: Path,
    lineno: int,
    target: str,
    idx: dict[str, list[Path]],
    paths: list[str],
    dirs: set[str],
    tracked: set[str],
) -> tuple[BrokenLink | None, str | None]:
    """Return ``(broken, rewrite_to)``.

    ``broken`` is None when the link is skipped or valid. ``rewrite_to`` is a
    repo-relative path when ``--fix`` can name exactly one file.
    """
    if target.startswith(SKIP_PREFIXES) or "://" in target:
        return None, None
    clean = unquote(target.split("#", 1)[0])
    if not clean or UUID_RE.match(clean):
        return None, None
    resolved = (path.parent / clean).resolve()
    try:
        rel_to = str(resolved.relative_to(ROOT))
    except ValueError:
        return None, None  # points outside the repository (sibling repo); not checked
    if is_valid_link_target(rel_to, clean, resolved, tracked, dirs):
        return None, None
    candidates = idx.get(Path(clean).name, [])
    new_target: str | None = None
    if len(candidates) == 1 and not clean.endswith("/"):
        new_target = str(candidates[0])
    else:
        new_target = resolve_by_suffix(clean, paths, dirs)
    hint = ""
    if resolved.exists() and rel_to not in tracked:
        hint = " (exists locally but is not git-tracked)"
    elif len(candidates) > 1:
        hint = f" (ambiguous: {', '.join(str(c) for c in candidates[:4])})"
    elif not candidates:
        hint = " (no file with that name)"
    source = str(path.relative_to(ROOT))
    broken = BrokenLink(source, lineno, target, clean, rel_to, hint)
    return broken, new_target


def check_file(
    path: Path,
    idx: dict[str, list[Path]],
    paths: list[str],
    dirs: set[str],
    tracked: set[str],
    fix: bool,
) -> tuple[list[BrokenLink], int]:
    text = path.read_text(encoding="utf-8")
    problems: list[BrokenLink] = []
    fixed = 0
    lines = text.split("\n")
    new_lines = []
    for lineno, line in enumerate(lines, 1):
        def repl(m: re.Match, lineno: int = lineno) -> str:
            nonlocal fixed
            target = m.group(1)
            broken, new_target = classify_target(path, lineno, target, idx, paths, dirs, tracked)
            if broken is None:
                return m.group(0)
            if fix and new_target:
                new_rel = os.path.relpath(ROOT / new_target, path.parent)
                if new_target.endswith("/"):
                    new_rel += "/"
                anchor = target.split("#", 1)[1] if "#" in target else ""
                fixed += 1
                return m.group(0).replace(
                    target, quote(new_rel, safe="/.-_~()") + ("#" + anchor if anchor else "")
                )
            problems.append(broken)
            return m.group(0)

        new_lines.append(LINK_RE.sub(repl, line))
    if fix and fixed:
        path.write_text("\n".join(new_lines), encoding="utf-8")
    return problems, fixed


def parse_added_lines(diff: str) -> list[tuple[str, int, str]]:
    """``(repo path, new lineno, line text)`` for ``+`` lines in a ``-U0`` diff."""
    path: str | None = None
    lineno: int | None = None
    added: list[tuple[str, int, str]] = []
    for line in diff.splitlines():
        if line.startswith("+++ "):
            raw = line[4:]
            if raw.startswith("b/"):
                raw = raw[2:]
            path = None if raw == "/dev/null" else raw
            lineno = None
            continue
        hunk = HUNK_RE.match(line)
        if hunk:
            lineno = int(hunk.group(1))
            continue
        if path is None or lineno is None:
            continue
        if line.startswith("+"):
            added.append((path, lineno, line[1:]))
            lineno += 1
        elif line.startswith("-") or line.startswith("\\"):
            continue
        else:
            lineno += 1
    return added


def git_diff(args: list[str]) -> str:
    # git diff exits 1 when there is a difference. That is a result, not a failure.
    got = subprocess.run(
        ["git", "diff", "-U0", "--no-color", *args, "--", "*.md"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if got.returncode > 1:
        raise subprocess.CalledProcessError(got.returncode, got.args, got.stdout, got.stderr)
    return got.stdout


def worktree_dirty() -> bool:
    for args in (["--quiet", "HEAD"], ["--cached", "--quiet", "HEAD"]):
        if subprocess.run(["git", "diff", *args], cwd=ROOT).returncode != 0:
            return True
    return False


def diff_args(staged: bool) -> list[str] | None:
    if staged:
        return ["--cached"]
    override = os.environ.get("MARKDOWN_LINKS_DIFF_BASE", "").strip()
    if override:
        return [override]
    if worktree_dirty():
        return ["HEAD"]
    if subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", "HEAD^"],
        cwd=ROOT,
        capture_output=True,
    ).returncode == 0:
        return ["HEAD^"]
    return None


def staged_names() -> set[str]:
    got = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--", "*.md", "scripts/markdown-link-baseline.txt"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if got.returncode > 1:
        raise subprocess.CalledProcessError(got.returncode, got.args, got.stdout, got.stderr)
    return {line for line in got.stdout.splitlines() if line}


def index_text(rel: str) -> str | None:
    got = subprocess.run(
        ["git", "show", f":{rel}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if got.returncode != 0:
        return None
    return got.stdout


def format_broken(item: BrokenLink, note: str) -> str:
    return f"{note} {item.source}:{item.lineno}: {item.target}{item.hint}"


def report(blocking: list[str], drafts: list[str], known: list[str], stale: list[str]) -> int:
    for line in drafts:
        print(line)
    for line in known:
        print(line)
    for line in blocking:
        print(line)
    for line in stale:
        print(line)
    if blocking or stale:
        bits = []
        if blocking:
            bits.append(f"{len(blocking)} blocking broken link(s)")
        if stale:
            bits.append(f"{len(stale)} stale baseline line(s)")
        print("; ".join(bits))
        return 1
    print(
        "Markdown link check passed. "
        f"{len(drafts)} draft-to-draft link(s) not blocking; {len(known)} baselined."
    )
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix", action="store_true", help="rewrite uniquely resolvable links")
    ap.add_argument("--all", action="store_true", help="include attic and archived logs")
    ap.add_argument(
        "--staged",
        action="store_true",
        help="check links added in the index, and baseline lines whose source is staged",
    )
    args = ap.parse_args()
    idx, paths, dirs = basename_index()
    tracked = set(paths)
    baseline = load_baseline(read_baseline_text(args.staged))
    base = diff_args(args.staged)
    added = parse_added_lines(git_diff(base)) if base is not None else []
    touched = {(path, lineno) for path, lineno, _text in added}

    if args.staged:
        drafts: list[str] = []
        blocking: list[str] = []
        for path_rel, lineno, text in added:
            path = ROOT / path_rel
            for match in LINK_RE.finditer(text):
                broken, _new = classify_target(
                    path, lineno, match.group(1), idx, paths, dirs, tracked
                )
                if broken is None:
                    continue
                if broken.draft_to_draft:
                    drafts.append(format_broken(broken, "draft"))
                else:
                    blocking.append(format_broken(broken, "BLOCK"))
        stale: list[str] = []
        staged = staged_names()
        for key in sorted(baseline):
            source, clean = key.split("\t", 1)
            if source not in staged:
                continue
            blob = index_text(source)
            if blob is None or clean not in link_cleans(blob):
                stale.append(f"stale {key} (staged source no longer contains this link)")
        return report(blocking, drafts, [], stale)

    problems: list[BrokenLink] = []
    fixed_total = 0
    for f in tracked_markdown(args.all):
        found, n = check_file(f, idx, paths, dirs, tracked, args.fix)
        problems.extend(found)
        fixed_total += n
    if args.fix:
        print(f"fixed {fixed_total} link(s)")

    drafts = []
    known = []
    blocking = []
    seen: set[str] = set()
    for item in problems:
        seen.add(item.key)
        if item.draft_to_draft:
            drafts.append(format_broken(item, "draft"))
            continue
        if item.key in baseline and (item.source, item.lineno) not in touched:
            known.append(format_broken(item, "baseline"))
            continue
        why = "BLOCK"
        if item.key in baseline:
            why = "BLOCK (baseline, but this diff edits the line)"
        blocking.append(format_broken(item, why))
    stale = [
        f"stale {key} (link is no longer broken; delete the baseline line)"
        for key in sorted(baseline)
        if key not in seen
    ]
    return report(blocking, drafts, known, stale)


if __name__ == "__main__":
    sys.exit(main())
