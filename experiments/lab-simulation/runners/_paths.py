"""Shared paths for lab-simulation runner scripts under ``runners/``."""

from __future__ import annotations

from pathlib import Path

LAB_SIM_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = LAB_SIM_ROOT / "results"
EXTERNAL_DIR = LAB_SIM_ROOT / "external"
REPO_ROOT = LAB_SIM_ROOT.parents[1]
