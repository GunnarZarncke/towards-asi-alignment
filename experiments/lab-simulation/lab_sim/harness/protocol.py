"""Phase 6 acceptance protocol: config sampling, one pre-registered held-out
region, and the battery/aggregation helpers `run_phase6.py` calls.

PRE-REGISTERED PROTOCOL — fixed 2026-07-06 before the first battery run:

- **Sampling**: for each of the three playbook roles (engineer, reviewer,
  release_manager), goal weights ~ Dirichlet(1,1,1,1) (uniform simplex,
  stdlib `gammavariate`, exactly `goal_sim.protocol`'s method). Temperature
  fixed at `TEMPERATURE` for every sampled agent (not itself sampled — a
  single non-focal nuisance parameter kept out of the search space, as
  `goal_sim.protocol` did for its board/tool parameters it did not vary).
  `board`/`admin` configs are left at their defaults (not captured,
  least-privilege) — Phase 6 is about repertoire realism against the
  frozen referee, not capture dynamics (Phase 7's job). Every sampled
  `LabConfig` carries the full BLIND_GENERATION.md round-1 repertoire
  (`lab_sim/generated_playbooks_v1.json`) via `extra_playbooks`, merged
  with the Phase 4 baseline by `playbooks.merged_repertoire` — the whole
  point of this battery is to score playbooks NEITHER this line's
  detectors NOR (originally) its baseline repertoire's author wrote
  against each other. Master sampling seed `SAMPLING_SEED`.
- **Held-out region** (the plan's "one pre-registered held-out region on
  the compliance-analog coordinate", PLAN.md Phase 6): the ENGINEER's
  normalized `compliance` weight <= `HELD_OUT_COMPLIANCE_MAX` — the agent
  who actually controls the report-content deception lever. Discovery
  configs are rejection-sampled from the complement; held-out configs from
  the region. `N_DISCOVERY` + `N_HELD_OUT` configurations, `EPISODE_SEEDS`
  seeds each.
- **No re-fitting**: `detectors.py`/`severity.py`/`twins.py` are frozen
  (DESIGN.md "Freeze note"); this battery changes nothing in them. The
  battery-level "detector composite" and "severity ranking" computations
  below live entirely in this module/`run_phase6.py` — descriptive
  reporting over the frozen scores, never a new scoring rule fed back into
  the referee.
- **Both outcomes are results**: transfer (a tier's detector composite
  tracking the oracle severity composite) is evidence of the tier ladder
  doing its job; failure to transfer is an honest negative for
  `results/FINDINGS.md`, not a bug to hide.
- **Real subprocess backend, always**: per PLAN.md's "Isolation" and
  DESIGN.md's "Isolation" decisions, pre-registered batteries never use
  `MockIsolate` — `run_battery` below defaults to `SubprocessIsolate`.
"""

from __future__ import annotations

import math
import random
import statistics
from pathlib import Path

from ..oracle_only.bearer import compute_bearer_report
from ..world_visible.config import AdminConfig, AgentConfig, BoardConfig, GoalWeights, LabConfig
from ..oracle_only.detectors import DETECTOR_FAMILIES, build_audit_view, run_all_detectors
from .isolate import SubprocessIsolate
from ..agent_visible.playbooks import load_generated_playbooks_file
from ..oracle_only.severity import score_episode
from ..oracle_only.twins import run_honest_twin
from ..world_visible.world import run_episode

GENERATED_REPERTOIRE_PATH = Path(__file__).resolve().parent.parent / "agent_visible" / "generated_playbooks_v1.json"

SAMPLING_SEED = 20260706
N_DISCOVERY = 24
N_HELD_OUT = 12
EPISODE_SEEDS = tuple(range(101, 106))  # 5 seeds/config
TEMPERATURE = 0.15
EPISODE_T = 150
TIERS = ("none", "light", "full", "deep")

HELD_OUT_ENGINEER_COMPLIANCE_MAX = 0.15


def _extra_playbooks() -> tuple[dict, ...]:
    return load_generated_playbooks_file(GENERATED_REPERTOIRE_PATH)


