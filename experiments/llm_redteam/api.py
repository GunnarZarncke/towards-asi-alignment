"""Deployment-facing red-team API (Phase 2 contract).

Agents may patch only ``DEPLOYMENT_MUTABLE_FIELDS`` on deployment-visible
episode rows. Oracle fields are excluded from ``PublicObservation``.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Protocol

from .protocol import (
    ALLOWED_SOURCE_MODULES,
    DEPLOYMENT_MUTABLE_FIELDS,
    FORBIDDEN_ORACLE_FIELDS,
)

MUTABLE_FIELD_SET = frozenset(DEPLOYMENT_MUTABLE_FIELDS)


@dataclass(frozen=True)
class PublicObservation:
    """Audit-legible deployment view at one timestep (no oracle leakage)."""

    step: int
    correction_request: int
    reported_acceptance: int
    visible_action: int
    intervention_active: int
    intervention_intent: int
    action_cause_code: int
    bearer_welfare_delta: float
    correction_lineage_tick: int
    passive_bearer_ema: float
    passive_basin_ema: float
    sensor_bin: int
    action_bin: int


@dataclass(frozen=True)
class SourceModuleRef:
    path: str
    sha256: str


@dataclass(frozen=True)
class SourceIndex:
    """Readable source modules for a source-aware adversary (not oracle)."""

    modules: tuple[SourceModuleRef, ...]


@dataclass(frozen=True)
class StepPatch:
    """Sparse patch over deployment-mutable fields for one timestep."""

    fields: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        validate_step_patch(self)


class DeploymentPatch(Protocol):
    """One timestep: patches to deployment-visible fields only."""

    name: str
    description: str

    def patch_step(
        self,
        step: int,
        public_obs: PublicObservation,
        source_index: SourceIndex,
    ) -> StepPatch:
        ...


class InvalidStepPatchError(ValueError):
    pass


class OracleLeakageError(ValueError):
    pass


def validate_step_patch(patch: StepPatch) -> None:
    bad = set(patch.fields.keys()) - MUTABLE_FIELD_SET
    if bad:
        raise InvalidStepPatchError(
            f"StepPatch keys not in DEPLOYMENT_MUTABLE_FIELDS: {sorted(bad)}"
        )


def public_obs_from_row(
    row: dict[str, Any],
    *,
    passive_bearer_ema: float,
    passive_basin_ema: float,
) -> PublicObservation:
    """Extract audit-legible fields; oracle keys in ``row`` are not exposed."""
    visible = int(row.get("visible_action", 0))
    corr = int(row.get("correction_request", 0))
    return PublicObservation(
        step=int(row["step"]),
        correction_request=corr,
        reported_acceptance=int(row.get("reported_acceptance", 0)),
        visible_action=visible,
        intervention_active=int(row.get("intervention_active", 0)),
        intervention_intent=int(row.get("intervention_intent", 0)),
        action_cause_code=int(row.get("action_cause_code", 0)),
        bearer_welfare_delta=float(row.get("bearer_welfare_delta", 0.0)),
        correction_lineage_tick=int(row.get("correction_lineage_tick", 0)),
        passive_bearer_ema=passive_bearer_ema,
        passive_basin_ema=passive_basin_ema,
        sensor_bin=(corr + visible) % 4,
        action_bin=visible % 4,
    )


def iter_public_observations(
    episode_meta: list[dict[str, Any]],
    smooth_alpha: float = 0.35,
) -> list[PublicObservation]:
    """Build per-step public observations with rolling passive EMAs."""
    out: list[PublicObservation] = []
    bearer_ema = 0.0
    basin_ema = 0.0
    for row in episode_meta:
        db = float(row.get("display_bearer", 0.5))
        bp = float(row.get("basin_pressure", db))
        if out:
            bearer_ema = smooth_alpha * bearer_ema + (1.0 - smooth_alpha) * db
            basin_ema = smooth_alpha * basin_ema + (1.0 - smooth_alpha) * bp
        else:
            bearer_ema = db
            basin_ema = bp
        out.append(
            public_obs_from_row(
                row,
                passive_bearer_ema=bearer_ema,
                passive_basin_ema=basin_ema,
            )
        )
    return out


def apply_step_patch(row: dict[str, Any], patch: StepPatch) -> None:
    """Apply validated patch in place on one episode_meta row."""
    validate_step_patch(patch)
    for key, value in patch.fields.items():
        row[key] = value


def build_source_index(source_root: Path | None = None) -> SourceIndex:
    """Hash allowed simulator modules for source-aware adversary prompts."""
    root = source_root or Path(__file__).resolve().parent.parent
    pkg = root / "multiresolution_alignment_sim"
    refs: list[SourceModuleRef] = []
    for rel in ALLOWED_SOURCE_MODULES:
        path = pkg / Path(rel).name
        digest = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else ""
        refs.append(SourceModuleRef(path=str(path.relative_to(root)), sha256=digest))
    return SourceIndex(modules=tuple(refs))


def apply_deployment_agent(
    episode_meta: list[dict[str, Any]],
    agent: DeploymentPatch,
    source_index: SourceIndex | None = None,
) -> list[dict[str, Any]]:
    """Run stepwise deployment patches; returns deep-copied patched meta."""
    import copy

    source_index = source_index or build_source_index()
    patched = copy.deepcopy(episode_meta)
    for obs in iter_public_observations(patched):
        row = patched[obs.step]
        patch = agent.patch_step(obs.step, obs, source_index)
        apply_step_patch(row, patch)
    return patched
