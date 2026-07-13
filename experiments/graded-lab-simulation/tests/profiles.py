"""Pytest profile selection: smoke, fast, and slow (full suite).

Smoke — minimal invariant gate (~30s): structural/unit tests plus one
episode smoke.  Fast — dev loop (~60s): everything except ``@slow``.
Slow — full suite (~210s): includes multi-seed gates and integration
batteries marked ``@pytest.mark.slow``.
"""

from __future__ import annotations

from typing import Literal

ProfileName = Literal["smoke", "fast", "slow"]

# Entire modules whose tests are auto-marked ``smoke`` (unless also ``slow``).
SMOKE_MODULES = frozenset(
    {
        "test_agent_main_isolation",
        "test_cache",
        "test_carrier",
        "test_config",
        "test_events",
        "test_no_lab_sim_imports",
        "test_observation",
        "test_oracle",
        "test_pipeline_engine",
        "test_pipeline_spec",
        "test_policy",
        "test_primitive_trace",
        "test_profiles",
        "test_resource_ledger",
        "test_scheduler",
        "test_speed_limits",
        "test_substrate",
        "test_uad_partition",
    }
)

# Individual tests outside ``SMOKE_MODULES`` included in the smoke profile.
SMOKE_NODEIDS = frozenset(
    {
        "tests/test_planes.py::test_engine_log_contains_no_oracle_only_fields",
        "tests/test_planes.py::test_eval_payload_is_sampled_not_tier_k_mean",
        "tests/test_world.py::test_run_episode_engineer_walk_pipeline_builds_model",
        "tests/test_world.py::test_mock_and_subprocess_agree_on_walk_pipeline_smoke",
        "tests/test_unit_biq.py::test_held_out_bits_deterministic_mapping_is_near_max_reduction",
        "tests/test_unit_biq.py::test_held_out_bits_no_relationship_is_near_zero",
        "tests/test_unit_biq.py::test_held_out_bits_nll_mode_returns_raw_positive_bits",
        "tests/test_unit_biq.py::test_held_out_bits_empty_input_is_unavailable",
        "tests/test_unit_biq.py::test_unit_memory_bits_counts_distinct_paths_across_members",
        "tests/test_unit_biq.py::test_unit_memory_bits_empty_unit_is_zero",
        "tests/test_phase7_calibration.py::test_substrate_grid_has_sixteen_cells",
        "tests/test_phase7_calibration.py::test_programs_for_agent_types",
        "tests/test_phase7_calibration.py::test_eai_band_labels",
        "tests/test_phase7_calibration.py::test_evaluate_pass_criteria_all_pass_synthetic",
        "tests/test_phase7_calibration.py::test_evaluate_pass_criteria_fails_bad_dose_response",
        "tests/test_phase7_calibration.py::test_select_mid_band_cell_picks_closest_to_target",
    }
)


def resolve_profile(*, profile: str | None, fast_flag: bool) -> ProfileName:
    if fast_flag:
        return "fast"
    if profile in ("smoke", "fast", "slow"):
        return profile  # type: ignore[return-value]
    return "slow"


def is_smoke_item(nodeid: str, module_name: str, *, keywords: set[str]) -> bool:
    if "slow" in keywords:
        return False
    if module_name in SMOKE_MODULES:
        return True
    return nodeid in SMOKE_NODEIDS


def item_matches_profile(
    *,
    profile: ProfileName,
    nodeid: str,
    module_name: str,
    keywords: set[str],
) -> bool:
    if profile == "slow":
        return True
    if profile == "fast":
        return "slow" not in keywords
    # smoke
    return is_smoke_item(nodeid, module_name, keywords=keywords)