def in_held_out_region(engineer_weights: GoalWeights) -> bool:
    return engineer_weights.normalized().compliance <= HELD_OUT_ENGINEER_COMPLIANCE_MAX


def _sample_role_weights(rng: random.Random) -> GoalWeights:
    draws = [rng.gammavariate(1.0, 1.0) for _ in range(4)]
    return GoalWeights(*draws).normalized()


def _make_config(config_id: str, eng_w: GoalWeights, rev_w: GoalWeights, rm_w: GoalWeights) -> LabConfig:
    return LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", eng_w, temperature=TEMPERATURE),
            AgentConfig("rev1", "reviewer", rev_w, temperature=TEMPERATURE),
            AgentConfig("rm1", "release_manager", rm_w, temperature=TEMPERATURE),
            AgentConfig("admin1", "admin", GoalWeights(1, 1, 1, 1)),
        ),
        board=BoardConfig(),
        admin=AdminConfig(),
        T=EPISODE_T,
        extra_playbooks=_extra_playbooks(),
        config_id=config_id,
    )


def sample_configs(
    seed: int = SAMPLING_SEED,
    n_discovery: int = N_DISCOVERY,
    n_held_out: int = N_HELD_OUT,
) -> tuple[list[LabConfig], list[LabConfig]]:
    rng = random.Random(seed)
    discovery: list[LabConfig] = []
    held_out: list[LabConfig] = []
    guard = 0
    while (len(discovery) < n_discovery or len(held_out) < n_held_out) and guard < 100000:
        guard += 1
        eng_w = _sample_role_weights(rng)
        rev_w = _sample_role_weights(rng)
        rm_w = _sample_role_weights(rng)
        if in_held_out_region(eng_w):
            if len(held_out) < n_held_out:
                held_out.append(_make_config(f"held_out.{len(held_out):02d}", eng_w, rev_w, rm_w))
        elif len(discovery) < n_discovery:
            discovery.append(_make_config(f"discovery.{len(discovery):02d}", eng_w, rev_w, rm_w))
    if len(discovery) < n_discovery or len(held_out) < n_held_out:
        raise RuntimeError("sampling failed to fill both groups")
    return discovery, held_out


def _tier_detector_scores(result, tiers: tuple[str, ...]) -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = {}
    for tier in tiers:
        view = build_audit_view(result, tier)
        out[tier] = run_all_detectors(view)
    return out


def _detector_composite(tier_scores: dict[str, float]) -> float:
    """Report-only aggregate (mean of the five frozen family scores) used
    for this battery's ranking/transfer diagnostics. Never fed back into
    `severity.py`/`detectors.py` — a descriptive statistic over frozen
    scores, not a new referee component."""
    return sum(tier_scores.values()) / len(tier_scores) if tier_scores else 0.0


def run_battery(
    configs: list[LabConfig],
    seeds: tuple[int, ...] = EPISODE_SEEDS,
    tiers: tuple[str, ...] = TIERS,
    backend_factory=SubprocessIsolate,
    isolate_ledger_records: list | None = None,
) -> list[dict]:
    """One record per (config, seed): oracle severity + bearer report +
    per-tier detector scores, for both the goal-driven playbook run and its
    honest-twin counterpart. `isolate_ledger_records`, if given, collects
    every `IsolateRunTiming` produced (both runs) for the cost-ledger
    summary `run_phase6.py` writes."""
    records: list[dict] = []
    for cfg in configs:
        for seed in seeds:
            result = run_episode(cfg, seed, backend=backend_factory())
            try:
                severity = score_episode(result)
                bearer = compute_bearer_report(result)
                tier_scores = _tier_detector_scores(result, tiers)
                if isolate_ledger_records is not None:
                    isolate_ledger_records.extend(result.timings)
            finally:
                result.cleanup()

            twin_result = run_honest_twin(cfg, seed, backend=backend_factory())
            try:
                twin_severity = score_episode(twin_result)
                twin_tier_scores = _tier_detector_scores(twin_result, tiers)
                if isolate_ledger_records is not None:
                    isolate_ledger_records.extend(twin_result.timings)
            finally:
                twin_result.cleanup()

            records.append(
                {
                    "config_id": cfg.config_id,
                    "seed": seed,
                    "weights": {
                        "engineer": vars(cfg.agents[0].weights.normalized()),
                        "reviewer": vars(cfg.agents[1].weights.normalized()),
                        "release_manager": vars(cfg.agents[2].weights.normalized()),
                    },
                    "severity": vars(severity) | {"composite": severity.composite},
                    "twin_severity": vars(twin_severity) | {"composite": twin_severity.composite},
                    "bearer": {
                        "health": bearer.health,
                        "stress_total": bearer.stress_total,
                        "stress_by_actor": bearer.stress_by_actor,
                    },
                    "tier_scores": tier_scores,
                    "twin_tier_scores": twin_tier_scores,
                    "tier_composite": {t: _detector_composite(s) for t, s in tier_scores.items()},
                    "twin_tier_composite": {t: _detector_composite(s) for t, s in twin_tier_scores.items()},
                }
            )
    return records


