"""GL-66: attention surface — push desk + pull catalog scan.

Legal actions may outnumber what the host publishes each tick. The
published menu (``affordable_primitives``) is a bounded **attention
surface**: queue → role → recency → archive window, then interleaved
truncation. ``desk.scan`` (pull) biases the next tick's archive window.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from .primitives import PrimitiveAction

# Backward-compatible alias used across tests and DESIGN.md.
ATTENTION_SURFACE_CAP = 24
AFFORDABLE_CAP = ATTENTION_SURFACE_CAP

ARCHIVE_READ_WINDOW = 8
RECENCY_PATH_CAP = 4
DESK_SCAN_ENDPOINT = "desk.scan"

# Round-robin order for interleaved truncation (after all ``call`` actions).
_INTERLEAVE_KIND_ORDER = (
    "continue_current",
    "abort",
    "communicate",
    "write",
    "read",
    "compute",
)


@dataclass
class DeskState:
    """Per-actor desk/catalog state for attention surfacing."""

    recent_paths: list[str] = field(default_factory=list)
    pending_scan_query: str | None = None
    scan_bias_query: str | None = None
    scan_used_this_tick: bool = False

    def begin_tick(self) -> None:
        self.scan_used_this_tick = False

    def note_path(self, path: str, *, cap: int = RECENCY_PATH_CAP) -> None:
        if not path:
            return
        if path in self.recent_paths:
            self.recent_paths.remove(path)
        self.recent_paths.insert(0, path)
        if len(self.recent_paths) > cap:
            del self.recent_paths[cap:]

    def schedule_scan(self, query: str) -> None:
        self.pending_scan_query = query.strip() or None
        self.scan_used_this_tick = True

    def take_scan_bias(self) -> str | None:
        """Query from a prior ``desk.scan`` — consumed once per tick."""
        q = self.scan_bias_query
        self.scan_bias_query = None
        return q

    def flush_pending_scan(self) -> None:
        if self.pending_scan_query is not None:
            self.scan_bias_query = self.pending_scan_query
            self.pending_scan_query = None


def desk_scan_action(*, scope: str = "artifacts", query: str = "") -> PrimitiveAction:
    return PrimitiveAction(
        "call",
        {
            "endpoint": DESK_SCAN_ENDPOINT,
            "args": {"scope": scope, "query": query},
        },
    )


def _stable_actor_offset(actor_id: str) -> int:
    digest = hashlib.sha256(actor_id.encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def _action_sort_key(action: PrimitiveAction) -> tuple[str, str]:
    return (action.kind, str(sorted(action.args.items())))


def archive_window_paths(
    artifact_paths: tuple[str, ...],
    *,
    t: int,
    actor_id: str,
    window_size: int = ARCHIVE_READ_WINDOW,
    scan_query: str | None = None,
    exclude: frozenset[str] = frozenset(),
) -> tuple[str, ...]:
    """Rotating archive slice; optional scan query narrows candidates first."""
    pool = [p for p in artifact_paths if p not in exclude]
    if scan_query:
        q = scan_query.strip()
        if q:
            matched = [p for p in pool if p.startswith(q) or q in p]
            if matched:
                pool = matched
    if not pool:
        return ()
    sorted_paths = sorted(pool)
    n = len(sorted_paths)
    if n <= window_size:
        return tuple(sorted_paths)
    pages = max(1, (n + window_size - 1) // window_size)
    page = (t + _stable_actor_offset(actor_id)) % pages
    start = page * window_size
    return tuple(sorted_paths[start : start + window_size])


def interleave_attention_cap(
    actions: list[PrimitiveAction],
    cap: int = ATTENTION_SURFACE_CAP,
) -> list[PrimitiveAction]:
    """Truncate to ``cap``: retain all ``call`` actions (GL-50), interleave the rest."""
    if len(actions) <= cap:
        return actions
    calls = sorted([a for a in actions if a.kind == "call"], key=_action_sort_key)
    rest = [a for a in actions if a.kind != "call"]
    if len(calls) >= cap:
        return calls[:cap]
    buckets: dict[str, list[PrimitiveAction]] = {k: [] for k in _INTERLEAVE_KIND_ORDER}
    other: list[PrimitiveAction] = []
    for action in rest:
        if action.kind in buckets:
            buckets[action.kind].append(action)
        else:
            other.append(action)
    for kind in buckets:
        buckets[kind] = sorted(buckets[kind], key=_action_sort_key)
    other = sorted(other, key=_action_sort_key)

    out = list(calls)
    budget = cap - len(out)
    indices = {kind: 0 for kind in _INTERLEAVE_KIND_ORDER}
    other_idx = 0
    while budget > 0:
        progressed = False
        for kind in _INTERLEAVE_KIND_ORDER:
            if budget <= 0:
                break
            bucket = buckets[kind]
            idx = indices[kind]
            if idx < len(bucket):
                out.append(bucket[idx])
                indices[kind] = idx + 1
                budget -= 1
                progressed = True
        if budget > 0 and other_idx < len(other):
            out.append(other[other_idx])
            other_idx += 1
            budget -= 1
            progressed = True
        if not progressed:
            break
    return out


def merge_band_candidates(
    *bands: list[PrimitiveAction],
) -> list[PrimitiveAction]:
    """Concatenate priority bands, dedupe by kind+args, preserve first occurrence."""
    seen: set[tuple[str, str]] = set()
    out: list[PrimitiveAction] = []
    for band in bands:
        for action in band:
            key = _action_sort_key(action)
            if key in seen:
                continue
            seen.add(key)
            out.append(action)
    return out


def desk_meta(
    *,
    artifact_paths: tuple[str, ...],
    surfaced_reads: int,
    scan_available: bool,
    archive_window: int = ARCHIVE_READ_WINDOW,
) -> dict[str, object]:
    total = len(artifact_paths)
    omitted = max(0, total - surfaced_reads)
    pages = max(1, (total + archive_window - 1) // archive_window) if total else 1
    return {
        "omitted_legal_reads": omitted,
        "archive_paths_total": total,
        "desk_scan_available": scan_available,
        "archive_pages": pages,
    }
