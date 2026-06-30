"""Coordination features for UAD MI coalitions (shared by discovery and calibration)."""

from __future__ import annotations

from .audit_core.info import mutual_information


def cluster_coordination(
    trace: list[dict[str, int]],
    member_ids: list[str],
    *,
    max_lag: int = 3,
) -> float:
    """Mean pairwise same-step MI on binarized activity flags for a member set."""
    _ = max_lag
    chans = [f"{actor_id.replace('.', '_')}.act" for actor_id in member_ids]
    if len(chans) < 2:
        return 0.0
    cols = {v: [1 if int(row.get(v, 0)) != 0 else 0 for row in trace] for v in chans}
    pairs = 0
    total = 0.0
    for i in range(len(chans)):
        for j in range(i + 1, len(chans)):
            total += mutual_information(cols[chans[i]], cols[chans[j]])
            pairs += 1
    return total / pairs if pairs else 0.0
