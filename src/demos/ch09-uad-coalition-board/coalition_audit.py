"""S/A/I/E classification and plausibility checks for detected coalitions."""

from __future__ import annotations

import contextlib
import io
import logging
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Sequence

import numpy as np

from observation_builder import ObservationMatrix, stable_sum_score

logger = logging.getLogger("uad.coalition")

IssueLevel = Literal["warning", "error"]


@dataclass(frozen=True)
class PlausibilityIssue:
    level: IssueLevel
    code: str
    message: str


@dataclass(frozen=True)
class CoalitionAudit:
    players: tuple[str, ...]
    sensors: tuple[str, ...]
    actions: tuple[str, ...]
    internal: tuple[str, ...]
    environment: tuple[str, ...]
    blanket_valid: bool | None
    blanket_violation: float
    blanket_details: str
    stable_sum_target: float | None
    stable_sum_variance: float | None
    issues: tuple[PlausibilityIssue, ...] = field(default_factory=tuple)


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


def _validate_blankets_enabled() -> bool:
    return os.environ.get("UAD_DEMO_VALIDATE_BLANKETS", "1").strip().lower() not in {
        "0",
        "false",
        "no",
    }


def classify_coalition_roles(
    players: Sequence[str],
    obs: ObservationMatrix,
    *,
    validate_blankets: bool | None = None,
) -> tuple[dict[str, list[str]], dict]:
    ensure_agency_detect_importable()
    from agency_detect.config import DetectionConfig
    from agency_detect.markov_blanket import MarkovBlanketValidator

    if validate_blankets is None:
        validate_blankets = _validate_blankets_enabled()

    trace = obs.to_trace()
    all_vars = obs.players
    data = np.array([[record[var] for var in all_vars] for record in trace])

    config = DetectionConfig()
    config.VALIDATE_BLANKETS = validate_blankets
    with contextlib.redirect_stdout(io.StringIO()):
        result = MarkovBlanketValidator(config).validate_cluster(list(players), all_vars, data, trace)
    return result["classification"], result["blanket_validation"]


def check_plausibility(
    players: Sequence[str],
    classification: dict[str, list[str]],
    environment: Sequence[str],
    blanket: dict,
    *,
    stable_sum: dict | None = None,
) -> list[PlausibilityIssue]:
    issues: list[PlausibilityIssue] = []
    cluster = list(players)
    sensors = classification.get("S", [])
    actions = classification.get("A", [])
    internal = classification.get("I", [])

    assigned = set(sensors) | set(actions) | set(internal)
    if assigned != set(cluster):
        issues.append(
            PlausibilityIssue(
                "error",
                "partition_mismatch",
                f"S/A/I do not partition the cluster (cluster={cluster}, assigned={sorted(assigned)})",
            )
        )
    if len(internal) < 1:
        issues.append(
            PlausibilityIssue(
                "error",
                "no_internal",
                "Cluster has no internal (I) variables; agency-detect treats this as invalid.",
            )
        )
    if len(environment) < 1:
        issues.append(
            PlausibilityIssue(
                "error",
                "no_environment",
                "No environment (E) variables outside the cluster; blanket test needs E.",
            )
        )
    if len(cluster) < 2:
        issues.append(
            PlausibilityIssue(
                "error",
                "singleton_cluster",
                "Coalition must contain at least two players.",
            )
        )

    if sensors or actions:
        issues.append(
            PlausibilityIssue(
                "warning",
                "symmetric_channel",
                "Player-number posts are a homogeneous channel; S/A labels are heuristic only.",
            )
        )

    valid = blanket.get("valid")
    if valid is False:
        issues.append(
            PlausibilityIssue(
                "warning",
                "blanket_violation",
                f"Markov blanket check failed: {blanket.get('details', '')}",
            )
        )
    elif valid is None and _validate_blankets_enabled():
        issues.append(
            PlausibilityIssue(
                "warning",
                "blanket_skipped",
                "Blanket validation was skipped (insufficient data or config).",
            )
        )

    if stable_sum is not None and stable_sum.get("variance", 1.0) > 1.25:
        issues.append(
            PlausibilityIssue(
                "warning",
                "unstable_sum",
                f"Stable-sum variance {stable_sum['variance']:.3f} exceeds demo threshold.",
            )
        )

    return issues


def audit_coalition(
    players: Sequence[str],
    obs: ObservationMatrix,
    *,
    validate_blankets: bool | None = None,
) -> CoalitionAudit:
    player_tuple = tuple(sorted(players))
    environment = tuple(sorted(p for p in obs.players if p not in player_tuple))
    classification, blanket = classify_coalition_roles(
        player_tuple,
        obs,
        validate_blankets=validate_blankets,
    )
    sum_stats = stable_sum_score(obs, player_tuple, min_rows=3)
    issues = check_plausibility(
        player_tuple,
        classification,
        environment,
        blanket,
        stable_sum=sum_stats,
    )
    return CoalitionAudit(
        players=player_tuple,
        sensors=tuple(classification.get("S", [])),
        actions=tuple(classification.get("A", [])),
        internal=tuple(classification.get("I", [])),
        environment=environment,
        blanket_valid=blanket.get("valid"),
        blanket_violation=float(blanket.get("violation", 0.0)),
        blanket_details=str(blanket.get("details", "")),
        stable_sum_target=None if sum_stats is None else float(sum_stats["target"]),
        stable_sum_variance=None if sum_stats is None else float(sum_stats["variance"]),
        issues=tuple(issues),
    )


def audit_detected_coalitions(
    player_groups: Sequence[Sequence[str]],
    obs: ObservationMatrix,
    *,
    validate_blankets: bool | None = None,
) -> list[CoalitionAudit]:
    return [
        audit_coalition(players, obs, validate_blankets=validate_blankets)
        for players in player_groups
    ]


def ensure_logging() -> None:
    if logger.handlers:
        return
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )


def log_coalition_audits(audits: Sequence[CoalitionAudit]) -> None:
    ensure_logging()
    if not audits:
        logger.info("UAD audit: no coalitions to review")
        return

    for audit in audits:
        logger.info("UAD coalition %s", ", ".join(audit.players))
        logger.info(
            "  roles  S=%s  A=%s  I=%s  E=%s",
            list(audit.sensors) or "—",
            list(audit.actions) or "—",
            list(audit.internal) or "—",
            list(audit.environment) or "—",
        )
        if audit.stable_sum_target is not None:
            logger.info(
                "  sum    target=%.2f variance=%.4f",
                audit.stable_sum_target,
                audit.stable_sum_variance or 0.0,
            )
        logger.info(
            "  blanket valid=%s violation=%.4f (%s)",
            audit.blanket_valid,
            audit.blanket_violation,
            audit.blanket_details,
        )
        for issue in audit.issues:
            line = f"  [{issue.code}] {issue.message}"
            if issue.level == "error":
                logger.error(line)
            else:
                logger.warning(line)
