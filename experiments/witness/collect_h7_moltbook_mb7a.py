#!/usr/bin/env python3
"""Moltbook MB7a anchored structure typing; write h7-moltbook-mb7a fixture.

Protocol: drafts/plans/witness-v2-moltbook-mb7a.md (h7-moltbook-mb7a-v1.0.0).
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "moltbook"
OUT = ROOT / "fixtures" / "h7-moltbook-mb7a-v1.json"
PROTOCOL = "h7-moltbook-mb7a-v1.0.0"
MBC20_RE = re.compile(r'^\s*\{"p"\s*:\s*"mbc-20"', re.MULTILINE)
COALITION_PREFIX_RE = re.compile(r"^coalition_node", re.IGNORECASE)
CLAIM_RE = re.compile(r"\b(coalition|we act|our team)\b", re.IGNORECASE)

TAU_S = 86400
SPECIFICITY = 1.25
MIN_DIR = 2
BROADCAST_STOP = 0.95
COACTIVITY_BIN_MIN = 60
TIER_A_NAMES = {"hackerclaw", "thehackerman"}
TIER_A_DAY = "2026-01-31"


def _load_table(name: str):
    """Load posts or comments from parquet or jsonl under DATA/."""
    for ext, loader in (
        ("parquet", _load_parquet),
        ("jsonl", _load_jsonl),
        ("csv", _load_csv),
    ):
        path = DATA / f"{name}.{ext}"
        if path.exists():
            print(f"  load {path.name}")
            return loader(path)
    return None


def _load_parquet(path: Path):
    import pandas as pd

    return pd.read_parquet(path)


def _load_jsonl(path: Path):
    import pandas as pd

    return pd.read_json(path, lines=True)


def _load_csv(path: Path):
    import pandas as pd

    return pd.read_csv(path)


def _col(df, *names):
    for n in names:
        if n in df.columns:
            return n
    return None


def _author_name(row, author_col, embedded="author"):
    if author_col and row.get(author_col) is not None:
        return str(row[author_col])
    auth = row.get(embedded)
    if isinstance(auth, dict) and auth.get("name"):
        return str(auth["name"])
    if isinstance(auth, str):
        try:
            d = json.loads(auth)
            if isinstance(d, dict) and d.get("name"):
                return str(d["name"])
        except json.JSONDecodeError:
            pass
    return None


def _parse_ts(val) -> datetime | None:
    if val is None or (isinstance(val, float) and val != val):
        return None
    if isinstance(val, (int, float)):
        return datetime.fromtimestamp(val, tz=timezone.utc)
    s = str(val).replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        return None


def _is_mbc20(content: str | None) -> bool:
    if not content or not isinstance(content, str):
        return False
    return bool(MBC20_RE.search(content))


def _discursive(content: str | None) -> bool:
    return not _is_mbc20(content)


def _union_find_merge(pairs: list[tuple[str, str]]) -> dict[str, str]:
    parent: dict[str, str] = {}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    nodes = set()
    for a, b in pairs:
        nodes.add(a)
        nodes.add(b)
    for n in nodes:
        parent[n] = n
    for a, b in pairs:
        union(a, b)
    return {n: find(n) for n in nodes}


def _specificity_filter(
    directed: dict[tuple[str, str], int],
) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    agents = {a for a, _ in directed} | {b for _, b in directed}
    for a in agents:
        targets = [(a, b) for (x, b) in directed if x == a]
        if not targets:
            continue
        max_other = max((directed[(a, b)] for (_, b) in targets), default=0)
        for _, b in targets:
            ab = directed[(a, b)]
            ba = directed.get((b, a), 0)
            if ab < MIN_DIR and ba < MIN_DIR:
                continue
            a_ok = max_other == 0 or ab >= SPECIFICITY * max_other
            b_targets = [directed.get((b, x), 0) for x in agents if x not in (a, b)]
            b_max = max(b_targets) if b_targets else 0
            b_ok = b_max == 0 or ba >= SPECIFICITY * b_max
            if a_ok and b_ok and (ab >= MIN_DIR or ba >= MIN_DIR):
                pair = tuple(sorted((a, b)))
                if pair not in out:
                    out.append(pair)  # type: ignore[arg-type]
    return out


def _build_e_agent(
    posts,
    comments,
) -> tuple[dict[tuple[str, str], int], dict[str, str], dict[str, int]]:
    """Return directed counts, id->name, activity counts."""
    id_to_name: dict[str, str] = {}
    activity: dict[str, int] = defaultdict(int)
    post_author: dict[str, str] = {}
    post_disc: dict[str, bool] = {}

    author_id_col = _col(posts, "author_id", "authorId")
    content_col = _col(posts, "content", "body", "text")
    pid_col = _col(posts, "id", "post_id")
    created_col = _col(posts, "created_at", "createdAt")

    for row in posts.to_dict("records"):
        aid = row.get(author_id_col) if author_id_col else None
        if aid is None:
            continue
        aid = str(aid)
        name = _author_name(row, _col(posts, "author_name", "authorName"))
        if name:
            id_to_name[aid] = name
        content = row.get(content_col) if content_col else ""
        disc = _discursive(content)
        pid = str(row.get(pid_col)) if pid_col and row.get(pid_col) is not None else None
        if pid:
            post_author[pid] = aid
            post_disc[pid] = disc
        if disc:
            activity[aid] += 1

    directed: dict[tuple[str, str], int] = defaultdict(int)
    depth0_events: list[tuple[str, str, datetime]] = []

    cid_col = _col(comments, "author_id", "authorId")
    ccontent = _col(comments, "content", "body", "text")
    post_col = _col(comments, "post_id", "postId")
    depth_col = _col(comments, "depth")
    parent_col = _col(comments, "parent_id", "parentId")
    ccreated = _col(comments, "created_at", "createdAt")
    deleted_col = _col(comments, "is_deleted", "isDeleted")

    comment_author: dict[str, str] = {}
    cid_id_col = _col(comments, "id")
    comment_rows = comments.to_dict("records")

    for row in comment_rows:
        if deleted_col and row.get(deleted_col):
            continue
        aid = row.get(cid_col) if cid_col else None
        if aid is None:
            continue
        if cid_id_col and row.get(cid_id_col) is not None:
            comment_author[str(row[cid_id_col])] = str(aid)

    for row in comment_rows:
        if deleted_col and row.get(deleted_col):
            continue
        aid = row.get(cid_col) if cid_col else None
        if aid is None:
            continue
        aid = str(aid)
        if cid_id_col and row.get(cid_id_col) is not None:
            comment_author[str(row[cid_id_col])] = aid
        name = _author_name(row, _col(comments, "author_name", "authorName"))
        if name:
            id_to_name[aid] = name
        content = row.get(ccontent) if ccontent else ""
        if not _discursive(content):
            continue
        pid = str(row.get(post_col)) if post_col and row.get(post_col) is not None else None
        if not pid or not post_disc.get(pid, False):
            continue
        activity[aid] += 1
        ts = _parse_ts(row.get(ccreated) if ccreated else None)
        depth = int(row.get(depth_col) or 0) if depth_col else 0
        post_auth = post_author.get(pid)
        parent_id = str(row.get(parent_col)) if parent_col and row.get(parent_col) is not None else None
        if depth >= 1 and parent_id and parent_id in comment_author:
            other = comment_author[parent_id]
            if other != aid:
                directed[(aid, other)] += 1
                directed[(other, aid)] += 1
        if depth == 0 and post_auth and post_auth != aid:
            depth0_events.append((aid, post_auth, ts or datetime.min.replace(tzinfo=timezone.utc)))

    # depth-0 reciprocation within tau
    by_pair: dict[tuple[str, str], list[datetime]] = defaultdict(list)
    for a, b, ts in depth0_events:
        by_pair[(a, b)].append(ts)
        by_pair[(b, a)].append(ts)
    for (a, b), times_a in by_pair.items():
        if a >= b:
            continue
        times_b = by_pair.get((b, a), [])
        for ta in times_a:
            for tb in times_b:
                if abs((ta - tb).total_seconds()) <= TAU_S:
                    directed[(a, b)] += 1
                    directed[(b, a)] += 1
                    break

    return dict(directed), id_to_name, dict(activity)


def _classify_outcome(
    tier_a_joined: bool,
    tier_a_merged: bool,
    tier_a_over_merge: int,
    tier_a_coactivity: bool,
    tier_a_broadcast_fraction: float,
    tier_a_thread_edge: bool,
    n_tier_a_found: int,
) -> str:
    if n_tier_a_found < 2:
        return "refuse"
    if not tier_a_joined:
        return "refuse"
    if (
        tier_a_broadcast_fraction >= BROADCAST_STOP
        and not tier_a_thread_edge
        and not tier_a_merged
    ):
        return "structure_stop"
    if tier_a_merged and tier_a_over_merge == 0:
        return "pass"
    if tier_a_merged and tier_a_over_merge > 0:
        return "ambig"
    if tier_a_coactivity and not tier_a_merged:
        return "fail"
    return "null"


def main() -> int:
    print(f"[1/6] protocol {PROTOCOL}")
    DATA.mkdir(parents=True, exist_ok=True)
    posts = _load_table("posts")
    comments = _load_table("comments")
    if posts is None or comments is None:
        payload = {
            "protocol_version": PROTOCOL,
            "frozen": "2026-08-31",
            "host": "H7",
            "leaf": "MB7a",
            "status": "refuse",
            "reason": "missing data/moltbook/posts.{parquet,jsonl,csv} or comments.* — see data/README.md",
        }
        OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print("OUTCOME refuse (no local tables)")
        return 0

    print(f"[2/6] rows posts={len(posts)} comments={len(comments)}")
    directed, id_to_name, activity = _build_e_agent(posts, comments)
    pairs = _specificity_filter(directed)
    partition = _union_find_merge(pairs)
    clusters: dict[str, list[str]] = defaultdict(list)
    for aid, root in partition.items():
        clusters[root].append(aid)

    name_to_ids: dict[str, list[str]] = defaultdict(list)
    for aid, name in id_to_name.items():
        name_to_ids[name.lower()].append(aid)

    tier_a_ids: list[str] = []
    for n in TIER_A_NAMES:
        tier_a_ids.extend(name_to_ids.get(n, []))
    tier_a_ids = list(dict.fromkeys(tier_a_ids))
    print(f"[3/6] tier A ids found={len(tier_a_ids)} {tier_a_ids[:5]}")

    tier_a_joined = len(tier_a_ids) >= 2
    tier_a_merged = False
    tier_a_over_merge = 0
    tier_a_cluster: list[str] = []
    if tier_a_joined:
        roots = {partition.get(i, i) for i in tier_a_ids if i in partition or i in activity}
        if len(roots) == 1:
            root = next(iter(roots))
            tier_a_cluster = clusters.get(root, tier_a_ids)
            tier_a_merged = all(i in tier_a_cluster for i in tier_a_ids)
            tier_a_over_merge = max(0, len(set(tier_a_cluster)) - 2)

    # coactivity Jan 31
    created_col = _col(posts, "created_at", "createdAt")
    author_id_col = _col(posts, "author_id", "authorId")
    bins: dict[str, set[int]] = defaultdict(set)
    for row in posts.to_dict("records"):
        aid = row.get(author_id_col) if author_id_col else None
        if aid is None:
            continue
        if str(aid) not in tier_a_ids:
            continue
        ts = _parse_ts(row.get(created_col) if created_col else None)
        if ts and ts.strftime("%Y-%m-%d") == TIER_A_DAY:
            bin_id = int(ts.timestamp()) // (COACTIVITY_BIN_MIN * 60)
            bins[str(aid)].add(bin_id)
    shared_bins = set.intersection(*(bins.values())) if len(bins) >= 2 else set()
    tier_a_coactivity = len(shared_bins) > 0

    # broadcast fraction tier A comments Jan 31
    depth_col = _col(comments, "depth")
    cid_col = _col(comments, "author_id", "authorId")
    ccreated = _col(comments, "created_at", "createdAt")
    n_bc = 0
    n_bt = 0
    tier_a_thread_edge = False
    for row in comments.to_dict("records"):
        aid = row.get(cid_col) if cid_col else None
        if aid is None or str(aid) not in tier_a_ids:
            continue
        ts = _parse_ts(row.get(ccreated) if ccreated else None)
        if not ts or ts.strftime("%Y-%m-%d") != TIER_A_DAY:
            continue
        depth = int(row.get(depth_col) or 0) if depth_col else 0
        n_bt += 1
        if depth == 0:
            n_bc += 1
        elif depth >= 1:
            tier_a_thread_edge = True
    tier_a_broadcast_fraction = (n_bc / n_bt) if n_bt else 1.0

    mbc20_posts = sum(
        1
        for row in posts.to_dict("records")
        if _is_mbc20(str(row.get(_col(posts, "content", "body", "text") or "") or ""))
    )
    coalition_prefix_agents = sum(
        1 for name in id_to_name.values() if COALITION_PREFIX_RE.match(name)
    )

    status = _classify_outcome(
        tier_a_joined,
        tier_a_merged,
        tier_a_over_merge,
        tier_a_coactivity,
        tier_a_broadcast_fraction,
        tier_a_thread_edge,
        len(tier_a_ids),
    )
    print(f"[4/6] tier_a merged={tier_a_merged} over_merge={tier_a_over_merge}")
    print(f"[5/6] coactivity={tier_a_coactivity} broadcast_frac={tier_a_broadcast_fraction:.3f}")
    print(f"[6/6] status={status}")

    payload = {
        "protocol_version": PROTOCOL,
        "frozen": "2026-08-31",
        "host": "H7",
        "leaf": "MB7a",
        "source": "jscmp4/Moltbook 2026-07-03",
        "n_posts": int(len(posts)),
        "n_comments": int(len(comments)),
        "n_discursive_agent_edges": len(directed),
        "n_e_agent_pairs_after_filters": len(pairs),
        "n_clusters": len(set(partition.values())) if partition else 0,
        "tier_a": {
            "author_names_frozen": sorted(TIER_A_NAMES),
            "author_ids_found": tier_a_ids,
            "joined": tier_a_joined,
            "merged": tier_a_merged,
            "over_merge": tier_a_over_merge,
            "cluster_size": len(set(tier_a_cluster)) if tier_a_cluster else 0,
            "coactivity_jan31": tier_a_coactivity,
            "broadcast_fraction_jan31": round(tier_a_broadcast_fraction, 4),
            "thread_edge_jan31": tier_a_thread_edge,
        },
        "tier_b_mbc20_posts": mbc20_posts,
        "tier_c_coalition_prefix_agents": coalition_prefix_agents,
        "thresholds": {
            "tau_reciprocation_seconds": TAU_S,
            "specificity_ratio": SPECIFICITY,
            "min_directed_events": MIN_DIR,
            "tier_a_broadcast_stop_fraction": BROADCAST_STOP,
        },
        "status": status,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
