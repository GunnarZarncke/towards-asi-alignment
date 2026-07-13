"""Phase 7a: passive unit discovery from primitive traces."""

from __future__ import annotations

from itertools import combinations

from .events import project_primitive_log

DEFAULT_MIN_JACCARD = 0.5
DEFAULT_MIN_COMMUNICATE_FRACTION = 0.5


def _semantic_success_sets(primitive_log: list[dict], *, tier: str = "full") -> dict[str, set[str]]:
    projected = project_primitive_log(primitive_log, tier)
    out: dict[str, set[str]] = {}
    for event in projected:
        if event.get("status") != "ok":
            continue
        step = event.get("semantic_step")
        actor_id = event.get("actor_id")
        if step and actor_id:
            out.setdefault(str(actor_id), set()).add(str(step))
    return out


def _activity_ticks(
    primitive_log: list[dict],
    *,
    tier: str = "full",
    kind: str | None = None,
) -> dict[str, set[int]]:
    projected = project_primitive_log(primitive_log, tier)
    out: dict[str, set[int]] = {}
    for event in projected:
        if event.get("status") != "ok":
            continue
        actor_id = event.get("actor_id")
        if not actor_id:
            continue
        if kind is not None:
            primitive = event.get("primitive")
            if not isinstance(primitive, dict) or primitive.get("kind") != kind:
                continue
        out.setdefault(str(actor_id), set()).add(int(event.get("t", 0)))
    return out


def _communicate_fraction(primitive_log: list[dict], actor_id: str, *, tier: str = "full") -> float:
    projected = project_primitive_log(primitive_log, tier)
    ok = [
        event
        for event in projected
        if event.get("actor_id") == actor_id and event.get("status") == "ok"
    ]
    if not ok:
        return 0.0
    comm = sum(
        1
        for event in ok
        if isinstance(event.get("primitive"), dict)
        and event["primitive"].get("kind") == "communicate"
    )
    return comm / len(ok)


def co_activity_matrix(
    primitive_log: list[dict],
    *,
    tier: str = "full",
    kind: str | None = None,
) -> dict[tuple[str, str], float]:
    """Jaccard similarity of ticks with successful primitives per actor pair."""
    by_actor = _activity_ticks(primitive_log, tier=tier, kind=kind)
    actors = sorted(by_actor)
    matrix: dict[tuple[str, str], float] = {}
    for a, b in combinations(actors, 2):
        sa, sb = by_actor[a], by_actor[b]
        union = sa | sb
        matrix[(a, b)] = len(sa & sb) / len(union) if union else 0.0
    return matrix


def co_semantic_step_matrix(
    primitive_log: list[dict],
    *,
    tier: str = "full",
) -> dict[tuple[str, str], float]:
    """Jaccard similarity of successful semantic-step sets per actor pair."""
    by_actor = _semantic_success_sets(primitive_log, tier=tier)
    actors = sorted(by_actor)
    matrix: dict[tuple[str, str], float] = {}
    for a, b in combinations(actors, 2):
        sa, sb = by_actor[a], by_actor[b]
        union = sa | sb
        matrix[(a, b)] = len(sa & sb) / len(union) if union else 0.0
    return matrix


def _communicate_partner(event: dict) -> str | None:
    primitive = event.get("primitive")
    if not isinstance(primitive, dict) or primitive.get("kind") != "communicate":
        return None
    args = primitive.get("args", {})
    if not isinstance(args, dict):
        return None
    message = args.get("message", {})
    if isinstance(message, dict):
        recipient = message.get("recipient")
        if recipient:
            return str(recipient)
    channel = str(args.get("channel", ""))
    if channel.startswith("dm_"):
        return channel.removeprefix("dm_")
    return None


def communicate_pair_edges(
    primitive_log: list[dict],
    *,
    tier: str = "full",
) -> list[tuple[str, str]]:
    projected = project_primitive_log(primitive_log, tier)
    edges: set[tuple[str, str]] = set()
    for event in projected:
        if event.get("status") != "ok":
            continue
        sender = event.get("actor_id")
        partner = _communicate_partner(event)
        if sender and partner and sender != partner:
            lo, hi = sorted((str(sender), str(partner)))
            edges.add((lo, hi))
    return sorted(edges)


def _union_find_clusters(edges: list[tuple[str, str]], actors: list[str]) -> dict[str, tuple[str, ...]]:
    parent = {actor: actor for actor in actors}

    def find(x: str) -> str:
        while parent[x] != x:
            x = parent[x]
        return x

    def union(x: str, y: str) -> None:
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for a, b in edges:
        if a in parent and b in parent:
            union(a, b)
    groups: dict[str, list[str]] = {}
    for actor in actors:
        root = find(actor)
        groups.setdefault(root, []).append(actor)
    return {f"unit_{i}": tuple(sorted(members)) for i, members in enumerate(groups.values(), start=1)}


def discovered_units_passive(
    primitive_log: list[dict],
    *,
    actor_ids: list[str] | None = None,
    tier: str = "full",
    min_jaccard: float = DEFAULT_MIN_JACCARD,
) -> dict[str, tuple[str, ...]]:
    """Merge coordination edges; partition every actor in ``actor_ids``."""
    projected = project_primitive_log(primitive_log, tier)
    actors = sorted(
        actor_ids
        if actor_ids is not None
        else {
            str(event.get("actor_id"))
            for event in projected
            if event.get("actor_id")
        }
    )
    if not actors:
        return {}
    edges = list(communicate_pair_edges(primitive_log, tier=tier))
    comm_fraction = {actor: _communicate_fraction(primitive_log, actor, tier=tier) for actor in actors}
    for pair, score in co_semantic_step_matrix(primitive_log, tier=tier).items():
        if score >= min_jaccard:
            edges.append(pair)
    for pair, score in co_activity_matrix(primitive_log, tier=tier, kind="communicate").items():
        if score < min_jaccard:
            continue
        a, b = pair
        if (
            comm_fraction.get(a, 0.0) >= DEFAULT_MIN_COMMUNICATE_FRACTION
            and comm_fraction.get(b, 0.0) >= DEFAULT_MIN_COMMUNICATE_FRACTION
        ):
            edges.append(pair)
    return _union_find_clusters(edges, actors)
