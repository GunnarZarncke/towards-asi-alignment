"""Pytest configuration for embedded-simulation."""

from __future__ import annotations

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--runslow",
        action="store_true",
        default=False,
        help="Run tests marked slow (full calibration refit, etc.)",
    )


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "slow: expensive integration test; skipped unless --runslow is passed",
    )


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if config.getoption("--runslow"):
        return
    skip_slow = pytest.mark.skip(reason="pass --runslow to run slow integration tests")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
