"""Vendored port of `embedded-simulation/embedded_sim/uad_core/` (PLAN.md
S5, recorded 2026-07-07): the lag-max mutual-information agent-clustering
detector PLAN.md's original ambition named as this line's UAD precedent
("embedded_sim's UAD precedent," see `lab_sim/oracle_only/uad.py`'s own
module docstring), never previously applied to lab-sim's actors.

Vendored, not cross-imported, on purpose -- each experiment line in this
repo is a self-contained codebase (AGENTS.md "Experiments"); importing
`embedded_sim` directly from `lab_sim` would create an inter-line
dependency this repo's four lines otherwise never have. `info.py` is
copied from `embedded_sim/audit_core/info.py` (only the two functions
`detection.py`/`markov_blanket.py` actually use); `config.py`,
`detection.py`, and `markov_blanket.py` are copied byte-for-byte from
`embedded_sim/uad_core/` except for the one import line each needs to
point at this package's local `info.py` instead of `..audit_core.info`.
No lab-sim-specific logic lives here -- that adapter is
`lab_sim/oracle_only/uad_mi.py`, one level up, which is the only new
code this port required.
"""

from __future__ import annotations

from .config import DetectionConfig
from .detection import AgentDetector, detect_agents

__all__ = ["AgentDetector", "DetectionConfig", "detect_agents"]
