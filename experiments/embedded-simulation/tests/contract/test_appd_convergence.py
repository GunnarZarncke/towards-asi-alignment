"""Contract: AppD roadmap items 2–6 (handle registry through safety case)."""

import json

from embedded_sim.bearer_trace import BEARER_ROW_FIELDS, BEARER_TRACE_PATH
from embedded_sim.embedded_audit import run_embedded_audit
from embedded_sim.handle_registry import HANDLE_REGISTRY, REGISTRY_PATH, load_handle_registry
from embedded_sim.lab import build_world, load_episode_rows_from_vfs
from embedded_sim.pipeline import run_episode
from embedded_sim.safety_case import SAFETY_CASE_PATH, TRACE_SOURCES
from embedded_sim.world import write_episode_logs


def test_handle_registry_on_vfs():
    world, _l, _m = build_world("none", "honest", seed=42, T=200)
    registry = load_handle_registry(world.vfs)
    assert registry
    assert set(registry) == {spec.handle_id for spec in HANDLE_REGISTRY}
    for spec in HANDLE_REGISTRY:
        entry = registry[spec.handle_id]
        assert entry["owner"]
        assert entry["operation"]
        assert entry["latency_bound_ms"] > 0
        assert entry["evasion_story"]
        assert entry["anchor_path"]


def test_workflow_events_carry_handle_invoked():
    world, _l, _m = build_world("none", "honest", seed=42, T=200)
    raw = world.vfs.read("/var/log/deploy/workflow.jsonl") or ""
    rows = [json.loads(ln) for ln in raw.splitlines() if ln.strip()]
    assert rows
    for row in rows:
        assert "release_ticket_id" in row
        assert "handle_invoked" in row
        assert "approval_state" in row
        assert "latency_ms" in row


def test_bearer_trace_written_with_appd_fields():
    world, _l, _m = build_world("none", "honest", seed=42, T=400)
    raw = world.vfs.read(BEARER_TRACE_PATH) or ""
    rows = [json.loads(ln) for ln in raw.splitlines() if ln.strip()]
    assert rows, "honest episode should emit bearer-impact rows"
    for row in rows:
        missing = [f for f in BEARER_ROW_FIELDS if f not in row]
        assert not missing, missing


def test_safety_case_emitted_with_nine_fields():
    world, _l, _m = build_world("none", "honest", seed=42, T=300)
    cert, *_ = run_embedded_audit(world, instrumentation="medium_handles")
    raw = world.vfs.read(SAFETY_CASE_PATH)
    assert raw
    case = json.loads(raw)
    for key in (
        "system_boundary",
        "trace_sources",
        "handle_registry",
        "value_bearer_grounding",
        "correction_latency_bound",
        "successor_gate",
        "adversarial_audit",
        "bridge_status",
        "decision",
    ):
        assert key in case, key
    assert case["handle_registry"] == REGISTRY_PATH
    assert set(case["trace_sources"]) == set(TRACE_SOURCES)
    assert cert.safety_case_path == SAFETY_CASE_PATH
    assert cert.numeric_risk is not None
    assert cert.tempo_check is not None


def test_numeric_leaf_satisfies_on_honest():
    ep = run_episode("none", "honest", seed=42, T=400, substrate="python")
    nr = ep.in_sim.numeric_risk
    assert nr is not None
    assert nr["satisfies"] is True
    assert ep.in_sim.safety_decision == "pass"


def test_successor_reaudit_on_honest_successor():
    ep = run_episode("none", "honest_successor", seed=42, T=400, substrate="python")
    reaudit = ep.in_sim.successor_reaudit
    assert reaudit is not None
    assert reaudit["applicable"] is True
    assert reaudit["cci_preserved"] is True
    assert reaudit["control_non_increasing"] is True


def test_tempo_flags_capture_theater_more_than_honest():
    honest = run_episode("none", "honest", seed=42, T=400, substrate="python")
    capture = run_episode("MB4", "capture_theater", seed=42, T=400, substrate="python")
    assert honest.in_sim.tempo_check is not None
    assert capture.in_sim.tempo_check is not None
    assert (
        capture.in_sim.tempo_check["worst_ratio"]
        >= honest.in_sim.tempo_check["worst_ratio"]
    )


def test_rewrite_logs_preserves_appd_artifacts():
    world, _l, _m = build_world("none", "honest", seed=7, T=150)
    write_episode_logs(world)
    assert load_handle_registry(world.vfs)
    assert world.vfs.read(BEARER_TRACE_PATH) is not None
