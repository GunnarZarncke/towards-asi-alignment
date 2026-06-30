"""Configurable lab ecology for UAD stress tests."""

from embedded_sim.lab import _actor_fleet, build_world, load_workflow_from_vfs
from embedded_sim.lab_ecology import LabEcologyConfig, set_lab_ecology


def teardown_function():
    set_lab_ecology()


def _ids(config: LabEcologyConfig) -> set[str]:
    set_lab_ecology(config)
    return {actor.actor_id for actor in _actor_fleet(seed=42, bridge="MB6")}


def test_adversarial_candidates_enabled_separately():
    ids = _ids(LabEcologyConfig(n_adversarial_candidates=3))
    assert {"actor.adv.0", "actor.adv.1", "actor.adv.2"} <= ids
    assert "audit.process" not in ids
    assert "actor.principal.humans" not in ids


def test_common_legitimate_lab_agents_enabled_separately():
    ids = _ids(LabEcologyConfig(common_legitimate_lab_agents=True))
    assert {
        "actor.lab.release_manager",
        "actor.lab.evaluation_reviewer",
        "actor.lab.incident_responder",
        "actor.lab.monitoring_service",
    } <= ids
    assert not any(actor_id.startswith("actor.decoy.") for actor_id in ids)


def test_auditor_and_alignment_target_enabled_separately():
    assert "audit.process" in _ids(LabEcologyConfig(auditor_agent=True))
    assert "actor.principal.humans" in _ids(LabEcologyConfig(alignment_target_agent=True))


def test_decoys_enabled_separately():
    ids = _ids(LabEcologyConfig(n_decoys=2))
    assert {"actor.decoy.0", "actor.decoy.1"} <= ids
    assert not any(actor_id.startswith("actor.adv.") for actor_id in ids)


def test_enriched_ecology_visible_but_hidden_groups_remain_oracle_only():
    set_lab_ecology(
        LabEcologyConfig(
            n_adversarial_candidates=2,
            common_legitimate_lab_agents=True,
            auditor_agent=True,
            alignment_target_agent=True,
            n_decoys=2,
        )
    )
    world, _ledger, _micro = build_world("MB6", "selection_basin", seed=42, T=200)
    workflow = load_workflow_from_vfs(world)
    actors = {ev.actor_id for ev in workflow}
    assert "audit.process" in actors
    assert "actor.principal.humans" in actors
    assert any(actor_id.startswith("actor.decoy.") for actor_id in actors)
    raw = world.vfs.read("/var/log/deploy/workflow.jsonl") or ""
    assert "hidden_group" not in raw

