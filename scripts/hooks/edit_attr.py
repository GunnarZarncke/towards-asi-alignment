"""Shared helpers for edit attribution: paths, snapshots, turns, interval classification, authbars.

Interval kinds (per tracked file, per pair of consecutive snapshots):

  human               no agent turn active
  human-during-agent  agent turn active, file not in its edit list, turn used no shell
  rejected            human-interval lines that undo agent lines since the last commit
                      (rewind, checkpoint restore, Cursor reject, hand revert)
  agent               file in exactly one active turn's edit list
  agent-declared      file matches a pattern the owning turn declared (declare_edits.py) for
                      shell edits no hook could measure; credited only if the file changed
  agent-bash          one active turn ran an unmeasured shell command, so its file list is incomplete
  agent-interrupted   the owning turn was interrupted; later lines may be human
  agent-overlap       several agent turns could own the file
  unattributed        the owning turn lost its end hook (no Stop, no next prompt)

Bars: human kinds add human weight, agent kinds add agent weight, rejected and
unattributed add none. Whitespace-only lines and \\begin{authbar} lines never
add weight (the hook rewrites keys itself).

Correction-prompt rule (frozen 2026-09-29; feeds the acceptance rate in
drafts/plans/tsa-on-itself.md §3.10, whose stop condition applies): a prompt is
kind "correction" if it follows an interrupted turn, or matches CORRECTION_START
at its start, or CORRECTION_ANY anywhere. Change the patterns only with a dated
note here; do not tune them against scored months.
"""

from __future__ import annotations

import fcntl
import fnmatch
import json
import os
import re
import subprocess
import tempfile
from collections import Counter
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable, Iterator

AUTH_BEGIN_RE = re.compile(r"\\begin\{authbar\}\{([^}]*)\}")
AUTH_END = "\\end{authbar}"
SITE_SYNC_PREFIX = "site/src/content/book/"
TS_PATTERN = r"\d{8}T\d{6}(?:\.\d{3})?Z"
LOST_AFTER = timedelta(hours=6)

HUMAN_KINDS = ("human", "human-during-agent")
AGENT_KINDS = ("agent", "agent-declared", "agent-bash", "agent-interrupted", "agent-overlap")
TRACKED_TOPS = ("chapters", "appendices", "frontmatter", "site/src")

CORRECTION_START = re.compile(
    r"^\s*(no\b|nope\b|not\s+(that|this|what)\b|don'?t\b|do\s+not\b|stop\b|wait\b|undo\b|"
    r"revert\b|roll\s*back\b|wrong\b|that'?s\s+(wrong|not)\b|this\s+is\s+(wrong|not)\b|"
    r"actually\b|instead\b|why\s+did\s+you\b)",
    re.IGNORECASE,
)
CORRECTION_ANY = re.compile(
    r"\b(revert|undo|roll\s*back|put\s+(it|that|this)\s+back|change\s+(it|that|this)\s+back|"
    r"you\s+(broke|removed|deleted|dropped|missed|forgot|ignored)|not\s+what\s+i\s+(asked|meant|wanted)|"
    r"i\s+(said|asked\s+for)|that'?s\s+wrong|is\s+wrong|incorrect)\b",
    re.IGNORECASE,
)


# --- time -------------------------------------------------------------------

def now_stamp() -> str:
    n = datetime.now(timezone.utc)
    return n.strftime("%Y%m%dT%H%M%S") + f".{n.microsecond // 1000:03d}Z"


def parse_ts(ts: str) -> datetime:
    fmt = "%Y%m%dT%H%M%S.%fZ" if "." in ts else "%Y%m%dT%H%M%SZ"
    return datetime.strptime(ts, fmt).replace(tzinfo=timezone.utc)


def format_ts(ts: str) -> str:
    return parse_ts(ts).strftime("%Y-%m-%dT%H:%MZ")


# --- repo and telemetry paths ----------------------------------------------

def repo_root() -> Path:
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return Path(env).resolve()
    out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    return Path(out)


def git_dir(root: Path | None = None) -> Path:
    root = root or repo_root()
    raw = subprocess.check_output(["git", "rev-parse", "--git-dir"], cwd=root, text=True).strip()
    p = Path(raw)
    return p if p.is_absolute() else root / p


