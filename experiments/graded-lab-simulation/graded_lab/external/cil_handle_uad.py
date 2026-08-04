"""Intervention-based ("handle") UAD ported to CIL's basin_stability (ET-2, follow-up).

Small first pass on the REPRODUCTION.md §14 item 1 sketch, run after GL-87's
passive-UAD null. Unlike graded-lab's LLM-agent substrate, CIL's
``basin_stability`` is a pure, seed-deterministic JAX pipeline
(``proposal_gen -> voting -> aggregation -> resource_update -> reward ->
q_learning -> trust_update -> election -> step_counter``), so a freeze probe
is a same-seed counterfactual re-run with one line changed, not a
subprocess-isolate intervention:

1. Run a baseline episode at seed ``s`` (unmodified pipeline).
2. For each candidate source agent ``i``, re-run at the *same* seed ``s``
   with one extra transform inserted right after ``voting_transform``
   (before aggregation/resource/reward/trust/q-learning all consume
   ``last_action``): overwrite agent ``i``'s realized action for that round
   with a fixed constant. All RNG draws (proposal draws, signal noise,
   epsilon-greedy sampling for every *other* agent) are byte-identical
   across baseline and freeze runs — the only difference is agent ``i``'s
   realized action, so any divergence in another agent ``j``'s subsequent
   actions is a real causal effect of ``i``'s realized choice, not sampling
   noise. This is a cleaner single-variable ``do(action_i = c)`` than the
   graded-lab line's ``program_freeze_probe`` (which disables a whole
   subprocess-isolate agent, not one action).

Dependency score: fraction of rounds where the target agent's realized
action differs between the freeze-source-``i`` run and baseline, at the
same seed. This is compared across seeds (a repeated-run null over
different random seeds, not the same-seed baseline itself, since the
same-seed baseline vs. itself is trivially zero) to see whether the
freeze effect exceeds ordinary seed-to-seed variation.

This module deliberately does *not* port the graded-lab line's full
specificity-ratio / union-find merge rule (``uad_handles.units_from_handle_matrix``)
— basin_stability's shared resource level couples every agent's reward to
every other agent's action, so a "some pair is privileged over all others"
merge rule needs a same-substrate specificity baseline before it would mean
anything here; see the module docstring in ``uad_handles.py`` for why that
merge rule was pre-registered *before* looking at fixture results on the
graded-lab substrate, which this port has not done. This module reports the
raw dependency matrix and a same-seed vs. cross-seed contrast instead, which
is the honest first question ("does an intervention move anything, more than
sampling noise would") rather than the harder second question ("is any pair
distinctively coupled").
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

_CIL_ROOT = Path(__file__).resolve().parents[2] / "external" / "cil"
_CIL_SRC = _CIL_ROOT / "src"


def _ensure_cil_on_path() -> None:
    for p in (str(_CIL_ROOT), str(_CIL_SRC)):
        if p not in sys.path:
            sys.path.insert(0, p)


def run_baseline_and_freeze_episodes(
    *,
    mechanism: str,
    n_agents: int,
    n_adversarial: int,
    seed: int,
    T: int = 200,
    freeze_action: int = 0,
) -> dict[str, Any]:
    """Run one baseline episode plus one freeze-probe episode per agent.

    Returns a dict with ``baseline_actions`` ((T, N) list of ints) and
    ``freeze_actions`` (dict ``{source_agent_index: (T, N) list of ints}``),
    all at the same seed, so any row-wise difference from ``baseline_actions``
    in ``freeze_actions[i]`` is a causal effect of freezing agent ``i``.
    """
    _ensure_cil_on_path()
    try:
        import jax.numpy as jnp
        import jax.lax as lax
        from cilib.core.category import sequential
    except ImportError as exc:
        raise ImportError(
            "run_baseline_and_freeze_episodes requires the pinned CIL sibling "
            "checkout's venv (external/cil/.venv/bin/python3 -m pip install -e "
            "external/cil). See external/cil/README.md."
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

    def _make_freeze_transform(freeze_agent: int | None):
        """``None`` -> identity (baseline). Otherwise overwrite one agent's
        ``last_action`` with ``freeze_action`` right after voting, before
        anything downstream reads it."""

        def _freeze(s):
            if freeze_agent is None:
                return s
            actions = s.node_attrs["last_action"]
            actions = actions.at[freeze_agent].set(freeze_action)
            return s.update_node_attrs("last_action", actions)

        return _freeze

    def _make_recorder(n_agents_: int, T_: int):
        def _record(s):
            step = s.global_attrs["step"]
            return s.update_global_attr(
                "et2h_action_history",
                s.global_attrs["et2h_action_history"].at[step].set(s.node_attrs["last_action"]),
            )

        return _record

    def _run_one(freeze_agent: int | None) -> list[list[int]]:
        state = create_initial_state(
            n_agents=n_agents,
            n_adversarial=n_adversarial,
            mechanism=mechanism,
            seed=seed,
            T=T,
        )
        state = state.update_global_attr(
            "et2h_action_history", jnp.zeros((T, n_agents), dtype=jnp.int32)
        )
        step_transform = sequential(
            proposal_generation_transform,
            make_voting_transform(mechanism),
            _make_freeze_transform(freeze_agent),
            make_aggregation_transform(mechanism),
            resource_update_transform,
            reward_transform,
            make_q_learning_transform(mechanism),
            trust_update_transform,
            make_election_transform(mechanism),
            _make_recorder(n_agents, T),
            step_counter_transform,
        )

        def scan_body(s, _):
            return step_transform(s), None

        final, _ = lax.scan(scan_body, state, None, length=T)
        return [[int(x) for x in row] for row in final.global_attrs["et2h_action_history"].tolist()]

    baseline_actions = _run_one(None)
    freeze_actions = {i: _run_one(i) for i in range(n_agents)}

    return {
        "mechanism": mechanism,
        "n_agents": n_agents,
        "n_adversarial": n_adversarial,
        "seed": seed,
        "T": T,
        "freeze_action": freeze_action,
        "baseline_actions": baseline_actions,
        "freeze_actions": freeze_actions,
    }


def _action_diff_rate(a: list[list[int]], b: list[list[int]], target: int) -> float:
    """Fraction of rounds where agent ``target``'s action differs between
    two (T, N) action matrices."""
    T = len(a)
    if T == 0:
        return 0.0
    diffs = sum(1 for t in range(T) if a[t][target] != b[t][target])
    return diffs / T


def dependency_matrix_from_episode(episode: dict[str, Any]) -> dict[tuple[int, int], float]:
    """Directed ``(source, target) -> action_diff_rate`` matrix for one seed.

    ``source`` is the frozen agent; ``target`` is any other agent whose
    action-series is compared, freeze run vs. baseline, at the same seed.
    Diagonal (``source == target``) is excluded — freezing an agent trivially
    changes its own actions on rounds where its policy would have chosen
    otherwise; that is not evidence about coupling to others.
    """
    n = episode["n_agents"]
    baseline = episode["baseline_actions"]
    matrix: dict[tuple[int, int], float] = {}
    for source in range(n):
        freeze_run = episode["freeze_actions"][source]
        for target in range(n):
            if source == target:
                continue
            matrix[(source, target)] = _action_diff_rate(baseline, freeze_run, target)
    return matrix


def cross_seed_null_rate(
    episodes: list[dict[str, Any]],
) -> float:
    """Baseline-vs-baseline action-diff rate across *different* seeds,
    averaged over all agents and all seed pairs — the "ordinary variation,
    no intervention at all" comparator for ``dependency_matrix_from_episode``'s
    per-pair rates. If a freeze-induced diff rate for pair (i, j) is no
    larger than this cross-seed null, the freeze is not doing better than
    "any two random episodes disagree about agent j's actions this often."
    """
    if len(episodes) < 2:
        return float("nan")
    n = episodes[0]["n_agents"]
    rates: list[float] = []
    for a_idx in range(len(episodes)):
        for b_idx in range(a_idx + 1, len(episodes)):
            a = episodes[a_idx]["baseline_actions"]
            b = episodes[b_idx]["baseline_actions"]
            for target in range(n):
                rates.append(_action_diff_rate(a, b, target))
    return sum(rates) / len(rates) if rates else float("nan")
