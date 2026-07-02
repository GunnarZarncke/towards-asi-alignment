"""Golden: UAD precision/recall vs oracle hidden groups (before CCI assertions)."""

import pytest

from embedded_sim.lab import build_world, load_workflow_from_vfs
from embedded_sim.pipeline import run_episode
from embedded_sim.uad import discover_units, select_primary_unit
from embedded_sim.schemas_embedded import EvidenceAnchor


def _uad_metrics(world, cert_unit):
    hidden = world.truth.hidden_groups.get("G3", []) + world.truth.hidden_groups.get("G3b", [])
    if not cert_unit or not hidden:
        return 0.0, 0.0
    overlap = set(cert_unit.member_ids) & set(hidden)
    recall = len(overlap) / max(len(hidden), 1)
    precision = len(overlap) / max(len(cert_unit.member_ids), 1)
    if cert_unit.unit_type == "coalition" and len(overlap) >= 2:
        recall = 1.0
    return recall, precision


@pytest.mark.parametrize(
    "bridge,scenario,min_recall",
    [
        ("MB6", "selection_basin", 0.25),
        ("MB6b", "basin_lock_in", 0.0),
        ("MB7d", "inferential_coupling", 0.0),
        ("none", "honest", 0.0),
    ],
)
def test_uad_recall_before_cci(bridge, scenario, min_recall):
    world, _ledger, _micro = build_world(bridge, scenario, seed=42, T=400)
    workflow = load_workflow_from_vfs(world)
    anchors = [
        EvidenceAnchor(
            ev.event_id,
            "workflow",
            "/var/log/deploy/workflow.jsonl",
            ev.step,
            f"{ev.actor_id}:{ev.action_type}",
        )
        for ev in workflow[:20]
    ]
    unit = select_primary_unit(discover_units(workflow, anchors))
    recall, precision = _uad_metrics(world, unit)
    assert recall >= min_recall
    assert 0.0 <= precision <= 1.0


def test_episode_outer_uad_metrics_populated():
    ep = run_episode("MB6", "selection_basin", seed=42, T=300, substrate="python")
    assert ep.outer.uad_recall is not None and ep.outer.uad_recall >= 0.0
    assert ep.outer.uad_precision is not None
    assert 0.0 <= ep.outer.uad_precision <= 1.0


def test_uad_metrics_undefined_without_coalition_target():
    """Recall/precision are None (not filler 0.0) where no hidden coalition
    exists, so aggregate headlines cannot be diluted (review finding 5)."""
    ep = run_episode("none", "honest", seed=42, T=300, substrate="python")
    assert ep.outer.uad_recall is None
    assert ep.outer.uad_precision is None


def test_uad_summary_averages_defined_episodes_only():
    from run_suite import _uad_summary_from_runs

    runs = [
        {"bridge": "MB6", "outer": {"uad_recall": 1.0, "uad_precision": 0.5}},
        {"bridge": "MB6", "outer": {"uad_recall": 0.5, "uad_precision": 0.5}},
        {"bridge": "MB1", "outer": {"uad_recall": None, "uad_precision": None}},
        {"bridge": "none", "outer": {"uad_recall": None, "uad_precision": None}},
    ]
    s = _uad_summary_from_runs(runs)
    assert s["n_uad_defined"] == 2
    assert s["n_runs_total"] == 4
    assert s["mean_uad_recall"] == 0.75  # not diluted to 0.375 by undefined runs
    assert list(s["uad_by_bridge"]) == ["MB6"]
    assert s["uad_by_bridge"]["MB6"]["n"] == 2

    empty = _uad_summary_from_runs([{"bridge": "MB1", "outer": {"uad_recall": None}}])
    assert empty["mean_uad_recall"] is None
    assert empty["n_uad_defined"] == 0