def telemetry_dir(root: Path | None = None) -> Path:
    d = (root or repo_root()) / "telemetry"
    d.mkdir(parents=True, exist_ok=True)
    return d


def hook_log(root: Path, msg: str) -> None:
    line = f"{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} {msg}\n"
    append_text(telemetry_dir(root) / "hooks.log", line)


def tracked_class(rel: str) -> str | None:
    rel = rel.replace("\\", "/").lstrip("./")
    if rel.startswith(SITE_SYNC_PREFIX):
        return None
    if rel.startswith(("chapters/", "appendices/", "frontmatter/")):
        return "manuscript"
    if rel.startswith("site/src/"):
        return "site"
    return None


def chapter_of(rel: str) -> str | None:
    name = Path(rel).name
    m = re.match(r"(ch\d+|app[A-Z]|preface|introduction|executive-overview|current-status)", name)
    if m:
        return m.group(1)
    parts = rel.split("/")
    if len(parts) >= 2 and parts[0] in ("chapters", "appendices", "frontmatter"):
        return Path(parts[1]).stem
    return None


# --- locked, atomic files ---------------------------------------------------

@contextmanager
def file_lock(path: Path) -> Iterator[None]:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(str(path) + ".lock", "a") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)


def write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".", suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)


def append_text(path: Path, text: str) -> None:
    with file_lock(path):
        with path.open("a", encoding="utf-8") as f:
            f.write(text)


def append_jsonl(path: Path, row: dict) -> None:
    append_text(path, json.dumps(row) + "\n")


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


# --- per-session hook state ---------------------------------------------------

def session_state_path(root: Path, tool: str, session: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9._-]", "-", session)[:80]
    d = telemetry_dir(root) / "state"
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{tool}-{safe}.json"


def load_state(root: Path, tool: str, session: str) -> dict:
    p = session_state_path(root, tool, session)
    if not p.exists():
        return {}
    text = p.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            obj, _ = json.JSONDecoder().raw_decode(text)
            hook_log(root, f"state {p.name}: corrupt, recovered first object")
            return obj if isinstance(obj, dict) else {}
        except json.JSONDecodeError:
            hook_log(root, f"state {p.name}: corrupt, reset")
            return {}


def save_state(root: Path, tool: str, session: str, data: dict) -> None:
    write_atomic(session_state_path(root, tool, session), json.dumps(data, indent=2) + "\n")


@contextmanager
def locked_state(root: Path, tool: str, session: str) -> Iterator[dict]:
    """Read-modify-write of one session's state under an exclusive lock."""
    p = session_state_path(root, tool, session)
    with file_lock(p):
        st = load_state(root, tool, session)
        yield st
        save_state(root, tool, session, st)


def turns_path(root: Path) -> Path:
    return telemetry_dir(root) / "turns.jsonl"


def load_turn_rows(root: Path) -> dict[str, dict]:
    """Turn records keyed by start snapshot sha; later rows win."""
    out: dict[str, dict] = {}
    for r in load_jsonl(turns_path(root)):
        if r.get("start_sha"):
            out[r["start_sha"]] = r
    return out


def declarations_path(root: Path) -> Path:
    return telemetry_dir(root) / "declarations.jsonl"


def pattern_matches(pattern: str, rel: str) -> bool:
    """Glob on the repo-relative path, or a regex with a 're:' prefix."""
    if pattern.startswith("re:"):
        try:
            return re.search(pattern[3:], rel) is not None
        except re.error:
            return False
    return fnmatch.fnmatch(rel, pattern.lstrip("./"))


def stat_map(root: Path) -> dict[str, list[int]]:
    """(mtime_ns, size) for every tracked-tree file; ~20 ms on this repo."""
    out: dict[str, list[int]] = {}
    for top in TRACKED_TOPS:
        for dp, _, files in os.walk(root / top):
            for f in files:
                p = Path(dp) / f
                rel = str(p.relative_to(root)).replace("\\", "/")
                if not tracked_class(rel):
                    continue
                try:
                    st = p.stat()
                except OSError:
                    continue
                out[rel] = [st.st_mtime_ns, st.st_size]
    return out


def changed_paths(before: dict, after: dict) -> list[str]:
    return sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))


