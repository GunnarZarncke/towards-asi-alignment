import pytest

from graded_lab.world_visible.substrate import (
    FORBIDDEN_PARAMETER_NAMES,
    SubstrateError,
    _validate_structure,
    load_substrate,
)


def _forbidden_keys_in_obj(obj: object, prefix: str = "") -> list[str]:
    hits: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            key_lower = str(key).lower()
            for forbidden in FORBIDDEN_PARAMETER_NAMES:
                if forbidden in key_lower:
                    hits.append(f"{prefix}{key}")
            hits.extend(_forbidden_keys_in_obj(value, prefix=f"{prefix}{key}."))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            hits.extend(_forbidden_keys_in_obj(item, prefix=f"{prefix}[{i}]."))
    return hits


def test_frozen_substrate_loads():
    sub = load_substrate()
    assert sub.version == "graded-substrate-v1"
    assert "engineer" in sub.data["resource_allowances_per_tick"]


def test_substrate_keys_have_no_forbidden_ambiguity_parameters():
    sub = load_substrate()
    hits = _forbidden_keys_in_obj(sub.data)
    assert not hits, f"forbidden keys in substrate: {hits}"


def test_frozen_substrate_has_full_section_coverage():
    """Structural validation now covers standing_mechanics/contention/
    eval_sampling/field_monitor_sampling, not just five top-level keys."""
    sub = load_substrate()
    _validate_structure(sub.data)  # must not raise


def test_validate_structure_rejects_missing_contention_field():
    sub = load_substrate()
    broken = dict(sub.data)
    broken["contention"] = {"shared_compute_slots": 4}  # missing the other key
    with pytest.raises(SubstrateError):
        _validate_structure(broken)
