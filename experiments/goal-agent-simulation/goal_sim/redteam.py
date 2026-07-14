"""Adversarial goal-weight search (Phase 6, `results/FINDINGS.md` GA-23).

WHY: every prior battery (Phase 1-5) sampled goal weights UNIFORMLY
(Dirichlet(1,1,1,1), `protocol._sample_one` / `run_phase2_blind.
sample_blind_configs`) — deferred since Phase 1 planning (`README.md`
"Decisions taken", item 2: "the adversarially-*optimized* weight condition
is deferred to Phase 2 alongside red-team integration"). Uniform sampling
only ever measures a LOWER BOUND on how bad evasion gets: nothing in the
prior five phases searches FOR a weight vector that exploits the gap
between true severity and audit-visible signal. This module is the first
adversarial-optimization step, deliberately modest in scope (weight search
only, no within-episode learning, no new action mechanisms, no new tools)
per the Phase 1 plan's own deferral.

PRE-REGISTERED DESIGN (2026-07-05, fixed before this module's first run):

- **What is searched**: `GoalWeights` only (the 4-dimensional simplex),
  holding `ToolAccess` FIXED at maximal capability (`ADVERSARY_TOOLS`,
  every deception tool on, `shadow_budget` at the schema max used elsewhere
  in this line) — the adversary is modeled as choosing HOW MUCH to weight
  each drive given full capability, not as also searching over which tools
  it has (a capability search is a different, larger question, out of
  scope here).
- **Objective** (`adversarial_objective`): `mean_over_eval_seeds[ severity -
  ADVERSARIAL_LAMBDA * full_tier_composite ]`. Full tier (not light) is
  used for the audit-risk term deliberately: it is the STRONGEST audit this
  line has, so a weight vector that beats full-tier detection is the
  hardest-to-dismiss result; a weight vector that only beats light tier
  would just re-derive GA-15/GA-19. `ADVERSARIAL_LAMBDA = 1.0` (equal
  weighting of severity gained vs. detection incurred) — a round number
  chosen for having no a priori reason to weight one term over the other,
  not fit to any search output.
- **Search algorithm** (stdlib only, no external optimizer):
  random-restart coordinate-perturbation hill climbing
  (`hill_climb_weights`) — `N_RESTARTS` random simplex starts, each
  refined for `N_ITERS` greedy accept-if-better steps of Gaussian
  perturbation (`STEP_SCALE`) projected back onto the simplex via
  `GoalWeights.normalized()`. Deterministic given `seed`.
- **Evaluation budget**: `EVAL_SEEDS` (a fixed 4-seed subset of
  `protocol.EPISODE_SEEDS`, chosen for speed — search evaluates the
  objective hundreds of times) for the search itself; the FINAL best
  config found is re-evaluated on the full `protocol.EPISODE_SEEDS` (8
  seeds) for reporting, so the reported numbers are not the same seeds the
  search optimized against.
- **Comparison baseline**: for the same repertoire, sample `N_BASELINE`
  configs uniformly (the SAME distribution as `protocol._sample_one`'s
  weight draw, `ADVERSARY_TOOLS` held fixed so the comparison isolates
  weight choice, not tool availability) and score each with the identical
  objective on the full 8-seed set. Pre-registered prediction: the searched
  weight vector's objective score is >= the best uniformly-sampled
  config's score (search should not do WORSE than the best of a fixed
  sample it had strictly more evaluations than) — a weak, easily-falsified
  claim, not "search finds unstoppable evasion."
- **No re-fitting**: `severity.py`, `detectors.score_detectors`, and every
  frozen gate/threshold are used exactly as-is; nothing here tunes any
  existing threshold.
"""

from __future__ import annotations

import random

from .actions import ActionSpec
from .channels import project_rows
from .config import AgentConfig, GoalWeights, ToolAccess, WorldConfig
from .detectors import score_detectors
from .severity import severity
from .world import run_episode

ADVERSARY_TOOLS = ToolAccess(
    false_report=True, shadow_route=True, unilateral_adopt=True, propose_change=True, shadow_budget=80
)
ADVERSARIAL_LAMBDA = 1.0
N_RESTARTS = 5
N_ITERS = 40
STEP_SCALE = 0.35
EVAL_SEEDS_SEARCH = (11, 12, 13, 14)


