"""CIL basin_stability GraphState -> action-series adapter (ET-2, Leaf A).

Two layers, deliberately separated so tests do not need JAX/CIL installed:

1. ``action_matrix_to_series`` — pure Python, JAX-independent. Converts a
   ``(T, N)`` nested-list action matrix into the per-actor action-code
   series dict our frozen UAD pipeline already consumes (same shape as
   ``passive_uad_score.external_trace_to_action_series`` produces for ET-1).
2. ``run_basin_stability_episode`` — imports the pinned sibling checkout at
   ``external/cil/`` and runs one episode. This composes CIL's own public,
   per-transform factories (``proposal_generation_transform``,
   ``make_voting_transform``, ...) via its public ``sequential()`` — the
   same functions ``basin_stability.transforms.make_step_transform`` itself
   composes — inserting our own action-recording transform where CIL would
   insert a metrics transform (before ``step_counter_transform``). No CIL
   source is edited; see PLAN_ET2.md for why the built-in ``metrics=`` dict
   mechanism (scalar-only, pre-allocated as 1-D arrays) cannot carry a
   per-agent vector directly.

Fragility note: this duplicates CIL's `make_step_transform` pipeline *order*
(pinned at `external/cil/PIN.txt`). A CIL re-pin that reorders those
transforms would silently break the "record before step_counter" invariant;
re-verify this order against the new pin before trusting recorded actions.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ET2_PROTOCOL_VERSION = "et2-0.1.0"

_CIL_ROOT = Path(__file__).resolve().parents[2] / "external" / "cil"
_CIL_SRC = _CIL_ROOT / "src"


def _ensure_cil_on_path() -> None:
    for p in (str(_CIL_ROOT), str(_CIL_SRC)):
        if p not in sys.path:
            sys.path.insert(0, p)


def action_matrix_to_series(
    actions: list[list[int]],
    actor_ids: list[str],
) -> dict[str, list[int]]:
    """Convert a (T, N) action matrix into a per-actor action-code series.

    Args:
        actions: outer list length T (rounds), inner list length N (agents),
            each entry an integer action/proposal index (already a discrete
            code — no text/tool-call mapping needed on this substrate).
        actor_ids: length-N list of stable actor identifiers, in the same
            column order as ``actions``' inner lists.
    """
    if actions and len(actions[0]) != len(actor_ids):
        raise ValueError(
            f"action matrix has {len(actions[0])} columns but {len(actor_ids)} actor_ids"
        )
    series: dict[str, list[int]] = {a: [] for a in actor_ids}
    for row in actions:
        for actor, code in zip(actor_ids, row):
            series[actor].append(int(code))
    return series


def default_actor_ids(n_agents: int) -> list[str]:
    return [f"agent_{i}" for i in range(n_agents)]


def run_basin_stability_episode(
    *,
    mechanism: str,
    n_agents: int,
    n_adversarial: int,
    seed: int,
    T: int = 200,
) -> dict[str, Any]:
    """Run one CIL basin_stability episode and return plain-Python results.

    Requires the pinned sibling checkout at ``external/cil/`` with its own
    venv (``external/cil/.venv``) providing jax/jaxlib/numpy — run this
    function using that venv's interpreter, not the graded-lab stdlib-only
    environment. Raises a clear ImportError otherwise.

    Returns:
        {
          "mechanism", "n_agents", "n_adversarial", "seed", "T",
          "actions": (T, N) nested list of ints,
          "node_types": (N,) list of 0/1 (0=cooperative, 1=adversarial),
          "resource_level": T-length list of floats,
          "capture_rate": T-length list of floats (PRD only meaningful),
          "delegation_gini": T-length list of floats (PLD only meaningful),
        }
    """
    _ensure_cil_on_path()
    try:
        import jax.numpy as jnp  # noqa: F401
        import jax.lax as lax
        from cilib.core.category import sequential
        from cilib.metrics.families.governance import capture_rate as capture_rate_fn
        from cilib.metrics.families.governance import delegation_gini as delegation_gini_fn
    except ImportError as exc:
        raise ImportError(
            "run_basin_stability_episode requires the pinned CIL sibling checkout's "
            "venv (external/cil/.venv/bin/python3 -m pip install -e external/cil). "
            "See external/cil/README.md."
        ) from exc

    from experiments.basin_stability.state import create_initial_state
    from experiments.basin_stability.transforms import (
        proposal_generation_transform,
        make_voting_transform,
        make_aggregation_transform,
        resource_update_transform,
        reward_transform,
        make_q_learning_transform,
        trust_update_transform,
        make_election_transform,
        step_counter_transform,
    )

    state = create_initial_state(
        n_agents=n_agents,
        n_adversarial=n_adversarial,
        mechanism=mechanism,
        seed=seed,
        T=T,
    )

    # Our own (T, N) / (T,) recording arrays, added via the public
    # GraphState.update_global_attr API — no CIL source touched.
    state = state.update_global_attr("et2_action_history", jnp.zeros((T, n_agents), dtype=jnp.int32))
    state = state.update_global_attr("et2_resource_history", jnp.zeros((T,)))
    state = state.update_global_attr("et2_capture_history", jnp.zeros((T,)))
    state = state.update_global_attr("et2_gini_history", jnp.zeros((T,)))

    def _record_transform(s):
        step = s.global_attrs["step"]
        s = s.update_global_attr(
            "et2_action_history",
            s.global_attrs["et2_action_history"].at[step].set(s.node_attrs["last_action"]),
        )
        s = s.update_global_attr(
            "et2_resource_history",
            s.global_attrs["et2_resource_history"].at[step].set(s.global_attrs["resource_level"]),
        )
        s = s.update_global_attr(
            "et2_capture_history",
            s.global_attrs["et2_capture_history"].at[step].set(capture_rate_fn(s)),
        )
        s = s.update_global_attr(
            "et2_gini_history",
            s.global_attrs["et2_gini_history"].at[step].set(delegation_gini_fn(s)),
        )
        return s

    # Same order as basin_stability.transforms.make_step_transform, with our
    # recorder inserted where CIL would insert its own metrics transform:
    # BEFORE step_counter_transform, so index `step` is the round just played.
    step_transform = sequential(
        proposal_generation_transform,
        make_voting_transform(mechanism),
        make_aggregation_transform(mechanism),
        resource_update_transform,
        reward_transform,
        make_q_learning_transform(mechanism),
        trust_update_transform,
        make_election_transform(mechanism),
        _record_transform,
        step_counter_transform,
    )

    def scan_body(s, _):
        return step_transform(s), None

    final, _ = lax.scan(scan_body, state, None, length=T)

    return {
        "mechanism": mechanism,
        "n_agents": n_agents,
        "n_adversarial": n_adversarial,
        "seed": seed,
        "T": T,
        "actions": [[int(x) for x in row] for row in final.global_attrs["et2_action_history"].tolist()],
        "node_types": [int(x) for x in final.node_types.tolist()],
        "resource_level": [float(x) for x in final.global_attrs["et2_resource_history"].tolist()],
        "capture_rate": [float(x) for x in final.global_attrs["et2_capture_history"].tolist()],
        "delegation_gini": [float(x) for x in final.global_attrs["et2_gini_history"].tolist()],
    }
