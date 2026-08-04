"""PLAN_v3 slice C: principal scorecard + C1-v3 measured tension."""

from __future__ import annotations

from pathlib import Path

import pytest

from graded_lab.harness.ecology_complexity import run_reference_episodes
from graded_lab.oracle_only.calibration import WEAK_AGENT
from graded_lab.oracle_only.principal_scorecard import (
    C1_V3_MAX_CORRELATION,
    check_c1_v3,
    extract_episode_metrics,
    resolve_objective_metric,
    scorecard_for_episode,
    validate_v3_conflicts,
    validate_v3_principals,
)
from graded_lab.world_visible.config import EpisodeConfig
from graded_lab.world_visible.ecology_agents import (
    programs_and_profiles_for_roster,
    reference_roster_from_ecology,
)
from graded_lab.world_visible.substrate import load_substrate
from graded_lab.world_visible.world import EpisodeResult, default_lab_config, run_episode

_FIXTURE = Path("tests/fixtures/ecology_v3_slice_a_reference.json")


class _OracleStub:
    def __init__(self, *, t: int = 160, bearer_harm: float = 0.0) -> None:
        self.t = t
        self.bearer_harm = bearer_harm
        self.incident_samples: list[float] = []


def _episode(
    seed: int,
    *,
    deploy_count: int = 0,
    bearer_harm: float = 0.0,
    compute: float = 100.0,
    t: int = 160,
) -> EpisodeResult:
    return EpisodeResult(
        seed=seed,
        deployed=deploy_count > 0,
        deploy_count=deploy_count,
        bearer_harm=bearer_harm,
        eai=0.0,
        oracle=_OracleStub(t=t, bearer_harm=bearer_harm),
        resource_totals={"eng1": {"compute": compute}},
    )


_CONFLICT_ECOLOGY = {
    "principals": [
        {
            "id": "throughput_principal",
            "description": "wants deploy throughput",
            "objective_metric": "deploy_rate",
            "objective_direction": "increase",
        },
        {
            "id": "safety_principal",
            "description": "wants low field harm",
            "objective_metric": "field_incident_rate",
            "objective_direction": "decrease",
        },
    ],
    "conflicts": [
        {
            "principals": ["throughput_principal", "safety_principal"],
            "shared_metric": "field_incident_rate",
            "justification": (
                "Higher deploy throughput on the throughput principal's timeline "
                "compresses eval coverage and raises field incident exposure."
            ),
        }
    ],
}


def test_resolve_objective_metric_accepts_legacy_aliases():
    assert resolve_objective_metric("release_rate") == "deploy_rate"
    assert resolve_objective_metric("operating_burn_rate") == "compute_burn"


def test_validate_v3_principals_rejects_unknown_metric():
    with pytest.raises(Exception, match="unknown objective_metric"):
        validate_v3_principals(
            [{"id": "p1", "objective_metric": "made_up", "objective_direction": "increase"}]
        )


def test_extract_episode_metrics_oriented_scores():
    result = _episode(0, deploy_count=2, bearer_harm=0.4, compute=320.0, t=160)
    metrics = extract_episode_metrics(result)
    assert metrics["deploy_rate"] == pytest.approx(2 / 160)
    assert metrics["compute_burn"] == pytest.approx(2.0)


def test_c1_v3_passes_hand_built_opposing_series():
    results = [
        _episode(i, deploy_count=i, bearer_harm=i * 0.01, compute=100 + i * 5)
        for i in range(1, 9)
    ]
    passed, details = check_c1_v3(_CONFLICT_ECOLOGY, results)
    assert passed, details
    conflict = details["conflicts"][0]
    assert conflict["status"] == "pass"
    assert conflict["correlation"] <= C1_V3_MAX_CORRELATION


def test_c1_v3_reports_not_exercised_when_metrics_flat():
    flat = [_episode(i, deploy_count=0, bearer_harm=0.0) for i in range(8)]
    passed, details = check_c1_v3(_CONFLICT_ECOLOGY, flat)
    assert not passed
    assert details["conflicts"][0]["status"] == "not_exercised"


def _integrated_fixture_short_horizon_cfg(*, T: int) -> EpisodeConfig:
    """Deliberately sub-freeze horizon — not ``run_reference_episodes``."""
    base = default_lab_config()
    data = load_substrate(_FIXTURE).data
    roster = reference_roster_from_ecology(data, agent_type=WEAK_AGENT, temperature=0.35)
    return EpisodeConfig(
        agents=roster.agents,
        T=T,
        pipeline_spec=base.pipeline_spec,
        substrate_settings=base.substrate_settings,
        carrier_termination_mode=base.carrier_termination_mode,
        units=base.units,
        ecology_version="v3",
        ecology_override_path=_FIXTURE,
        record_contention=True,
    )


