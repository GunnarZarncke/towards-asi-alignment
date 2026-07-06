"""Episode-result cache: pure optimization, safe to delete, never a
correctness input (see PLAN.md "Avoiding recomputation, kept lean").

Keyed on sha256(config, seed, CODE_VERSION) so a code change bumping
``CODE_VERSION`` can never silently serve a stale cached result. Caches a
SUMMARY dict (digests, not live objects) — callers needing the live engine/
workspace (e.g. Phase 5 deep-tier detectors reading files) must run the
episode fresh; caching targets battery-scale severity/digest aggregation
(Phase 6+), not detector development.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from pathlib import Path

from .config import CODE_VERSION, LabConfig

DEFAULT_CACHE_DIR = Path(__file__).resolve().parent.parent / "results" / "episode_cache"


def cache_key(cfg: LabConfig, seed: int) -> str:
    blob = json.dumps({"config": asdict(cfg), "seed": seed, "code_version": CODE_VERSION}, sort_keys=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def load_cached(key: str, cache_dir: Path = DEFAULT_CACHE_DIR) -> dict | None:
    path = cache_dir / f"{key}.json"
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def store_cached(key: str, result: dict, cache_dir: Path = DEFAULT_CACHE_DIR) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    (cache_dir / f"{key}.json").write_text(json.dumps(result, sort_keys=True), encoding="utf-8")
