"""Parallel isolate execution within a pipeline timestep."""

from __future__ import annotations

import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, TypeVar

from .bridge import MachineIsolate
from .js_isolate import run_js_file
from .world import EmbeddedWorld

T = TypeVar("T")
R = TypeVar("R")


def default_isolate_workers() -> int:
    return max(1, min(8, os.cpu_count() or 1))


def run_timestep(
    items: list[T],
    fn: Callable[[T], R],
    *,
    workers: int = 1,
    label: str = "",
) -> list[R]:
    """Run a timestep function over items, optionally in parallel."""
    if workers <= 1 or len(items) <= 1:
        return [fn(item) for item in items]

    workers = min(workers, len(items))
    results: list[R | None] = [None] * len(items)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(fn, item): idx for idx, item in enumerate(items)}
        for future in as_completed(futures):
            idx = futures[future]
            results[idx] = future.result()
    return results  # type: ignore[return-value]


@dataclass
class IsolateExecution:
    world: EmbeddedWorld
    isolate: MachineIsolate
    script_path: Path
    label: str = ""
    exclusive: bool = False


def run_isolate_batch(
    executions: list[IsolateExecution],
    *,
    workers: int = 1,
) -> list[dict]:
    """Run multiple JS isolates in parallel (one world per execution)."""

    def _run(job: IsolateExecution) -> dict:
        ctx = job.world.bridge_lock if job.exclusive else _null_lock()
        with ctx:
            return run_js_file(job.world, job.isolate, job.script_path)

    return run_timestep(executions, _run, workers=workers, label="isolate_batch")


class _null_lock:
    def __enter__(self):
        return None

    def __exit__(self, *args):
        return False