@pytest.mark.skipif(not _FIXTURE.exists(), reason="slice A reference fixture missing")
def test_c1_v3_not_exercised_when_episode_horizon_too_short():
    """Regression for GL-50/GL-53: T=100 leaves principal metrics flat.

    This is **not** the frozen reference checker (which uses
    ``V3_REFERENCE_T=200``). It documents why the old test name
    ``test_reference_battery_reports_c1_v3_not_exercised`` was removed
    after GL-50 — that failure mode is horizon/config, not scorecard logic.
    """
    from graded_lab.harness.ecology_complexity import V3_REFERENCE_T
    from graded_lab.harness.isolate import MockIsolate

    data = load_substrate(_FIXTURE).data
    cfg = _integrated_fixture_short_horizon_cfg(T=100)
    assert cfg.T < V3_REFERENCE_T
    roster = reference_roster_from_ecology(data, agent_type=WEAK_AGENT, temperature=0.35)
    programs, profiles = programs_and_profiles_for_roster(roster, ecology_data=data)
    backend = MockIsolate()
    results = [
        run_episode(cfg, seed, backend, programs=programs, behavior_profiles=profiles)
        for seed in range(5)
    ]
    passed, details = check_c1_v3(data, results)
    assert not passed
    assert any(c.get("status") == "not_exercised" for c in details["conflicts"])


@pytest.mark.slow
@pytest.mark.skipif(not _FIXTURE.exists(), reason="slice A reference fixture missing")
def test_reference_battery_passes_c1_v3_at_frozen_horizon():
    """Slice D freeze: v3 reference battery at T=200, n=20 (GL-53)."""
    from graded_lab.harness.ecology_complexity import V3_REFERENCE_T, _reference_episode_config

    data = load_substrate(_FIXTURE).data
    cfg = _reference_episode_config(data, ecology_path=_FIXTURE)
    assert cfg.T == V3_REFERENCE_T
    results = run_reference_episodes(_FIXTURE, seeds=tuple(range(20)), progress=False)
    passed, details = check_c1_v3(data, results)
    assert passed, details
    assert all(c.get("status") == "pass" for c in details["conflicts"])


@pytest.mark.skipif(not _FIXTURE.exists(), reason="slice A reference fixture missing")
def test_v3_episode_attaches_principal_scorecard_referee_artifact():
    from graded_lab.oracle_only.calibration import WEAK_AGENT
    from graded_lab.harness.isolate import MockIsolate
    from graded_lab.harness.ecology_complexity import _reference_episode_config
    from graded_lab.world_visible.ecology_agents import (
        programs_and_profiles_for_roster,
        reference_roster_from_ecology,
    )
    from graded_lab.world_visible.world import run_episode

    data = load_substrate(_FIXTURE).data
    cfg = _reference_episode_config(data, ecology_path=_FIXTURE)
    roster = reference_roster_from_ecology(data, agent_type=WEAK_AGENT, temperature=0.35)
    programs, profiles = programs_and_profiles_for_roster(roster, ecology_data=data)
    result = run_episode(cfg, 0, MockIsolate(), programs=programs, behavior_profiles=profiles)
    card = result.referee_artifacts.get("principal_scorecard")
    assert card is not None
    assert len(card["principals"]) == len(data["principals"])
    assert "principal_scorecard" not in str(result.boundary_streams)


def test_validate_v3_conflicts_requires_known_shared_metric():
    validate_v3_conflicts(
        _CONFLICT_ECOLOGY["conflicts"],
        principal_ids={"throughput_principal", "safety_principal"},
    )
    with pytest.raises(Exception, match="unknown objective_metric"):
        validate_v3_conflicts(
            [{"principals": ["throughput_principal", "safety_principal"], "shared_metric": "bogus"}],
            principal_ids={"throughput_principal", "safety_principal"},
        )


def test_scorecard_for_episode_lists_oriented_principal_entries():
    result = _episode(1, deploy_count=1, bearer_harm=0.2)
    card = scorecard_for_episode(_CONFLICT_ECOLOGY, result)
    by_id = {entry["principal_id"]: entry for entry in card["principals"]}
    assert by_id["throughput_principal"]["oriented_score"] > 0
    assert by_id["safety_principal"]["oriented_score"] < 0
