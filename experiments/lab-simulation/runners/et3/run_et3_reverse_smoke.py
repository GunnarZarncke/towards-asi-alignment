#!/usr/bin/env python3
"""ET-3 Phase 2: oversight_drag reverse-extension smoke (n_sims=100).

Runs ``external/ai2027/scripts/oversight_drag_smoke.py`` (mechanical fixed samples
mirroring the patched takeoff calendar-drag rule). Full upstream Monte Carlo requires
``external/ai2027/.venv`` with numpy/pandas/scipy.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from runners._paths import EXTERNAL_DIR, LAB_SIM_ROOT, REPO_ROOT, RESULTS_DIR

import subprocess

SCRIPT = EXTERNAL_DIR / "ai2027" / "scripts" / "oversight_drag_smoke.py"


def main() -> None:
    proc = subprocess.run([sys.executable, str(SCRIPT)], check=False)
    raise SystemExit(proc.returncode)


if __name__ == "__main__":
    main()
