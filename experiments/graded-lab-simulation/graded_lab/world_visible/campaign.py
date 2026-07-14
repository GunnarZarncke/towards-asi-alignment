"""Cross-episode campaign state for Phase 8 selection (MB6).

Grants and standing persist across consecutive episodes within a
population member; compute/IO windows still reset each episode.
See DESIGN.md "Phase 8 — multi-episode selection (MB6)".
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CampaignState:
    grants: dict[str, set[str]] = field(default_factory=dict)
    standing: dict[str, float] = field(default_factory=dict)

    def copy(self) -> CampaignState:
        return CampaignState(
            grants={actor: set(caps) for actor, caps in self.grants.items()},
            standing=dict(self.standing),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "grants": {actor: sorted(caps) for actor, caps in self.grants.items()},
            "standing": dict(self.standing),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> CampaignState:
        grants_raw = payload.get("grants", {})
        standing_raw = payload.get("standing", {})
        grants: dict[str, set[str]] = {}
        if isinstance(grants_raw, dict):
            for actor, caps in grants_raw.items():
                if isinstance(caps, list):
                    grants[str(actor)] = {str(c) for c in caps}
        standing: dict[str, float] = {}
        if isinstance(standing_raw, dict):
            for actor, value in standing_raw.items():
                standing[str(actor)] = float(value)
        return cls(grants=grants, standing=standing)
