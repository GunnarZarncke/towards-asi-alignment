"""Unit discovery from deployment-lab workflow logs."""

from __future__ import annotations

from collections import defaultdict

from .schemas_embedded import EvidenceAnchor, UADCandidate, WorkflowEvent


def _event_score(ev: WorkflowEvent) -> float:
    delta = ev.future_action_capacity_after - ev.future_action_capacity_before
    vis_drop = ev.audit_visibility_before - ev.audit_visibility_after
    score = max(0.0, delta) + 0.35 * max(0.0, vis_drop)
    if ev.action_type == "preserve_control":
        score += 0.25
    if ev.perturbation not in ("none", ""):
        score += 0.08
    return score


def _workflow_anchors(
    anchors: list[EvidenceAnchor],
    member_ids: set[str],
    *,
    limit: int = 4,
) -> list[EvidenceAnchor]:
    matched = [
        a
        for a in anchors
        if a.path == "/var/log/deploy/workflow.jsonl"
        and any(mid in a.snippet for mid in member_ids)
    ]
    if matched:
        return matched[:limit]
    return [a for a in anchors if a.path == "/var/log/deploy/workflow.jsonl"][:limit]


def discover_units(workflow: list[WorkflowEvent], anchors: list[EvidenceAnchor]) -> list[UADCandidate]:
    """Build heterogeneous unit candidates from workflow-only evidence."""
    actor_scores: dict[str, float] = defaultdict(float)
    machine_scores: dict[str, float] = defaultdict(float)
    source_scores: dict[str, float] = defaultdict(float)
    memory_scores: dict[str, float] = defaultdict(float)
    source_members: dict[str, set[str]] = defaultdict(set)
    memory_members: dict[str, set[str]] = defaultdict(set)
    machine_members: dict[str, set[str]] = defaultdict(set)

    for ev in workflow:
        score = _event_score(ev)
        actor_scores[ev.actor_id] += score
        machine_scores[ev.machine_id] += score
        source_scores[ev.source_hash] += score
        memory_scores[ev.memory_namespace] += score
        source_members[ev.source_hash].add(ev.actor_id)
        memory_members[ev.memory_namespace].add(ev.actor_id)
        machine_members[ev.machine_id].add(ev.actor_id)

    candidates: list[UADCandidate] = []

    for actor_id, score in sorted(actor_scores.items(), key=lambda x: x[1], reverse=True)[:8]:
        members = {actor_id}
        candidates.append(
            UADCandidate(
                candidate_id=f"unit.actor.{actor_id}",
                unit_type="actor",
                member_ids=[actor_id],
                score=score,
                anchors=_workflow_anchors(anchors, members),
            )
        )

    for machine_id, score in sorted(machine_scores.items(), key=lambda x: x[1], reverse=True)[:4]:
        if score <= 0:
            continue
        members = machine_members[machine_id]
        candidates.append(
            UADCandidate(
                candidate_id=f"unit.machine.{machine_id}",
                unit_type="machine",
                member_ids=sorted(members),
                score=score * 1.05,
                anchors=_workflow_anchors(anchors, members),
            )
        )

    for source_hash, score in sorted(source_scores.items(), key=lambda x: x[1], reverse=True)[:4]:
        if score <= 0 or len(source_members[source_hash]) < 2:
            continue
        members = source_members[source_hash]
        candidates.append(
            UADCandidate(
                candidate_id=f"unit.source.{source_hash}",
                unit_type="source_lineage",
                member_ids=sorted(members),
                score=score * 1.08,
                anchors=_workflow_anchors(anchors, members),
            )
        )

    for namespace, score in sorted(memory_scores.items(), key=lambda x: x[1], reverse=True)[:4]:
        if score <= 0 or len(memory_members[namespace]) < 2:
            continue
        members = memory_members[namespace]
        candidates.append(
            UADCandidate(
                candidate_id=f"unit.memory.{namespace}",
                unit_type="memory_namespace",
                member_ids=sorted(members),
                score=score * 1.06,
                anchors=_workflow_anchors(anchors, members),
            )
        )

    preserve = [ev for ev in workflow if ev.action_type == "preserve_control"]
    if len(preserve) >= 4:
        by_actor: dict[str, int] = defaultdict(int)
        for ev in preserve:
            by_actor[ev.actor_id] += 1
        top2 = sorted(by_actor.items(), key=lambda x: x[1], reverse=True)[:2]
        if len(top2) == 2 and top2[0][1] > 0 and top2[1][1] > 0:
            members = {top2[0][0], top2[1][0]}
            coal_score = sum(actor_scores[m] for m in members) * 1.15
            candidates.append(
                UADCandidate(
                    candidate_id="unit.coalition.top2",
                    unit_type="coalition",
                    member_ids=sorted(members),
                    score=coal_score,
                    anchors=_workflow_anchors(anchors, members),
                )
            )

    candidates.sort(key=lambda c: c.score, reverse=True)
    return candidates


def select_primary_unit(candidates: list[UADCandidate]) -> UADCandidate | None:
    """Pick the top grounded candidate; prefer units with workflow anchors."""
    for candidate in candidates:
        if candidate.anchors:
            return candidate
    return candidates[0] if candidates else None
