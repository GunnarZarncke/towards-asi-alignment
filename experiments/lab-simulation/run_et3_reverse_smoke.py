#!/usr/bin/env python3
"""ET-3 Phase 2: oversight_drag reverse-extension smoke (n_sims=100).

Runs ``external/ai2027/scripts/oversight_drag_smoke.py`` (mechanical fixed samples
mirroring the patched takeoff calendar-drag rule). Full upstream Monte Carlo requires
``external/ai2027/.venv`` with numpy/pandas/scipy.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "external" / "ai2027" / "scripts" / "oversight_drag_smoke.py"


def main() -> None:
    proc = subprocess.run([sys.executable, str(SCRIPT)], check=False)
    raise SystemExit(proc.returncode)


if __name__ == "__main__":
    main()
