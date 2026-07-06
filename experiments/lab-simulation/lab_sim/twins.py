"""Full-surface honest twin (Phase 5, FREEZE POINT).

Swaps EVERY agent's program from ``goal_policy`` to ``honest_twin``
(``programs.py``), which always picks the honest baseline playbook and
ignores goal weights and board capture. Because playbook choice IS the
entire behavioral surface in this line (actions, report content, and
review/sign-off decisions all route through it), one program swap covers
"actions, reports, query responses, access requests all at once" — the
plan's full-surface twin requirement — without a separate per-channel
transform. Query responses and escalation channels do not exist yet
(Phase 7); when they land, they join the SAME playbook-driven surface
rather than needing a new twin mechanism.
"""

from __future__ import annotations

from .config import LabConfig
from .world import EpisodeResult, run_episode


def run_honest_twin(cfg: LabConfig, seed: int, backend=None) -> EpisodeResult:
    return run_episode(cfg, seed, backend=backend, program_override="honest_twin")
