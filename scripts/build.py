#!/usr/bin/env python3
"""Build wrapper — delegates to build.sh."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    return subprocess.call([str(ROOT / "build.sh")])


if __name__ == "__main__":
    raise SystemExit(main())
