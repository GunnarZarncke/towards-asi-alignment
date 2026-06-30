"""Audit path rebuilds CCI trace from VFS rows only (no micro oracle)."""

import inspect

from embedded_sim.lab import build_world, rebuild_audit_inputs


def test_rebuild_audit_inputs_does_not_use_micro():
    src = inspect.getsource(rebuild_audit_inputs)
    assert "world.micro" not in src
    assert "build_audit_trace_from_rows" in src


def test_artifact_trace_matches_row_count():
    world, _ledger, _micro = build_world("MB6", "selection_basin", seed=42, T=200)
    rows, audit, _lineage = rebuild_audit_inputs(world, instrumentation="medium_handles")
    assert len(rows) == 200
    assert len(audit.correction_request) == len(rows)
    assert audit.instrumentation == "medium_handles"
