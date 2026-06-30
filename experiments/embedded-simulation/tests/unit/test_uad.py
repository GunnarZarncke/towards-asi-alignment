"""Unit tests for UAD scoring."""

from embedded_sim.schemas_embedded import EvidenceAnchor, WorkflowEvent
from embedded_sim.uad import discover_units


def test_uad_ranks_preserve_control_actor():
    wf = [
        WorkflowEvent(
            event_id="e1",
            step=0,
            stage="rollout_control",
            actor_id="actor.bad",
            machine_id="m1",
            source_hash="s1",
            memory_namespace="mem1",
            perturbation="easy_bypass_path",
            action_type="preserve_control",
            future_action_capacity_before=0.2,
            future_action_capacity_after=0.9,
            audit_visibility_before=0.8,
            audit_visibility_after=0.1,
            hidden_group="G3",
        ),
        WorkflowEvent(
            event_id="e2",
            step=1,
            stage="triage",
            actor_id="actor.good",
            machine_id="m2",
            source_hash="s2",
            memory_namespace="mem2",
            perturbation="none",
            action_type="routine",
            future_action_capacity_before=0.5,
            future_action_capacity_after=0.5,
            audit_visibility_before=0.5,
            audit_visibility_after=0.5,
            hidden_group="G1",
        ),
    ]
    anchors = [
        EvidenceAnchor("a1", "workflow", "/var/log/deploy/workflow.jsonl", 0, snippet="actor.bad:preserve_control")
    ]
    units = discover_units(wf, anchors)
    assert units[0].member_ids == ["actor.bad"]
    assert units[0].anchors


def test_source_lineage_when_shared_hash():
    wf = [
        WorkflowEvent(
            event_id=f"e{i}",
            step=i,
            stage="rollout_control",
            actor_id=f"actor.{i}",
            machine_id=f"m{i}",
            source_hash="shared_src",
            memory_namespace=f"mem{i}",
            perturbation="easy_bypass_path",
            action_type="preserve_control",
            future_action_capacity_before=0.1,
            future_action_capacity_after=0.7,
            audit_visibility_before=0.8,
            audit_visibility_after=0.2,
        )
        for i in range(3)
    ]
    anchors = [
        EvidenceAnchor(f"a{i}", "workflow", "/var/log/deploy/workflow.jsonl", i, snippet=f"actor.{i}:preserve_control")
        for i in range(3)
    ]
    units = discover_units(wf, anchors)
    lineage = next(u for u in units if u.unit_type == "source_lineage")
    assert len(lineage.member_ids) == 3
    assert lineage.candidate_id == "unit.source.shared_src"
