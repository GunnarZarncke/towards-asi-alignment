#!/usr/bin/env python3
"""Run ET-3 foster extension smoke tests in the pinned AI 2027 checkout."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

DEFAULT_CHECKOUT = Path("/Users/GunnarZarncke/repos/timelines-takeoff-ai-2027")
FORK_BRANCH = "gunnar/et3-annex"


def main() -> None:
    checkout = Path(os.environ.get("AI2027_CHECKOUT", DEFAULT_CHECKOUT))
    py = checkout / ".venv" / "bin" / "python"
    if not py.is_file():
        print(f"[et3/foster] missing venv python at {py}", file=sys.stderr)
        raise SystemExit(1)
    proc = subprocess.run(
        [str(py), "takeoff/test_foster_smoke.py"],
        cwd=checkout,
        check=False,
    )
    raise SystemExit(proc.returncode)


if __name__ == "__main__":
    main()
