"""UAD mode: full (agency-detect MI) vs fake (heuristic-only)."""

from __future__ import annotations

import os
from typing import Literal

UADMode = Literal["full", "fake"]

_mode: UADMode = "full"


def get_uad_mode() -> UADMode:
    return _mode


def set_uad_mode(mode: UADMode) -> None:
    global _mode
    if mode not in ("full", "fake"):
        raise ValueError(f"unknown UAD mode: {mode!r}")
    _mode = mode


def init_uad_mode_from_env() -> UADMode:
    raw = os.environ.get("EMBEDDED_UAD_MODE", "full").strip().lower()
    if raw in ("fake", "heuristic", "heuristic_only"):
        set_uad_mode("fake")
    else:
        set_uad_mode("full")
    return get_uad_mode()


def uad_artifact_suffix(mode: UADMode | None = None) -> str:
    """Filename suffix for non-default UAD mode artifacts."""
    mode = mode or get_uad_mode()
    return "" if mode == "full" else "_fake_uad"
