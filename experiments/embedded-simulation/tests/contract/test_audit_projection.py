"""Contract: ground truth never flows through red-team-writable artifacts.

Two directions:
1. Audit direction — VFS logs carry only the audit-visible projection
   (no oracle fields for the auditor to peek at).
2. Oracle direction — red-team patches to VFS logs never alter the truth rows
   the outer evaluator scores against.

Plus tamper-evidence: hash-chained logs anchored in the (non-red-team-writable)
attestation manifest invalidate certificates built on patched traces, while the
unsigned regime (NEGATIVE_RESULTS N-4) stays reproducible via config.
"""

import copy
import json

import pytest

from embedded_sim.audit_projection import ORACLE_ONLY_FIELDS
from embedded_sim.bridge import MachineIsolate, default_redteam_caps
from embedded_sim.embedded_audit import run_embedded_audit
from embedded_sim.lab import build_world, load_episode_rows_from_vfs
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


@pytest.mark.parametrize(
    "bridge,scenario",
    [
        ("none", "honest"),
        ("MB4", "capture_theater"),
        ("MB9", "grounding_silent_gap"),
        ("MB7d", "inferential_coupling"),
        ("MB5", "successor_relabel"),
    ],
)
def test_vfs_correction_log_has_no_oracle_fields(bridge, scenario):
    world, _ledger, _micro = build_world(bridge, scenario, seed=42, T=120)
    rows = load_episode_rows_from_vfs(world)
    assert rows
    for row in rows:
        leaked = set(row) & set(ORACLE_ONLY_FIELDS)
        assert not leaked, f"oracle fields on VFS: {sorted(leaked)}"


def test_redteam_patches_do_not_alter_outer_truth():
    world, _ledger, _micro = build_world("MB4", "capture_theater", seed=42, T=150)
    truth_before = copy.deepcopy(world.episode_meta)
    n = run_redteam(world, "full_redteam", substrate="python")
    assert n > 0
    assert world.episode_meta == truth_before
    patched = load_episode_rows_from_vfs(world)
    reported_vfs = [r["reported_acceptance"] for r in patched]
    reported_truth = [r["reported_acceptance"] for r in world.episode_meta]
    assert reported_vfs != reported_truth


def test_anchored_chain_verifies_when_untampered():
    world, _ledger, _micro = build_world("none", "honest", seed=42, T=120)
    manifest = json.loads(world.vfs.read("/etc/attest/manifest.json"))
    anchors = manifest["trace_anchors"]
    for name in ("correction", "workflow"):
        raw = world.vfs.read(anchors[name]["path"])
        ok, reason = verify_chain(raw, anchors[name])
        assert ok, f"{name}: {reason}"


def test_tampered_trace_invalidates_certificate():
    world, _ledger, _micro = build_world("none", "honest", seed=42, T=400)
    run_redteam(world, "theater_inflate", substrate="python")
    cert, *_ = run_embedded_audit(world, "medium_handles", substrate="python")
    assert cert.safety_decision == "invalid_certificate"
    assert any("trace integrity" in n for n in cert.notes)


def test_untampered_honest_world_still_certifies():
    world, _ledger, _micro = build_world("none", "honest", seed=42, T=400)
    cert, *_ = run_embedded_audit(world, "medium_handles", substrate="python")
    assert cert.safety_decision == "pass"


def test_unsigned_naive_forgery_caught_by_schema_crosscheck(integrity_mode_guard):
    """Even unsigned, naive patches break the AppD correction-schema recompute.

    `full_redteam` patches `visible_action`/`reported_acceptance` without
    recomputing `pre/post_behavior_hash`, `behavioral_uplift`,
    `latency_to_effect_ms` — the trace is internally inconsistent.
    """
    set_trace_integrity_mode("none")
    world, _ledger, _micro = build_world("MB4", "capture_theater", seed=42, T=400)
    manifest = json.loads(world.vfs.read("/etc/attest/manifest.json"))
    assert "trace_anchors" not in manifest
    run_redteam(world, "full_redteam", substrate="python")
    cert, *_ = run_embedded_audit(world, "medium_handles", substrate="python")
    assert cert.safety_decision == "invalid_certificate"
    assert any("correction schema" in n for n in cert.notes)


def test_unsigned_regime_reproduces_forged_pass(integrity_mode_guard):
    """N-4: without trace integrity, a *schema-consistent* forger still wins.

    The AppD fields are deterministic functions of visible data, so an
    adversary who recomputes them forges an internally coherent trace; only
    the attestation-anchored hash chain distinguishes it.
    """
    set_trace_integrity_mode("none")
    world, _ledger, _micro = build_world("MB4", "capture_theater", seed=42, T=400)
    run_redteam(world, "consistent_forge", substrate="python")
    cert, *_ = run_embedded_audit(world, "medium_handles", substrate="python")
    assert cert.safety_decision == "pass"


def test_signed_regime_catches_consistent_forger():
    """With anchors on, the schema-aware forger is caught by the hash chain."""
    world, _ledger, _micro = build_world("MB4", "capture_theater", seed=42, T=400)
    run_redteam(world, "consistent_forge", substrate="python")
    cert, *_ = run_embedded_audit(world, "medium_handles", substrate="python")
    assert cert.safety_decision == "invalid_certificate"
    assert any("trace integrity" in n for n in cert.notes)


def test_redteam_cannot_write_attestation_manifest():
    world, _ledger, _micro = build_world("none", "honest", seed=42, T=60)
    isolate = MachineIsolate(
        machine_id=world.redteam_machine_id,
        actor_id="redteam.agent",
        cwd="/home/redteam",
        env={"ROLE": "redteam"},
        caps=default_redteam_caps(),
        vfs=world.vfs,
    )
    ok, detail = isolate.write_file("/etc/attest/manifest.json", "{}")
    assert not ok
    assert detail == "EACCES"
