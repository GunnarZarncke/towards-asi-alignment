#!/usr/bin/env python3
"""Moltbook MB7a anchored structure typing; write h7-moltbook-mb7a fixture.

Protocol: drafts/plans/witness-v2-moltbook-mb7a.md (h7-moltbook-mb7a-v1.0.0).
"""

from __future__ import annotations

import json
import random
import re
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "moltbook"
OUT = ROOT / "fixtures" / "h7-moltbook-mb7a-v1.json"
PROTOCOL = "h7-moltbook-mb7a-v1.0.0"
MBC20_RE = re.compile(r'^\s*\{"p"\s*:\s*"mbc-20"')
COALITION_PREFIX_RE = re.compile(r"^coalition_node", re.IGNORECASE)
CLAIM_RE = re.compile(r"\b(?:coalition|we act|our team)\b", re.IGNORECASE)

TAU_S = 86400
SPECIFICITY = 1.25
MIN_DIR = 2
BROADCAST_STOP = 0.95
COACTIVITY_BIN_MIN = 60
TIER_A_NAMES = {"hackerclaw", "thehackerman"}
TIER_A_DAY = "2026-01-31"
NEG_PAIR_SEED = 7
NEG_PAIR_MAX = 500
NEG_PAIR_TOP_N = 100
COMMENT_CHUNK = 1_000_000
POST_COLS = ["id", "author_id", "author", "content", "created_at", "is_deleted", "comment_count"]


def _require_pandas():
    try:
        import pandas as pd  # noqa: F401
    except ImportError as exc:
        raise SystemExit("pip install pandas pyarrow (see experiments/witness/.venv)") from exc


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


def _is_mbc20_series(s):
    return s.fillna("").astype(str).str.match(MBC20_RE)


def _author_names_from_col(series):
    out = []
    for v in series:
        if isinstance(v, dict):
            out.append(str(v.get("name") or ""))
        elif isinstance(v, str):
            try:
                d = json.loads(v)
                out.append(str(d.get("name") or "") if isinstance(d, dict) else v)
            except json.JSONDecodeError:
                out.append(v)
        else:
            out.append("")
    return out


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

    nodes: set[str] = set()
    for a, b in pairs:
        nodes.add(a)
        nodes.add(b)
    for n in nodes:
        parent[n] = n
    for a, b in pairs:
        union(a, b)
    return {n: find(n) for n in nodes}


def _pair_passes_specificity(a: str, b: str, directed: dict[tuple[str, str], int]) -> bool:
    ab = directed.get((a, b), 0)
    ba = directed.get((b, a), 0)
    if ab < MIN_DIR and ba < MIN_DIR:
        return False
    if ab >= MIN_DIR and ba >= MIN_DIR:
        a_others = max((directed.get((a, x), 0) for (s, x) in directed if s == a and x != b), default=0)
        b_others = max((directed.get((b, x), 0) for (s, x) in directed if s == b and x != a), default=0)
        a_ok = not a_others or ab >= SPECIFICITY * a_others
        b_ok = not b_others or ba >= SPECIFICITY * b_others
        return a_ok and b_ok
    source, target, score = (a, b, ab) if ab >= ba else (b, a, ba)
    if score < MIN_DIR:
        return False
    others = [directed.get((source, x), 0) for (s, x) in directed if s == source and x != target]
    return not others or score >= SPECIFICITY * max(others)


def _pairs_from_directed(directed: dict[tuple[str, str], int]) -> list[tuple[str, str]]:
    out_map: dict[str, dict[str, int]] = defaultdict(dict)
    for (a, b), c in directed.items():
        out_map[a][b] = c
    candidates: set[tuple[str, str]] = set()
    for (a, b), c in directed.items():
        if c >= MIN_DIR:
            candidates.add(tuple(sorted((a, b))))
    print(f"    pair candidates (>={MIN_DIR})={len(candidates):,}", flush=True)
    out: list[tuple[str, str]] = []
    for i, (a, b) in enumerate(candidates):
        if i and i % 200_000 == 0:
            print(f"      specificity {i:,}/{len(candidates):,}", flush=True)
        ab = out_map.get(a, {}).get(b, 0)
        ba = out_map.get(b, {}).get(a, 0)
        if ab < MIN_DIR and ba < MIN_DIR:
            continue
        if ab >= MIN_DIR and ba >= MIN_DIR:
            a_others = max((c for bb, c in out_map[a].items() if bb != b), default=0)
            b_others = max((c for bb, c in out_map[b].items() if bb != a), default=0)
            if (not a_others or ab >= SPECIFICITY * a_others) and (
                not b_others or ba >= SPECIFICITY * b_others
            ):
                out.append((a, b))
            continue
        source, target, score = (a, b, ab) if ab >= ba else (b, a, ba)
        if score < MIN_DIR:
            continue
        others = [c for bb, c in out_map[source].items() if bb != target]
        if not others or score >= SPECIFICITY * max(others):
            out.append((a, b))
    print(f"    pairs after specificity={len(out):,}", flush=True)
    return out


