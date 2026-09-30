#!/usr/bin/env python3
"""Read-only recap of a Cursor/Claude session from recorded hooks + git.

Sources (best effort, no writes):
  - telemetry/prompts/*.jsonl  — verbatim user prompts + correction tags
  - telemetry/turns.jsonl      — agent turns, touched files, status
  - refs/snapshots/            — turn timing (via edit_attr.Engine)
  - git log in the session window — all committed files (incl. reference/, drafts/, …)
  - optional Cursor agent transcript JSONL — user queries when telemetry is missing

Does not append ledger rows, session logs, or prompt digests.

With no arguments, picks the most recent Cursor/Claude session from telemetry for
this repo, merges the matching Cursor transcript when found, and includes commits
in the inferred window.

Examples:
  python3 scripts/session_summary.py                    # latest session (defaults)
  python3 scripts/session_summary.py --session 9d8fadfc
  python3 scripts/session_summary.py --since 2026-09-29 --until 2026-09-30
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "hooks"))

from edit_attr import (  # noqa: E402
    AGENT_KINDS,
    Engine,
    HUMAN_KINDS,
    format_ts,
    load_jsonl,
    load_turn_rows,
    parse_ts,
    repo_root,
    run_git,
    telemetry_dir,
    tracked_class,
    turns_path,
)

USER_QUERY_RE = re.compile(r"<user_query>\s*(.*?)\s*</user_query>", re.DOTALL | re.IGNORECASE)
TRAILER_RE = re.compile(
    r"^(Human-Delta|Agent-Delta|Rejected-Delta|Unattributed-Delta|"
    r"Interrupts|Correction-Prompts):\s*(.+)$",
    re.MULTILINE,
)


def extract_user_text(prompt: str) -> str:
    m = USER_QUERY_RE.search(prompt or "")
    if m:
        return m.group(1).strip()
    text = prompt or ""
    for tag in ("<external_links>", "<timestamp>", "<git_status>", "<open_and_recently_viewed_files>"):
        text = text.split(tag, 1)[0]
    return text.strip()


def parse_iso(s: str) -> datetime:
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return datetime.fromisoformat(s).astimezone(timezone.utc)


def load_all_prompts(root: Path) -> list[dict]:
    rows: list[dict] = []
    prompt_dir = telemetry_dir(root) / "prompts"
    if not prompt_dir.exists():
        return rows
    for path in sorted(prompt_dir.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    rows.sort(key=lambda r: r.get("ts") or "")
    return rows


def session_matches(session: str, prefix: str) -> bool:
    return session == prefix or session.startswith(prefix)


def filter_prompts(
    prompts: list[dict],
    session_prefix: str | None,
    since: datetime | None,
    until: datetime | None,
) -> list[dict]:
    out: list[dict] = []
    for r in prompts:
        ts_raw = r.get("ts")
        if not ts_raw:
            continue
        ts = parse_iso(ts_raw)
        if since and ts < since:
            continue
        if until and ts > until:
            continue
        if session_prefix and not session_matches(r.get("session") or "", session_prefix):
            continue
        out.append(r)
    return out


def turns_for_sessions(root: Path, sessions: set[str]) -> list[dict]:
    rows = []
    for r in load_jsonl(turns_path(root)):
        sess = r.get("session") or ""
        if any(session_matches(sess, s) for s in sessions):
            rows.append(r)
    return rows


def window_from_prompts_and_turns(
    prompts: list[dict], turns: list[dict]
) -> tuple[datetime | None, datetime | None]:
    stamps: list[datetime] = []
    for r in prompts:
        if r.get("ts"):
            stamps.append(parse_iso(r["ts"]))
    for r in turns:
        if r.get("ts"):
            stamps.append(parse_iso(r["ts"]))
    if not stamps:
        return None, None
    pad_before = timedelta(minutes=30)
    pad_after = timedelta(hours=3)  # commits often land after the last Stop hook
    return min(stamps) - pad_before, max(stamps) + pad_after


def find_transcript(session_prefix: str) -> Path | None:
    base = Path.home() / ".cursor/projects"
    if not base.exists():
        return None
    patterns = [
        f"**/agent-transcripts/{session_prefix}*/{session_prefix}*.jsonl",
        f"**/agent-transcripts/*/{session_prefix}*.jsonl",
        f"**/agent-transcripts/{session_prefix}*/{session_prefix}.jsonl",
    ]
    for pat in patterns:
        hits = sorted(base.glob(pat))
        if hits:
            return hits[-1]
    return None


def latest_session_from_telemetry(root: Path) -> tuple[str | None, datetime | None]:
    """Session id prefix and timestamp of its newest prompt."""
    prompts = load_all_prompts(root)
    if not prompts:
        return None, None
    latest = max(prompts, key=lambda r: r.get("ts") or "")
    sess = latest.get("session") or ""
    if not sess:
        return None, None
    ts = parse_iso(latest["ts"]) if latest.get("ts") else None
    return sess[:8], ts


def find_latest_transcript(root: Path) -> tuple[Path | None, str | None]:
    """Newest agent transcript for this repo under ~/.cursor/projects/."""
    base = Path.home() / ".cursor/projects"
    if not base.exists():
        return None, None
    repo_name = root.name
    candidates = list(base.glob(f"*{repo_name}*/agent-transcripts/**/*.jsonl"))
    if not candidates:
        candidates = list(base.glob("**/agent-transcripts/**/*.jsonl"))
    if not candidates:
        return None, None
    latest = max(candidates, key=lambda p: p.stat().st_mtime)
    folder = latest.parent.name
    session_id = folder if folder != "agent-transcripts" else latest.stem
    prefix = session_id.split("-")[0] if session_id else None
    return latest, prefix


def start_of_today_utc() -> datetime:
    now = datetime.now(timezone.utc)
    return now.replace(hour=0, minute=0, second=0, microsecond=0)


@dataclass
class ResolvedDefaults:
    session_prefix: str | None
    since: datetime | None
    until: datetime | None
    transcript: Path | None
    label: str


def resolve_defaults(
    root: Path,
    session: str | None,
    since: datetime | None,
    until: datetime | None,
    transcript_arg: str | None,
    no_transcript: bool,
) -> ResolvedDefaults:
    """Fill gaps when the user passes no (or partial) filters."""
    if session or since or until:
        prefix = session
        tx: Path | None = None
        if not no_transcript:
            if transcript_arg and transcript_arg.lower() != "auto":
                tx = Path(transcript_arg).expanduser()
            elif transcript_arg == "auto" or (transcript_arg is None and prefix):
                tx = find_transcript(prefix) if prefix else None
        return ResolvedDefaults(prefix, since, until, tx, "explicit args")

    prefix, _ = latest_session_from_telemetry(root)
    tx = None
    if prefix and not no_transcript:
        tx = find_transcript(prefix)
        label = f"latest telemetry session `{prefix}`"
    else:
        tx_path, tx_prefix = find_latest_transcript(root)
        if tx_path and tx_prefix:
            prefix = tx_prefix
            tx = tx_path if not no_transcript else None
            label = f"latest transcript `{tx_path.name}` (session `{prefix}`)"
        else:
            since = start_of_today_utc()
            until = datetime.now(timezone.utc)
            label = f"today UTC ({since.date()}) — no telemetry or transcript"
    if prefix and not no_transcript and tx is None:
        tx = find_transcript(prefix)
    return ResolvedDefaults(prefix, since, until, tx, label)


def load_transcript_user_messages(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        obj = json.loads(line)
        if obj.get("role") != "user":
            continue
        content = obj.get("message", {}).get("content", [])
        parts: list[str] = []
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    parts.append(block.get("text") or "")
        else:
            parts.append(str(content))
        text = extract_user_text("\n".join(parts))
        if text:
            rows.append({"index": str(i), "text": text})
    return rows


def parse_commit_trailers(body: str) -> dict[str, str]:
    return {m.group(1): m.group(2).strip() for m in TRAILER_RE.finditer(body or "")}


def commits_in_window(root: Path, start: datetime, end: datetime) -> list[dict[str, Any]]:
    fmt = lambda d: d.strftime("%Y-%m-%dT%H:%M:%S")
    hashes = [
        h.strip()
        for h in run_git(
            root,
            ["log", f"--since={fmt(start)}", f"--until={fmt(end)}", "--format=%H"],
            check=False,
        ).splitlines()
        if h.strip()
    ]
    commits: list[dict[str, Any]] = []
    for h in hashes:
        meta = run_git(root, ["log", "-1", "--format=%H%x00%s%x00%b", h], check=False).split("\0")
        body = meta[2] if len(meta) > 2 else ""
        files = [
            f.strip()
            for f in run_git(
                root, ["diff-tree", "--no-commit-id", "--name-only", "-r", h], check=False
            ).splitlines()
            if f.strip()
        ]
        commits.append(
            {
                "hash": h,
                "short": h[:9],
                "subject": meta[1] if len(meta) > 1 else "",
                "trailers": parse_commit_trailers(body),
                "files": files,
            }
        )
    return commits


def rel_path(root: Path, raw: str) -> str:
    p = Path(raw)
    try:
        return str(p.resolve().relative_to(root)).replace("\\", "/")
    except ValueError:
        return raw.replace("\\", "/")


def agent_interval_files(root: Path, eng: Engine, sessions: set[str]) -> dict[str, list[str]]:
    """Tracked-tree files attributed to agent kinds for matching sessions."""
    from human_delta import all_interval_rows  # noqa: WPS433 — shared engine helper

    by_session: dict[str, set[str]] = defaultdict(set)
    for row in all_interval_rows(root, eng):
        if row.get("kind") not in AGENT_KINDS:
            continue
        sess = row.get("session") or ""
        if not any(session_matches(sess, s) for s in sessions):
            continue
        by_session[sess].add(row["file"])
    return {k: sorted(v) for k, v in by_session.items()}


def group_paths(paths: Iterable[str]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for p in sorted(set(paths)):
        top = p.split("/", 1)[0] if "/" in p else p or "(root)"
        groups[top].append(p)
    return dict(groups)


def truncate(text: str, limit: int) -> str:
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def render_markdown(data: dict[str, Any]) -> str:
    lines: list[str] = []
    title = data.get("title") or "Session summary"
    lines.append(f"# {title}")
    lines.append("")
    if data.get("window"):
        lines.append(f"**Window:** {data['window']}")
    if data.get("sessions"):
        lines.append(f"**Sessions:** {', '.join(f'`{s[:8]}…`' for s in data['sessions'])}")
    if data.get("sources"):
        lines.append(f"**Sources:** {', '.join(data['sources'])}")
    lines.append("")

    lines.append("## User requests")
    user_items = data.get("user_requests") or []
    if not user_items:
        lines.append("_No prompts found (telemetry missing or filters too narrow)._")
    else:
        for i, item in enumerate(user_items, 1):
            kind = item.get("kind") or "request"
            pid = item.get("prompt_id") or ""
            ts = item.get("ts") or ""
            head = f"{i}. "
            if kind != "request":
                head += f"**[{kind}]** "
            if pid:
                head += f"`{pid}` "
            if ts:
                head += f"({ts}) "
            lines.append(head + item.get("text", ""))
    lines.append("")

    lines.append("## Agent turns")
    turns = data.get("agent_turns") or []
    if not turns:
        lines.append("_No turn records in telemetry/turns.jsonl._")
    else:
        for i, t in enumerate(turns, 1):
            status = t.get("status") or "?"
            changed = t.get("tree_changed")
            flag = "edited" if changed else "no tracked-tree edit"
            lines.append(
                f"### Turn {i} — {status}, {flag} "
                f"(`{t.get('prompt_id') or '?'}`)"
            )
            touched = t.get("touched") or []
            if touched:
                for path in touched:
                    lines.append(f"- `{path}`")
            else:
                lines.append("- _(no files in turn edit list)_")
            if t.get("bash"):
                lines.append("- _unmeasured shell command (agent-bash risk)_")
            if t.get("failures"):
                lines.append(f"- _tool failures: {len(t['failures'])}_")
            lines.append("")

    commits = data.get("commits") or []
    lines.append(f"## Commits ({len(commits)})")
    if not commits:
        lines.append("_None in window (or git log empty)._")
    else:
        for c in commits:
            lines.append(f"- `{c['short']}` {c['subject']}")
            tr = c.get("trailers") or {}
            for key in ("Human-Delta", "Agent-Delta", "Rejected-Delta", "Interrupts", "Correction-Prompts"):
                if key in tr:
                    lines.append(f"  - {key}: {tr[key]}")
    lines.append("")

    all_files = data.get("all_committed_files") or []
    lines.append(f"## Files committed ({len(all_files)})")
    if all_files:
        for top, paths in group_paths(all_files).items():
            lines.append(f"- **{top}/** ({len(paths)})")
            for p in paths[:12]:
                lines.append(f"  - `{p}`")
            if len(paths) > 12:
                lines.append(f"  - … +{len(paths) - 12} more")
    else:
        lines.append("_None._")
    lines.append("")

    tracked = data.get("tracked_agent_files") or []
    if tracked:
        lines.append("## Tracked-tree agent attribution (hooks)")
        for path in tracked:
            lines.append(f"- `{path}`")
        lines.append("")

    if data.get("notes"):
        lines.append("## Notes")
        for note in data["notes"]:
            lines.append(f"- {note}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_summary(
    root: Path,
    session_prefix: str | None,
    since: datetime | None,
    until: datetime | None,
    transcript_path: Path | None,
    prompt_chars: int,
    full_prompts: bool,
) -> dict[str, Any]:
    notes: list[str] = []
    sources: list[str] = []

    prompts = filter_prompts(load_all_prompts(root), session_prefix, since, until)
    if prompts:
        sources.append("telemetry/prompts")
    sessions = {r.get("session") or "" for r in prompts if r.get("session")}
    if session_prefix and not sessions:
        sessions.add(session_prefix)

    turn_rows = turns_for_sessions(root, sessions) if sessions else []
    if turn_rows:
        sources.append("telemetry/turns")

    w_start, w_end = window_from_prompts_and_turns(prompts, turn_rows)
    if since:
        w_start = since if w_start is None else min(w_start, since)
    if until:
        w_end = until if w_end is None else max(w_end, until)

    eng = Engine(root)
    tracked_agent: set[str] = set()
    if sessions:
        for files in agent_interval_files(root, eng, sessions).values():
            tracked_agent.update(files)
        if tracked_agent:
            sources.append("edit-intervals")

    user_requests: list[dict[str, str]] = []
    seen_text: set[str] = set()

    def add_request(item: dict[str, str]) -> None:
        key = item["text"][:120]
        if key in seen_text:
            return
        seen_text.add(key)
        user_requests.append(item)

    for r in prompts:
        text = extract_user_text(r.get("prompt") or "")
        if not full_prompts:
            text = truncate(text, prompt_chars)
        add_request(
            {
                "ts": r.get("ts", "")[:19] + "Z" if r.get("ts") else "",
                "prompt_id": r.get("prompt_id") or "",
                "kind": r.get("kind") or "request",
                "text": text,
            }
        )

    if transcript_path and transcript_path.exists():
        sources.append(f"transcript:{transcript_path.name}")
        for i, row in enumerate(load_transcript_user_messages(transcript_path), 1):
            text = row["text"] if full_prompts else truncate(row["text"], prompt_chars)
            add_request(
                {"ts": "", "prompt_id": f"transcript-{i}", "kind": "request", "text": text}
            )

    commits: list[dict[str, Any]] = []
    all_files: list[str] = []
    if w_start and w_end:
        commits = commits_in_window(root, w_start, w_end)
        if commits:
            sources.append("git log")
        for c in commits:
            all_files.extend(c.get("files") or [])

    if not prompts and not turn_rows and not commits and not user_requests:
        notes.append(
            "No telemetry or commits matched. Hooks may be off, telemetry/ is empty, "
            "or pass --transcript auto / a narrower --session prefix."
        )
    elif not prompts and user_requests:
        notes.append("User prompts from transcript only; agent turn list may be incomplete.")
    if turn_rows and not tracked_agent:
        notes.append(
            "Turns recorded but no tracked-tree agent intervals yet — "
            "reference/ and drafts/ edits appear only under Commits."
        )

    title_bits = []
    if session_prefix:
        title_bits.append(f"session `{session_prefix}`")
    if w_start and w_end:
        title_bits.append(f"{w_start.date()} → {w_end.date()}")
    title = "Session summary — " + ", ".join(title_bits) if title_bits else "Session summary"

    for t in turn_rows:
        t["touched"] = [rel_path(root, p) for p in (t.get("touched") or [])]

    return {
        "title": title,
        "window": (
            f"{w_start.strftime('%Y-%m-%dT%H:%MZ')} → {w_end.strftime('%Y-%m-%dT%H:%MZ')}"
            if w_start and w_end
            else None
        ),
        "sessions": sorted(sessions),
        "sources": sources,
        "user_requests": user_requests,
        "agent_turns": turn_rows,
        "commits": commits,
        "all_committed_files": sorted(set(all_files)),
        "tracked_agent_files": sorted(tracked_agent),
        "notes": notes,
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Read-only session recap from hooks + git.")
    p.add_argument("--session", metavar="PREFIX", help="Cursor/Claude session id prefix")
    p.add_argument("--since", metavar="ISO", help="UTC start (e.g. 2026-09-29 or 2026-09-29T08:00:00Z)")
    p.add_argument("--until", metavar="ISO", help="UTC end")
    p.add_argument(
        "--transcript",
        metavar="PATH",
        help="Transcript .jsonl, or 'auto' (default when a session is known)",
    )
    p.add_argument(
        "--no-transcript",
        action="store_true",
        help="Do not merge Cursor agent transcript user messages",
    )
    p.add_argument("--format", choices=("markdown", "json"), default="markdown")
    p.add_argument("--prompt-chars", type=int, default=280, help="Truncate prompts unless --full-prompts")
    p.add_argument("--full-prompts", action="store_true", help="Print full prompt / user_query text")
    p.add_argument(
        "--commit",
        metavar="HASH",
        help="Include this commit even if outside the inferred window (extends window to its time)",
    )
    args = p.parse_args()

    root = repo_root()
    since = parse_iso(args.since) if args.since else None
    until = parse_iso(args.until) if args.until else None

    resolved = resolve_defaults(
        root,
        args.session,
        since,
        until,
        args.transcript,
        args.no_transcript,
    )
    if resolved.label != "explicit args":
        print(f"session_summary: {resolved.label}", file=sys.stderr)

    data = build_summary(
        root,
        resolved.session_prefix,
        resolved.since,
        resolved.until,
        resolved.transcript,
        args.prompt_chars,
        args.full_prompts,
    )
    if resolved.label != "explicit args":
        data.setdefault("notes", []).insert(
            0, f"Defaults: {resolved.label} (override with --session / --since / --no-transcript)."
        )

    if args.commit:
        h = args.commit
        meta = run_git(root, ["log", "-1", "--format=%H%x00%ci%x00%s%x00%b", h], check=False).split("\0")
        if meta and meta[0]:
            full_hash = meta[0]
            files = [
                f.strip()
                for f in run_git(
                    root, ["diff-tree", "--no-commit-id", "--name-only", "-r", full_hash], check=False
                ).splitlines()
                if f.strip()
            ]
            entry = {
                "hash": full_hash,
                "short": full_hash[:9],
                "subject": meta[2] if len(meta) > 2 else "",
                "trailers": parse_commit_trailers(meta[3] if len(meta) > 3 else ""),
                "files": files,
            }
            known = {c["hash"] for c in data["commits"]}
            if full_hash not in known:
                data["commits"].insert(0, entry)
            data["all_committed_files"] = sorted(
                set(data.get("all_committed_files") or []) | set(files)
            )
            if "git log (--commit)" not in data.get("sources", []):
                data.setdefault("sources", []).append("git log (--commit)")

    if args.format == "json":
        print(json.dumps(data, indent=2))
    else:
        print(render_markdown(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
