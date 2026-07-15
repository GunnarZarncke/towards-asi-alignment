"""Build episode rosters from v2 ecology JSON (V2-2b multi-actor support).

When ``role_population`` is absent, defaults to one actor per role with
the legacy ids ``eng1`` / ``rev1`` / ``rm1`` / ``admin1`` so V2-2 round
artifacts remain replayable without modification.
"""

from __future__ import annotations

from .config import ROLES, AgentConfig, GoalWeights
from .substrate import SubstrateError, is_v2_shaped_ecology

DEFAULT_ROLE_POPULATION: dict[str, int] = {role: 1 for role in ROLES}

_ROLE_ID_PREFIX: dict[str, str] = {
    "engineer": "eng",
    "reviewer": "rev",
    "release_manager": "rm",
    "admin": "admin",
}

# Legacy single-actor ids (V2-2 reference battery compatibility).
_LEGACY_SINGLE_IDS: dict[str, str] = {
    "engineer": "eng1",
    "reviewer": "rev1",
    "release_manager": "rm1",
    "admin": "admin1",
}

MAX_ACTORS_PER_ROLE = 8


def role_population_from_ecology(data: dict) -> dict[str, int]:
    """Per-role headcount; v1-shaped JSONs always return one each."""
    if not is_v2_shaped_ecology(data):
        return dict(DEFAULT_ROLE_POPULATION)
    raw = data.get("role_population")
    if raw is None:
        return dict(DEFAULT_ROLE_POPULATION)
    if not isinstance(raw, dict):
        raise SubstrateError("role_population must be an object")
    out: dict[str, int] = {}
    for role in ROLES:
        if role not in raw:
            raise SubstrateError(f"role_population missing role {role!r}")
        count = raw[role]
        if not isinstance(count, int) or isinstance(count, bool):
            raise SubstrateError(f"role_population[{role!r}] must be an integer")
        if count < 1 or count > MAX_ACTORS_PER_ROLE:
            raise SubstrateError(
                f"role_population[{role!r}] must be in [1, {MAX_ACTORS_PER_ROLE}]"
            )
        out[role] = count
    return out


def actor_id_for(role: str, index: int, *, count: int) -> str:
    """Stable actor ids: legacy names at count=1, else ``eng1``…``engN``."""
    if count == 1:
        return _LEGACY_SINGLE_IDS[role]
    prefix = _ROLE_ID_PREFIX[role]
    return f"{prefix}{index}"


def build_agents_from_ecology(
    data: dict,
    *,
    goal_weights: GoalWeights | None = None,
    temperature: float = 0.35,
) -> tuple[AgentConfig, ...]:
    population = role_population_from_ecology(data)
    gw = (goal_weights or GoalWeights(1.0, 1.0, 0.5, 0.5)).normalized()
    agents: list[AgentConfig] = []
    for role in ROLES:
        count = population[role]
        for i in range(1, count + 1):
            agents.append(
                AgentConfig(
                    actor_id_for(role, i, count=count),
                    role,
                    gw,
                    temperature=temperature,
                )
            )
    return tuple(agents)