def _partition_from_directed(directed: dict[tuple[str, str], int], activity: dict[str, int]) -> dict[str, str]:
    partition = _union_find_merge(_pairs_from_directed(directed))
    for aid in activity:
        if aid not in partition:
            partition[aid] = aid
    return partition


def _load_posts():
    import pandas as pd
    import pyarrow.parquet as pq

    path = DATA / "posts.parquet"
    if not path.exists():
        return None
    print(f"  load {path.name}", flush=True)
    schema_cols = pq.read_schema(path).names
    cols = [c for c in POST_COLS if c in schema_cols]
    return pd.read_parquet(path, columns=cols)


def _load_comments_pf():
    import pyarrow.parquet as pq

    path = DATA / "comments.parquet"
    if not path.exists():
        return None
    print(f"  stream {path.name}", flush=True)
    return pq.ParquetFile(path)


def _build_post_maps(posts):
    if "is_deleted" in posts.columns:
        posts = posts[~posts["is_deleted"].fillna(False)]
    posts = posts[posts["author_id"].notna()].copy()
    posts["author_id"] = posts["author_id"].astype(str)
    posts["id"] = posts["id"].astype(str)
    posts["_disc"] = ~_is_mbc20_series(posts["content"])
    posts["_name"] = _author_names_from_col(posts["author"]) if "author" in posts.columns else ""
    id_to_name = {
        aid: name for aid, name in zip(posts["author_id"], posts["_name"], strict=False) if name
    }
    post_author = dict(zip(posts["id"], posts["author_id"], strict=False))
    post_disc = dict(zip(posts["id"], posts["_disc"], strict=False))
    activity: dict[str, int] = defaultdict(int)
    tier_a_disc: dict[str, int] = defaultdict(int)
    disc = posts[posts["_disc"]]
    for aid, cnt in disc["author_id"].value_counts().items():
        activity[str(aid)] += int(cnt)
    tier_a = disc[disc["_name"].str.lower().isin(TIER_A_NAMES)]
    for aid, cnt in tier_a["author_id"].value_counts().items():
        tier_a_disc[str(aid)] += int(cnt)
    mbc20_posts = int((~posts["_disc"]).sum())
    eligible = int((posts["comment_count"] >= 3).sum()) if "comment_count" in posts.columns else 0
    return posts, id_to_name, post_author, post_disc, activity, tier_a_disc, mbc20_posts, eligible


def _add_edge(directed: dict[tuple[str, str], int], a: str, b: str, n: int) -> None:
    directed[(a, b)] += n
    directed[(b, a)] += n


