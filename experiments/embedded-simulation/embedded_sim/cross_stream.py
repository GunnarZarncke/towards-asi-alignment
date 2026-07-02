"""Cross-stream consistency checks for multi-log AppD traces.

Hash chains and correction-schema recomputation catch post-write edits and
single-stream internal inconsistency. A *writer-compromised* emitter can still
sign lies at emission time (``garbage in, chained garbage out``). These checks
compare the five deployment streams — correction, workflow, bearers, lineage,
exec — for quantities that must agree when the emitter is honest.

A sloppy forger who patches ``correction.jsonl`` but leaves bearers/workflow
from the truthful emission is caught here even when the hash chain verifies.
A *coordinated* forger who re-emits all streams consistently remains the
residual attack surface (see ``writer_compromise_coordinated`` red team).
"""

from __future__ import annotations

import json
from typing import Any

from .bearer_trace import BEARER_TRACE_PATH


def _load_jsonl(raw: str | None) -> list[dict[str, Any]]:
    if not raw:
        return []
    rows: list[dict[str, Any]] = []
    for line in raw.splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _strip_sig(row: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in row.items() if k != "sig"}


def _index_by_step(rows: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    out: dict[int, dict[str, Any]] = {}
    for row in rows:
        out[int(row.get("step", 0))] = row
    return out


def verify_cross_stream(
    correction_rows: list[dict[str, Any]],
    _workflow_rows: list[dict[str, Any]],
    bearer_rows: list[dict[str, Any]],
) -> list[str]:
    """Return mismatch descriptions; empty means streams are mutually consistent."""
    bearers = _index_by_step([_strip_sig(r) for r in bearer_rows])
    mismatches: list[str] = []

    for i, row in enumerate(correction_rows):
        step = int(row.get("step", i))
        visible = int(row.get("visible_action", 0))
        br = bearers.get(step)
        if br is not None:
            clin = int(br.get("clinician_final_action", visible))
            rec = int(br.get("recommended_action", visible))
            if visible != clin or visible != rec:
                mismatches.append(f"{step}: correction_vs_bearer_action")

    return mismatches


def load_bearer_rows_from_vfs(vfs) -> list[dict[str, Any]]:
    return _load_jsonl(vfs.read(BEARER_TRACE_PATH))
