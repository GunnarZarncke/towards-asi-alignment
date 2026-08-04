"""Profile selection rules."""

from __future__ import annotations

from tests.profiles import (
    SMOKE_MODULES,
    SMOKE_NODEIDS,
    is_smoke_item,
    item_matches_profile,
    resolve_profile,
)


def test_resolve_profile_fast_flag_overrides():
    assert resolve_profile(profile="slow", fast_flag=True) == "fast"


def test_resolve_profile_defaults_to_slow():
    assert resolve_profile(profile="slow", fast_flag=False) == "slow"
    assert resolve_profile(profile=None, fast_flag=False) == "slow"


def test_smoke_modules_are_auto_detected():
    assert is_smoke_item(
        "tests/test_config.py::test_code_version",
        "test_config",
        keywords=set(),
    )


def test_slow_tests_are_never_smoke():
    assert not is_smoke_item(
        "tests/test_world.py::test_phase3_gate_deploy_sometimes_across_20_seeds",
        "test_world",
        keywords={"slow"},
    )


def test_explicit_smoke_nodeid():
    assert is_smoke_item(
        "tests/test_world.py::test_run_episode_engineer_walk_pipeline_builds_model",
        "test_world",
        keywords=set(),
    )


def test_profile_fast_excludes_slow():
    assert item_matches_profile(
        profile="fast",
        nodeid="tests/test_world.py::test_phase3_gate_deploy_sometimes_across_20_seeds",
        module_name="test_world",
        keywords={"slow"},
    ) is False


def test_profile_smoke_only_includes_smoke_set():
    assert item_matches_profile(
        profile="smoke",
        nodeid="tests/test_config.py::test_code_version",
        module_name="test_config",
        keywords=set(),
    )
    assert not item_matches_profile(
        profile="smoke",
        nodeid="tests/test_detectors.py::test_none_tier_sees_nothing",
        module_name="test_detectors",
        keywords=set(),
    )


def test_smoke_manifest_is_nonempty():
    assert SMOKE_MODULES
    assert SMOKE_NODEIDS