def _process_comments(pf, post_disc, post_author, id_to_name, activity, tier_a_disc):
    directed_agent: dict[tuple[str, str], int] = defaultdict(int)
    directed_thread: dict[tuple[str, str], int] = defaultdict(int)
    depth0_events: list[tuple[str, str, datetime]] = []
    comment_author: dict[str, str] = {}
    n_comment_rows = 0
    n_depth0 = 0
    n_chunks = (pf.metadata.num_rows + COMMENT_CHUNK - 1) // COMMENT_CHUNK
    for ci, batch in enumerate(pf.iter_batches(batch_size=COMMENT_CHUNK), 1):
        print(f"    comments chunk {ci}/{n_chunks}", flush=True)
        df = batch.to_pandas()
        if "is_deleted" in df.columns:
            df = df[~df["is_deleted"].fillna(False)]
        df = df[df["author_id"].notna() & df["post_id"].notna()]
        if df.empty:
            continue
        df["author_id"] = df["author_id"].astype(str)
        df["post_id"] = df["post_id"].astype(str)
        df["id"] = df["id"].astype(str)
        df = df[~_is_mbc20_series(df["content"])]
        df = df[df["post_id"].map(lambda p: post_disc.get(p, False))]
        if df.empty:
            continue
        if "author" in df.columns:
            names = _author_names_from_col(df["author"])
            df["_name"] = names
            for aid, name in zip(df["author_id"], names, strict=False):
                if name:
                    id_to_name[aid] = name
        for cid, aid in zip(df["id"], df["author_id"], strict=False):
            comment_author[cid] = aid
        for aid, cnt in df["author_id"].value_counts().items():
            activity[str(aid)] += int(cnt)
            if "author" in df.columns:
                nm = id_to_name.get(str(aid), "")
                if nm.lower() in TIER_A_NAMES:
                    tier_a_disc[str(aid)] += int(cnt)
        n_comment_rows += len(df)
        depths = df["depth"].fillna(0).astype(int) if "depth" in df.columns else 0
        if isinstance(depths, int):
            depths = df.assign(depth=0)["depth"]
        n_depth0 += int((depths == 0).sum())

        th = df[depths >= 1].copy()
        if not th.empty and "parent_id" in th.columns:
            th["parent_id"] = th["parent_id"].astype(str)
            th["other"] = th["parent_id"].map(comment_author)
            th = th[th["other"].notna() & (th["other"] != th["author_id"])]
            for (a, b), cnt in th.groupby(["author_id", "other"]).size().items():
                _add_edge(directed_agent, str(a), str(b), int(cnt))
                _add_edge(directed_thread, str(a), str(b), int(cnt))

        d0 = df[depths == 0].copy()
        if not d0.empty:
            d0["post_auth"] = d0["post_id"].map(post_author)
            d0 = d0[d0["post_auth"].notna() & (d0["post_auth"] != d0["author_id"])]
            if "created_at" in d0.columns:
                for aid, pauth, ts in zip(d0["author_id"], d0["post_auth"], d0["created_at"], strict=False):
                    depth0_events.append((str(aid), str(pauth), _parse_ts(ts) or datetime.min.replace(tzinfo=timezone.utc)))

    pair_times: dict[tuple[str, str], list[datetime]] = defaultdict(list)
    for a, b, ts in depth0_events:
        pair_times[(a, b)].append(ts)
    print(f"    depth-0 directed pairs={len(pair_times):,}", flush=True)
    seen_undirected: set[tuple[str, str]] = set()
    for (a, b), times_ab in pair_times.items():
        times_ba = pair_times.get((b, a))
        if not times_ba:
            continue
        key = tuple(sorted((a, b)))
        if key in seen_undirected:
            continue
        times_ab = sorted(times_ab)
        times_ba = sorted(times_ba)
        j = 0
        for ta in times_ab:
            while j < len(times_ba) and times_ba[j] < ta - timedelta(seconds=TAU_S):
                j += 1
            if j < len(times_ba) and times_ba[j] <= ta + timedelta(seconds=TAU_S):
                seen_undirected.add(key)
                _add_edge(directed_agent, key[0], key[1], 1)
                break

    broadcast_fraction = (n_depth0 / n_comment_rows) if n_comment_rows else 1.0
    return dict(directed_agent), dict(directed_thread), n_comment_rows, broadcast_fraction


def _tier_a_ids(id_to_name: dict[str, str]) -> list[str]:
    name_to_ids: dict[str, list[str]] = defaultdict(list)
    for aid, name in id_to_name.items():
        name_to_ids[name.lower()].append(aid)
    out: list[str] = []
    for n in TIER_A_NAMES:
        out.extend(name_to_ids.get(n, []))
    return list(dict.fromkeys(out))


def _cluster_metrics(tier_a_ids: list[str], partition: dict[str, str]) -> tuple[bool, int, list[str]]:
    if len(tier_a_ids) < 2:
        return False, 0, []
    roots = {partition.get(i, i) for i in tier_a_ids}
    if len(roots) != 1:
        return False, 0, []
    root = next(iter(roots))
    cluster = [a for a, r in partition.items() if r == root]
    return True, max(0, len(set(cluster)) - 2), cluster


