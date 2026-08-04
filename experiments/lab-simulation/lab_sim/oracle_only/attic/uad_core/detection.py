"""Vendored from `embedded_sim/uad_core/detection.py` (see package
docstring) -- lag-max mutual-information agent clustering (agency-detect
port, stdlib-only). Byte-for-byte identical except the import below
points at this package's local `info.py`."""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations

from .config import DetectionConfig
from .info import mutual_information
from .markov_blanket import MarkovBlanketValidator


def lagmax_mi(x: list[int], y: list[int], *, max_lag: int) -> float:
    best = 0.0
    for tau in range(-max_lag, max_lag + 1):
        if tau == 0:
            best = max(best, mutual_information(x, y))
            continue
        if tau > 0:
            xi, yi = x[:-tau], y[tau:]
        else:
            xi, yi = x[-tau:], y[:tau]
        if xi and yi:
            best = max(best, mutual_information(xi, yi))
    return best


def build_similarity_matrix(
    data: list[list[int]],
    *,
    max_lag: int,
) -> tuple[list[list[float]], list[list[float]]]:
    n_vars = len(data[0])
    columns = [[row[i] for row in data] for i in range(n_vars)]
    sim = [[0.0] * n_vars for _ in range(n_vars)]
    for i, j in combinations(range(n_vars), 2):
        w = lagmax_mi(columns[i], columns[j], max_lag=max_lag)
        sim[i][j] = sim[j][i] = w
    max_sim = max((v for row in sim for v in row), default=0.0)
    dist = [[1.0 - sim[i][j] / (max_sim + 1e-12) for j in range(n_vars)] for i in range(n_vars)]
    return sim, dist


def filter_weak_connections(
    clusters: dict[int, list[str]],
    vars_active: list[str],
    sim: list[list[float]],
    *,
    weak_thresh: float,
) -> tuple[dict[int, list[str]], list[str]]:
    env_bucket: list[str] = []
    filtered: dict[int, list[str]] = {}

    for lbl, mem in clusters.items():
        if len(mem) <= 1:
            continue
        idx = [vars_active.index(v) for v in mem]
        sub = [[sim[i][j] for j in idx] for i in idx]
        mean_intra = (sum(sum(row) for row in sub) - sum(sub[i][i] for i in range(len(idx)))) / max(
            len(idx) * (len(idx) - 1), 1
        )
        kept: list[str] = []
        for v in mem:
            j = vars_active.index(v)
            row_idx = idx.index(j)
            sim_to_cluster = (sum(sub[row_idx]) - sub[row_idx][row_idx]) / max(len(idx) - 1, 1)
            if sim_to_cluster >= weak_thresh * mean_intra:
                kept.append(v)
            else:
                env_bucket.append(v)
        if kept:
            filtered[lbl] = kept
    return filtered, env_bucket


def _complete_linkage_labels(dist: list[list[float]], n_clusters: int) -> list[int]:
    n = len(dist)
    if n == 0:
        return []
    clusters: list[set[int]] = [{i} for i in range(n)]
    while len(clusters) > max(1, n_clusters):
        best_i, best_j, best_d = 0, 1, float("inf")
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                d = max(dist[a][b] for a in clusters[i] for b in clusters[j])
                if d < best_d:
                    best_i, best_j, best_d = i, j, d
        clusters[best_i] = clusters[best_i] | clusters[best_j]
        del clusters[best_j]

    labels = [-1] * n
    for lbl, cluster in enumerate(clusters):
        for idx in cluster:
            labels[idx] = lbl
    return labels


class AgentDetector:
    """Main UAD pipeline: lagged MI clustering + optional blanket validation."""

    def __init__(self, config: DetectionConfig | None = None):
        self.config = config or DetectionConfig()
        self.validator = MarkovBlanketValidator(self.config)

    def detect_agents(self, trace: list[dict[str, int]]) -> dict[str | int, dict]:
        if not trace:
            return {}

        vars_ = list(trace[0].keys())
        data = [[int(rec[v]) for v in vars_] for rec in trace]

        active_idx = [i for i, v in enumerate(vars_) if len({row[i] for row in data}) > 1]
        inactive_idx = [i for i in range(len(vars_)) if i not in active_idx]
        if len(active_idx) < 2:
            return {}

        vars_active = [vars_[i] for i in active_idx]
        data_active = [[row[i] for i in active_idx] for row in data]

        sim, dist = build_similarity_matrix(data_active, max_lag=self.config.max_lag)
        labels = _complete_linkage_labels(dist, self.config.n_agents)

        clusters: dict[int, list[str]] = defaultdict(list)
        for var, lbl in zip(vars_active, labels, strict=True):
            clusters[int(lbl)].append(var)

        filtered, env_bucket = filter_weak_connections(
            dict(clusters),
            vars_active,
            sim,
            weak_thresh=self.config.weak_threshold,
        )

        for i in inactive_idx:
            env_bucket.append(vars_[i])

        validated: dict[str | int, dict] = {}
        failed: list[str] = []
        for lbl, variables in filtered.items():
            if not variables:
                continue
            result = self.validator.validate_cluster(variables, vars_, data)
            if result["blanket_validation"]["valid"] is False and self.config.validate_blankets:
                failed.extend(variables)
            else:
                validated[lbl] = {"variables": variables, **result}

        env_bucket.extend(failed)
        if env_bucket:
            validated["env"] = {
                "variables": env_bucket,
                "classification": {"S": [], "A": [], "I": env_bucket},
                "blanket_validation": {
                    "valid": None,
                    "violation": 0.0,
                    "details": "environment bucket",
                },
            }
        return validated


def detect_agents(trace: list[dict[str, int]], **config_overrides) -> dict[str | int, dict]:
    config = DetectionConfig(**config_overrides)
    return AgentDetector(config).detect_agents(trace)
