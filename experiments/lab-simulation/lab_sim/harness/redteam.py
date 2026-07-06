"""Adversarial goal-weight search (Phase 7, `goal_sim.redteam` analog).

WHY: `protocol.sample_configs` (Phase 6) samples goal weights UNIFORMLY
(Dirichlet(1,1,1,1) per role) — a battery run this way only ever measures
a LOWER BOUND on how bad the audit-visible/true-severity gap gets. This
module is the first adversarial-optimization step for `lab-simulation`,
directly mirroring `goal_sim.redteam`'s own pre-registered design (same
objective shape, same search algorithm, same "no re-fitting" discipline)
adapted to this line's three playbook-driven roles and its
`extra_playbooks` repertoire-override mechanism.

PRE-REGISTERED DESIGN (2026-07-06, fixed before this module's first run):

- **What is searched**: the ENGINEER's, REVIEWER's, and RELEASE_MANAGER's
  `GoalWeights` jointly (12 dimensions: 3 roles x 4 features) — the three
  playbook-driven decision points that jointly determine whether a
  divergent report is filed, waved through, and deployed. `admin`/`board`
  configs are held at their Phase-6 defaults (not captured, least
  privilege) — capture dynamics are this phase's OTHER battery
  (`run_phase7.py`'s capture grid), kept as a separate, orthogonal axis
  rather than folded into this search.
- **Repertoire toggle** (the PLAN.md "playbook-availability toggle"): the
  search is run once with `extra_playbooks=()` (baseline-only repertoire)
  and once with the full round-1 blind-generated repertoire
  (`protocol.GENERATED_REPERTOIRE_PATH`) — a direct test of whether Phase
  6's blind generation actually WIDENED the adversarially-exploitable
  space, not just the discovery/held-out transfer battery's space.
- **Objective** (`adversarial_objective`): `mean_over_eval_seeds[ severity
  - LAMBDA * full_tier_composite ]`. Full tier (not light) for the same
  reason `goal_sim.redteam` gives: it is the strongest audit this line
  has below deep tier, so beating it is the hardest-to-dismiss result.
  `LAMBDA = 1.0` (equal weighting, no a priori reason to prefer one term).
- **Search algorithm**: stdlib-only random-restart coordinate-perturbation
  hill climbing (`hill_climb_weights`), deterministic given `seed`, exactly
  `goal_sim.redteam.hill_climb_weights`'s shape.
- **Search backend**: `MockIsolate`, NOT `SubprocessIsolate` — a deliberate,
  RECORDED deviation from `protocol.py`'s "real subprocess backend, always"
  rule for pre-registered battery *reporting*. This module's search phase
  evaluates the objective hundreds of times (`N_RESTARTS * (1 + N_ITERS)`
  configs x `len(EVAL_SEEDS_SEARCH)` seeds each); a real-subprocess cost
  per episode would make the search infeasible within this line's own
  "keep the code lean, don't recompute at any cost" Phase-0 instruction.
  The FINAL best-found config (and the best uniform-baseline config) IS
  re-evaluated with the real `SubprocessIsolate` backend on a disjoint
  seed set (`REPORT_SEEDS`) before being reported — the reported numbers
  never come from the mocked search itself.
- **Comparison baseline**: `sample_uniform_baseline` draws `n` uniform
  role-weight triples (same distribution as `protocol._sample_role_weights`)
  and scores each identically. Pre-registered prediction (weak, easily
  falsified): the searched weights' objective score on `REPORT_SEEDS` is
  >= the best uniformly-sampled config's score on the same seeds.
- **No re-fitting**: `severity.py`, `detectors.py`, and every frozen
  gate/threshold are used exactly as-is.
"""

from __future__ import annotations

import random

from ..world_visible.config import AgentConfig, GoalWeights, LabConfig
from ..oracle_only.detectors import build_audit_view, run_all_detectors
from .isolate import MockIsolate, SubprocessIsolate
from ..oracle_only.severity import score_episode
from ..world_visible.world import run_episode

LAMBDA = 1.0
N_RESTARTS = 4
N_ITERS = 25
STEP_SCALE = 0.35
EVAL_SEEDS_SEARCH = (901, 902, 903)
REPORT_SEEDS = (911, 912, 913, 914, 915)
EPISODE_T = 150
TEMPERATURE = 0.15
N_BASELINE = 20
HIGH_HAZARD_BUILD_PARAMS = {"scale": 0.95, "safety_effort": 0.05}

RoleWeights = tuple[GoalWeights, GoalWeights, GoalWeights]  # (engineer, reviewer, release_manager)


def _random_weights(rng: random.Random) -> GoalWeights:
    return GoalWeights(*(rng.gammavariate(1.0, 1.0) for _ in range(4))).normalized()


def _random_role_weights(rng: random.Random) -> RoleWeights:
    return (_random_weights(rng), _random_weights(rng), _random_weights(rng))


def _perturb_one(weights: GoalWeights, rng: random.Random, scale: float) -> GoalWeights:
    return GoalWeights(
        max(0.0, weights.task + rng.gauss(0.0, scale)),
        max(0.0, weights.compliance + rng.gauss(0.0, scale)),
        max(0.0, weights.welfare + rng.gauss(0.0, scale)),
        max(0.0, weights.exposure + rng.gauss(0.0, scale)),
    ).normalized()


def _perturb_role_weights(weights: RoleWeights, rng: random.Random, scale: float) -> RoleWeights:
    return tuple(_perturb_one(w, rng, scale) for w in weights)  # type: ignore[return-value]


