"""GL-66 attention-surface mode switch (production default: gl66).

Legacy v1 UAD/BIQ fixtures and pre-GL-66 ablation gates were calibrated on
the pre-attention-surface affordable builder. Tests that still depend on that
semantics opt in via ``LEGACY_ATTENTION_MODULES`` in ``conftest.py`` or the
``legacy_attention_surface`` marker.
"""

from __future__ import annotations

from contextvars import ContextVar
from typing import Literal

AttentionSurfaceMode = Literal["gl66", "legacy"]

_attention_mode: ContextVar[AttentionSurfaceMode] = ContextVar(
    "attention_surface_mode", default="gl66"
)


def get_attention_surface_mode() -> AttentionSurfaceMode:
    return _attention_mode.get()


def set_attention_surface_mode(mode: AttentionSurfaceMode):
    return _attention_mode.set(mode)


def reset_attention_surface_mode(token) -> None:
    _attention_mode.reset(token)
