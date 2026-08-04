"""Compatibility shim → :mod:`uad_handles` (GL-51).

The pre-GL-51 mutual freeze-AND merge path was moved to
``attic/freeze_and_merge.py``. This module re-exports access-UAD entry
points under the historical names.
"""

from __future__ import annotations

from .uad_handles import (
    DEFAULT_MIN_DEPENDENCY,
    DEFAULT_SPECIFICITY_RATIO,
    dependency_matrix,
    discovered_units_handles,
    discovered_units_intervention,
    units_from_handle_matrix,
)

# Historical constant name.
DEFAULT_MIN_COMPENSATION = DEFAULT_MIN_DEPENDENCY

__all__ = [
    "DEFAULT_MIN_COMPENSATION",
    "DEFAULT_MIN_DEPENDENCY",
    "DEFAULT_SPECIFICITY_RATIO",
    "dependency_matrix",
    "discovered_units_handles",
    "discovered_units_intervention",
    "units_from_handle_matrix",
]
