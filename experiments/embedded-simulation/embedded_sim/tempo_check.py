"""AppD tempo defense: latency_to_effect / reversibility_window ratio."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

TEMPO_THRESHOLD = 1.0


@dataclass
class TempoCheck:
    worst_ratio: float
    tempo_failure: bool
    n_correction_events: int
    n_undefined_latency: int


def compute_tempo(correction_rows: list[dict[str, Any]]) -> TempoCheck:
    """Flag when corrections land slower than the reversibility window allows."""
    events = [
        r
        for r in correction_rows
        if r.get("latency_to_effect_ms") is not None or "correction_id" in r
    ]
    ratios: list[float] = []
    n_undef = 0
    for row in events:
        lat = row.get("latency_to_effect_ms")
        rev = row.get("reversibility_window_ms")
        if lat is None:
            n_undef += 1
            continue
        if not rev or int(rev) <= 0:
            continue
        ratios.append(float(lat) / float(rev))
    worst = max(ratios) if ratios else 0.0
    return TempoCheck(
        worst_ratio=round(worst, 4),
        tempo_failure=worst > TEMPO_THRESHOLD,
        n_correction_events=len(events),
        n_undefined_latency=n_undef,
    )
