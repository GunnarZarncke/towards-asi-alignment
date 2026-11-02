#!/usr/bin/env python3
"""One-shot sandbox probe (orchestrator use)."""

from __future__ import annotations

import asyncio
import json
import sys

from sandboxed_agent_mcp.auth_info import auth_summary
from sandboxed_agent_mcp.sandbox import run_sandboxed

PROMPT = """\
Answer in plain text with four numbered sections:

1. Model — what model are you (name/id) and any version or build info you can state.
2. Time — current date and time to the best of your knowledge.
3. File-tool scope — what you believe Read, Glob, and Grep can reach (cwd, path rules).
4. Evidence — use Glob and/or Read on paths under your current working directory only; list what you actually see. If a path is denied, say so.

Do not run shell commands. If something is unknown, say unknown.
"""


async def main() -> int:
    root = sys.argv[1] if len(sys.argv) > 1 else None
    if not root:
        print("usage: run_probe.py ABS_ROOT", file=sys.stderr)
        return 2

    model = sys.argv[2] if len(sys.argv) > 2 else "claude-haiku-4-5-20251001"

    print("auth:", json.dumps(auth_summary()), flush=True)
    print("root:", root, "model:", model, "system_prompt: (empty)", flush=True)

    try:
        text = await run_sandboxed(
            prompt=PROMPT,
            root=root,
            system_prompt="",
            allow_write=False,
            max_turns=15,
            model=model,
        )
    except Exception as exc:
        print("ERROR:", exc, file=sys.stderr)
        return 1

    print("\n--- sub-agent result ---\n")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