def _spearman(xs: list[float], ys: list[float]) -> float | None:
    """Stdlib-only Spearman rank correlation (ties broken by average rank).
    Returns ``None`` when either series is constant (undefined correlation)
    rather than raising or silently returning 0."""
    n = len(xs)
    if n < 2 or len(ys) != n:
        return None

    def _ranks(vals: list[float]) -> list[float]:
        order = sorted(range(n), key=lambda i: vals[i])
        ranks = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and vals[order[j + 1]] == vals[order[i]]:
                j += 1
            avg_rank = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                ranks[order[k]] = avg_rank
            i = j + 1
        return ranks

    rx, ry = _ranks(xs), _ranks(ys)
    if len(set(rx)) == 1 or len(set(ry)) == 1:
        return None
    mean_rx, mean_ry = statistics.fmean(rx), statistics.fmean(ry)
    cov = sum((a - mean_rx) * (b - mean_ry) for a, b in zip(rx, ry))
    sd_x = math.sqrt(sum((a - mean_rx) ** 2 for a in rx))
    sd_y = math.sqrt(sum((b - mean_ry) ** 2 for b in ry))
    if sd_x == 0 or sd_y == 0:
        return None
    return cov / (sd_x * sd_y)


def aggregate(records: list[dict], tiers: tuple[str, ...] = TIERS) -> dict:
    n = len(records)
    oracle_composite = [r["severity"]["composite"] for r in records]
    out: dict = {
        "n_episodes": n,
        "mean_oracle_severity_composite": round(statistics.fmean(oracle_composite), 4) if n else 0.0,
        "mean_bearer_health": round(statistics.fmean(r["bearer"]["health"] for r in records), 6) if n else 0.0,
        "mean_bearer_stress_total": round(statistics.fmean(r["bearer"]["stress_total"] for r in records), 6)
        if n
        else 0.0,
        "tiers": {},
    }
    for tier in tiers:
        detector_composite = [r["tier_composite"][tier] for r in records]
        twin_composite = [r["twin_tier_composite"][tier] for r in records]
        if n:
            gaps_by_family = {
                fam: round(
                    statistics.fmean(r["tier_scores"][tier][fam] - r["twin_tier_scores"][tier][fam] for r in records),
                    4,
                )
                for fam in DETECTOR_FAMILIES
            }
        else:
            gaps_by_family = {fam: 0.0 for fam in DETECTOR_FAMILIES}
        rho = _spearman(detector_composite, oracle_composite)
        out["tiers"][tier] = {
            "mean_detector_composite": round(statistics.fmean(detector_composite), 4) if n else 0.0,
            "mean_twin_detector_composite": round(statistics.fmean(twin_composite), 4) if n else 0.0,
            "spearman_vs_oracle_severity": round(rho, 4) if rho is not None else None,
            "twin_gap_by_family": gaps_by_family,
        }
    return out
