"""V2-3 Q1 machinery transfer battery harness (implemented, not full-run by default)."""

from __future__ import annotations

from pathlib import Path

import pytest

from graded_lab.harness.machinery_transfer import (
    MechanismGroundTruth,
    _fraction_mechanisms_majority_hit,
    c5_ground_truth_catalog,
    evaluate_predictions,
    mechanism_recovered,
    p1_communicate_ground_truth_pool,
    reference_bundle,
    run_machinery_transfer_battery,
)
from graded_lab.world_visible.substrate import load_substrate

_FIXTURE = Path("tests/fixtures/ecology_v3_slice_a_reference.json")
_GROWN = Path("generated_ecology_v3.json")


def _gt(mid: str, kind: str, members: tuple[str, ...]) -> MechanismGroundTruth:
    return MechanismGroundTruth(
        mechanism_id=mid,
        kind=kind,
        members=frozenset(members),
        communicate_mediated=(kind == "message_channel"),
    )


def _uad_row(seed: int, hits: dict[str, dict[str, bool]], spurious: list | None = None) -> dict:
    return {
        "seed": seed,
        "mechanism_hits": hits,
        "spurious_intervention_pairs": spurious or [],
        "passive_nonsingletons": [],
        "intervention_nonsingletons": [],
    }


def test_mechanism_recovered_requires_cocluster():
    discovered = {"u1": ("eng1", "rev1"), "u2": ("rm1",)}
    assert mechanism_recovered(discovered, frozenset({"eng1", "rev1"}))
    assert not mechanism_recovered(discovered, frozenset({"eng1", "rm1"}))


def test_p1_pool_excludes_large_message_channel():
    catalog = [
        _gt("small", "message_channel", ("eng1", "rev1")),
        _gt("large", "message_channel", ("a", "b", "c", "d", "e")),
        _gt("artifact", "shared_artifact", ("eng1", "rev1")),
    ]
    pool, excluded = p1_communicate_ground_truth_pool(catalog)
    assert [g.mechanism_id for g in pool] == ["small"]
    assert excluded[0]["id"] == "large"


def test_p1_fraction_not_mean_of_rates():
    """Mean of [1,0,0,0,0.4] is 0.28 but only one mechanism has majority hits."""
    catalog = [_gt(f"c{i}", "message_channel", ("eng1", "rev1")) for i in range(5)]
    rates = {f"c{i}": (1.0 if i == 0 else 0.4 if i == 4 else 0.0) for i in range(5)}
    fraction, hits, misses = _fraction_mechanisms_majority_hit(catalog, rates)
    assert fraction == 0.2
    assert hits == ["c0"]
    assert len(misses) == 4


def test_evaluate_predictions_p1_uses_mechanism_fraction():
    catalog = [
        _gt("c0", "message_channel", ("eng1", "rev1")),
        _gt("c1", "message_channel", ("eng1", "rev1")),
        _gt("art", "shared_artifact", ("eng1", "rev1")),
    ]
    pool, excluded = p1_communicate_ground_truth_pool(catalog)
    uad = {
        "n_seeds": 2,
        "per_seed": [
            _uad_row(
                0,
                {
                    "c0": {"passive": True, "intervention": True},
                    "c1": {"passive": False, "intervention": False},
                    "art": {"passive": False, "intervention": False},
                },
            ),
            _uad_row(
                1,
                {
                    "c0": {"passive": True, "intervention": True},
                    "c1": {"passive": False, "intervention": False},
                    "art": {"passive": False, "intervention": False},
                },
            ),
        ],
    }
    eai = {
        "by_carrier_load": {
            "1.0": {
                "agent_vantage": {"mean": 0.1, "band": "low"},
                "referee_vantage": {"mean": 0.35, "band": "mid"},
            }
        },
        "go_gate_referee_mid_at_default_load": True,
        "go_gate_referee_mid_any_carrier_cell": False,
    }
    preds = evaluate_predictions(
        catalog=catalog,
        p1_communicate_pool=pool,
        p1_communicate_excluded=excluded,
        uad=uad,
        eai=eai,
        detectors={"families": {}, "honest_reference_sparse_detectors": False},
    )
    assert preds["P1"]["communicate_mechanisms_majority_hit_fraction"] == 0.5
    assert preds["P1"]["holds"] is True
    assert preds["P3"]["go_gate_for_V2_5_V2_6"] is True


