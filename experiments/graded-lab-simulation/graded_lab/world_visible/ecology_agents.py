"""Build episode rosters from v2/v3 ecology JSON (V2-2b multi-actor support).

When ``role_population`` is absent, defaults to one actor per role with
the legacy ids ``eng1`` / ``rev1`` / ``rm1`` / ``admin1`` so V2-2 round
artifacts remain replayable without modification.

PLAN_v3 slice F: ``role_population[role]`` may be an integer (identical
clones, v2-compatible) or a list of per-actor override objects
(``{program?, program_map?, goal_weights?}``) whose length is the headcount.
"""

from __future__ import annotations

from dataclasses import dataclass

from .config import ROLES, AgentConfig, GoalWeights
from .program_map import ProgramMapError, ResolvedActorGenotype, parse_actor_override
from .substrate import SubstrateError, is_v2_shaped_ecology, is_v3_shaped_ecology

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


@dataclass(frozen=True)
class EcologyRoster:
    agents: tuple[AgentConfig, ...]
    genotypes_by_actor: dict[str, ResolvedActorGenotype]


def _parse_population_count(raw: object, *, role: str) -> int:
    if isinstance(raw, int) and not isinstance(raw, bool):
        if raw < 1 or raw > MAX_ACTORS_PER_ROLE:
            raise SubstrateError(
                f"role_population[{role!r}] must be in [1, {MAX_ACTORS_PER_ROLE}]"
            )
        return raw
    if isinstance(raw, list):
        if not raw:
            raise SubstrateError(f"role_population[{role!r}] list must be non-empty")
        if len(raw) > MAX_ACTORS_PER_ROLE:
            raise SubstrateError(
                f"role_population[{role!r}] list length exceeds {MAX_ACTORS_PER_ROLE}"
            )
        return len(raw)
    raise SubstrateError(
        f"role_population[{role!r}] must be an integer or a list of actor overrides"
    )


def role_population_from_ecology(data: dict) -> dict[str, int]:
    """Per-role headcount; v1-shaped JSONs always return one each."""
    if not is_v2_shaped_ecology(data) and not is_v3_shaped_ecology(data):
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
        out[role] = _parse_population_count(raw[role], role=role)
    return out


def _role_population_entries(data: dict, role: str) -> list[object] | None:
    """Return per-actor override list for ``role``, or ``None`` if integer clones."""
    if not is_v3_shaped_ecology(data):
        return None
    raw = data.get("role_population")
    if not isinstance(raw, dict):
        return None
    value = raw.get(role)
    if isinstance(value, list):
        return value
    return None


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
    return build_ecology_roster(data, goal_weights=goal_weights, temperature=temperature).agents


def build_ecology_roster(
    data: dict,
    *,
    goal_weights: GoalWeights | None = None,
    temperature: float = 0.35,
    default_genotypes_by_role: dict[str, ResolvedActorGenotype] | None = None,
) -> EcologyRoster:
    """Build agents and optional per-actor genotypes from ecology JSON."""
    population = role_population_from_ecology(data)
    default_gw = (goal_weights or GoalWeights(1.0, 1.0, 0.5, 0.5)).normalized()
    agents: list[AgentConfig] = []
    genotypes: dict[str, ResolvedActorGenotype] = {}
    for role in ROLES:
        count = population[role]
        entries = _role_population_entries(data, role)
        for i in range(1, count + 1):
            actor_id = actor_id_for(role, i, count=count)
            gw = default_gw
            temp = temperature
            if entries is not None:
                raw_entry = entries[i - 1]
                if not isinstance(raw_entry, dict):
                    raise SubstrateError(
                        f"role_population[{role!r}][{i - 1}] must be an object"
                    )
                try:
                    genotype = parse_actor_override(raw_entry, role=role)
                except ProgramMapError as exc:
                    raise SubstrateError(str(exc)) from exc
                genotypes[actor_id] = genotype
                if genotype.goal_weights is not None:
                    gw = genotype.goal_weights
                if genotype.temperature is not None:
                    temp = genotype.temperature
            elif default_genotypes_by_role and role in default_genotypes_by_role:
                genotypes[actor_id] = default_genotypes_by_role[role]
                gt = default_genotypes_by_role[role]
                if gt.goal_weights is not None:
                    gw = gt.goal_weights
                if gt.temperature is not None:
                    temp = gt.temperature
            agents.append(AgentConfig(actor_id, role, gw, temperature=temp))
    return EcologyRoster(agents=tuple(agents), genotypes_by_actor=genotypes)


def default_genotypes_for_agent_type(agent_type: str) -> dict[str, ResolvedActorGenotype]:
    """Expand a frozen reference agent type (e.g. ``WEAK_AGENT``) to per-role genotypes."""
    from ..oracle_only.calibration import _ROLE_PROGRAMS

    by_role = _ROLE_PROGRAMS.get(agent_type)
    if by_role is None:
        raise SubstrateError(f"unknown agent_type {agent_type!r}")
    out: dict[str, ResolvedActorGenotype] = {}
    for role, preset in by_role.items():
        from .program_map import expand_preset, resolve_runtime_genotype

        out[role] = resolve_runtime_genotype(expand_preset(preset, role=role))
    return out


def reference_roster_from_ecology(
    data: dict,
    *,
    agent_type: str,
    temperature: float = 0.35,
) -> EcologyRoster:
    """Reference scoring roster: ecology overrides win; else frozen ``agent_type`` presets."""
    return build_ecology_roster(
        data,
        temperature=temperature,
        default_genotypes_by_role=default_genotypes_for_agent_type(agent_type),
    )


def programs_and_profiles_for_roster(
    roster: EcologyRoster,
) -> tuple[dict[str, str], dict[str, dict[str, object]]]:
    """Program keys and host-injected behavior profiles per actor."""
    programs: dict[str, str] = {}
    profiles: dict[str, dict[str, object]] = {}
    for agent in roster.agents:
        genotype = roster.genotypes_by_actor.get(agent.actor_id)
        if genotype is None:
            raise SubstrateError(
                f"actor {agent.actor_id!r} missing genotype in reference roster"
            )
        programs[agent.actor_id] = genotype.program_key
        if genotype.behavior_profile is not None:
            profiles[agent.actor_id] = genotype.behavior_profile
    return programs, profiles