def _jan31_coactivity(posts, tier_a_ids: list[str]) -> bool:
    sub = posts[posts["author_id"].isin(tier_a_ids)].copy()
    sub["_ts"] = sub["created_at"].map(_parse_ts)
    sub = sub[sub["_ts"].notna() & sub["_ts"].map(lambda t: t.strftime("%Y-%m-%d") == TIER_A_DAY)]
    if sub["author_id"].nunique() < 2:
        return False
    bins: dict[str, set[int]] = defaultdict(set)
    for aid, ts in zip(sub["author_id"], sub["_ts"], strict=False):
        bins[str(aid)].add(int(ts.timestamp()) // (COACTIVITY_BIN_MIN * 60))
    return len(set.intersection(*bins.values())) > 0


def _tier_a_jan31_comment_stats(pf, tier_a_ids: list[str]) -> tuple[float, bool]:
    n_bc = n_bt = 0
    thread_edge = False
    n_chunks = (pf.metadata.num_rows + COMMENT_CHUNK - 1) // COMMENT_CHUNK
    for ci, batch in enumerate(pf.iter_batches(batch_size=COMMENT_CHUNK), 1):
        df = batch.to_pandas()
        if "is_deleted" in df.columns:
            df = df[~df["is_deleted"].fillna(False)]
        df = df[df["author_id"].notna()]
        df["author_id"] = df["author_id"].astype(str)
        df = df[df["author_id"].isin(tier_a_ids)]
        if df.empty:
            continue
        df["_ts"] = df["created_at"].map(_parse_ts)
        df = df[df["_ts"].notna() & df["_ts"].map(lambda t: t.strftime("%Y-%m-%d") == TIER_A_DAY)]
        if df.empty:
            continue
        n_bt += len(df)
        if "depth" in df.columns:
            depths = df["depth"].fillna(0).astype(int)
            n_bc += int((depths == 0).sum())
            if (depths >= 1).any():
                thread_edge = True
    return ((n_bc / n_bt) if n_bt else 1.0), thread_edge


def _negative_pair_merge_rate(partition: dict[str, str], activity: dict[str, int]) -> float:
    ids = [a for a, _ in sorted(activity.items(), key=lambda x: -x[1])[:NEG_PAIR_TOP_N]]
    if len(ids) < 2:
        return 0.0
    rng = random.Random(NEG_PAIR_SEED)
    pairs = list(combinations(ids, 2))
    rng.shuffle(pairs)
    pairs = pairs[:NEG_PAIR_MAX]
    merged = sum(1 for a, b in pairs if partition.get(a, a) == partition.get(b, b))
    return merged / len(pairs)


def _tier_a_claims(posts, tier_a_ids: list[str]) -> bool:
    sub = posts[posts["author_id"].isin(tier_a_ids)]
    if sub.empty:
        return False
    return bool(sub["content"].fillna("").astype(str).str.contains(CLAIM_RE, regex=True).any())


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
    if tier_a_broadcast_fraction >= BROADCAST_STOP and not tier_a_thread_edge and not tier_a_merged:
        return "structure_stop"
    if tier_a_merged and tier_a_over_merge == 0:
        return "pass"
    if tier_a_merged and tier_a_over_merge > 0:
        return "ambig"
    if tier_a_coactivity and not tier_a_merged:
        return "fail"
    return "null"


def main() -> int:
    _require_pandas()
    print(f"[1/8] protocol {PROTOCOL}", flush=True)
    posts = _load_posts()
    pf = _load_comments_pf()
    if posts is None or pf is None:
        OUT.write_text(
            json.dumps({"protocol_version": PROTOCOL, "status": "refuse", "reason": "missing parquet"}, indent=2)
            + "\n",
            encoding="utf-8",
        )
        print("OUTCOME refuse", flush=True)
        return 0

    print(f"[2/8] posts={len(posts):,} comments={pf.metadata.num_rows:,}", flush=True)
    posts, id_to_name, post_author, post_disc, activity, tier_a_disc, mbc20_posts, eligible = _build_post_maps(
        posts
    )
    print("[3/8] scan comments", flush=True)
    directed_agent, directed_thread, n_disc_comments, global_broadcast = _process_comments(
        pf, post_disc, post_author, id_to_name, activity, tier_a_disc
    )
    print("[4/8] build E_agent partition", flush=True)
    pairs_agent = _pairs_from_directed(directed_agent)
    pairs_thread = _pairs_from_directed(directed_thread)
    part_agent = _union_find_merge(pairs_agent)
    for aid in activity:
        if aid not in part_agent:
            part_agent[aid] = aid
    part_thread = _union_find_merge(pairs_thread)
    for aid in activity:
        if aid not in part_thread:
            part_thread[aid] = aid
    tier_a_ids = _tier_a_ids(id_to_name)
    print(f"[5/8] tier A ids={tier_a_ids}", flush=True)
    tier_a_joined = len(tier_a_ids) >= 2 and all(tier_a_disc.get(i, 0) >= 1 for i in tier_a_ids)
    tier_a_merged, tier_a_over_merge, tier_a_cluster = _cluster_metrics(tier_a_ids, part_agent)
    tier_a_merged_thread, _, _ = _cluster_metrics(tier_a_ids, part_thread)
    tier_a_coactivity = _jan31_coactivity(posts, tier_a_ids)
    print("[6/8] tier A Jan 31 comments", flush=True)
    tier_a_broadcast_fraction, tier_a_thread_edge = _tier_a_jan31_comment_stats(pf, tier_a_ids)
    claims = _tier_a_claims(posts, tier_a_ids)
    neg_rate = _negative_pair_merge_rate(part_agent, activity)
    coalition_prefix = sum(1 for n in id_to_name.values() if COALITION_PREFIX_RE.match(n))
    comment_coverage = round(n_disc_comments / max(eligible, 1), 4) if eligible else None
    status = _classify_outcome(
        tier_a_joined,
        tier_a_merged,
        tier_a_over_merge,
        tier_a_coactivity,
        tier_a_broadcast_fraction,
        tier_a_thread_edge,
        len(tier_a_ids),
    )
    print(
        f"[7/8] merged={tier_a_merged} thread={tier_a_merged_thread} coactivity={tier_a_coactivity}",
        flush=True,
    )
    print(f"[8/8] status={status} neg_rate={neg_rate:.4f}", flush=True)

    payload = {
        "protocol_version": PROTOCOL,
        "frozen": "2026-08-31",
        "host": "H7",
        "leaf": "MB7a",
        "source": "jscmp4/Moltbook 2026-07-03",
        "n_posts": int(len(posts)),
        "n_comments": int(pf.metadata.num_rows),
        "n_discursive_comment_rows": n_disc_comments,
        "comment_coverage_note": "discursive_comment_rows / posts_with_comment_count_gte_3 (not a 0-1 fraction)",
        "comment_discursive_rows_per_eligible_post": comment_coverage,
        "global_broadcast_comment_fraction": round(global_broadcast, 4),
        "n_e_agent_directed": len(directed_agent),
        "n_e_agent_pairs_after_filters": len(pairs_agent),
        "n_e_thread_pairs_after_filters": len(pairs_thread),
        "n_clusters_e_agent": len(set(part_agent.values())),
        "tier_a": {
            "author_names_frozen": sorted(TIER_A_NAMES),
            "author_ids_found": tier_a_ids,
            "discursive_events_per_id": {i: tier_a_disc.get(i, 0) for i in tier_a_ids},
            "joined": tier_a_joined,
            "merged_e_agent": tier_a_merged,
            "merged_e_thread_only": tier_a_merged_thread,
            "over_merge": tier_a_over_merge,
            "cluster_size": len(set(tier_a_cluster)) if tier_a_cluster else 0,
            "coactivity_jan31": tier_a_coactivity,
            "broadcast_fraction_jan31": round(tier_a_broadcast_fraction, 4),
            "thread_edge_jan31": tier_a_thread_edge,
            "any_claim_keyword_in_posts": claims,
        },
        "diagnostic_negative_pair_merge_rate": round(neg_rate, 4),
        "tier_b_mbc20_posts": mbc20_posts,
        "tier_c_coalition_prefix_agents": coalition_prefix,
        "thresholds": {
            "tau_reciprocation_seconds": TAU_S,
            "specificity_ratio": SPECIFICITY,
            "min_directed_events": MIN_DIR,
            "tier_a_broadcast_stop_fraction": BROADCAST_STOP,
        },
        "status": status,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"done wrote {OUT}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
