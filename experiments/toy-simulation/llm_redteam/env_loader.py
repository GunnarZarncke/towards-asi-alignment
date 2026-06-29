"""Load repo-root ``.env`` without extra dependencies."""

from __future__ import annotations

import os
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def load_repo_env(env_path: Path | None = None) -> dict[str, str]:
    """Parse KEY=VALUE lines from ``.env`` and set ``os.environ`` (no overwrite)."""
    path = env_path or repo_root() / ".env"
    loaded: dict[str, str] = {}
    if not path.is_file():
        return loaded
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        loaded[key] = value
        os.environ.setdefault(key, value)
    return loaded


def require_openai_api_key() -> str:
    load_repo_env()
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key or key.startswith("sk-your-"):
        raise RuntimeError(
            "OPENAI_API_KEY missing. Copy .env_sample to .env and set a real key."
        )
    return key
