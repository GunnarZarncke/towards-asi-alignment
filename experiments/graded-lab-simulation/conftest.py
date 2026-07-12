"""Pytest path setup, slow-test gating, and speed-limit enforcement."""

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


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--fast",
        action="store_true",
        default=False,
        help="Skip tests marked slow (dev loop only; does not refresh full-suite baselines)",
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
        "slow: expensive multi-seed or full-episode integration test",
    )
    config._speed_durations: dict[str, float] = {}


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    if not config.getoption("--fast"):
        return
    skip_slow = pytest.mark.skip(
        reason="slow test skipped (pass --fast only skips; omit --fast for full suite)"
    )
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


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

    if config.getoption("--update-speed-baseline"):
        payload = save_baseline(durations)
        print(
            f"\n[speed] updated baseline: {len(payload['tests'])} tests, "
            f"suite {payload['suite_total_seconds']:.2f}s"
        )

    if config.getoption("--no-speed-check"):
        return

    limits = load_limits()
    baseline = load_baseline()
    suite_cap = limits.fast_suite_max_seconds if config.getoption("--fast") else None
    violations = check_speeds(durations, limits, baseline, suite_cap=suite_cap)
    if not violations:
        suite_total = sum(durations.values())
        cap = suite_cap if suite_cap is not None else limits.suite_max_seconds
        print(
            f"\n[speed] OK: {len(durations)} tests, suite {suite_total:.2f}s "
            f"(limit {cap:.2f}s)"
        )
        return

    print("\n[speed] LIMIT VIOLATIONS:")
    for line in violations:
        print(f"  - {line}")
    print(
        "  Hint: refresh committed baselines after an intentional change with "
        "`pytest --update-speed-baseline --no-speed-check` (full suite, no --fast)."
    )
    session.exitstatus = 1
