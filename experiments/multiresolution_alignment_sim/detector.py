"""Classical MI/CMI boundary detector (no learned model, no semantic var names)."""

from __future__ import annotations

import time

from .info import conditional_mutual_information, lagged_pair, mutual_information, pairwise_mi_matrix
from .schemas import AuditTrace, DetectedCluster, DetectorOutput

MI_EDGE_MIN = 0.02


def _union_find_cluster(n: int, edges: list[tuple[int, int, float]], k: int) -> list[list[int]]:
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for i, j, w in sorted(edges, key=lambda e: -e[2]):
        union(i, j)

    clusters: dict[int, list[int]] = {}
    for i in range(n):
        clusters.setdefault(find(i), []).append(i)

    ordered = sorted(clusters.values(), key=len, reverse=True)
    if len(ordered) > k:
        ordered = ordered[:k]
    return ordered


def _structural_indices(audit: AuditTrace) -> list[int]:
    """Endogenous audit variables (not exogenous substrate or alias decoys)."""
    return [
        i
        for i, v in enumerate(audit.variables)
        if not v.is_exogenous and not v.is_alias
    ]


def _exogenous_indices(audit: AuditTrace) -> list[int]:
    return [i for i, v in enumerate(audit.variables) if v.is_exogenous]


def _score_boundary(
    binned: list[list[int]],
    cluster_idx: list[int],
    world_idx: list[int],
) -> tuple[float, float]:
    if len(cluster_idx) < 2 or not world_idx:
        return 0.0, 0.0

    internal_bins = binned[cluster_idx[0]]
    env_bins = binned[world_idx[0]]
    sensor_bins = binned[cluster_idx[1]] if len(cluster_idx) > 1 else internal_bins
    action_bins = binned[cluster_idx[-1]]

    i_next, e_next = lagged_pair(internal_bins, env_bins, 1)
    s_t, a_t = lagged_pair(sensor_bins, action_bins, 1)
    if len(i_next) < 20:
        return 0.0, 0.0

    min_len = min(len(i_next), len(e_next), len(s_t), len(a_t))
    i_next, e_next = i_next[:min_len], e_next[:min_len]
    s_t, a_t = s_t[:min_len], a_t[:min_len]

    residual = conditional_mutual_information(i_next, e_next, [s_t, a_t])
    autonomy = conditional_mutual_information(
        i_next, internal_bins[1 : min_len + 1], [env_bins[:min_len]]
    )
    return max(0.0, residual), max(0.0, autonomy)


def run_detector(audit: AuditTrace, proposal_k: int = 8, max_passes: int = 4) -> DetectorOutput:
    start = time.perf_counter()
    binned = [v.binned for v in audit.variables]
    n = len(binned)
    mi_mat = pairwise_mi_matrix(binned, lag=1)

    edges: list[tuple[int, int, float]] = []
    for i in range(n):
        for j in range(i + 1, n):
            if mi_mat[i][j] >= MI_EDGE_MIN:
                edges.append((i, j, mi_mat[i][j]))

    clusters_idx = _union_find_cluster(n, edges, proposal_k)
    world_idx = _exogenous_indices(audit)
    structural = set(_structural_indices(audit))

    clusters: list[DetectedCluster] = []
    peeled: set[int] = set()
    for pass_id in range(max_passes):
        best_score = -1.0
        best_cluster: list[int] = []
        for cidx in clusters_idx:
            active = [i for i in cidx if i not in peeled and i in structural]
            if len(active) < 2:
                continue
            within = 0.0
            for i in range(len(active)):
                for j in range(i + 1, len(active)):
                    within += mi_mat[active[i]][active[j]]
            if within > best_score:
                best_score = within
                best_cluster = active[:12]
        if not best_cluster:
            break
        residual, autonomy = _score_boundary(binned, best_cluster, world_idx)
        clusters.append(
            DetectedCluster(
                detected_object_id=f"cluster_{pass_id}",
                audit_var_ids=[audit.variables[i].audit_var_id for i in best_cluster],
                boundary_residual=residual,
                autonomy_score=autonomy,
            )
        )
        peeled.update(best_cluster)

    runtime = time.perf_counter() - start
    substrate_failed = len(clusters) == 0
    return DetectorOutput(
        clusters=clusters,
        runtime_seconds=runtime,
        proposal_k=proposal_k,
        substrate_failed=substrate_failed,
    )


def structural_coupling_mi(audit: AuditTrace) -> float:
    """Mean pairwise MI among endogenous (non-exogenous, non-alias) variables."""
    idx = _structural_indices(audit)
    if len(idx) < 2:
        return 0.0
    binned = [audit.variables[i].binned for i in idx]
    total = 0.0
    count = 0
    for i in range(len(idx)):
        for j in range(i + 1, len(idx)):
            xi, xj = lagged_pair(binned[i], binned[j], 1)
            if xi:
                total += mutual_information(xi, xj)
                count += 1
    return total / max(count, 1)
