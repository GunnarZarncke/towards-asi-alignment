"""Contract: embedded audit path is artifact-driven, not scenario/bridge labeled."""

from pathlib import Path

from embedded_sim.deploy_gate import SUCCESSOR_CANDIDATE_PATH, successor_gate_applicable
from embedded_sim.lab import build_world, rebuild_audit_inputs
from embedded_sim.world import VirtualFS

AUDIT_PATH = Path(__file__).resolve().parents[2] / "embedded_sim"


def test_embedded_audit_path_has_no_scenario_or_bridge_branches():
    for name in ("embedded_audit.py", "deploy_gate.py"):
        src = (AUDIT_PATH / name).read_text(encoding="utf-8")
        assert "world.bridge" not in src, name
        assert "world.scenario" not in src, name


def test_rebuild_audit_inputs_uses_public_manifest_label():
    world, _ledger, _micro = build_world("MB6", "selection_basin", seed=42, T=100)
    _rows, audit, _lineage = rebuild_audit_inputs(world)
    assert audit.scenario == "deployment_lab"
    assert audit.scenario != world.scenario


def test_successor_gate_applicable_from_candidate_artifact_only():
    vfs = VirtualFS()
    assert not successor_gate_applicable(vfs)
    vfs.write(SUCCESSOR_CANDIDATE_PATH, "// candidate\n")
    assert successor_gate_applicable(vfs)


def test_non_successor_world_has_no_gate_candidate():
    world, _ledger, _micro = build_world("none", "honest", seed=42, T=100)
    assert not successor_gate_applicable(world.vfs)