def classify_prompt(prompt: str, after_interrupt: bool) -> tuple[str, str]:
    if after_interrupt:
        return "correction", "after-interrupt"
    m = CORRECTION_START.search(prompt or "")
    if m:
        return "correction", "start:" + m.group(1).lower().strip()
    m = CORRECTION_ANY.search(prompt or "")
    if m:
        return "correction", "any:" + m.group(1).lower()
    return "request", ""


# --- git helpers ---------------------------------------------------------------

def run_git(root: Path, args: list[str], check: bool = True, input: str | None = None) -> str:
    return subprocess.run(
        ["git", *args], cwd=root, text=True, capture_output=True, check=check, input=input
    ).stdout


def tree_of(root: Path, sha: str) -> str:
    return run_git(root, ["rev-parse", f"{sha}^{{tree}}"], check=False).strip()


def numstat(root: Path, a: str, b: str, paths: Iterable[str] | None = None) -> list[tuple[int, int, str]]:
    cmd = ["diff", "--numstat", "--no-renames", a, b, "--"]
    if paths:
        cmd.extend(paths)
    rows = []
    for line in run_git(root, cmd, check=False).splitlines():
        parts = line.split("\t")
        if len(parts) != 3 or parts[0] == "-" or parts[1] == "-":
            continue
        rows.append((int(parts[0]), int(parts[1]), parts[2]))
    return rows


def diff_lines(root: Path, sha_a: str, sha_b: str, rel: str) -> list[tuple[int, str, str]]:
    """Changed lines as (line_no, 'old'|'new', text); old-side numbers for removals."""
    out = run_git(root, ["diff", "-U0", "--no-renames", sha_a, sha_b, "--", rel], check=False)
    events: list[tuple[int, str, str]] = []
    old_ln = new_ln = 0
    hunk_re = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")
    for line in out.splitlines():
        hm = hunk_re.match(line)
        if hm:
            old_ln, new_ln = int(hm.group(1)), int(hm.group(3))
            continue
        if line.startswith(("+++", "---", "diff", "index", "\\")):
            continue
        if line.startswith("+"):
            events.append((new_ln, "new", line[1:]))
            new_ln += 1
        elif line.startswith("-"):
            events.append((old_ln, "old", line[1:]))
            old_ln += 1
    return events


