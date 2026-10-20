"""Optional PostHog capture for Python-backed chapter demos."""

from __future__ import annotations

import atexit
import os
from functools import lru_cache
from typing import Any

from posthog import Posthog

_client: Posthog | None = None


@lru_cache
def _privacy_mode() -> bool:
    raw = os.environ.get("POSTHOG_PRIVACY_MODE", "true").strip().lower()
    return raw not in {"0", "false", "no", "off"}


def get_client() -> Posthog | None:
    global _client
    if _client is not None:
        return _client
    key = (
        os.environ.get("POSTHOG_PROJECT_TOKEN")
        or os.environ.get("POSTHOG_API_KEY")
        or ""
    ).strip()
    host = (os.environ.get("POSTHOG_HOST") or "").strip()
    if not key or not host:
        return None
    _client = Posthog(
        project_api_key=key,
        host=host,
        enable_exception_autocapture=True,
        privacy_mode=_privacy_mode(),
    )
    atexit.register(_client.shutdown)
    return _client


def capture_demo_event(
    event: str,
    demo_slug: str,
    properties: dict[str, Any] | None = None,
) -> None:
    client = get_client()
    if client is None:
        return
    props: dict[str, Any] = {"app": "chapter_demo", "demo_slug": demo_slug}
    if properties:
        props.update(properties)
    client.capture(event, properties=props)
