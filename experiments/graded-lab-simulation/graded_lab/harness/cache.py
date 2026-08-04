"""Episode cache keyed on config, seed, CODE_VERSION, and substrate hash."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from pathlib import Path

from ..world_visible.config import CODE_VERSION, EpisodeConfig
from ..world_visible.substrate import load_substrate

DEFAULT_CACHE_DIR = Path(__file__).resolve().parent.parent.parent / "results" / "episode_cache"


def cache_key(cfg: EpisodeConfig, seed: int) -> str:
    substrate = load_substrate()
    # Hash substrate CONTENT, not just its declared version/path — an
    # unbumped edit to generated_substrate_v1.json must invalidate the cache
    # (PLAN.md reuse table: "Cache key includes frozen-substrate hash").
    substrate_hash = hashlib.sha256(
        json.dumps(substrate.data, sort_keys=True).encode("utf-8")
    ).hexdigest()
    blob = json.dumps(
        {
            "config": asdict(cfg),
            "seed": seed,
            "code_version": CODE_VERSION,
            "substrate_version": substrate.version,
            "substrate_hash": substrate_hash,
        },
        sort_keys=True,
    )
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def load_cached(key: str, cache_dir: Path = DEFAULT_CACHE_DIR) -> dict | None:
    path = cache_dir / f"{key}.json"
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def store_cached(key: str, result: dict, cache_dir: Path = DEFAULT_CACHE_DIR) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    (cache_dir / f"{key}.json").write_text(json.dumps(result, sort_keys=True), encoding="utf-8")
