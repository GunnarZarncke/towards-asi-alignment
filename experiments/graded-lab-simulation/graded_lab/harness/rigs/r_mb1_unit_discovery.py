"""R-MB1 — unit discovery on unseen ground truth (PLAN_v4).

Question: does frozen UAD (passive + intervention) recover
declared-and-enforced coupling mechanisms it was not co-developed with?
(P1/P2 class, decomposed out of the coupled V2-3 battery.)

Precondition (frozen V4-1, mechanical, computed from ``primitive_log``
timestamps/actor ids only — never from UAD's own partition output): the
fixture's reference traces contain at least ``K_MIN_MEAN_COACTIVITY``
mean same-tick co-activity events per multi-member C5-declared
mechanism, averaged over the fixture's seeds. GL-76's diagnosis — v3's
short-burst one-shot scripts defeat co-activity clustering — becomes a
measured precondition instead of a post-hoc explanation: this rig is
expected to SKIP on the S-inherited v3_grown substrate.
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Any

from ..fixtures import ReferenceFixture
from ..machinery_transfer import (
    MECHANISM_MAJORITY_SEED_FRACTION,
    P1_COMMUNICATE_RECOVERY_FRACTION,
    MechanismGroundTruth,
    _fraction_mechanisms_majority_hit,
    _ground_truth_pair_set,
    _cocluster_pairs,
    _mechanism_pass_rates,
    c5_ground_truth_catalog,
    mechanism_recovered,
    p1_communicate_ground_truth_pool,
)
from ..isolate import MockIsolate
from ...oracle_only.uad_discovery import discovered_units_uad
from ...oracle_only.uad_intervention import discovered_units_intervention
from .base import PreconditionReport, RigResult

RIG_ID = "R-MB1"

# --- V4-1 frozen precondition constant (do not tune post-registration) ---
K_MIN_MEAN_COACTIVITY = 1.0


def count_coactivity_events(result: Any, members: frozenset[str]) -> int:
    """Count ticks with >= 2 distinct ``members`` each issuing an ok primitive.

    Mechanical: reads only ``t``, ``actor_id``, ``status`` off
    ``primitive_log``. Does not call UAD or any CMI test.
    """
    by_tick: dict[int, set[str]] = {}
    for event in result.primitive_log:
        if event.get("status") != "ok":
            continue
        actor = str(event.get("actor_id", ""))
        if actor not in members:
            continue
        by_tick.setdefault(int(event.get("t", 0)), set()).add(actor)
    return sum(1 for actors in by_tick.values() if len(actors) >= 2)


def check_precondition(fixture: ReferenceFixture) -> PreconditionReport:
    catalog = c5_ground_truth_catalog(fixture.ecology_data, fixture.roster)
    multi_member = [gt for gt in catalog if len(gt.members) >= 2]
    per_mechanism_mean: dict[str, float] = {}
    for gt in multi_member:
        counts = [
            count_coactivity_events(fixture.results_by_seed[seed], gt.members)
            for seed in fixture.seeds
        ]
        per_mechanism_mean[gt.mechanism_id] = sum(counts) / len(counts) if counts else 0.0
    overall_mean = (
        sum(per_mechanism_mean.values()) / len(per_mechanism_mean)
        if per_mechanism_mean
        else 0.0
    )
    satisfied = bool(multi_member) and overall_mean >= K_MIN_MEAN_COACTIVITY
    return PreconditionReport(
        rig_id=RIG_ID,
        satisfied=satisfied,
        measured={
            "per_mechanism_mean_coactivity_events": per_mechanism_mean,
            "overall_mean_coactivity_events": overall_mean,
            "n_multi_member_mechanisms": len(multi_member),
            "n_seeds": len(fixture.seeds),
        },
        threshold={"k_min_mean_coactivity_events": K_MIN_MEAN_COACTIVITY},
        note=(
            "Mean same-tick co-activity events per multi-member C5-declared "
            "mechanism, averaged over the fixture's seeds; computed from "
            "primitive_log timestamps/actor ids only, never from UAD's "
            "discovered partition (PLAN_v4 R-MB1 precondition contract)."
        ),
    )


def _score_seed_from_fixture(
    seed: int,
    fixture: ReferenceFixture,
    catalog: list[MechanismGroundTruth],
    *,
    backend=None,
) -> dict[str, Any]:
    """UAD scoring reusing the fixture's already-run passive episode.

    Only the intervention arm pays for its own additional (counterfactual)
    episodes, per PLAN_v4 architecture item 2 ("rigs consume traces, they
    do not re-simulate ... a rig that needs interventional episodes
    declares that and pays for its own runs").
    """
    backend = backend or MockIsolate()
    result = fixture.results_by_seed[seed]
    passive = discovered_units_uad(result=result, rng_seed=seed)
    intervention = discovered_units_intervention(
        result,
        fixture.cfg,
        seed,
        fixture.programs,
        backend=backend,
        candidate_source="all_pairs",
    )
    mechanism_hits: dict[str, dict[str, bool]] = {}
    for gt in catalog:
        mechanism_hits[gt.mechanism_id] = {
            "passive": mechanism_recovered(passive, gt.members),
            "intervention": mechanism_recovered(intervention, gt.members),
        }
    allowed_pairs = _ground_truth_pair_set(catalog)
    spurious = sorted(
        _cocluster_pairs(intervention) - allowed_pairs,
        key=lambda p: tuple(sorted(p)),
    )
    return {
        "seed": seed,
        "passive_nonsingletons": [list(c) for c in passive.values() if len(c) > 1],
        "intervention_nonsingletons": [
            list(c) for c in intervention.values() if len(c) > 1
        ],
        "mechanism_hits": mechanism_hits,
        "spurious_intervention_pairs": [sorted(p) for p in spurious],
    }


class _FixtureStub:
    """Minimal per-worker fixture carrying only what scoring needs.

    ``results_by_seed`` is populated per-job in the worker so each task
    ships only its own seed's precomputed episode, not the whole fixture.
    """

    def __init__(self, cfg: Any, programs: dict[str, str]) -> None:
        self.cfg = cfg
        self.programs = programs
        self.results_by_seed: dict[int, Any] = {}


_PARALLEL_CTX: dict[str, Any] | None = None


def _init_parallel_worker(ctx: dict[str, Any]) -> None:
    global _PARALLEL_CTX
    _PARALLEL_CTX = ctx


def _work_seed(args: tuple[int, Any]) -> dict[str, Any]:
    seed, result = args
    assert _PARALLEL_CTX is not None
    fixture = _PARALLEL_CTX["fixture_stub"]
    fixture.results_by_seed[seed] = result
    return _score_seed_from_fixture(seed, fixture, _PARALLEL_CTX["catalog"])


def score_uad_from_fixture(
    fixture: ReferenceFixture,
    catalog: list[MechanismGroundTruth],
    *,
    backend=None,
    progress: bool = True,
    workers: int = 1,
) -> dict[str, Any]:
    """Score UAD passive+intervention from an already-built fixture.

    ``workers > 1`` parallelizes the per-seed intervention battery (the
    dominant cost, GL-75c pattern) across a process pool; each job ships
    only its own seed's precomputed episode result, not the whole fixture.
    """
    if workers <= 1:
        per_seed: list[dict[str, Any]] = []
        for i, seed in enumerate(fixture.seeds):
            if progress:
                print(f"[r-mb1 uad {i + 1}/{len(fixture.seeds)}] seed={seed}", flush=True)
            per_seed.append(_score_seed_from_fixture(seed, fixture, catalog, backend=backend))
        return {"per_seed": per_seed, "n_seeds": len(fixture.seeds)}

    ctx = {"fixture_stub": _FixtureStub(fixture.cfg, fixture.programs), "catalog": catalog}
    rows_by_seed: dict[int, dict[str, Any]] = {}
    with ProcessPoolExecutor(
        max_workers=workers, initializer=_init_parallel_worker, initargs=(ctx,)
    ) as pool:
        futures = {
            pool.submit(_work_seed, (seed, fixture.results_by_seed[seed])): seed
            for seed in fixture.seeds
        }
        done = 0
        for fut in as_completed(futures):
            done += 1
            seed = futures[fut]
            rows_by_seed[seed] = fut.result()
            if progress:
                print(f"[r-mb1 uad parallel {done}/{len(fixture.seeds)}] seed={seed} done", flush=True)
    return {
        "per_seed": [rows_by_seed[seed] for seed in fixture.seeds],
        "n_seeds": len(fixture.seeds),
    }


def evaluate_uad_predictions(
    catalog: list[MechanismGroundTruth],
    p1_pool: list[MechanismGroundTruth],
    uad: dict[str, Any],
) -> dict[str, Any]:
    """P1/P2 only (decomposed out of ``machinery_transfer.evaluate_predictions``)."""
    non_communicate = [gt for gt in catalog if not gt.communicate_mediated]
    passive_rates = _mechanism_pass_rates(uad, catalog, "passive")
    intervention_rates = _mechanism_pass_rates(uad, catalog, "intervention")

    comm_fraction, comm_hit_ids, comm_miss_ids = _fraction_mechanisms_majority_hit(
        p1_pool, passive_rates
    )
    non_comm_misses = [
        gt.mechanism_id
        for gt in non_communicate
        if passive_rates.get(gt.mechanism_id, 0.0) < MECHANISM_MAJORITY_SEED_FRACTION
    ]
    p1_holds = (
        comm_fraction >= P1_COMMUNICATE_RECOVERY_FRACTION and len(non_comm_misses) >= 1
    )

    passive_recovered = {
        gt.mechanism_id
        for gt in catalog
        if passive_rates.get(gt.mechanism_id, 0.0) >= MECHANISM_MAJORITY_SEED_FRACTION
    }
    intervention_recovered = {
        gt.mechanism_id
        for gt in catalog
        if intervention_rates.get(gt.mechanism_id, 0.0) >= MECHANISM_MAJORITY_SEED_FRACTION
    }
    strict_superset = passive_recovered <= intervention_recovered and (
        len(intervention_recovered) > len(passive_recovered)
    )
    spurious_pairs = [
        pair for row in uad["per_seed"] for pair in row["spurious_intervention_pairs"]
    ]
    p2_holds = strict_superset and len(spurious_pairs) >= 1

    return {
        "P1": {
            "holds": p1_holds,
            "communicate_majority_hit_fraction": comm_fraction,
            "communicate_majority_hit_ids": comm_hit_ids,
            "communicate_majority_miss_ids": comm_miss_ids,
            "non_communicate_passive_miss_ids": non_comm_misses,
        },
        "P2": {
            "holds": p2_holds,
            "strict_superset": strict_superset,
            "n_spurious_intervention_pairs": len(spurious_pairs),
            "spurious_pairs_sample": spurious_pairs[:10],
        },
    }


def run_rig(
    fixture: ReferenceFixture,
    *,
    substrate_class: str = "S-inherited",
    workers: int = 1,
    progress: bool = True,
) -> RigResult:
    precondition = check_precondition(fixture)
    if not precondition.satisfied:
        return RigResult(
            rig_id=RIG_ID,
            precondition=precondition,
            outcome="skip",
            substrate_class=substrate_class,
            payload={},
            predictions={},
        )

    catalog = c5_ground_truth_catalog(fixture.ecology_data, fixture.roster)
    p1_pool, p1_excluded = p1_communicate_ground_truth_pool(catalog)
    uad = score_uad_from_fixture(fixture, catalog, progress=progress, workers=workers)
    predictions = evaluate_uad_predictions(catalog, p1_pool, uad)
    outcome = "pass" if (predictions["P1"]["holds"] or predictions["P2"]["holds"]) else "null"
    return RigResult(
        rig_id=RIG_ID,
        precondition=precondition,
        outcome=outcome,
        substrate_class=substrate_class,
        payload={
            "ecology_path": str(fixture.ecology_path),
            "n_mechanisms": len(catalog),
            "p1_communicate_pool_size": len(p1_pool),
            "p1_communicate_excluded": p1_excluded,
            "uad": uad,
        },
        predictions=predictions,
    )
