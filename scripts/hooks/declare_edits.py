#!/usr/bin/env python3
"""Declare which tracked files an unmeasurable shell edit will change.

Use before a Claude Code background command, or any Cursor shell command, that writes under
chapters/, appendices/, frontmatter/, or site/src/. Foreground Claude Code commands are
measured by the hooks and need no declaration.

  python3 scripts/hooks/declare_edits.py 'chapters/ch1*.tex' 're:^site/src/content/cards/'

Patterns are globs on repo-relative paths, or regexes with a 're:' prefix. A declaration only
credits files that actually changed during the turn and match; everything else keeps its
measured label. Over-declaring moves nothing to the agent that did not change; under-declaring
leaves the edit as unmeasured shell work, never as human work.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from edit_attr import append_jsonl, declarations_path, now_stamp, repo_root  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("patterns", nargs="+")
    p.add_argument("--tool", choices=["claude", "cursor", "manual"])
    p.add_argument("--session", default=None)
    args = p.parse_args()
    claude_session = os.environ.get("CLAUDE_CODE_SESSION_ID", "")
    tool = args.tool or ("claude" if claude_session else "cursor")
    session = args.session if args.session is not None else (claude_session if tool == "claude" else "")
    append_jsonl(declarations_path(repo_root()), {
        "ts": now_stamp(), "tool": tool, "session": session, "patterns": args.patterns,
    })
    print(f"declared {len(args.patterns)} pattern(s) for {tool}/{session[:8] or '*'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
