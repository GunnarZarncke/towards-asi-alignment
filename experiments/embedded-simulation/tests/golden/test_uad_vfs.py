"""Golden: UAD reads workflow from VFS only (no hidden_group in artifact)."""

from embedded_sim.lab import build_world, load_workflow_from_vfs
from embedded_sim.uad import discover_units
from embedded_sim.schemas_embedded import EvidenceAnchor


def test_workflow_vfs_omits_hidden_group():
    world, _ledger, _micro = build_world("MB6", "selection_basin", seed=42, T=200)
    raw = world.vfs.read("/var/log/deploy/workflow.jsonl") or ""
    assert "hidden_group" not in raw
    workflow = load_workflow_from_vfs(world)
    assert len(workflow) > 0
    assert all(ev.hidden_group == "G1" for ev in workflow)


def test_uad_finds_preserve_control_from_vfs_workflow():
    world, _ledger, _micro = build_world("MB6", "selection_basin", seed=42, T=300)
    workflow = load_workflow_from_vfs(world)
    preserve = [ev for ev in workflow if ev.action_type == "preserve_control"]
    assert len(preserve) >= 4
    anchors = [
        EvidenceAnchor(
            f"{ev.event_id}",
            "workflow",
            "/var/log/deploy/workflow.jsonl",
            ev.step,
            f"{ev.actor_id}:{ev.action_type}",
        )
        for ev in preserve[:5]
    ]
    units = discover_units(workflow, anchors)
    assert units[0].score > 0
    coal = next((u for u in units if u.unit_type == "coalition"), None)
    assert coal is not None or any(ev.action_type == "preserve_control" for ev in workflow)
