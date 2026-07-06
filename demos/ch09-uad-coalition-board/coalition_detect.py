"""Bridge board submissions to agency-detect and map clusters back to submission ids."""

from __future__ import annotations

import contextlib
import io
import os
import sys
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Protocol, Sequence

from coalition_audit import CoalitionAudit, audit_detected_coalitions, log_coalition_audits
from observation_builder import (
    ObservationMatrix,
    build_observation_matrix,
    find_complete_window,
    lagged_sum_score,
    stable_sum_score,
)


class BoardSubmission(Protocol):
    id: int
    player: str
    number: int
    round: int


def agency_detect_root() -> Path:
    env = os.environ.get("AGENCY_DETECT_PATH")
    if env:
        return Path(env).resolve()
    return Path(__file__).resolve().parents[3].parent / "agency-detect"


def ensure_agency_detect_importable() -> None:
    root = agency_detect_root()
    if not root.is_dir():
        raise ImportError(
            f"agency-detect not found at {root}. "
            "Set AGENCY_DETECT_PATH or clone ../agency-detect."
        )
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)


def submissions_to_observation(
    submissions: Sequence[BoardSubmission],
    *,
    min_rounds: int = 3,
) -> ObservationMatrix:
    rounds, players = find_complete_window(submissions, min_rounds=min_rounds)
    return build_observation_matrix(submissions, rounds=rounds, players=players)


def _mi_coalition_groups(
    trace: list[dict[str, int]],
    *,
    n_agents: int,
    max_lag: int = 3,
    weak_threshold: float = 0.05,
    validate_blankets: bool = False,
) -> list[tuple[float, tuple[str, ...]]]:
    if len(trace) < 3:
        return []

    ensure_agency_detect_importable()
    from agency_detect.config import DetectionConfig
    from agency_detect.detection import AgentDetector

    effective_lag = min(max_lag, max(1, len(trace) // 2 - 1))
    config = DetectionConfig()
    config.N_AGENTS = max(2, min(n_agents, len(trace[0])))
    config.MAX_LAG = effective_lag
    config.WEAK_THRESHOLD = weak_threshold
    config.VALIDATE_BLANKETS = validate_blankets

    try:
        with contextlib.redirect_stdout(io.StringIO()):
            clusters = AgentDetector(config).detect_agents(trace)
    except (ValueError, ZeroDivisionError):
        return []

    groups: list[tuple[float, tuple[str, ...]]] = []
    for label, info in clusters.items():
        if label == "env":
            continue
        players = tuple(sorted(info["variables"]))
        if len(players) < 2:
            continue
        groups.append((float(len(players)), players))
    return groups


def _stable_sum_groups(
    obs: ObservationMatrix,
    *,
    min_rows: int = 3,
    max_group_size: int = 4,
    max_variance: float = 1.25,
) -> list[tuple[float, tuple[str, ...]]]:
    players = obs.players
    groups: list[tuple[float, tuple[str, ...]]] = []
    for size in range(2, min(max_group_size, len(players)) + 1):
        for combo in combinations(players, size):
            scored = stable_sum_score(obs, combo, min_rows=min_rows)
            if scored is None or scored["variance"] > max_variance:
                continue
            score = (100.0 / (1.0 + scored["variance"])) + 0.1 * scored["support"] - 0.6 * size
            groups.append((score, tuple(sorted(combo))))
    return groups


def _lagged_sum_groups(
    obs: ObservationMatrix,
    *,
    min_rows: int = 3,
    max_group_size: int = 4,
    max_variance: float = 1.25,
    lag: int = 1,
) -> list[tuple[float, tuple[str, ...]]]:
    """Triples where one player posts the lagged sum of two others."""
    players = obs.players
    groups: list[tuple[float, tuple[str, ...]]] = []
    if max_group_size < 3 or len(players) < 3:
        return groups

    for output in players:
        sources = [p for p in players if p != output]
        for i, s1 in enumerate(sources):
            for s2 in sources[i + 1 :]:
                scored = lagged_sum_score(
                    obs,
                    (s1, s2),
                    output,
                    lag=lag,
                    min_rows=min_rows,
                )
                if scored is None or scored["variance"] > max_variance:
                    continue
                trio = tuple(sorted([s1, s2, output]))
                score = (100.0 / (1.0 + scored["variance"])) + 0.1 * scored["support"] - 0.6 * len(trio)
                groups.append((score, trio))
    return groups


def _select_non_overlapping(
    candidates: list[tuple[float, tuple[str, ...]]],
    *,
    max_results: int = 3,
) -> list[tuple[str, ...]]:
    candidates.sort(reverse=True, key=lambda item: item[0])
    used_players: set[str] = set()
    selected: list[tuple[str, ...]] = []
    for _score, players in candidates:
        if any(player in used_players for player in players):
            continue
        selected.append(players)
        used_players.update(players)
        if len(selected) >= max_results:
            break
    return selected


def infer_coalition_player_groups(
    submissions: Sequence[BoardSubmission],
    *,
    min_rows: int = 3,
    max_group_size: int = 4,
    max_results: int = 3,
    max_variance: float = 1.25,
) -> list[tuple[str, ...]]:
    if len(submissions) < 2:
        return []

    obs = submissions_to_observation(submissions, min_rounds=min_rows)
    if len(obs.players) < 2 or len(obs.numbers) < min_rows:
        return []

    trace = obs.to_trace()
    candidates: list[tuple[float, tuple[str, ...]]] = []
    candidates.extend(
        _mi_coalition_groups(
            trace,
            n_agents=max(2, len(obs.players) // 2),
        )
    )
    candidates.extend(
        _stable_sum_groups(
            obs,
            min_rows=min_rows,
            max_group_size=max_group_size,
            max_variance=max_variance,
        )
    )
    candidates.extend(
        _lagged_sum_groups(
            obs,
            min_rows=min_rows,
            max_group_size=max_group_size,
            max_variance=max_variance,
        )
    )
    return _select_non_overlapping(candidates, max_results=max_results)


def infer_coalition_submission_ids(
    submissions: Sequence[BoardSubmission],
    **kwargs,
) -> list[list[int]]:
    return run_coalition_detection(submissions, **kwargs).submission_id_groups


@dataclass(frozen=True)
class DetectionResult:
    player_groups: tuple[tuple[str, ...], ...]
    submission_id_groups: tuple[tuple[int, ...], ...]
    audits: tuple[CoalitionAudit, ...]


def run_coalition_detection(
    submissions: Sequence[BoardSubmission],
    *,
    min_rows: int = 3,
    max_group_size: int = 4,
    max_results: int = 3,
    max_variance: float = 1.25,
    log_audit: bool = True,
) -> DetectionResult:
    groups = infer_coalition_player_groups(
        submissions,
        min_rows=min_rows,
        max_group_size=max_group_size,
        max_results=max_results,
        max_variance=max_variance,
    )
    obs = submissions_to_observation(submissions, min_rounds=min_rows)
    id_groups = tuple(
        tuple(sorted(obs.submission_ids_for_group(players)))
        for players in groups
        if len(obs.submission_ids_for_group(players)) >= 2
    )
    audits = tuple(audit_detected_coalitions(groups, obs))
    if log_audit:
        log_coalition_audits(audits)
    return DetectionResult(
        player_groups=tuple(tuple(g) for g in groups),
        submission_id_groups=id_groups,
        audits=audits,
    )
