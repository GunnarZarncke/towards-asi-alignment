"""Unit tests for grounded handle inference."""

from embedded_sim.handles import infer_handles
from embedded_sim.schemas_embedded import EvidenceAnchor, WorkflowEvent


def test_infer_handles_from_probe_rows():
    rows = [
        {
            "step": 10,
            "intervention_active": 1,
            "intervention_intent": 1,
            "visible_action": 1,
            "correction_request": 1,
            "reported_acceptance": 0.8,
            "bearer_welfare_delta": -0.1,
            "correction_lineage_tick": 2,
        }
    ]
    wf = [
        WorkflowEvent(
            event_id="e1",
            step=10,
            stage="rollout_control",
            actor_id="actor.a",
            machine_id="m1",
            source_hash="s1",
            memory_namespace="mem.a",
            perturbation="none",
            action_type="preserve_control",
            future_action_capacity_before=0.2,
            future_action_capacity_after=0.8,
            audit_visibility_before=0.7,
            audit_visibility_after=0.2,
        )
    ]
    anchors = [EvidenceAnchor("a1", "file", "/var/log/deploy/correction.jsonl", 1, snippet="{")]
    handles = infer_handles(rows, wf, anchors)
    roles = {h.role for h in handles}
    assert "correction" in roles
    assert "bearer_welfare" in roles
    assert all(h.anchors for h in handles)
