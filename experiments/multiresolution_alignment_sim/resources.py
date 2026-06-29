"""CPU/GPU monitoring and adaptive throttling for experiment batches."""

from __future__ import annotations

import os
import shutil
import subprocess
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class ResourceSnapshot:
    cpu_percent: float
    gpu_percent: float | None
    gpu_available: bool
    cpu_cores: int
    workers: int = 1

    def format_short(self) -> str:
        gpu = f"{self.gpu_percent:.0f}%" if self.gpu_percent is not None else "n/a"
        return f"cpu={self.cpu_percent:.0f}% gpu={gpu} workers={self.workers}"


@dataclass
class ResourceGovernor:
    """Keep CPU (and GPU when present) below target via waits and worker tuning."""

    cpu_target: float = 0.80
    gpu_target: float = 0.80
    workers: int = 1
    throttle_enabled: bool = True
    _peak_cpu: float = field(default=0.0, init=False)
    _peak_gpu: float | None = field(default=None, init=False)

    def __post_init__(self) -> None:
        self.cpu_target_pct = self.cpu_target * 100.0
        self.gpu_target_pct = self.gpu_target * 100.0
        if self.workers < 1:
            self.workers = 1

    @staticmethod
    def resolve_workers(spec: str | int) -> int:
        if isinstance(spec, int):
            return max(1, spec)
        if str(spec).lower() == "auto":
            cores = os.cpu_count() or 1
            return max(1, int(cores * 0.75))
        return max(1, int(spec))

    @staticmethod
    def sample_cpu_percent(interval: float = 0.05) -> float:
        try:
            import psutil  # type: ignore[import-untyped]

            return float(psutil.cpu_percent(interval=interval))
        except ImportError:
            try:
                load1, _, _ = os.getloadavg()
                cores = os.cpu_count() or 1
                return min(100.0, (load1 / cores) * 100.0)
            except (AttributeError, OSError):
                return 0.0

    @staticmethod
    def sample_gpu_percent() -> tuple[float | None, bool]:
        if not shutil.which("nvidia-smi"):
            return None, False
        try:
            out = subprocess.check_output(
                [
                    "nvidia-smi",
                    "--query-gpu=utilization.gpu",
                    "--format=csv,noheader,nounits",
                ],
                text=True,
                timeout=2,
            )
            vals = [float(line.strip()) for line in out.splitlines() if line.strip()]
            if not vals:
                return None, True
            return max(vals), True
        except (subprocess.SubprocessError, ValueError, OSError):
            return None, True

    def snapshot(self) -> ResourceSnapshot:
        cpu = self.sample_cpu_percent()
        gpu, gpu_avail = self.sample_gpu_percent()
        self._peak_cpu = max(self._peak_cpu, cpu)
        if gpu is not None:
            self._peak_gpu = max(self._peak_gpu or 0.0, gpu)
        return ResourceSnapshot(
            cpu_percent=cpu,
            gpu_percent=gpu,
            gpu_available=gpu_avail,
            cpu_cores=os.cpu_count() or 1,
            workers=self.workers,
        )

    def _over_target(self, snap: ResourceSnapshot) -> bool:
        if snap.cpu_percent >= self.cpu_target_pct:
            return True
        if snap.gpu_percent is not None and snap.gpu_percent >= self.gpu_target_pct:
            return True
        return False

    def wait_until_cool(self, max_wait: float = 60.0) -> ResourceSnapshot:
        if not self.throttle_enabled:
            return self.snapshot()
        deadline = time.time() + max_wait
        snap = self.snapshot()
        while self._over_target(snap) and time.time() < deadline:
            time.sleep(0.25)
            snap = self.snapshot()
        return snap

    def max_workers(self) -> int:
        cores = os.cpu_count() or 1
        return max(1, int(cores * self.cpu_target))

    def adapt_workers(self) -> int:
        if not self.throttle_enabled:
            return self.workers
        snap = self.snapshot()
        cap = self.max_workers()
        if self._over_target(snap):
            self.workers = max(1, self.workers - 1)
        elif snap.cpu_percent < self.cpu_target_pct * 0.55 and self.workers < cap:
            self.workers = min(cap, self.workers + 1)
        return self.workers

    def peak_summary(self) -> dict[str, float | int | None]:
        return {
            "peak_cpu_percent": round(self._peak_cpu, 1),
            "peak_gpu_percent": round(self._peak_gpu, 1) if self._peak_gpu is not None else None,
            "final_workers": self.workers,
        }


def execute_run_tasks(
    tasks: list[dict[str, Any]],
    run_fn: Callable[[dict[str, Any]], dict[str, object]],
    governor: ResourceGovernor | None = None,
) -> list[dict[str, object]]:
    """Run tasks sequentially or in governed parallel batches."""
    if not tasks:
        return []

    results: list[dict[str, object]] = []
    idx = 0
    while idx < len(tasks):
        workers = governor.adapt_workers() if governor else 1
        batch = tasks[idx : idx + workers]
        if governor:
            governor.wait_until_cool()
        if workers <= 1:
            for task in batch:
                results.append(run_fn(task))
        else:
            try:
                with ProcessPoolExecutor(max_workers=workers) as pool:
                    results.extend(pool.map(run_fn, batch))
            except (PermissionError, OSError):
                for task in batch:
                    results.append(run_fn(task))
        idx += len(batch)
    return results


def resource_suffix(governor: ResourceGovernor | None) -> str:
    if governor is None:
        return ""
    return f" [{governor.snapshot().format_short()}]"
