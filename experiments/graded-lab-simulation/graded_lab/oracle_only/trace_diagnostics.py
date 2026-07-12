"""Phase-4 trace and counterfactual diagnostics.

These role-level outputs test retained boundary streams and matched controls.
They are deliberately not ecology-BIQ: they do not recover units with UAD,
estimate MI/CMI, measure retained-state entropy, or estimate held-out
surprise.  The former ``ecology_biq`` module remains a temporary compatibility
shim for old callers only.
"""

from .ecology_biq import (
    compute_biq_ctrl,
    compute_biq_mem,
    compute_biq_pred,
    compute_biq_surp,
    compute_role_boundary_proxy,
)

__all__ = (
    "compute_biq_ctrl",
    "compute_biq_mem",
    "compute_biq_pred",
    "compute_biq_surp",
    "compute_role_boundary_proxy",
)
