#!/usr/bin/env python3
"""Invoke C2 stack harness; write c2-tool-scout-v2 fixture."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "fixtures" / "c2-tool-scout-v2.json"
HARNESS = Path.home() / "repos/ciris/review/harness/c2_tool_scout_harness.py"
VENV_PY = Path.home() / "repos/ciris/review/harness/.venv/bin/python"
PROTOCOL = "c2-v2.0.0"


def main() -> int:
    print("[1/2] harness", HARNESS)
    if not HARNESS.is_file():
        OUT.write_text(
            json.dumps(
                {
                    "protocol_version": PROTOCOL,
                    "status": "refuse",
                    "reason": f"harness missing: {HARNESS}",
                    "host": "H1",
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print("OUTCOME refuse missing harness")
        return 0
    py = str(VENV_PY) if VENV_PY.is_file() else sys.executable
    cmd = [
        py,
        str(HARNESS),
        "--url",
        "http://127.0.0.1:8080",
        "--emit",
        str(OUT),
    ]
    print("[2/2]", " ".join(cmd))
    proc = subprocess.run(cmd, text=True)
    print(proc.stdout or "", end="")
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    if OUT.is_file():
        data = json.loads(OUT.read_text(encoding="utf-8"))
        print("fixture status", data.get("status"))
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
