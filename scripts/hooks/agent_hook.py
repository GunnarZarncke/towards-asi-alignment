#!/usr/bin/env python3
"""Normalise Claude Code / Cursor hook JSON; snapshot, record turns and prompts. Always exit 0.

Turn lifecycle (one row per close in telemetry/turns.jsonl; later rows for the same start win):
  start       prompt submitted -> agent-start snapshot
  completed   Stop / Cursor stop -> agent-end snapshot, always (even with no change)
  user-stopped  Claude tool call interrupted by the user (PostToolUseFailure is_interrupt)
  aborted     Cursor stop with status "aborted"
  api-error   Claude StopFailure / Cursor stop "error"
  interrupted a new prompt arrived with the previous Claude turn still open: Claude Code
              runs no hook when the user interrupts text generation, so the end is unknown
  lost        a new prompt arrived with the previous Cursor turn still open (missed hook)

Shell edits (Claude Code): PreToolUse/PostToolUse on Bash stat the tracked trees before and
after each foreground command; changed files join the turn's edit list. Only a command that
could not be measured (background, missing pre-map) marks the turn "bash" (file list
incomplete). Edits no hook can measure are declared by the agent with
scripts/hooks/declare_edits.py; declarations inside the turn are attached when it closes.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "hooks"))

from edit_attr import (  # noqa: E402
    append_jsonl,
    changed_paths,
    classify_prompt,
    declarations_path,
    load_jsonl,
    now_stamp,
    parse_ts,
    stat_map,
    hook_log,
    locked_state,
    repo_root,
    session_state_path,
    telemetry_dir,
    tree_of,
    turns_path,
)

CURSOR_PAYLOAD_KEYS = ("cursor_version", "conversation_id", "generation_id", "workspace_roots")


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def snapshot(root: Path, label: str, tool: str, session: str, generation: str = "") -> str:
    script = root / "scripts" / "hooks" / "snapshot.sh"
    r = subprocess.run(
        ["bash", str(script), label, tool, session, generation],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        hook_log(root, f"snapshot {label} {tool} {session[:8]} failed: {r.stderr.strip()}")
        return ""
    return r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""


def record_prompt(root: Path, tool: str, session: str, prompt_id: str, prompt: str,
                  snapshot_ref: str, after_interrupt: bool) -> None:
    kind, rule = classify_prompt(prompt, after_interrupt)
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    append_jsonl(
        telemetry_dir(root) / "prompts" / f"{day}.jsonl",
        {
            "ts": utc_now(),
            "tool": tool,
            "session": session,
            "prompt_id": prompt_id,
            "prompt": prompt,
            "attachments": [],
            "snapshot_ref": snapshot_ref,
            "kind": kind,
            "correction_rule": rule,
            "after_interrupt": after_interrupt,
        },
    )


def rel_file(root: Path, raw: str | None) -> str | None:
    if not raw:
        return None
    p = Path(raw)
    try:
        return str(p.resolve().relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(p).replace("\\", "/")


def is_open(st: dict) -> bool:
    return bool(st.get("start_sha")) and not st.get("ended")


def turn_declarations(root: Path, tool: str, session: str, st: dict) -> list[str]:
    started = st.get("started")
    if not started:
        return []
    t0 = parse_ts(started)
    out: list[str] = []
    for r in load_jsonl(declarations_path(root)):
        if r.get("tool") != tool or r.get("session") not in ("", session):
            continue
        if parse_ts(r["ts"]) < t0:
            continue
        for pat in r.get("patterns") or []:
            if pat not in out:
                out.append(pat)
    return out


def close_turn(root: Path, tool: str, session: str, st: dict, status: str, end_sha: str | None) -> None:
    start = st.get("start_sha") or ""
    changed = None
    if start and end_sha:
        changed = tree_of(root, start) != tree_of(root, end_sha)
    append_jsonl(
        turns_path(root),
        {
            "ts": utc_now(),
            "tool": tool,
            "session": session,
            "prompt_id": st.get("prompt_id") or "",
            "start_sha": start,
            "end_sha": end_sha,
            "status": status,
            "touched": st.get("touched") or [],
            "bash": bool(st.get("bash")),
            "tree_changed": changed,
            "failures": st.get("failures") or [],
            "declared": turn_declarations(root, tool, session, st),
        },
    )
    st["ended"] = True


def start_turn(root: Path, tool: str, session: str, prompt_id: str, prompt: str,
               stale_status: str) -> None:
    with locked_state(root, tool, session) as st:
        after_interrupt = False
        if is_open(st):
            close_turn(root, tool, session, st, stale_status, None)
            after_interrupt = stale_status == "interrupted"
        sha = snapshot(root, "agent-start", tool, session, prompt_id)
        st.clear()
        st.update(start_sha=sha, prompt_id=prompt_id, touched=[], bash=False, ended=False, failures=[],
                  started=now_stamp())
    record_prompt(root, tool, session, prompt_id, prompt, sha, after_interrupt)


def end_turn(root: Path, tool: str, session: str, status: str, only_if_open: bool = False) -> None:
    with locked_state(root, tool, session) as st:
        if not st.get("start_sha") or (only_if_open and not is_open(st)):
            return
        if st.get("ended"):
            hook_log(root, f"{tool} {session[:8]}: end event after close ({status}); re-closing")
        sha = snapshot(root, "agent-end", tool, session, st.get("prompt_id") or "")
        close_turn(root, tool, session, st, status, sha or None)


def add_touched(root: Path, tool: str, session: str, rel: str | None, bash: bool) -> None:
    with locked_state(root, tool, session) as st:
        if bash:
            st["bash"] = True
        if rel:
            touched = list(st.get("touched") or [])
            if rel not in touched:
                touched.append(rel)
            st["touched"] = touched


def pre_map_path(root: Path, session: str, tool_use_id: str) -> Path:
    safe = "".join(c if c.isalnum() or c in "._-" else "-" for c in f"{session}-{tool_use_id}")[:120]
    return telemetry_dir(root) / "state" / f"pre-{safe}.json"


def measure_before(root: Path, session: str, data: dict) -> None:
    inp = data.get("tool_input") or {}
    if data.get("tool_name") != "Bash" or inp.get("run_in_background") or not data.get("tool_use_id"):
        return
    pre_map_path(root, session, data["tool_use_id"]).write_text(json.dumps(stat_map(root)), encoding="utf-8")


def measure_after(root: Path, session: str, data: dict) -> None:
    """Add the files a shell command changed; fall back to 'bash' when it could not be measured."""
    inp = data.get("tool_input") or {}
    p = pre_map_path(root, session, str(data.get("tool_use_id") or ""))
    if inp.get("run_in_background") or not data.get("tool_use_id") or not p.exists():
        add_touched(root, "claude", session, None, True)
        return
    before = json.loads(p.read_text(encoding="utf-8"))
    p.unlink(missing_ok=True)
    changed = changed_paths(before, stat_map(root))
    with locked_state(root, "claude", session) as st:
        touched = list(st.get("touched") or [])
        touched.extend(c for c in changed if c not in touched)
        st["touched"] = touched


def under_cursor(data: dict, session: str) -> bool:
    """Cursor also runs .claude/settings.json hooks; its own adapter already covers the turn."""
    if any(k in data for k in CURSOR_PAYLOAD_KEYS):
        return True
    if os.environ.get("CLAUDECODE"):
        return False
    return session_state_path(repo_root(), "cursor", session).exists()


def handle_claude(root: Path, event: str, data: dict) -> None:
    session = str(data.get("session_id") or "unknown")
    if under_cursor(data, session):
        if event == "UserPromptSubmit":
            hook_log(root, f"claude hook skipped: Cursor session {session[:8]} (keys: {sorted(data)[:12]})")
        return
    if event == "UserPromptSubmit":
        prompt = data.get("prompt") or data.get("user_prompt") or ""
        start_turn(root, "claude", session, str(data.get("prompt_id") or ""), prompt, "interrupted")
    elif event == "PreToolUse":
        measure_before(root, session, data)
    elif event == "PostToolUse":
        if data.get("tool_name") == "Bash":
            measure_after(root, session, data)
        else:
            inp = data.get("tool_input") or {}
            path = inp.get("file_path") or inp.get("notebook_path") or inp.get("path")
            add_touched(root, "claude", session, rel_file(root, path), False)
    elif event == "PostToolUseFailure":
        if data.get("tool_name") == "Bash":
            measure_after(root, session, data)  # a failing command may still have written files
        inp = data.get("tool_input") or {}
        with locked_state(root, "claude", session) as st:
            fails = list(st.get("failures") or [])
            fails.append({
                "tool_name": data.get("tool_name"),
                "error_type": data.get("error_type"),
                "is_interrupt": bool(data.get("is_interrupt")),
                "file": rel_file(root, inp.get("file_path") or inp.get("notebook_path")),
            })
            st["failures"] = fails[-50:]
        if data.get("is_interrupt"):
            end_turn(root, "claude", session, "user-stopped", only_if_open=True)
    elif event == "Stop":
        if not data.get("stop_hook_active"):
            end_turn(root, "claude", session, "completed")
    elif event == "StopFailure":
        end_turn(root, "claude", session, "api-error")
    elif event == "SessionEnd":
        # An open turn here was interrupted during text generation; its exact end is unknown.
        end_turn(root, "claude", session, "interrupted", only_if_open=True)


def handle_cursor(root: Path, event: str, data: dict) -> None:
    session = str(data.get("conversation_id") or "unknown")
    gen = str(data.get("generation_id") or "")
    if event == "beforeSubmitPrompt":
        start_turn(root, "cursor", session, gen, data.get("prompt") or "", "lost")
        print(json.dumps({"continue": True}))
    elif event == "afterFileEdit":
        add_touched(root, "cursor", session, rel_file(root, data.get("file_path")), False)
    elif event == "stop":
        status = {"aborted": "aborted", "error": "api-error"}.get(str(data.get("status")), "completed")
        end_turn(root, "cursor", session, status)


def main() -> int:
    tool = "claude"
    event = ""
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--tool" and i + 1 < len(args):
            tool = args[i + 1]
            i += 2
            continue
        if args[i] == "--event" and i + 1 < len(args):
            event = args[i + 1]
            i += 2
            continue
        i += 1
    printed = False
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
        root = repo_root()
        if tool == "claude":
            handle_claude(root, event, data)
        elif tool == "cursor":
            handle_cursor(root, event, data)
            printed = event == "beforeSubmitPrompt"
        else:
            hook_log(root, f"unknown tool {tool}")
    except Exception as e:
        try:
            hook_log(repo_root(), f"agent_hook {tool} {event}: {type(e).__name__}: {e}")
        except Exception:
            pass
    if tool == "cursor" and event == "beforeSubmitPrompt" and not printed:
        print(json.dumps({"continue": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
