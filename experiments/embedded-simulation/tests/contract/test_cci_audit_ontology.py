"""Contract: CCI audit path uses telemetry predicates, not scenario or bridge labels."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "embedded_sim" / "audit_core"


def test_cci_audit_has_no_scenario_branches():
    src = (ROOT / "cci_audit.py").read_text(encoding="utf-8")
    assert "audit.scenario" not in src
    assert "MB1" not in src
    assert "MB4" not in src
    assert "instrument_capture" not in src


def test_structural_signals_use_neutral_names():
    src = (ROOT / "structural_signals.py").read_text(encoding="utf-8")
    predicate_src, _, _ = src.partition("def map_signals_to_legacy_cert_fields")
    assert "audit.scenario" not in predicate_src
    for legacy in ("MB1", "MB3", "MB4", "MB5", "MB6", "MB7", "MB8", "MB9"):
        assert legacy not in predicate_src
    assert "ground_handle_divergence" in predicate_src
    assert "shadow_routing_under_probes" in predicate_src


def test_legacy_fields_mapped_at_boundary():
    from embedded_sim.audit_core.structural_signals import (
        StructuralSignals,
        map_signals_to_legacy_cert_fields,
    )
    from embedded_sim.audit_core.schemas import CCICertificate

    cert = CCICertificate(
        raw_capacity=0.5,
        latency=1.0,
        manipulation=0.1,
        irreversibility=0.5,
        ontology_translation=0.0,
        plurality=0.5,
        exit_capacity=0.5,
        independence=0.5,
        naive_reported_cci_bits=0.1,
        behavioral_cci_bits=0.1,
        status="belowThreshold",
    )
    signals = StructuralSignals(
        ground_handle_divergence=True,
        shadow_routing_under_probes=True,
    )
    map_signals_to_legacy_cert_fields(cert, signals)
    assert cert.instrument_capture_detected
    assert cert.inferential_coupling_detected
