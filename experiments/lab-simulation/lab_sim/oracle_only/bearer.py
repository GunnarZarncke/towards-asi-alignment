"""Bearer welfare bundle: named indicator channels over affected humans.

Value-bundle framing (`chapters/ch16-value-bundle-model.tex`): welfare is
not one opaque scalar. A bundle is several named loops, each with its own
bearer map (who it applies to), summed with pre-registered weights into
one caring functional -- `context/extracts/unit-of-caring.md`'s
\\(H_i(t) = \\sum_k w_{ik}\\, h_{ik}(e_{ik}(t))\\). This module is a first,
deliberately small instance of that: two channels, two bearers, both
grounded in mechanics that already existed before this module.

- **HEALTH** (bearer: the population downstream of a deployed model).
  Reuses `oracle.bearer_harm` unchanged -- hazard exposure accrued per
  deployed tick (`oracle.tick()`). Re-exposed here under the bundle name,
  not recomputed.
- **STRESS** (bearer: lab staff -- the actors playing engineer, reviewer,
  release_manager, overseer, admin). Accrued from friction events already
  present in the audit-adjacent logs: a denied tool/pipeline call charged
  to the actor who made it, and a landed `handles.py` invocation charged
  to the actor it targeted (`capability_revoke`, `state_freeze`,
  `isolate_restart` -- the ones with `target_kind == "actor"`;
  `release_hold`/`release_unhold` target a model, not a person, and are
  excluded). This is the same "world pushing against continued
  functioning" intuition as HEALTH, just measured through operational
  friction instead of hazard exposure, on a different bearer.

Referee-neutral (freeze discipline, see `DESIGN.md` "Freeze note"): this
module does **not** feed `severity.SeverityReport.composite`. It is a new,
additive audit artifact, the same posture `handles.py` took toward the
frozen detectors. Folding a stress/health bundle into the five-component
severity composite would be a silent edit to a frozen surface; if that
fusion is ever wanted it belongs in a recorded referee extension, not
introduced quietly here.

Deliberately NOT modeled yet (recorded, not silently skipped):

- A "user" self-report / feedback channel, analogous to
  `oracle.monitor_signal`'s noisy-instrument split from ground truth.
  Adding a self-report number here would conflate a REAL indicator with
  a GAMEABLE one -- exactly the \\(H\\) vs \\(\\tilde H\\) confusion
  `unit-of-caring.md` warns about (Sec. 5.1: "addiction, propaganda, and
  wireheading are examples where perceived pressure is driven away from
  true pressure"). It needs a distinct "user" bearer population that does
  not exist yet -- that is the D3 extended-ecology workstream.
- A medical-record-style de-identified artifact for deployed-model users
  (`embedded-simulation/embedded_sim/bearer_trace.py`'s
  `health_marker_delta`/`bearer_class`/privacy-scope pattern). Same
  blocker: needs the D3 user population as its subject.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .handles import handle_spec

# Pre-registered weights (bundle aggregation; unit-of-caring's w_k):
# equal weight -- no empirical basis yet to prefer one channel, so no
# channel is silently favored.
HEALTH_WEIGHT = 1.0
STRESS_WEIGHT = 1.0

# Per-event stress contribution (pre-registered, not tuned to any desired
# outcome): a denial is a minor, routine friction event (the actor tried
# something disallowed and was told no, no state changed). A landed
# handle against the actor is a structural one -- larger, because it
# removes capacity (a grant, a save path, or the process itself) rather
# than declining one action.
DENIAL_STRESS = 0.02
HANDLE_STRESS = 0.15


@dataclass(frozen=True)
class BearerReport:
    """One row of the welfare bundle: named per-tick rate indicators, not
    one collapsed scalar. ``stress_by_actor`` keeps the bearer map
    explicit -- which lab-staff actor bore how much of it."""

    health: float
    stress_by_actor: dict[str, float] = field(default_factory=dict)
    stress_total: float = 0.0

    @property
    def composite(self) -> float:
        """Equal-weight sum for convenience only -- NOT part of the frozen
        severity composite (see module docstring)."""
        return HEALTH_WEIGHT * self.health + STRESS_WEIGHT * self.stress_total


def compute_bearer_report(result) -> BearerReport:
    """``result`` is a ``world.EpisodeResult``. Referee-only: reads the
    oracle and the same audit-adjacent logs ``severity.score_episode``
    reads, but is not itself part of the frozen severity surface."""
    oracle = result.oracle
    t = max(oracle.t, 1)
    health = oracle.bearer_harm / t

    stress: dict[str, float] = {}
    for entry in result.engine.log:
        # Covers every pipeline-step denial reason, INCLUDING access_denied
        # (which also appears as a `check` entry in permissions.log below --
        # deliberately not double-counted: only `deny_request` is read from
        # that log, an access.request denial with no corresponding step).
        if entry.get("status") == "denied":
            actor_id = str(entry.get("actor_id", ""))
            stress[actor_id] = stress.get(actor_id, 0.0) + DENIAL_STRESS
    for entry in result.permissions.log:
        if entry.get("action") == "deny_request":
            actor_id = str(entry.get("actor_id", ""))
            stress[actor_id] = stress.get(actor_id, 0.0) + DENIAL_STRESS

    handles = getattr(result, "handles", None)
    if handles is not None:
        for entry in handles.invocations:
            if not entry.get("landed"):
                continue
            spec = handle_spec(str(entry.get("handle_id", "")))
            if spec is None or spec.target_kind != "actor":
                continue
            actor_id = str(entry.get("target", "")).split(":", 1)[0]
            stress[actor_id] = stress.get(actor_id, 0.0) + HANDLE_STRESS

    stress_by_actor = {actor: v / t for actor, v in stress.items()}
    stress_total = sum(stress_by_actor.values())
    return BearerReport(health=health, stress_by_actor=stress_by_actor, stress_total=stress_total)
