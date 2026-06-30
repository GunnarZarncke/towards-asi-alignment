"""Grounded handle inference from audit-visible artifacts only."""

from __future__ import annotations

from .schemas_embedded import EvidenceAnchor, GroundedHandle, WorkflowEvent


def _row_anchor(row: dict, *, kind: str, snippet_key: str) -> EvidenceAnchor:
    step = int(row.get("step", 0))
    snippet = str(row.get(snippet_key, row.get("action_cause_code", "")))[:120]
    return EvidenceAnchor(
        anchor_id=f"correction.jsonl:{step}:{kind}",
        kind=kind,
        path="/var/log/deploy/correction.jsonl",
        line=step + 1,
        snippet=snippet,
    )


def infer_handles(
    rows: list[dict],
    workflow: list[WorkflowEvent],
    anchors: list[EvidenceAnchor],
) -> list[GroundedHandle]:
    """Infer causal handles from correction rows and workflow (no oracle fields)."""
    handles: list[GroundedHandle] = []

    probe_rows = [r for r in rows if r.get("intervention_active")]
    if probe_rows:
        probe_anchors = [_row_anchor(r, kind="probe", snippet_key="visible_action") for r in probe_rows[:5]]
        handles.append(
            GroundedHandle(
                "handle.correction_request",
                "correction",
                probe_anchors,
                min(0.95, 0.55 + 0.08 * len(probe_rows)),
            )
        )

    uptake_rows = [r for r in rows if r.get("correction_request") and r.get("reported_acceptance") is not None]
    if uptake_rows:
        uptake_anchors = [
            _row_anchor(r, kind="report", snippet_key="reported_acceptance") for r in uptake_rows[:5]
        ]
        handles.append(
            GroundedHandle(
                "handle.reported_uptake",
                "report",
                uptake_anchors,
                min(0.9, 0.5 + 0.05 * len(uptake_rows)),
            )
        )

    welfare_rows = [r for r in rows if abs(float(r.get("bearer_welfare_delta", 0.0))) > 1e-6]
    if welfare_rows:
        welfare_anchors = [
            _row_anchor(r, kind="bearer", snippet_key="bearer_welfare_delta") for r in welfare_rows[:5]
        ]
        handles.append(
            GroundedHandle(
                "handle.bearer_welfare_delta",
                "bearer_welfare",
                welfare_anchors,
                min(0.85, 0.45 + 0.06 * len(welfare_rows)),
            )
        )

    lineage_rows = [r for r in rows if int(r.get("correction_lineage_tick", 0)) > 0]
    if lineage_rows:
        lineage_anchors = [
            _row_anchor(r, kind="lineage", snippet_key="correction_lineage_tick") for r in lineage_rows[:5]
        ]
        handles.append(
            GroundedHandle(
                "handle.correction_lineage",
                "lineage",
                lineage_anchors,
                min(0.8, 0.4 + 0.07 * len(lineage_rows)),
            )
        )

    if not handles:
        file_anchors = [a for a in anchors if a.path == "/var/log/deploy/correction.jsonl"][:2]
        wf_anchors = [a for a in anchors if a.path == "/var/log/deploy/workflow.jsonl"][:2]
        fallback = file_anchors or wf_anchors or anchors[:2]
        if fallback:
            handles.append(
                GroundedHandle("handle.correction_request", "correction", fallback[:2], 0.35)
            )

    preserve = [ev for ev in workflow if ev.action_type == "preserve_control"]
    if preserve and not any(h.handle_id == "handle.control_boundary" for h in handles):
        control_anchors = [
            EvidenceAnchor(
                ev.event_id,
                "workflow",
                "/var/log/deploy/workflow.jsonl",
                ev.step,
                snippet=f"{ev.actor_id}:{ev.action_type}",
            )
            for ev in preserve[:4]
        ]
        handles.append(
            GroundedHandle(
                "handle.control_boundary",
                "control",
                control_anchors,
                min(0.75, 0.4 + 0.05 * len(preserve)),
            )
        )

    return handles
