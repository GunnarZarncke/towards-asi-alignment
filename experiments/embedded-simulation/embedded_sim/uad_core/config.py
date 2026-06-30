"""Detection configuration (adapted from agency-detect DetectionConfig)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DetectionConfig:
    n_agents: int = 4
    max_lag: int = 3
    weak_threshold: float = 0.05
    validate_blankets: bool = False
    blanket_tolerance: float = 1.0
    cmi_smoothing_alpha: float = 0.1
    env_mi_percentile: float = 50.0
    future_mi_percentile: float = 50.0
