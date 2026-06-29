#!/usr/bin/env python3
"""Contract tests for Phase 2 deployment API."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from llm_redteam.api import (
    InvalidStepPatchError,
    StepPatch,
    apply_deployment_agent,
    build_source_index,
    iter_public_observations,
    public_obs_from_row,
)
from llm_redteam.deployment_agents import DEPLOYMENT_AGENTS
from llm_redteam.episode_runner import audit_outcome_key, run_batch_episode, run_deployment_episode
from llm_redteam.strategies import STRATEGIES

SCENARIOS = (
    "capture_theater",
    "grounding_silent_gap",
    "boundary_alias",
    "hidden_capability",
    "selection_basin",
)


def test_step_patch_rejects_invalid_keys() -> None:
    try:
        StepPatch(fields={"true_action": 1})
        raise AssertionError("expected InvalidStepPatchError")
    except InvalidStepPatchError:
        pass


def test_public_observation_excludes_oracle_fields() -> None:
    row = {
        "step": 0,
        "correction_request": 1,
        "reported_acceptance": 0,
        "visible_action": 1,
        "intervention_active": 0,
        "intervention_intent": 0,
        "action_cause_code": 0,
        "bearer_welfare_delta": 0.0,
        "correction_lineage_tick": 0,
        "display_bearer": 0.5,
        "true_action": 99,
        "silent_harm": True,
    }
    obs = public_obs_from_row(row, passive_bearer_ema=0.5, passive_basin_ema=0.5)
    assert not hasattr(obs, "true_action")
    assert not hasattr(obs, "silent_harm")


def test_all_deployment_agents_satisfy_protocol() -> None:
    source_index = build_source_index()
    sample_row = {
        "step": 0,
        "correction_request": 1,
        "reported_acceptance": 0,
        "visible_action": 1,
        "intervention_active": 1,
        "intervention_intent": 2,
        "action_cause_code": 1,
        "bearer_welfare_delta": -0.1,
        "correction_lineage_tick": 3,
        "display_bearer": 0.4,
        "basin_pressure": 0.2,
    }
    obs_list = iter_public_observations([sample_row])
    for name, agent in DEPLOYMENT_AGENTS.items():
        patch = agent.patch_step(0, obs_list[0], source_index)
        assert isinstance(patch, StepPatch), name
        assert set(patch.fields.keys()) <= set(
            __import__(
                "llm_redteam.protocol", fromlist=["DEPLOYMENT_MUTABLE_FIELDS"]
            ).DEPLOYMENT_MUTABLE_FIELDS
        ), name


def test_batch_vs_deployment_api_equivalence() -> None:
    """All strategies should match batch runner on patched meta and audit outcomes."""
    seed = 11
    T = 500
    mismatches: list[str] = []
    for name in STRATEGIES:
        for scenario in ("capture_theater", "grounding_silent_gap", "capture_mild"):
            batch = run_batch_episode(scenario, seed, T, STRATEGIES[name])  # type: ignore[arg-type]
            deploy = run_deployment_episode(scenario, seed, T, DEPLOYMENT_AGENTS[name])
            if audit_outcome_key(batch) != audit_outcome_key(deploy):
                mismatches.append(
                    f"{name}/{scenario}: batch={audit_outcome_key(batch)} "
                    f"deploy={audit_outcome_key(deploy)}"
                )
    if mismatches:
        raise AssertionError("batch vs deployment mismatch: " + "; ".join(mismatches))


def test_deployment_episode_runs_all_agents() -> None:
    for name, agent in DEPLOYMENT_AGENTS.items():
        for scenario in SCENARIOS:
            result = run_deployment_episode(scenario, 11, 300, agent)
            assert result["strategy"] == name
            assert result["runner"] == "deployment_api"
            assert result["cci_status"] in ("passes", "belowThreshold", "capturedInvalid")


def test_apply_deployment_agent_matches_runner() -> None:
    from multiresolution_alignment_sim.simulator import simulate

    micro, ledger, episode_meta = simulate("capture_mild", 12, T=100)
    del micro, ledger
    agent = DEPLOYMENT_AGENTS["theater_inflate"]
    patched = apply_deployment_agent(episode_meta, agent)
    assert any(
        r["correction_request"] and r["reported_acceptance"] == 1 for r in patched
    )


def main() -> None:
    test_step_patch_rejects_invalid_keys()
    test_public_observation_excludes_oracle_fields()
    test_all_deployment_agents_satisfy_protocol()
    test_batch_vs_deployment_api_equivalence()
    test_deployment_episode_runs_all_agents()
    test_apply_deployment_agent_matches_runner()
    print("smoke_api_contract: OK")
    print(f"  deployment_agents={list(DEPLOYMENT_AGENTS.keys())}")
    print(f"  source_modules={len(build_source_index().modules)}")


if __name__ == "__main__":
    main()