def blob_text(root: Path, sha: str, rel: str) -> str | None:
    r = subprocess.run(["git", "show", f"{sha}:{rel}"], cwd=root, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


# --- snapshots -----------------------------------------------------------------

@dataclass
class Snap:
    ts: str
    label: str
    tool: str
    session: str
    sha: str
    ref: str
    generation: str = ""
    parent: str = ""


def parse_ref_name(name: str) -> tuple[str, str, str, str] | None:
    short = name.split("refs/snapshots/", 1)[-1]
    m = re.match(rf"^({TS_PATTERN})-(agent-start|agent-end|precommit)-([^-]+)-(.*)$", short)
    if not m:
        return None
    return m.group(1), m.group(2), m.group(3), m.group(4)


def list_snapshots(root: Path) -> list[Snap]:
    try:
        out = run_git(
            root,
            ["for-each-ref", "--format=%(refname)%00%(objectname)%00%(parent)%00%(subject)", "refs/snapshots/"],
        )
    except subprocess.CalledProcessError:
        return []
    snaps: list[Snap] = []
    for line in out.splitlines():
        parts = line.split("\0")
        if len(parts) != 4:
            continue
        ref, sha, parent, subject = parts
        parsed = parse_ref_name(ref)
        if not parsed:
            continue
        ts, label, tool, session = parsed
        words = subject.split()
        gen = words[4] if len(words) >= 5 and words[4] != "-" else ""
        snaps.append(Snap(ts, label, tool, session, sha, ref, gen, parent.split()[0] if parent else ""))
    snaps.sort(key=lambda s: (parse_ts(s.ts), s.ref))
    return snaps


# --- turns and interval classification -----------------------------------------------

@dataclass
class Turn:
    tool: str
    session: str
    start: Snap
    end_ts: str | None
    status: str  # completed | aborted | interrupted | api-error | lost | open
    final: bool
    touched: set[str] = field(default_factory=set)
    bash: bool | None = None  # None: no turn record, file list unknown
    prompt_id: str = ""
    declared: list[str] = field(default_factory=list)


def resolve_turns(snaps: list[Snap], rows: dict[str, dict], now: datetime | None = None) -> list[Turn]:
    now = now or datetime.now(timezone.utc)
    by_sha = {s.sha: s for s in snaps}
    turns: list[Turn] = []
    for i, s in enumerate(snaps):
        if s.label != "agent-start":
            continue
        rec = rows.get(s.sha, {})
        t = Turn(
            tool=s.tool,
            session=s.session,
            start=s,
            end_ts=None,
            status="open",
            final=False,
            touched=set(rec.get("touched") or []),
            bash=rec.get("bash") if "bash" in rec else None,
            prompt_id=rec.get("prompt_id") or s.generation,
            declared=list(rec.get("declared") or []),
        )
        later = snaps[i + 1 :]
        if rec.get("end_sha") in by_sha:
            t.end_ts, t.status, t.final = by_sha[rec["end_sha"]].ts, rec.get("status") or "completed", True
        else:
            nxt = next(
                (x for x in later if x.tool == s.tool and x.session == s.session and x.label != "precommit"),
                None,
            )
            if nxt is not None:
                t.end_ts, t.final = nxt.ts, True
                if nxt.label == "agent-end":
                    t.status = "completed"
                else:
                    # Claude Code never runs Stop on a user interrupt; other tools missed a hook.
                    t.status = "interrupted" if s.tool == "claude" else "lost"
            else:
                if s.tool == "claude":
                    # A manual commit (no Claude session in the committer env) proves the turn is over.
                    pc = next((x for x in later if x.label == "precommit" and x.generation == "none"), None)
                    if pc is not None:
                        t.end_ts, t.status = pc.ts, "interrupted"
                if parse_ts(s.ts) + LOST_AFTER < now:
                    t.final = True
                    if t.end_ts is None:
                        far = next((x for x in later if parse_ts(x.ts) > parse_ts(s.ts) + LOST_AFTER), None)
                        t.end_ts, t.status = (far.ts if far else None), "lost"
        turns.append(t)
    return turns


def file_kind(path: str, active: list[Turn]) -> tuple[str, Turn | None]:
    if not active:
        return "human", None
    owners = [t for t in active if path in t.touched]
    if len(owners) == 1:
        t = owners[0]
        return ("agent-interrupted" if t.status == "interrupted" else "agent"), t
    if len(owners) > 1:
        return "agent-overlap", None
    declared = [t for t in active if any(pattern_matches(p, path) for p in t.declared)]
    if len(declared) == 1:
        t = declared[0]
        return ("agent-interrupted" if t.status == "interrupted" else "agent-declared"), t
    if len(declared) > 1:
        return "agent-overlap", None
    shellish = [t for t in active if t.bash is None or t.bash or t.status == "lost"]
    if not shellish:
        return "human-during-agent", None
    if len(shellish) > 1:
        return "agent-overlap", None
    t = shellish[0]
    if t.status == "lost":
        return "unattributed", t
    if t.status == "interrupted":
        return "agent-interrupted", t
    return "agent-bash", t


class Engine:
    """Classifies every pair of consecutive snapshots; caches git diffs."""

    def __init__(self, root: Path, now: datetime | None = None):
        self.root = root
        self.snaps = list_snapshots(root)
        self.turns = resolve_turns(self.snaps, load_turn_rows(root), now)
        self.pairs = list(zip(self.snaps, self.snaps[1:]))
        self._ns: dict[tuple[str, str], list[tuple[int, int, str]]] = {}
        self._dl: dict[tuple[str, str, str], list[tuple[int, str, str]]] = {}

    def active(self, a: Snap, b: Snap) -> list[Turn]:
        ta, tb = parse_ts(a.ts), parse_ts(b.ts)
        out = []
        for t in self.turns:
            if parse_ts(t.start.ts) > ta:
                continue
            if t.end_ts is not None and parse_ts(t.end_ts) < tb:
                continue
            if t.end_ts is None and t.status == "lost":
                continue
            out.append(t)
        return out

    def final(self, a: Snap, b: Snap) -> bool:
        return all(t.final for t in self.active(a, b))

    def numstat(self, a: Snap, b: Snap) -> list[tuple[int, int, str]]:
        key = (a.sha, b.sha)
        if key not in self._ns:
            self._ns[key] = [r for r in numstat(self.root, a.sha, b.sha) if tracked_class(r[2])]
        return self._ns[key]

    def lines(self, a: Snap, b: Snap, rel: str) -> list[tuple[int, str, str]]:
        key = (a.sha, b.sha, rel)
        if key not in self._dl:
            self._dl[key] = diff_lines(self.root, a.sha, b.sha, rel)
        return self._dl[key]

    def reverted(self, a: Snap, b: Snap, rel: str) -> tuple[list[int], list[int]]:
        """Line numbers in a->b that undo agent lines written since the last commit."""
        added_by_agent: Counter[str] = Counter()
        removed_by_agent: Counter[str] = Counter()
        for x, y in self.pairs:
            if y.parent != a.parent or parse_ts(y.ts) > parse_ts(a.ts):
                continue
            if not any(p == rel for _, _, p in self.numstat(x, y)):
                continue
            kind, _ = file_kind(rel, self.active(x, y))
            if kind not in AGENT_KINDS:
                continue
            for _, side, text in self.lines(x, y, rel):
                (added_by_agent if side == "new" else removed_by_agent)[text] += 1
        rev_old: list[int] = []
        rev_new: list[int] = []
        for ln, side, text in self.lines(a, b, rel):
            pool, out = (added_by_agent, rev_old) if side == "old" else (removed_by_agent, rev_new)
            if pool[text] > 0:
                pool[text] -= 1
                out.append(ln)
        return rev_old, rev_new

    def rows_for_pair(self, a: Snap, b: Snap) -> list[dict]:
        active = self.active(a, b)
        out: list[dict] = []
        for added, removed, path in self.numstat(a, b):
            kind, turn = file_kind(path, active)
            base = {
                "ts_start": a.ts,
                "ts_end": b.ts,
                "tool": turn.tool if turn else ",".join(sorted({t.tool for t in active})),
                "session": turn.session if turn else ",".join(sorted({t.session for t in active})),
                "generation": turn.prompt_id if turn else "",
                "file": path,
                "class": tracked_class(path),
                "chapter": chapter_of(path),
                "sha_start": a.sha,
                "sha_end": b.sha,
            }
            if kind in HUMAN_KINDS:
                rev_old, rev_new = self.reverted(a, b, path)
                h_add, h_rem = added - len(rev_new), removed - len(rev_old)
                if h_add or h_rem:
                    out.append({**base, "kind": kind, "added": h_add, "removed": h_rem,
                                "reverted_old": rev_old, "reverted_new": rev_new})
                if rev_old or rev_new:
                    out.append({**base, "kind": "rejected", "added": len(rev_new), "removed": len(rev_old)})
            else:
                out.append({**base, "kind": kind, "added": added, "removed": removed})
        return out


# --- authbars --------------------------------------------------------------------

def parse_authbar_spans(text: str) -> list[tuple[int, int, str]]:
    """Return (start_line, end_line, key) 1-based, inclusive."""
    lines = text.splitlines()
    spans: list[tuple[int, int, str]] = []
    i = 0
    while i < len(lines):
        m = AUTH_BEGIN_RE.search(lines[i])
        if not m:
            i += 1
            continue
        j = i + 1
        while j < len(lines) and AUTH_END not in lines[j]:
            j += 1
        spans.append((i + 1, j + 1 if j < len(lines) else len(lines), m.group(1).strip()))
        i = j + 1
    return spans


def set_nth_authbar_key(text: str, index: int, new_key: str) -> str:
    """Replace the index-th (0-based) \\begin{authbar}{...} key."""
    n = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal n
        hit = n == index
        n += 1
        return f"\\begin{{authbar}}{{{new_key}}}" if hit else m.group(0)

    return AUTH_BEGIN_RE.sub(repl, text)


def span_index_for_line(spans: list[tuple[int, int, str]], line: int) -> int | None:
    for i, (a, b, _) in enumerate(spans):
        if a <= line <= b:
            return i
    return None


def derive_key(prior: str, human: int, agent: int) -> str:
    has_h = prior in ("GZ", "GZ+AI") or human > 0
    has_a = prior in ("AI", "GZ+AI") or agent > 0
    if has_h and has_a:
        return "GZ+AI"
    if has_h:
        return "GZ"
    if has_a:
        return "AI"
    return prior or "AI"


def porcelain(root: Path) -> str:
    return run_git(root, ["status", "--porcelain"], check=False)
