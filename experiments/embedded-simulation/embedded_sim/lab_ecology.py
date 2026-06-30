"""Configurable lab-agent ecology for UAD stress tests."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LabEcologyConfig:
    """Optional actor populations; defaults preserve the historical lab."""

    n_adversarial_candidates: int = 0
    common_legitimate_lab_agents: bool = False
    auditor_agent: bool = False
    alignment_target_agent: bool = False
    n_decoys: int = 0

    @property
    def enabled(self) -> bool:
        return any(
            (
                self.n_adversarial_candidates > 0,
                self.common_legitimate_lab_agents,
                self.auditor_agent,
                self.alignment_target_agent,
                self.n_decoys > 0,
            )
        )


_current = [LabEcologyConfig()]


def get_lab_ecology() -> LabEcologyConfig:
    return _current[0]


def set_lab_ecology(config: LabEcologyConfig | None = None) -> None:
    _current[0] = config or LabEcologyConfig()