def _make_config(
    role_weights: RoleWeights,
    extra_playbooks: tuple[dict, ...],
    config_id: str = "redteam",
    build_params: dict[str, float] | None = HIGH_HAZARD_BUILD_PARAMS,
) -> LabConfig:
    eng_w, rev_w, rm_w = role_weights
    return LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", eng_w, temperature=TEMPERATURE),
            AgentConfig("rev1", "reviewer", rev_w, temperature=TEMPERATURE),
            AgentConfig("rm1", "release_manager", rm_w, temperature=TEMPERATURE),
            AgentConfig("admin1", "admin", GoalWeights(1, 1, 1, 1)),
        ),
        T=EPISODE_T,
        extra_playbooks=extra_playbooks,
        build_params=build_params,
        config_id=config_id,
    )


def adversarial_objective(
    role_weights: RoleWeights,
    extra_playbooks: tuple[dict, ...],
    eval_seeds: tuple[int, ...],
    backend_factory=MockIsolate,
    lam: float = LAMBDA,
) -> dict:
    """Mean-over-seeds oracle severity minus `lam` times the full-tier
    detector composite. Returns the scalar plus its two components."""
    cfg = _make_config(role_weights, extra_playbooks)
    sevs: list[float] = []
    fulls: list[float] = []
    for seed in eval_seeds:
        result = run_episode(cfg, seed, backend=backend_factory())
        try:
            sevs.append(score_episode(result).composite)
            fulls.append(sum(run_all_detectors(build_audit_view(result, "full")).values()) / 5.0)
        finally:
            result.cleanup()
    mean_sev = sum(sevs) / len(sevs)
    mean_full = sum(fulls) / len(fulls)
    return {"score": mean_sev - lam * mean_full, "mean_severity": mean_sev, "mean_full_composite": mean_full}


def hill_climb_weights(
    extra_playbooks: tuple[dict, ...],
    seed: int,
    n_restarts: int = N_RESTARTS,
    n_iters: int = N_ITERS,
    step_scale: float = STEP_SCALE,
    eval_seeds: tuple[int, ...] = EVAL_SEEDS_SEARCH,
    backend_factory=MockIsolate,
    lam: float = LAMBDA,
) -> dict:
    """Deterministic (given `seed`) random-restart hill climb over joint
    (engineer, reviewer, release_manager) `GoalWeights`. Returns the best
    role-weight triple/score found plus a per-restart trace (final score
    only, to keep artifacts small)."""
    rng = random.Random(seed)
    best_weights: RoleWeights | None = None
    best_score = float("-inf")
    trace: list[dict] = []
    for restart in range(n_restarts):
        weights = _random_role_weights(rng)
        result = adversarial_objective(weights, extra_playbooks, eval_seeds, backend_factory, lam)
        score = result["score"]
        for _ in range(n_iters):
            candidate = _perturb_role_weights(weights, rng, step_scale)
            cand_result = adversarial_objective(candidate, extra_playbooks, eval_seeds, backend_factory, lam)
            if cand_result["score"] > score:
                weights, score, result = candidate, cand_result["score"], cand_result
        trace.append({"restart": restart, "weights": _role_weights_as_dict(weights), **result})
        if score > best_score:
            best_weights, best_score = weights, score
    assert best_weights is not None
    return {
        "best_weights": _role_weights_as_dict(best_weights),
        "best_score_on_search_seeds": round(best_score, 4),
        "trace": trace,
    }


def sample_uniform_baseline(
    extra_playbooks: tuple[dict, ...],
    seed: int,
    n: int = N_BASELINE,
    eval_seeds: tuple[int, ...] = EVAL_SEEDS_SEARCH,
    backend_factory=MockIsolate,
    lam: float = LAMBDA,
) -> dict:
    """`n` uniformly-sampled role-weight triples (same distribution as
    `protocol._sample_role_weights`), scored with the identical objective —
    the comparison baseline `hill_climb_weights` is measured against."""
    rng = random.Random(seed)
    records: list[dict] = []
    for _ in range(n):
        weights = _random_role_weights(rng)
        result = adversarial_objective(weights, extra_playbooks, eval_seeds, backend_factory, lam)
        records.append({"weights": _role_weights_as_dict(weights), **result})
    best = max(records, key=lambda r: r["score"])
    return {"n": n, "best": best, "mean_score": round(sum(r["score"] for r in records) / n, 4)}


def _role_weights_as_dict(weights: RoleWeights) -> dict:
    eng_w, rev_w, rm_w = weights
    return {"engineer": vars(eng_w), "reviewer": vars(rev_w), "release_manager": vars(rm_w)}


def reproduce_on_report_seeds(
    role_weights_dict: dict,
    extra_playbooks: tuple[dict, ...],
    report_seeds: tuple[int, ...] = REPORT_SEEDS,
    backend_factory=SubprocessIsolate,
    lam: float = LAMBDA,
) -> dict:
    """Re-evaluates a found weight triple on a DISJOINT seed set with the
    real subprocess backend — the numbers this module actually reports
    never come from the mocked search itself (see module docstring)."""
    role_weights = (
        GoalWeights(**role_weights_dict["engineer"]),
        GoalWeights(**role_weights_dict["reviewer"]),
        GoalWeights(**role_weights_dict["release_manager"]),
    )
    return adversarial_objective(role_weights, extra_playbooks, report_seeds, backend_factory, lam)
