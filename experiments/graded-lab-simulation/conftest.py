"""Pytest path setup, profile selection, and speed-limit enforcement."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from graded_lab.harness.speed_limits import (  # noqa: E402
    check_speeds,
    load_baseline,
    load_limits,
    save_baseline,
)
from tests.profiles import (  # noqa: E402
    is_smoke_item,
    resolve_profile,
)

# Tests calibrated on the pre-GL-66 affordable builder (full-read + GL-50 cap).
LEGACY_ATTENTION_MODULES = frozenset(
    {
        "test_uad_ecology_partition",
        "test_uad_intervention",
        "test_uad_passive",
        "test_uad_blind_scenarios",
        "test_unit_biq",
        "test_primitive_trace",
        "test_v3_c2_v3_causal_gate",
        "test_v3_slice_a_flow_ablation",
    }
)


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--profile",
        choices=("smoke", "fast", "slow"),
        default="slow",
        help="Test profile: smoke (~30s), fast (~60s, no @slow), slow/full (~210s)",
    )
    parser.addoption(
        "--fast",
        action="store_true",
        default=False,
        help="Alias for --profile fast (dev loop; skips @slow tests)",
    )
    parser.addoption(
        "--update-speed-baseline",
        action="store_true",
        default=False,
        help="Rewrite tests/speed_baseline.json from this run's call durations",
    )
    parser.addoption(
        "--no-speed-check",
        action="store_true",
        default=False,
        help="Skip suite/per-test speed limit enforcement (for baseline refresh)",
    )


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "smoke: minimal invariant gate (selected automatically; run with --profile smoke)",
    )
    config.addinivalue_line(
        "markers",
        "slow: expensive multi-seed or full-episode integration test",
    )
    config.addinivalue_line(
        "markers",
        "legacy_attention_surface: use pre-GL-66 affordable builder for this test",
    )
    config.addinivalue_line(
        "markers",
        "gl66_attention_surface: force GL-66 attention surface even in a legacy module",
    )
    config._speed_durations: dict[str, float] = {}
    config._active_profile = resolve_profile(
        profile=config.getoption("--profile"),
        fast_flag=config.getoption("--fast"),
    )


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    profile = config._active_profile
    selected: list[pytest.Item] = []
    deselected: list[pytest.Item] = []

    for item in items:
        module_name = item.module.__name__.split(".")[-1] if item.module else ""
        keywords = set(item.keywords)

        if is_smoke_item(item.nodeid, module_name, keywords=keywords):
            item.add_marker(pytest.mark.smoke)

        if profile == "slow":
            selected.append(item)
            continue
        if profile == "fast":
            if "slow" in keywords:
                deselected.append(item)
            else:
                selected.append(item)
            continue
        # smoke
        if "smoke" in item.keywords:
            selected.append(item)
        else:
            deselected.append(item)

    if deselected:
        config.hook.pytest_deselected(items=deselected)
    items[:] = selected


@pytest.fixture(autouse=True)
def _legacy_attention_surface_for_calibrated_tests(request):
    """Opt legacy modules into pre-GL-66 affordances without changing production."""
    from graded_lab.world_visible.attention_policy import (
        reset_attention_surface_mode,
        set_attention_surface_mode,
    )

    if request.node.get_closest_marker("gl66_attention_surface") is not None:
        yield
        return

    module_name = request.module.__name__.split(".")[-1] if request.module else ""
    use_legacy = (
        request.node.get_closest_marker("legacy_attention_surface") is not None
        or module_name in LEGACY_ATTENTION_MODULES
    )
    if not use_legacy:
        yield
        return

    token = set_attention_surface_mode("legacy")
    try:
        yield
    finally:
        reset_attention_surface_mode(token)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return
    config = item.config
    durations: dict[str, float] = getattr(config, "_speed_durations", {})
    durations[item.nodeid] = float(report.duration)
    config._speed_durations = durations


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    config = session.config
    durations: dict[str, float] = getattr(config, "_speed_durations", {})
    if not durations:
        return

    profile = config._active_profile

    if config.getoption("--update-speed-baseline"):
        if profile != "slow":
            print(
                f"\n[speed] skipped baseline update: --update-speed-baseline "
                f"requires --profile slow (got {profile!r})"
            )
        else:
            payload = save_baseline(durations)
            print(
                f"\n[speed] updated baseline: {len(payload['tests'])} tests, "
                f"suite {payload['suite_total_seconds']:.2f}s"
            )

    if config.getoption("--no-speed-check"):
        return

    limits = load_limits()
    baseline = load_baseline()
    if profile == "smoke":
        suite_cap = limits.smoke_suite_max_seconds
    elif profile == "fast":
        suite_cap = limits.fast_suite_max_seconds
    else:
        suite_cap = limits.suite_max_seconds

    violations = check_speeds(durations, limits, baseline, suite_cap=suite_cap)
    if not violations:
        suite_total = sum(durations.values())
        print(
            f"\n[speed] OK [{profile}]: {len(durations)} tests, "
            f"suite {suite_total:.2f}s (limit {suite_cap:.2f}s)"
        )
        return

    print(f"\n[speed] LIMIT VIOLATIONS [{profile}]:")
    for line in violations:
        print(f"  - {line}")
    print(
        "  Hint: refresh committed baselines after an intentional change with "
        "`pytest --profile slow --update-speed-baseline --no-speed-check`."
    )
    session.exitstatus = 1
