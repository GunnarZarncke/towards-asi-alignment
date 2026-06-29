"""LLM red-team harness for multiresolution alignment simulation (scaffold)."""

from .harness import run_redteam_suite
from .protocol import RedTeamProtocol
from .strategies import STRATEGIES, AuditPatchStrategy

__all__ = [
    "AuditPatchStrategy",
    "RedTeamProtocol",
    "STRATEGIES",
    "run_redteam_suite",
]
