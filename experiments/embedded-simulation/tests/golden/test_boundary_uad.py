"""UAD boundary-route units from perturbation + capacity signals."""

from embedded_sim.lab import build_world, load_workflow_from_vfs
from embedded_sim.uad import discover_units


def test_mb1_discovers_boundary_route_candidate():
    world, _ledger, _micro = build_world("MB1", "boundary_alias", seed=42, T=400)
    workflow = load_workflow_from_vfs(world)
    units = discover_units(workflow, [])
    boundary = [u for u in units if u.unit_type == "boundary_route"]
    assert boundary, "expected boundary_route candidate from bypass perturbations"
    assert boundary[0].score > 0
    assert boundary[0].member_ids
