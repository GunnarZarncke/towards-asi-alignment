"""Incremental progress logging for long batch runs.

Stdout is line-buffered when possible so piped / sandboxed invocations still
emit updates promptly. Optional append-only log under ``logs/``.
"""

from __future__ import annotations

import sys
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

_log_path: Path | None = None


def configure_progress_logging(log_dir: Path | None = None) -> Path | None:
    """Enable line-buffered stdout and an optional progress log file."""
    global _log_path
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(line_buffering=True)
        except (OSError, ValueError):
            pass
    _log_path = None
    if log_dir is None:
        return None
    log_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    _log_path = log_dir / f"suite_progress_{stamp}.log"
    _emit(f"progress log: {_log_path}")
    return _log_path


def progress(message: str) -> None:
    """Timestamped line to stdout (and progress log when configured)."""
    _emit(message)


def progress_interval(total: int, *, every: int = 0) -> int:
    """Return a print cadence: explicit ``every`` or ~100 ticks over ``total``."""
    if every > 0:
        return every
    return max(1, total // 100)


def progress_tick(
    label: str,
    n: int,
    total: int,
    *,
    t0: float,
    detail: str = "",
    every: int = 0,
) -> None:
    """Emit a progress line when ``n`` crosses the reporting interval."""
    if total <= 0:
        return
    step = progress_interval(total, every=every)
    if n != 1 and n != total and n % step != 0:
        return
    elapsed = time.perf_counter() - t0
    rate = n / elapsed if elapsed > 0 else 0.0
    remaining = (total - n) / rate if rate > 0 else 0.0
    pct = 100.0 * n / total
    extra = f" {detail}" if detail else ""
    progress(
        f"{label} [{n}/{total} {pct:.1f}%] "
        f"elapsed={elapsed:.0f}s eta={remaining:.0f}s{extra}"
    )


@contextmanager
def suite_phase(name: str) -> Iterator[None]:
    """Mark the start and end of a suite stage with wall-clock duration."""
    t0 = time.perf_counter()
    progress(f"=== START {name} ===")
    try:
        yield
    finally:
        progress(f"=== DONE {name} ({time.perf_counter() - t0:.0f}s) ===")


def _emit(message: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
    line = f"[{ts}Z] {message}"
    print(line, flush=True)
    if _log_path is not None:
        with _log_path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
