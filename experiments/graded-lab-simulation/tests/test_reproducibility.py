"""Regression coverage for seed reproducibility across Python processes."""

from __future__ import annotations

import subprocess
import sys


def _episode_summary() -> str:
    program = """
from graded_lab.harness.isolate import MockIsolate
from graded_lab.world_visible.world import default_lab_config, run_episode
result = run_episode(default_lab_config(), seed=5, backend=MockIsolate())
print(result.digests["combined"], result.deploy_count, result.eai)
"""
    return subprocess.check_output([sys.executable, "-c", program], text=True).strip()


def test_same_seed_is_reproducible_in_fresh_processes():
    assert _episode_summary() == _episode_summary()
