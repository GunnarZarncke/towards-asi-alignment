"""Goal-agent simulation — Milestone v5 Phase 1 (new line, separate from embedded-simulation).

Why a new line
--------------
The `embedded-simulation` line scripts every behavior through `SimConfig`
scenario knobs; even 20 scenarios are 20 fixed mechanisms, so held-out *seeds*
test robustness to noise, not to an unseen mechanism. This line replaces
"scenario config -> scripted behavior" with "goal weights x tool access ->
emergent behavior": an agent picks actions each tick by softmax over a
utility that weighs task progress, compliance, bearer welfare, and audit
exposure. Deception, shadow routing, and unapproved practice changes are
*chosen*, not scripted, so a held-out region of goal/tool space is a
qualitatively different generalization test than a held-out scenario name.

The old line is kept unchanged for comparability with prior recorded results.

Three planes (inherited discipline)
-----------------------------------
- **World/oracle** (`world.py`): full ground truth per step, including the
  agent's true action, true uptake, shadow routing, and welfare deltas.
- **Audit view** (`channels.py`): a projection of oracle rows into
  audit-visible channels, gated by instrumentation tier. `true_*` fields
  never cross this boundary.
- **Referee** (`labels.py` + `protocol.py`): mechanism-derived episode labels
  computed from oracle ground truth with thresholds fixed *before* any run
  (see `labels.py` docstring), compared post-hoc against audit verdicts.

Module map
----------
- `config.py`    — GoalWeights / ToolAccess / WorldConfig dataclasses.
- `agents.py`    — GoalPolicy (softmax utility agent) + BoardPolicy
                   (correction issuance, escalation, sign-off).
- `world.py`     — the step loop; emits oracle rows.
- `labels.py`    — pre-registered mechanism-derived episode labels.
- `channels.py`  — audit projection + instrumentation tiers.
- `detectors.py` — audit-side structural detectors (fixed thresholds).
- `info.py`      — stdlib MI estimator + quantile binning (ported pattern).
- `protocol.py`  — goal/tool-space sampling, discovery/held-out region split,
                   battery runner, mini MI scan.

Run
---
    cd experiments/goal-agent-simulation
    python3 run_phase1.py          # full acceptance protocol -> results/
    python3 -m pytest tests/ -q
"""

from .config import AgentConfig, BoardConfig, GoalWeights, ToolAccess, WorldConfig
from .labels import label_episode
from .world import run_episode

__all__ = [
    "AgentConfig",
    "BoardConfig",
    "GoalWeights",
    "ToolAccess",
    "WorldConfig",
    "label_episode",
    "run_episode",
]
