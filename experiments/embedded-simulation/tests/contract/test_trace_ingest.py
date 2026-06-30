"""Trace ingest hook: audit external correction.jsonl without micro oracle."""

import json
from pathlib import Path

import pytest

from embedded_sim.structural_fixtures import synthesize_rows
from embedded_sim.trace_ingest import audit_trace_bundle, load_correction_jsonl


FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


@pytest.fixture(scope="module")
def sample_correction_path() -> Path:
    path = FIXTURES / "sample_capture_theater.jsonl"
    FIXTURES.mkdir(parents=True, exist_ok=True)
    rows = synthesize_rows(300, "capture_theater", seed=5)
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    return path


def test_load_correction_jsonl(sample_correction_path: Path):
    rows = load_correction_jsonl(sample_correction_path)
    assert len(rows) == 300
    assert "correction_request" in rows[0]


def test_audit_trace_bundle(sample_correction_path: Path):
    result = audit_trace_bundle(sample_correction_path, instrumentation="medium_handles", seed=5)
    assert result.n_correction_rows == 300
    assert result.cci_status == "capturedInvalid"
    assert result.safety_decision == "invalid_certificate"


def test_audit_trace_bundle_roundtrip(tmp_path: Path):
    rows = synthesize_rows(200, "instrument_capture", seed=3)
    path = tmp_path / "correction.jsonl"
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    result = audit_trace_bundle(path, instrumentation="medium_handles")
    assert result.structural_flags["instrument_capture_detected"]
    assert result.cci_status == "belowThreshold"
