"""Compatibility shim → :mod:`uad_discovery` (GL-51).

The pre-GL-51 Jaccard / communicate-edge heuristic was moved to
``attic/coordination_heuristic.py``. This module re-exports the proper
passive UAD entry points under the historical names so calibration and
older imports keep working.
"""

from __future__ import annotations

from .uad_discovery import (
    cmi_edge_matrix,
    discovered_units_passive,
    discovered_units_uad,
)

__all__ = [
    "cmi_edge_matrix",
    "discovered_units_passive",
    "discovered_units_uad",
]