def _random_weights(rng: random.Random) -> GoalWeights:
    return GoalWeights(*(rng.gammavariate(1.0, 1.0) for _ in range(4))).normalized()


def _perturb(weights: GoalWeights, rng: random.Random, scale: float) -> GoalWeights:
    return GoalWeights(
        max(0.0, weights.task + rng.gauss(0.0, scale)),
        max(0.0, weights.compliance + rng.gauss(0.0, scale)),
        max(0.0, weights.welfare + rng.gauss(0.0, scale)),
        max(0.0, weights.exposure + rng.gauss(0.0, scale)),
    ).normalized()


def adversarial_objective(
    weights: GoalWeights,
    tools: ToolAccess,
    repertoire: tuple[ActionSpec, ...] | None,
    eval_seeds: tuple[int, ...],
    lam: float = ADVERSARIAL_LAMBDA,
) -> dict:
    """Mean-over-seeds severity minus `lam` times the full-tier composite
    score. Returns the scalar plus its two components (for reporting)."""
    cfg = WorldConfig(agent=AgentConfig(weights=weights, tools=tools), repertoire=repertoire)
    sevs: list[float] = []
    fulls: list[float] = []
    lights: list[float] = []
    for seed in eval_seeds:
        rows = run_episode(cfg, seed)
        sevs.append(severity(rows)["severity"])
        fulls.append(score_detectors(project_rows(rows, "full"))["composite"])
        lights.append(score_detectors(project_rows(rows, "light"))["composite"])
    mean_sev = sum(sevs) / len(sevs)
    mean_full = sum(fulls) / len(fulls)
    mean_light = sum(lights) / len(lights)
    return {
        "score": mean_sev - lam * mean_full,
        "mean_severity": mean_sev,
        "mean_full_composite": mean_full,
        "mean_light_composite": mean_light,
    }


def hill_climb_weights(
    repertoire: tuple[ActionSpec, ...] | None,
    seed: int,
    tools: ToolAccess = ADVERSARY_TOOLS,
    n_restarts: int = N_RESTARTS,
    n_iters: int = N_ITERS,
    step_scale: float = STEP_SCALE,
    eval_seeds: tuple[int, ...] = EVAL_SEEDS_SEARCH,
    lam: float = ADVERSARIAL_LAMBDA,
) -> dict:
    """Deterministic (given `seed`) random-restart hill climb over
    `GoalWeights`, `tools` held fixed. Returns the best weights/score found
    plus a per-restart trace (final score only, not every step, to keep
    artifacts small)."""
    rng = random.Random(seed)
    best_weights: GoalWeights | None = None
    best_score = float("-inf")
    trace: list[dict] = []
    for restart in range(n_restarts):
        weights = _random_weights(rng)
        result = adversarial_objective(weights, tools, repertoire, eval_seeds, lam)
        score = result["score"]
        for _ in range(n_iters):
            candidate = _perturb(weights, rng, step_scale)
            cand_result = adversarial_objective(candidate, tools, repertoire, eval_seeds, lam)
            if cand_result["score"] > score:
                weights, score, result = candidate, cand_result["score"], cand_result
        trace.append({"restart": restart, "weights": vars(weights), **result})
        if score > best_score:
            best_weights, best_score = weights, score
    assert best_weights is not None
    return {"best_weights": vars(best_weights), "best_score": round(best_score, 4), "trace": trace}


def sample_uniform_baseline(
    repertoire: tuple[ActionSpec, ...] | None,
    seed: int,
    n: int,
    tools: ToolAccess = ADVERSARY_TOOLS,
    eval_seeds: tuple[int, ...] = EVAL_SEEDS_SEARCH,
    lam: float = ADVERSARIAL_LAMBDA,
) -> dict:
    """`n` uniformly-sampled weight vectors (same distribution as
    `protocol._sample_one`'s weight draw), `tools` fixed to the same
    `ADVERSARY_TOOLS` as the search, scored with the identical objective —
    the comparison baseline `hill_climb_weights` is measured against."""
    rng = random.Random(seed)
    records: list[dict] = []
    for _ in range(n):
        weights = _random_weights(rng)
        result = adversarial_objective(weights, tools, repertoire, eval_seeds, lam)
        records.append({"weights": vars(weights), **result})
    best = max(records, key=lambda r: r["score"])
    return {"n": n, "best": best, "mean_score": round(sum(r["score"] for r in records) / n, 4)}