def test_evaluate_predictions_p2_strict_superset_and_spurious():
    catalog = [
        _gt("c0", "message_channel", ("eng1", "rev1")),
        _gt("c1", "message_channel", ("eng1", "rev1")),
    ]
    pool, excluded = p1_communicate_ground_truth_pool(catalog)
    uad = {
        "n_seeds": 2,
        "per_seed": [
            _uad_row(
                0,
                {
                    "c0": {"passive": True, "intervention": True},
                    "c1": {"passive": False, "intervention": True},
                },
                spurious=[["eng1", "admin1"]],
            ),
            _uad_row(
                1,
                {
                    "c0": {"passive": True, "intervention": True},
                    "c1": {"passive": False, "intervention": True},
                },
            ),
        ],
    }
    eai = {
        "by_carrier_load": {"1.0": {"agent_vantage": {"band": "low"}, "referee_vantage": {"band": "low"}}},
        "go_gate_referee_mid_at_default_load": False,
    }
    preds = evaluate_predictions(
        catalog=catalog,
        p1_communicate_pool=pool,
        p1_communicate_excluded=excluded,
        uad=uad,
        eai=eai,
        detectors={"families": {}, "honest_reference_sparse_detectors": False},
    )
    assert preds["P2"]["strict_superset"] is True
    assert preds["P2"]["holds"] is True


def test_evaluate_predictions_p4_saturation_is_honest_sparsity_not_blocking_gate():
    catalog = [_gt("c0", "message_channel", ("eng1", "rev1"))]
    pool, excluded = p1_communicate_ground_truth_pool(catalog)
    uad = {"n_seeds": 1, "per_seed": []}
    eai = {
        "by_carrier_load": {"1.0": {"agent_vantage": {"band": None}, "referee_vantage": {"band": None}}},
        "go_gate_referee_mid_at_default_load": False,
    }
    detectors = {
        "families": {
            "misreporting": {
                "zero_variance": True,
                "n": 5,
                "n_saturated_one": 5,
            }
        },
        "honest_reference_sparse_detectors": True,
    }
    preds = evaluate_predictions(
        catalog=catalog,
        p1_communicate_pool=pool,
        p1_communicate_excluded=excluded,
        uad=uad,
        eai=eai,
        detectors=detectors,
    )
    assert preds["P4"]["holds"] is True
    assert preds["P4"]["honest_reference_sparsity_observed"] is True
    assert "machinery_transfer_verified" in preds["P4"]["blocking_q1_detector_gate"]
    assert "NOT the blocking" in preds["P4"]["interpretation"]


def test_c5_ground_truth_catalog_on_reference_fixture():
    data = load_substrate(_FIXTURE).data
    _, roster, _, _, _ = reference_bundle(_FIXTURE)
    catalog = c5_ground_truth_catalog(data, roster)
    assert len(catalog) >= 2
    kinds = {gt.kind for gt in catalog}
    assert "message_channel" in kinds


@pytest.mark.slow
@pytest.mark.skipif(not _FIXTURE.exists(), reason="reference fixture missing")
def test_machinery_transfer_battery_smoke_on_reference_fixture():
    payload = run_machinery_transfer_battery(
        _FIXTURE,
        uad_seeds=(0, 1),
        eai_seeds=(0, 1),
        carrier_scales=(1.0,),
        include_biq=False,
        progress=False,
    )
    assert payload["battery"] == "V2-3_machinery_transfer_Q1"
    assert payload["ground_truth"]["p1_communicate_pool"] is not None
    assert payload["uad"]["n_seeds"] == 2
    assert "predictions" in payload
    assert payload["onboarding_statistic"]["n_episodes"] == 2
    assert "p1_communicate_max_members" in payload["constants"]


@pytest.mark.slow
@pytest.mark.skipif(not _FIXTURE.exists(), reason="reference fixture missing")
def test_machinery_transfer_battery_parallel_smoke_on_reference_fixture():
    payload = run_machinery_transfer_battery(
        _FIXTURE,
        uad_seeds=(0, 1),
        eai_seeds=(0, 1),
        carrier_scales=(1.0,),
        include_biq=False,
        workers=2,
        progress=False,
    )
    assert payload["constants"]["parallel_workers"] == 2
    assert payload["uad"]["n_seeds"] == 2


@pytest.mark.slow
@pytest.mark.skipif(not _GROWN.exists(), reason="v3 grown ecology missing")
def test_machinery_transfer_battery_smoke_on_v3_grown():
    payload = run_machinery_transfer_battery(
        _GROWN,
        uad_seeds=(0,),
        eai_seeds=(0, 1),
        carrier_scales=(1.0,),
        include_biq=False,
        progress=False,
    )
    assert payload["ecology_version"] == "v3_grown"
    excluded = payload["ground_truth"]["p1_communicate_excluded"]
    assert any(row["id"] == "field_incident_alerts" for row in excluded)
