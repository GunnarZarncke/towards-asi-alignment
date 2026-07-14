"""Contract: writer-compromise red team + cross-stream consistency checks."""

import json

import pytest

from embedded_sim.cross_stream import verify_cross_stream
from embedded_sim.embedded_audit import run_embedded_audit
from embedded_sim.lab import build_world
from embedded_sim.redteam import run_redteam
from embedded_sim.trace_integrity import (
    get_trace_integrity_mode,
    set_trace_integrity_mode,
    verify_chain,
)


@pytest.fixture
def integrity_mode_guard():
    prev = get_trace_integrity_mode()
    yield
    set_trace_integrity_mode(prev)


def test_honest_world_cross_stream_clean():
    world, _l, _m = build_world("none", "honest", seed=42, T=400)
    cert, *_ = run_embedded_audit(world, "medium_handles", substrate="python")
    assert cert.safety_decision == "pass"
    assert not any("cross-stream" in n for n in cert.notes)


def test_capture_theater_honest_emission_cross_stream_clean():
    world, _l, _m = build_world("MB4", "capture_theater", seed=42, T=400)
    cert, *_ = run_embedded_audit(world, "medium_handles", substrate="python")
    assert not any("cross-stream" in n for n in cert.notes)


def test_writer_compromise_caught_with_valid_chain(integrity_mode_guard):
    """Sloppy emitter: chain verifies, schema recomputes, cross-stream fails."""
    world, _l, _m = build_world("MB4", "capture_theater", seed=42, T=400)
    run_redteam(world, "writer_compromise", substrate="python")
    manifest = json.loads(world.vfs.read("/etc/attest/manifest.json"))
    for name in ("correction", "workflow", "bearers"):
        anchor = manifest["trace_anchors"][name]
        raw = world.vfs.read(anchor["path"])
        ok, reason = verify_chain(raw, anchor)
        assert ok, f"{name}: {reason}"
    cert, *_ = run_embedded_audit(world, "medium_handles", substrate="python")
    assert cert.safety_decision == "invalid_certificate"
    assert any("cross-stream" in n for n in cert.notes)


def test_consistent_forge_caught_by_cross_stream_unsigned(integrity_mode_guard):
    """Post-write forger with schema recompute still leaves bearers stale."""
    set_trace_integrity_mode("none")
    world, _l, _m = build_world("MB4", "capture_theater", seed=42, T=400)
    run_redteam(world, "consistent_forge", substrate="python")
    cert, *_ = run_embedded_audit(world, "medium_handles", substrate="python")
    assert cert.safety_decision == "invalid_certificate"
    assert any("cross-stream" in n for n in cert.notes)


def test_unsigned_coordinated_writer_compromise_residual_pass(integrity_mode_guard):
    """Coordinated emitter: all streams aligned — residual ES-4 surface."""
    set_trace_integrity_mode("none")
    world, _l, _m = build_world("MB4", "capture_theater", seed=42, T=400)
    run_redteam(world, "writer_compromise_coordinated", substrate="python")
    cert, *_ = run_embedded_audit(world, "medium_handles", substrate="python")
    assert cert.safety_decision == "pass"
    assert not any("cross-stream" in n for n in cert.notes)
    assert not any("correction schema" in n for n in cert.notes)


def test_coordinated_writer_compromise_signed_chain_valid(integrity_mode_guard):
    """Signed lies: chain ok, cross-stream ok, in-sim may still pass (false pass)."""
    world, _l, _m = build_world("MB4", "capture_theater", seed=42, T=400)
    run_redteam(world, "writer_compromise_coordinated", substrate="python")
    manifest = json.loads(world.vfs.read("/etc/attest/manifest.json"))
    anchor = manifest["trace_anchors"]["correction"]
    ok, reason = verify_chain(world.vfs.read(anchor["path"]), anchor)
    assert ok, reason
    cert, *_ = run_embedded_audit(world, "medium_handles", substrate="python")
    assert cert.safety_decision == "pass"
    assert not any("trace integrity" in n for n in cert.notes)
