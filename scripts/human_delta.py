#!/usr/bin/env python3
"""Edit-attribution ledger, commit trailers, weekly/monthly summaries, bar derivation.

Interval kinds and bar weights: see scripts/hooks/edit_attr.py.
Stop (drafts/plans/tsa-on-itself.md §3.12): unattributed share of tracked lines above 20%
in a week or month -> exit 1; fix hook coverage before trusting the bars.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "hooks"))

from edit_attr import (  # noqa: E402
    AGENT_KINDS,
    AUTH_BEGIN_RE,
    HUMAN_KINDS,
    Engine,
    Snap,
    append_jsonl,
    blob_text,
    derive_key,
    diff_lines,
    file_lock,
    format_ts,
    git_dir,
    hook_log,
    load_jsonl,
    numstat,
    parse_authbar_spans,
    parse_ts,
    repo_root,
    run_git,
    set_nth_authbar_key,
    span_index_for_line,
    telemetry_dir,
    tracked_class,
    write_atomic,
)

INTERRUPT_STATUSES = ("interrupted", "user-stopped", "aborted")


def _root() -> Path:
    return repo_root()


def interval_jsonl(root: Path) -> Path:
    return telemetry_dir(root) / "edit-intervals.jsonl"


def span_ledger_path(root: Path) -> Path:
    return root / "drafts/project/self-audit/edit-attribution/span-ledger.json"


def bar_updates_path(root: Path) -> Path:
    return root / "drafts/project/self-audit/edit-attribution/bar-updates.jsonl"


def load_span_ledger(root: Path) -> dict:
    p = span_ledger_path(root)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def save_span_ledger(root: Path, data: dict) -> None:
    write_atomic(span_ledger_path(root), json.dumps(data, indent=2, sort_keys=True) + "\n")


# --- ledger -------------------------------------------------------------------

def append_new_intervals(root: Path, eng: Engine | None = None) -> int:
    """Append rows for pairs after the ledger cursor. Stops at the first pair whose
    active turns are unresolved (a running or not-yet-classified turn), so rows are final."""
    eng = eng or Engine(root)
    path = interval_jsonl(root)
    with file_lock(path):
        rows = load_jsonl(path)
        cursor = max((parse_ts(r["ts_end"]) for r in rows), default=None)
        existing = {(r["ts_start"], r["ts_end"], r["file"], r["kind"]) for r in rows}
        n = 0
        with path.open("a", encoding="utf-8") as f:
            for a, b in eng.pairs:
                if cursor is not None and parse_ts(b.ts) <= cursor:
                    continue
                if not eng.final(a, b):
                    break
                for row in eng.rows_for_pair(a, b):
                    key = (row["ts_start"], row["ts_end"], row["file"], row["kind"])
                    if key in existing:
                        continue
                    f.write(json.dumps(row) + "\n")
                    existing.add(key)
                    n += 1
    return n


def all_interval_rows(root: Path, eng: Engine | None = None) -> list[dict]:
    """Persisted ledger rows plus final pairs not yet appended. Does not write."""
    eng = eng or Engine(root)
    persisted = load_jsonl(interval_jsonl(root))
    cursor = max((parse_ts(r["ts_end"]) for r in persisted), default=None)
    existing = {(r["ts_start"], r["ts_end"], r["file"], r["kind"]) for r in persisted}
    extra: list[dict] = []
    for a, b in eng.pairs:
        if cursor is not None and parse_ts(b.ts) <= cursor:
            continue
        if not eng.final(a, b):
            break
        for row in eng.rows_for_pair(a, b):
            key = (row["ts_start"], row["ts_end"], row["file"], row["kind"])
            if key not in existing:
                extra.append(row)
    return persisted + extra


# --- commit trailers -------------------------------------------------------------

def staged_tracked(root: Path) -> list[str]:
    out = run_git(root, ["diff", "--cached", "--name-only", "--diff-filter=ACMR"], check=False)
    return [p for p in out.splitlines() if tracked_class(p)]


def bucket_of(kind: str) -> str:
    if kind in HUMAN_KINDS:
        return "human"
    if kind in AGENT_KINDS:
        return "agent"
    return kind  # rejected | unattributed


def write_edit_attribution(root: Path, pre: Snap, eng: Engine) -> dict:
    """Sum every interval since HEAD (all turns and gaps, not only the last one)."""
    head = run_git(root, ["rev-parse", "HEAD"], check=False).strip()
    staged = set(staged_tracked(root))
    pairs = [(a, b) for a, b in eng.pairs if b.parent == head and parse_ts(b.ts) <= parse_ts(pre.ts)]
    sums: dict[str, dict] = defaultdict(lambda: {"files": set(), "added": 0, "removed": 0})
    agents: set[str] = set()
    if pairs:
        for a, b in pairs:
            for r in eng.rows_for_pair(a, b):
                if r["file"] not in staged:
                    continue
                s = sums[bucket_of(r["kind"])]
                s["files"].add(r["file"])
                s["added"] += r["added"]
                s["removed"] += r["removed"]
                if r["kind"] in AGENT_KINDS and r["session"]:
                    agents.add(f"{r['tool']}/{r['session'][:8]}")
    else:
        s = sums["human"]
        for added, removed, path in numstat(root, head, pre.sha):
            if path in staged:
                s["files"].add(path)
                s["added"] += added
                s["removed"] += removed
    epoch_starts = {t.start.sha: t for t in eng.turns if t.start.parent == head}
    interrupts = sorted(
        f"{t.tool}/{t.session[:8]}" for t in epoch_starts.values() if t.status in INTERRUPT_STATUSES
    )
    corrections = 0
    for p in sorted((telemetry_dir(root) / "prompts").glob("*.jsonl")):
        for r in load_jsonl(p):
            if r.get("snapshot_ref") in epoch_starts and r.get("kind") == "correction":
                corrections += 1
    payload = {
        k: {"files": len(v["files"]), "added": v["added"], "removed": v["removed"]}
        for k, v in sums.items()
    }
    payload["_meta"] = {
        "since": f"HEAD {head[:9]}",
        "agents": sorted(agents),
        "interrupts": interrupts,
        "correction_prompts": corrections,
    }
    write_atomic(git_dir(root) / "EDIT_ATTRIBUTION", json.dumps(payload, indent=2) + "\n")
    return payload


def trailer_lines(payload: dict) -> str:
    meta = payload.get("_meta", {})
    zero = {"files": 0, "added": 0, "removed": 0}

    def fmt(name: str, key: str, note: str) -> str:
        v = payload.get(key, zero)
        return f"{name}: {v['files']} files, +{v['added']}/-{v['removed']} lines ({note})"

    out = [
        fmt("Human-Delta", "human", f"since {meta.get('since', '')}"),
        fmt("Agent-Delta", "agent", ", ".join(meta.get("agents") or []) or "none"),
    ]
    if payload.get("rejected", zero)["files"]:
        out.append(fmt("Rejected-Delta", "rejected", "agent lines undone by hand"))
    if payload.get("unattributed", zero)["files"]:
        out.append(fmt("Unattributed-Delta", "unattributed", "hook missed"))
    if meta.get("interrupts"):
        out.append(f"Interrupts: {len(meta['interrupts'])} ({', '.join(meta['interrupts'])})")
    if meta.get("correction_prompts"):
        out.append(f"Correction-Prompts: {meta['correction_prompts']}")
    return "\n".join(out) + "\n"


def cmd_precommit() -> int:
    root = _root()
    eng = Engine(root)
    pre = next((s for s in reversed(eng.snaps) if s.label == "precommit"), None)
    if not pre:
        hook_log(root, "precommit: no precommit snapshot")
        return 0
    write_edit_attribution(root, pre, eng)
    append_new_intervals(root, eng)
    cmd_derive_bars(stage=True)
    return 0


def cmd_prepare_msg(msg_file: str) -> int:
    root = _root()
    attr_path = git_dir(root) / "EDIT_ATTRIBUTION"
    if not attr_path.exists() or not msg_file:
        return 0
    payload = json.loads(attr_path.read_text(encoding="utf-8"))
    text = Path(msg_file).read_text(encoding="utf-8")
    if "Human-Delta:" in text:
        return 0
    Path(msg_file).write_text(text.rstrip() + "\n\n" + trailer_lines(payload), encoding="utf-8")
    return 0


def cmd_post_commit() -> int:
    root = _root()
    n = append_new_intervals(root)
    hook_log(root, f"post-commit: appended {n} interval rows")
    return 0


# --- reports ----------------------------------------------------------------------

def tally(rows: list[dict]) -> dict[str, int]:
    t: dict[str, int] = defaultdict(int)
    for r in rows:
        t[bucket_of(r["kind"])] += r["added"] + r["removed"]
        if r["kind"] == "agent-interrupted":
            t["interrupted"] += r["added"] + r["removed"]
    return t


def cmd_month(year_month: str) -> int:
    root = _root()
    append_new_intervals(root)
    prefix = year_month.replace("-", "")
    rows = [r for r in load_jsonl(interval_jsonl(root)) if r["ts_end"].startswith(prefix)]
    agg: dict[tuple, list[int]] = defaultdict(lambda: [0, 0, 0])
    for r in rows:
        key = (r["kind"], r["class"], r.get("chapter") or "")
        agg[key][0] += r["added"]
        agg[key][1] += r["removed"]
        agg[key][2] += 1
    t = tally(rows)
    tracked = sum(v for k, v in t.items() if k != "interrupted")
    share = t["unattributed"] / tracked if tracked else 0.0
    out = root / "drafts/project/self-audit/edit-attribution" / f"{year_month}.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = ["kind,class,chapter,added,removed,intervals"]
    for (kind, cls, ch), (a, r, n) in sorted(agg.items()):
        lines.append(f"{kind},{cls},{ch},{a},{r},{n}")
    lines.append(f"# unattributed_share,{share:.4f},tracked_lines,{tracked}")
    lines.append(f"# rejected_lines,{t['rejected']},interrupted_agent_lines,{t['interrupted']}")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out)
    if share > 0.20:
        print(f"STOP: unattributed share {share:.1%} > 20%", file=sys.stderr)
        return 1
    return 0


def cmd_week() -> int:
    """Print last-seven-day totals from snapshots + persisted ledger. Does not append rows."""
    root = _root()
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    rows = [r for r in all_interval_rows(root) if parse_ts(r["ts_end"]) >= cutoff]
    t = tally(rows)
    total = t["human"] + t["agent"] + t["rejected"] + t["unattributed"]
    share = t["unattributed"] / total if total else 0.0
    print(
        f"week human={t['human']} agent={t['agent']} (interrupted={t['interrupted']}) "
        f"rejected={t['rejected']} unattributed={t['unattributed']} share={share:.1%}"
    )
    if share > 0.20 and total:
        print("STOP: unattributed share above 20%", file=sys.stderr)
        return 1
    return 0


# --- bars -------------------------------------------------------------------------

def apply_row_to_spans(root: Path, r: dict, ledger: dict) -> None:
    rel = r["file"]
    if tracked_class(rel) != "manuscript" or not rel.endswith(".tex"):
        return
    kind = r["kind"]
    bucket = "human" if kind in HUMAN_KINDS else ("agent" if kind in AGENT_KINDS else None)
    if bucket is None:
        return
    text_new = blob_text(root, r["sha_end"], rel)
    if text_new is None:
        return
    text_old = blob_text(root, r["sha_start"], rel)
    spans_new = parse_authbar_spans(text_new)
    spans_old = parse_authbar_spans(text_old) if text_old is not None else []
    skip = {("old", n) for n in r.get("reverted_old") or []} | {("new", n) for n in r.get("reverted_new") or []}
    for line, side, text in diff_lines(root, r["sha_start"], r["sha_end"], rel):
        if (side, line) in skip or not text.strip() or AUTH_BEGIN_RE.search(text):
            continue
        idx = span_index_for_line(spans_new if side == "new" else spans_old, line)
        if idx is None:
            continue
        declared = spans_new[idx][2] if idx < len(spans_new) else "AI"
        e = ledger.setdefault(
            f"{rel}#{idx}",
            {"file": rel, "index": idx, "human": 0, "agent": 0, "prior": declared, "key": declared},
        )
        e[bucket] += 1
        e["dirty"] = True


def rewrite_keys(text: str, entries: list[dict]) -> tuple[str, list[tuple[dict, str, str]]]:
    spans = parse_authbar_spans(text)
    changes = []
    for e in sorted(entries, key=lambda e: e["index"]):
        if e["index"] >= len(spans):
            continue
        old = spans[e["index"]][2]
        new = derive_key(e.get("prior") or old, e["human"], e["agent"])
        if new != old:
            text = set_nth_authbar_key(text, e["index"], new)
            changes.append((e, old, new))
    return text, changes


def stage_key_change(root: Path, rel: str, entries: list[dict]) -> None:
    """Change keys in the index copy only, so unstaged hunks stay unstaged."""
    idx_text = blob_text(root, "", rel)  # ":rel" = index version
    if idx_text is None:
        return
    new_idx, changes = rewrite_keys(idx_text, entries)
    if not changes:
        return
    sha = run_git(root, ["hash-object", "-w", "--stdin"], input=new_idx).strip()
    mode = run_git(root, ["ls-files", "-s", "--", rel]).split()[0]
    run_git(root, ["update-index", "--cacheinfo", f"{mode},{sha},{rel}"])


def cmd_derive_bars(stage: bool = False) -> int:
    """Recompute keys for spans with new tracked lines. With stage=True (pre-commit),
    only files in the commit are rewritten; other spans stay dirty until committed."""
    root = _root()
    append_new_intervals(root)
    ledger = load_span_ledger(root)
    as_of = ledger.pop("_as_of", "") or ""
    max_ts = as_of
    for r in load_jsonl(interval_jsonl(root)):
        if as_of and parse_ts(r["ts_end"]) <= parse_ts(as_of):
            continue
        apply_row_to_spans(root, r, ledger)
        if not max_ts or parse_ts(r["ts_end"]) > parse_ts(max_ts):
            max_ts = r["ts_end"]
    if max_ts:
        ledger["_as_of"] = max_ts

    staged = set(staged_tracked(root)) if stage else None
    by_file: dict[str, list[dict]] = defaultdict(list)
    for sid, e in ledger.items():
        if not sid.startswith("_") and e.get("dirty"):
            by_file[e["file"]].append(e)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for rel, entries in by_file.items():
        if staged is not None and rel not in staged:
            continue
        path = root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        new_text, changes = rewrite_keys(text, entries)
        for e, old, new in changes:
            e["key"] = new
            append_jsonl(bar_updates_path(root), {
                "ts": now, "file": rel, "span": f"{rel}#{e['index']}", "from": old, "to": new,
                "human_lines": e["human"], "agent_lines": e["agent"],
            })
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            if stage:
                stage_key_change(root, rel, entries)
        for e in entries:
            e.pop("dirty", None)

    save_span_ledger(root, ledger)
    if stage:
        own = [span_ledger_path(root), bar_updates_path(root)]
        subprocess.run(["git", "add", "--"] + [str(p.relative_to(root)) for p in own if p.exists()],
                       cwd=root, check=False)
    return 0


def cmd_prune() -> int:
    root = _root()
    rows = load_jsonl(interval_jsonl(root))
    if not rows:
        print("no ledger; refusing to prune")
        return 0
    cursor = max(parse_ts(r["ts_end"]) for r in rows)
    cutoff = datetime.now(timezone.utc) - timedelta(days=90)
    n = 0
    for s in Engine(root).snaps:
        ts = parse_ts(s.ts)
        if ts > cutoff or ts > cursor:
            continue
        run_git(root, ["update-ref", "-d", s.ref], check=False)
        n += 1
    print(f"pruned {n} snapshot refs")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--month", metavar="YYYY-MM")
    p.add_argument("--week", action="store_true")
    p.add_argument("--derive-bars", action="store_true")
    p.add_argument("cmd", nargs="?", choices=["precommit", "prepare-msg", "post-commit", "prune-snapshots"])
    p.add_argument("msg_file", nargs="?")
    args = p.parse_args()
    try:
        if args.month:
            return cmd_month(args.month)
        if args.week:
            return cmd_week()
        if args.derive_bars:
            return cmd_derive_bars(stage=False)
        if args.cmd == "precommit":
            return cmd_precommit()
        if args.cmd == "prepare-msg":
            return cmd_prepare_msg(args.msg_file or "")
        if args.cmd == "post-commit":
            return cmd_post_commit()
        if args.cmd == "prune-snapshots":
            return cmd_prune()
        p.print_help()
        return 2
    except Exception as e:
        try:
            hook_log(_root(), f"human_delta error: {type(e).__name__}: {e}")
        except Exception:
            pass
        print(f"human_delta: {e}", file=sys.stderr)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
