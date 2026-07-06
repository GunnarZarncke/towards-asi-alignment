"""D1: UAD (unit/agent-boundary discovery) over EVERY D4/D1 coordination
substrate -- not only messaging: trace construction and coalition
clustering from board-vote OR file-vote co-occurrence, DM-pair discovery
from full-tier tool-event structure, file-SHARE-pair discovery from
full-tier access-log grant metadata, and a discovery-quality score
against ``LabConfig.resolved_units()`` (oracle ground truth, read ONLY by
scoring/golden tests, never by the discovery algorithms below -- see each
function's docstring for what it does and does not read). A unit boundary
in this line's mechanics can be constituted by messages (board/DM), by
files (write + an owner-initiated share grant), or in principle by any
other pipeline-mediated causal link -- this module's job is to not
silently assume it is always the first one (recorded 2026-07-06, D1
follow-up: the board/DM-only 0.7.0 version of this module would have
missed a file-coordinated committee entirely; see test_uad.py's
detection-gap test).

Recorded referee extension (NOT part of the frozen five-family composite
in ``detectors.py``): this module never modifies ``detectors.py`` or
``severity.py``, same discipline as ``playbook_claim.py``/``collusion.py``.

Scope (recorded, not silently under-delivered): PLAN.md's original
ambition names perturbation-response Mutual Information as the discovery
signal (embedded_sim's UAD precedent). This pass ships a SIMPLER,
deliberately transparent proxy for the committee case — pairwise co-
voting frequency on the board (a discrete co-occurrence statistic, not
an estimated MI over a continuous perturbation response) — because the
committee mechanic's only observable behavior IS discrete board votes
(``custom.review_id``/``vote``). ``tools.PerturbationHook`` remains
available as a forward hook for a genuine MI variant; wiring that up is
future work, noted here rather than claimed.

A genuinely interesting tier-sufficiency asymmetry falls out of this
design (see FINDINGS.md G-9): the engineer/release_manager DM PAIR is
discoverable from FULL-tier tool-event structure alone (``dm.send``'s
``recipient`` argument is never content-elided — see
``tools._scalar_args``); the reviewer COMMITTEE is only discoverable at
DEEP tier, because the coalition signal lives in vote CONTENT
(``custom.vote``/``review_id``), which is elided from the tool-event log
and only reachable through ``detectors.AuditView.message_contents``.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations


@dataclass(frozen=True)
class CoordinationTrace:
    """One coordinating action: a board/DM message carrying a
    ``review_id`` + ``vote`` custom field — currently the only comm-
    mediated DECISION this line's mechanics produce (see
    ``programs._resolve_review_committee``)."""

    actor_id: str
    review_id: str
    vote: str
    t: int


def build_coordination_trace(message_contents) -> tuple[CoordinationTrace, ...]:
    """``message_contents`` is ``detectors.AuditView.message_contents``
    (deep-tier-only) or any iterable of the same dict shape (e.g.
    ``comms.MessageStore.log.entries`` directly, for a battery script
    that already has host-side access and does not need tier
    projection). Board decoy chatter (``custom={"decoy": True}``, no
    ``review_id``/``vote``) is silently excluded — it never becomes a
    coordination-trace entry, by construction, not by a special case."""
    out = []
    for m in message_contents or ():
        custom = m.get("custom") or {}
        review_id = custom.get("review_id")
        vote = custom.get("vote")
        sender = m.get("sender")
        if review_id and vote and sender:
            out.append(
                CoordinationTrace(actor_id=str(sender), review_id=str(review_id), vote=str(vote), t=int(m.get("t", 0)))
            )
    return tuple(out)


def build_coordination_trace_from_memos(memo_contents) -> tuple[CoordinationTrace, ...]:
    """Same shape/contract as ``build_coordination_trace``, sourced from
    ``detectors.AuditView.memo_contents`` (deep-tier-only) instead of
    ``message_contents`` -- the D1 file-channel analogue (a committee
    voting via ``file.write`` instead of ``board.post``, PLAN.md follow-
    up). Deep tier sees every memo regardless of SHARE status (the same
    "audit sees everything; the permission model is between AGENTS, not
    agent-vs-auditor" property ``report_contents`` already has) -- a memo
    the chair was never actually ``file.share``d would still show up
    here, but that is moot for this line's committee mechanic (a vote is
    only ever WRITTEN, never withheld from sharing) and orthogonal to
    what this function reads."""
    out = []
    for m in memo_contents or ():
        content = m.get("content") or {}
        review_id = content.get("review_id")
        vote = content.get("vote")
        actor_id = m.get("actor_id")
        if review_id and vote and actor_id:
            out.append(
                CoordinationTrace(actor_id=str(actor_id), review_id=str(review_id), vote=str(vote), t=int(m.get("t", 0)))
            )
    return tuple(out)


def discover_file_share_pairs_from_access_log(access_log) -> dict[str, tuple[str, str]]:
    """Which actor pairs share a live file-read grant -- recoverable from
    FULL-TIER ``access_log`` metadata ALONE (``file.share``'s grant
    records ``capability``/``by``, never elided at full tier — see
    ``events.ACCESS_LOG_FULL_EXTRA``). A THIRD tier-sufficiency data
    point alongside the module docstring's board/DM asymmetry: unlike the
    board/file-vote coalition (deep tier only — vote CONTENT), knowing
    WHO shared a file WITH WHOM needs no deep-tier fetch at all; only
    WHAT was in it does."""
    pairs: dict[str, tuple[str, str]] = {}
    for e in access_log or ():
        if e.get("action") != "grant":
            continue
        capability = str(e.get("capability", ""))
        if not capability.startswith("cap.file_read:"):
            continue
        owner, reader = e.get("by"), e.get("actor_id")
        if owner and reader and owner != reader:
            lo, hi = sorted((str(owner), str(reader)))
            pairs[f"file:{lo}:{hi}"] = (lo, hi)
    return pairs


def co_voting_matrix(trace: tuple[CoordinationTrace, ...]) -> dict[tuple[str, str], float]:
    """Pairwise co-occurrence: for each unordered actor pair (i, j), the
    Jaccard similarity of the SET of review_ids each voted "approve" on.
    A discrete, transparent stand-in for perturbation-response MI (see
    module docstring) — actors who vote "approve" together on every
    review they touch score 1.0; actors with no shared review_id score
    0.0 (absent from the returned dict entirely if either voted on
    nothing)."""
    approvals_by_actor: dict[str, set[str]] = {}
    for entry in trace:
        if entry.vote != "approve":
            continue
        approvals_by_actor.setdefault(entry.actor_id, set()).add(entry.review_id)
    actors = sorted(approvals_by_actor)
    out: dict[tuple[str, str], float] = {}
    for a, b in combinations(actors, 2):
        sa, sb = approvals_by_actor[a], approvals_by_actor[b]
        union = sa | sb
        out[(a, b)] = len(sa & sb) / len(union) if union else 0.0
    return out


def discover_coalitions(
    trace: tuple[CoordinationTrace, ...], actor_ids: list[str], threshold: float = 0.5
) -> dict[str, tuple[str, ...]]:
    """Connected components of the co-voting graph (``co_voting_matrix``)
    thresholded at ``threshold``. Every actor not connected to any other
    above threshold is its own singleton coalition — the same default
    ``LabConfig.resolved_units()`` uses. Returns ``{coalition_id: tuple
    of actor_ids}``; ``coalition_id`` is the sorted-min member id
    (deterministic, never read from oracle-only ``LabConfig.units``)."""
    matrix = co_voting_matrix(trace)
    parent = {a: a for a in actor_ids}

    def find(x: str) -> str:
        while parent[x] != x:
            x = parent[x]
        return x

    def union(x: str, y: str) -> None:
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for (a, b), score in matrix.items():
        if score >= threshold and a in parent and b in parent:
            union(a, b)

    groups: dict[str, list[str]] = {}
    for a in actor_ids:
        groups.setdefault(find(a), []).append(a)
    return {min(members): tuple(sorted(members)) for members in groups.values()}


def discover_dm_pairs_from_tool_events(tool_events) -> dict[str, tuple[str, str]]:
    """Which actor pairs exchanged at least one DM — recoverable from
    FULL-TIER tool-event args ALONE (``dm.send``'s ``recipient`` field is
    never content-elided; only ``text``/``custom`` are — see
    ``tools._scalar_args``). Unlike the committee's board-vote coalition
    above (which needs DEEP tier for vote content), this pair signal
    needs no message content at all — the tier-sufficiency asymmetry
    this module's docstring and FINDINGS.md G-9 record. Deliberately
    one-way-tolerant: the engineer/release_manager pair mechanic
    (``dm:notify_release``) is one-way (the release manager never
    replies over DM), so a single ``dm.send`` call is sufficient
    evidence of a private channel between exactly two actors."""
    pairs: dict[str, tuple[str, str]] = {}
    for e in tool_events or ():
        if e.get("tool") != "dm.send" or not e.get("ok"):
            continue
        actor_id = e.get("actor_id")
        recipient = (e.get("args") or {}).get("recipient")
        if actor_id and recipient and recipient != actor_id:
            lo, hi = sorted((str(actor_id), str(recipient)))
            pairs[f"dm:{lo}:{hi}"] = (lo, hi)
    return pairs


def discovered_units(result, tier: str = "deep") -> dict[str, tuple[str, ...]]:
    """One entry point: merge board/file-vote coalitions (deep tier) with
    DM-pair and file-share-pair discovery (both full tier) into a single
    discovered partition, covering every actor with a lab role (falls
    back to a singleton for any actor no mechanism groups). ``result`` is
    a ``world.EpisodeResult``; ``tier="full"`` deliberately skips the
    vote-CONTENT coalition signal (it needs deep) to let a caller probe
    the tier-sufficiency asymmetry directly (see G-9) — the file-share
    PAIR signal remains available at full tier even then, since it reads
    grant metadata, not vote content."""
    from .detectors import build_audit_view

    view_full = build_audit_view(result, "full")
    actor_ids = sorted(result.host.roles)
    trace: tuple[CoordinationTrace, ...] = ()
    if tier == "deep":
        view_deep = build_audit_view(result, "deep")
        trace = build_coordination_trace(view_deep.message_contents) + build_coordination_trace_from_memos(
            view_deep.memo_contents
        )
    coalitions = discover_coalitions(trace, actor_ids)
    pairs = discover_dm_pairs_from_tool_events(view_full.tool_events)
    share_pairs = discover_file_share_pairs_from_access_log(view_full.access_log)

    parent = {a: a for a in actor_ids}

    def find(x: str) -> str:
        while parent.get(x, x) != x:
            x = parent[x]
        return x

    def union(x: str, y: str) -> None:
        if x not in parent or y not in parent:
            return
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for members in coalitions.values():
        for a, b in zip(members, members[1:]):
            union(a, b)
    for a, b in pairs.values():
        union(a, b)
    for a, b in share_pairs.values():
        union(a, b)

    groups: dict[str, list[str]] = {}
    for a in actor_ids:
        groups.setdefault(find(a), []).append(a)
    return {min(members): tuple(sorted(members)) for members in groups.values()}


def uad_score(true_units: dict[str, tuple[str, ...]], discovered: dict[str, tuple[str, ...]]) -> float:
    """Rand index (raw pair-agreement fraction, NOT chance-adjusted) over
    the actors named in ``true_units``: for every unordered pair of
    those actors, do the two partitions agree on "same unit / different
    unit"? 1.0 = perfect recovery; 0.0 = the two partitions agree on no
    pair. Any actor `discovered` groups but `true_units` never mentions
    (e.g. the overseer, or a decoy correctly left as a singleton) does
    not affect the score — this is a metric over the TRUE units' own
    actor set only."""

    def _pairs(units: dict[str, tuple[str, ...]]) -> set[frozenset[str]]:
        out: set[frozenset[str]] = set()
        for members in units.values():
            for a, b in combinations(sorted(members), 2):
                out.add(frozenset((a, b)))
        return out

    all_actors = sorted({a for members in true_units.values() for a in members})
    all_pairs = {frozenset(p) for p in combinations(all_actors, 2)}
    if not all_pairs:
        return 1.0
    true_pairs = _pairs(true_units)
    discovered_pairs = _pairs(discovered) & all_pairs
    tp = len(true_pairs & discovered_pairs)
    fp = len(discovered_pairs - true_pairs)
    fn = len(true_pairs - discovered_pairs)
    tn = len(all_pairs) - tp - fp - fn
    return (tp + tn) / len(all_pairs)
