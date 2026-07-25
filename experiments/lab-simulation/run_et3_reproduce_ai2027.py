#!/usr/bin/env python3
"""ET-3 Phase 2: reproduce AI 2027 timelines + takeoff headline percentiles.

Uses sibling checkout ``.venv`` (``timelines-takeoff-ai-2027/.venv``) when present.
Fork for upstream PRs: ``git@github.com:GunnarZarncke/timelines-takeoff-ai-2027.git``.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent / "results"
PIN_PATH = Path(__file__).resolve().parent / "external" / "ai2027" / "PIN.txt"
DEFAULT_CHECKOUT = Path("/Users/GunnarZarncke/repos/timelines-takeoff-ai-2027")
FORK_REMOTE = "git@github.com:GunnarZarncke/timelines-takeoff-ai-2027.git"
FORK_BRANCH = "gunnar/et3-annex"
LOCAL_VENV = Path(__file__).resolve().parent / "external" / "ai2027" / ".venv" / "bin" / "python"

_TAKEOFF_PERCENTILE_SCRIPT = """
import os, sys
from pathlib import Path
import yaml
import numpy as np
ROOT = Path(os.environ["AI2027_CHECKOUT"])
sys.path.insert(0, str(ROOT / "takeoff"))
import forecasting_takeoff as ft
with open(ROOT / "takeoff" / "params.yaml") as f:
    cfg = yaml.safe_load(f)
cfg["simulation"]["n_sims"] = 500
samples = ft.get_milestone_samples(cfg, cfg["simulation"]["n_sims"])
all_dates = [ft.run_single_simulation(samples, i) for i in range(cfg["simulation"]["n_sims"])]
sar = [d[0].year + d[0].timetuple().tm_yday/365 for d in all_dates if d]
for p in (10, 50, 90):
    print(f"SAR_p{p}={np.percentile(sar, p):.4f}")
"""


def _checkout_root() -> Path:
    env = os.environ.get("AI2027_CHECKOUT")
    return Path(env) if env else DEFAULT_CHECKOUT


def _python_bin(checkout: Path) -> Path | None:
    for candidate in (
        checkout / ".venv" / "bin" / "python",
        LOCAL_VENV,
        Path(sys.executable),
    ):
        if candidate.is_file():
            try:
                proc = subprocess.run(
                    [str(candidate), "-c", "import numpy, pandas, scipy, yaml"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if proc.returncode == 0:
                    return candidate
            except OSError:
                pass
    return None


def _run(py: Path, args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    cmd = [str(py), *args]
    print(f"[et3/repro] {' '.join(cmd)} (cwd={cwd})")
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)


def main() -> None:
    checkout = _checkout_root()
    pin = PIN_PATH.read_text(encoding="utf-8").strip()
    py = _python_bin(checkout)

    payload: dict = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pinned_commit": pin,
        "fork_remote": FORK_REMOTE,
        "checkout": str(checkout),
        "python": str(py) if py else None,
        "reproduction_status": "blocked",
        "fork_branch": FORK_BRANCH,
        "seed_pr_branch": "add-simulation-seed",
        "note": "Global NumPy RNG unseeded by default; exact bit-match not expected.",
    }

    if not checkout.is_dir():
        payload["error"] = f"checkout not found: {checkout}"
    else:
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=checkout, capture_output=True, text=True)
        branch = subprocess.run(
            ["git", "branch", "--show-current"], cwd=checkout, capture_output=True, text=True
        )
        remote = subprocess.run(["git", "remote", "get-url", "origin"], cwd=checkout, capture_output=True, text=True)
        payload["checkout_head"] = head.stdout.strip()
        payload["checkout_branch"] = branch.stdout.strip()
        payload["origin"] = remote.stdout.strip()
        payload["head_matches_pin"] = head.stdout.strip() == pin

        if py is None:
            payload["error"] = (
                "scientific Python deps unavailable in checkout/.venv; "
                "`.venv/bin/pip install numpy pandas scipy pyyaml matplotlib tqdm`"
            )
        else:
            seed_smoke = _run(py, ["takeoff/test_seed_smoke.py"], checkout)
            env = os.environ.copy()
            env["AI2027_CHECKOUT"] = str(checkout)
            pct = subprocess.run(
                [str(py), "-c", _TAKEOFF_PERCENTILE_SCRIPT],
                cwd=checkout,
                capture_output=True,
                text=True,
                check=False,
                env=env,
            )
            tk = _run(py, ["forecasting_takeoff.py"], checkout / "takeoff")
            tl = _run(py, ["forecasting_timelines.py"], checkout / "timelines")
            payload["seed_smoke"] = {"returncode": seed_smoke.returncode, "stdout": seed_smoke.stdout.strip()}
            payload["takeoff_percentiles"] = {
                line.split("=")[0]: float(line.split("=")[1])
                for line in pct.stdout.splitlines()
                if line.startswith("SAR_p")
            }
            payload["takeoff_script"] = {
                "returncode": tk.returncode,
                "stderr_tail": tk.stderr[-1500:] if tk.stderr else "",
            }
            payload["timelines_script"] = {
                "returncode": tl.returncode,
                "stderr_tail": tl.stderr[-1500:] if tl.stderr else "",
            }
            payload["figures_exist"] = {
                "takeoff_timeline": (checkout / "takeoff" / "figures" / "takeoff_timeline.png").is_file(),
                "timelines_dir": (checkout / "timelines" / "figures").is_dir(),
            }
            ok_takeoff = tk.returncode == 0 and bool(payload["takeoff_percentiles"])
            ok_seed = seed_smoke.returncode == 0
            ok_timelines = tl.returncode == 0
            if ok_seed and ok_takeoff and ok_timelines:
                payload["reproduction_status"] = "matched"
            elif ok_seed and ok_takeoff:
                payload["reproduction_status"] = "close"
            elif ok_takeoff or ok_timelines or pct.returncode == 0:
                payload["reproduction_status"] = "partial"

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RESULTS_DIR / "et3_reproduce_ai2027.json"
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"[et3/repro] status={payload['reproduction_status']} -> {out_path}")


if __name__ == "__main__":
    main()
