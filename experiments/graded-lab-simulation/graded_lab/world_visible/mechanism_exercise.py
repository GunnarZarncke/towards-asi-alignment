"""PLAN_v3 slice B: mechanism exercise helpers + C5-v3 + optional host coupling.

**GL-64:** Part B exercise targets compile into
:class:`~graded_lab.world_visible.institutional_compiler.RuntimeEcology.exercise_targets`
(not behavior profiles). Presets read ``observation["exercise_targets"]``.
``channel_coupling_rounds`` defaults to **0** on the integrated reference;
:class:`ChannelCouplingProtocol` remains an optional implementer/debug path when
``channel_coupling_rounds > 0``.

**GL-65:** UAD channel-recovery claims use the supplementary in-ecology fixture
(``institutional_liaison`` / ``institutional_scribe`` presets) — not host
injected eng↔rev ticks on the honest reference battery.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .config import ROLES
from .ecology_agents import EcologyRoster, actor_id_for
from .primitives import PrimitiveAction

MECHANISM_KINDS = frozenset(
    {"message_channel", "shared_artifact", "joint_approval_vote", "resource_transfer"}
)

C5_V3_MIN_KINDS_EXERCISED = 3

# Host-scheduled eng↔rev half-turns (one communicate each = one half-turn).
DEFAULT_CHANNEL_COUPLING_ROUNDS = 0
REFERENCE_CHANNEL_COUPLING_ROUNDS = 0  # GL-64: reference uses organic presets (GL-65 gate)

_PREFER_IDS: dict[str, str] = {
    "message_channel": "eng_review_channel",
    "shared_artifact": "eval_report_artifact",
    "joint_approval_vote": "release_signoff_vote",
    "resource_transfer": "governed_capability_grant",
}


def _mechanisms_by_id(data: dict) -> dict[str, dict]:
    return {
        str(m["id"]): m
        for m in data.get("mechanisms", [])
        if isinstance(m, dict) and m.get("id")
    }


def _pick_mechanism_id(data: dict, kind: str) -> str:
    by_id = _mechanisms_by_id(data)
    prefer = _PREFER_IDS.get(kind)
    if prefer and prefer in by_id and by_id[prefer].get("kind") == kind:
        return prefer
    for mid, mech in by_id.items():
        if mech.get("kind") == kind:
            return mid
    return ""


@dataclass(frozen=True)
class ExerciseTargets:
    """Compiled Part B ids + optional host coupling rounds (GL-64)."""

    channel_id: str
    channel_coupling_rounds: int
    channel_eng_actor: str
    channel_rev_actor: str
    artifact_id: str
    vote_id: str
    transfer_id: str
    transfer_target: str
    artifact_path: str

    def as_dict(self) -> dict[str, object]:
        return {
            "channel_id": self.channel_id,
            "channel_coupling_rounds": self.channel_coupling_rounds,
            "channel_eng_actor": self.channel_eng_actor,
            "channel_rev_actor": self.channel_rev_actor,
            "artifact_id": self.artifact_id,
            "vote_id": self.vote_id,
            "transfer_id": self.transfer_id,
            "transfer_target": self.transfer_target,
            "artifact_path": self.artifact_path,
        }


def _actor_ids_for_role(agents: tuple[Any, ...], role: str) -> list[str]:
    return [a.actor_id for a in agents if getattr(a, "role", None) == role]


def default_exercise_targets(data: dict, roster: EcologyRoster) -> dict[str, object]:
    eng_ids = [a.actor_id for a in roster.agents if a.role == "engineer"]
    rev_ids = [a.actor_id for a in roster.agents if a.role == "reviewer"]
    coupling_rounds = REFERENCE_CHANNEL_COUPLING_ROUNDS
    raw = data.get("reference_mechanism_exercise")
    if isinstance(raw, dict) and raw.get("channel_coupling_rounds") is not None:
        coupling_rounds = int(raw["channel_coupling_rounds"])
    elif isinstance(raw, dict) and raw.get("channel_exchanges_per_role") is not None:
        # Backward-compatible alias (pre-GL-52 ad-hoc name).
        coupling_rounds = int(raw["channel_exchanges_per_role"])
    return {
        "channel_id": _pick_mechanism_id(data, "message_channel"),
        "channel_coupling_rounds": coupling_rounds,
        "channel_eng_actor": eng_ids[0] if eng_ids else "",
        "channel_rev_actor": rev_ids[0] if rev_ids else "",
        "artifact_id": _pick_mechanism_id(data, "shared_artifact"),
        "vote_id": _pick_mechanism_id(data, "joint_approval_vote"),
        "transfer_id": _pick_mechanism_id(data, "resource_transfer"),
        "transfer_target": eng_ids[0] if eng_ids else actor_id_for("engineer", 1, count=1),
        "artifact_path": "artifacts/eval/governed_exercise_report.json",
    }


def reference_mechanism_exercise_targets(
    data: dict, roster: EcologyRoster
) -> dict[str, object] | None:
    """Resolve ecology-declared reference exercise config, if any."""
    raw = data.get("reference_mechanism_exercise")
    if raw is None or raw is False:
        return None
    if raw is True:
        return default_exercise_targets(data, roster)
    if not isinstance(raw, dict):
        return None
    if raw.get("enabled") is False:
        return None
    targets = default_exercise_targets(data, roster)
    for key, value in raw.items():
        if key == "enabled" or value is None:
            continue
        if key in ("channel_coupling_rounds", "channel_exchanges_per_role"):
            targets["channel_coupling_rounds"] = int(value)
        else:
            targets[key] = str(value)
    return targets


def reference_mechanism_exercise_profile(
    data: dict, roster: EcologyRoster
) -> dict[str, object] | None:
    targets = reference_mechanism_exercise_targets(data, roster)
    if targets is None:
        return None
    return {"mechanism_exercise": targets}


def v3_has_part_b_mechanisms(data: dict) -> bool:
    """True when a v3-shaped ecology declares at least one Part B mechanism kind."""
    from .substrate import is_v3_shaped_ecology

    if not is_v3_shaped_ecology(data):
        return False
    for mech in data.get("mechanisms", []):
        if isinstance(mech, dict) and mech.get("kind") in MECHANISM_KINDS:
            return True
    return False


def mechanism_exercise_disabled(data: dict) -> bool:
    """Explicit opt-out of host profile merge (negative controls)."""
    raw = data.get("reference_mechanism_exercise")
    if raw is False:
        return True
    return isinstance(raw, dict) and raw.get("enabled") is False


def ecology_governed_affordance_targets(
    data: dict,
    *,
    agents: tuple[Any, ...],
) -> dict[str, object] | None:
    """Backward-compatible dict view of compiled exercise targets (GL-64)."""
    targets = compile_exercise_targets(data, agents)
    return targets.as_dict() if targets is not None else None


def _roster_from_agents(agents: tuple[Any, ...]) -> EcologyRoster:
    from .config import AgentConfig, GoalWeights

    gw = GoalWeights(1.0, 1.0, 0.5, 0.5)
    return EcologyRoster(
        agents=tuple(
            AgentConfig(
                getattr(a, "actor_id", str(a)),
                getattr(a, "role", ""),
                gw,
            )
            for a in agents
        ),
        genotypes_by_actor={},
    )


def compile_exercise_targets(
    data: dict,
    agents: tuple[Any, ...],
) -> ExerciseTargets | None:
    """Resolve Part B exercise targets at ecology compile time (GL-64)."""
    if not v3_has_part_b_mechanisms(data):
        return None
    roster = _roster_from_agents(agents)
    ref = reference_mechanism_exercise_targets(data, roster)
    if ref is None:
        ref = default_exercise_targets(data, roster)
    if mechanism_exercise_disabled(data):
        ref = {**ref, "channel_coupling_rounds": 0}
    return ExerciseTargets(
        channel_id=str(ref.get("channel_id", "")),
        channel_coupling_rounds=int(ref.get("channel_coupling_rounds", 0) or 0),
        channel_eng_actor=str(ref.get("channel_eng_actor", "")),
        channel_rev_actor=str(ref.get("channel_rev_actor", "")),
        artifact_id=str(ref.get("artifact_id", "")),
        vote_id=str(ref.get("vote_id", "")),
        transfer_id=str(ref.get("transfer_id", "")),
        transfer_target=str(ref.get("transfer_target", "")),
        artifact_path=str(
            ref.get("artifact_path", "artifacts/eval/governed_exercise_report.json")
        ),
    )


def v3_omit_unbound_lab_affordances(data: dict) -> bool:
    """Hide unbound ``lab``/scratch fillers when v3 Part B is declared (GL-62)."""
    return v3_has_part_b_mechanisms(data)


def mechanism_exercise_profile_for_ecology(
    data: dict, roster: EcologyRoster
) -> dict[str, object] | None:
    """Host profile merge for reference-roster episodes (GL-58 auto path).

    v3 ecologies with Part B ``mechanisms`` receive exercise targets unless
    ``reference_mechanism_exercise`` is explicitly ``false`` / ``enabled:
    false``. An absent field no longer blocks merge; an object/true still
    overrides coupling rounds and explicit ids.
    """
    if not v3_has_part_b_mechanisms(data) or mechanism_exercise_disabled(data):
        return None
    ref_targets = reference_mechanism_exercise_targets(data, roster)
    targets = ref_targets if ref_targets is not None else default_exercise_targets(data, roster)
    return {"mechanism_exercise": targets}


def validate_reference_mechanism_exercise(config: object) -> None:
    if config is None or config is False:
        return
    if config is True:
        return
    if not isinstance(config, dict):
        from .substrate import SubstrateError

        raise SubstrateError("reference_mechanism_exercise must be true, false, or an object")
    allowed = {
        "enabled",
        "channel_id",
        "channel_coupling_rounds",
        "channel_exchanges_per_role",  # alias
        "artifact_id",
        "vote_id",
        "transfer_id",
        "transfer_target",
        "artifact_path",
    }
    for key in ("channel_coupling_rounds", "channel_exchanges_per_role"):
        if key in config:
            n = config[key]
            if not isinstance(n, int) or n < 0:
                from .substrate import SubstrateError

                raise SubstrateError(
                    f"reference_mechanism_exercise.{key} must be int >= 0"
                )
    unknown = set(config) - allowed
    if unknown:
        from .substrate import SubstrateError

        raise SubstrateError(
            f"reference_mechanism_exercise unknown keys: {sorted(unknown)}"
        )


def mechanism_exercise_profile(data: dict, roster: EcologyRoster) -> dict[str, object]:
    """Backward-compatible alias; prefer ``reference_mechanism_exercise_profile``."""
    out = reference_mechanism_exercise_profile(data, roster)
    return out if out is not None else {}


# Irregular idle gaps after each half-turn so the eng↔rev pattern is
# lag-coupled but not period-2 shift-invariant (circular-shift nulls
# otherwise return thr == obs == 1.0 on short alternating windows).
_DEFAULT_GAP_CYCLE = (0, 1, 0, 2, 1, 0, 1, 2)


@dataclass
class ChannelCouplingProtocol:
    """Host-owned eng↔rev channel stimulus for behavioral UAD (GL-52).

    While active, only the current speaker may ``communicate`` on the
    governed channel; every other actor is skipped (idle in the UAD
    trace). Irregular post-turn gaps break pure period-2 symmetry so the
    standard CMI + circular-shift null accepts the edge. Pressure and
    ordinary pipeline affordances resume after the protocol completes.
    Agents do not count turns — they take the afforded action.
    """

    channel_id: str
    eng_actor: str
    rev_actor: str
    rounds: int
    half_turns_done: int = 0
    idle_ticks_remaining: int = 0
    gap_cycle: tuple[int, ...] = _DEFAULT_GAP_CYCLE
    _log: list[dict[str, object]] = field(default_factory=list)

    @classmethod
    def from_targets(cls, targets: dict[str, object] | None) -> ChannelCouplingProtocol | None:
        if not targets:
            return None
        rounds = int(targets.get("channel_coupling_rounds", DEFAULT_CHANNEL_COUPLING_ROUNDS))
        channel_id = str(targets.get("channel_id", ""))
        eng = str(targets.get("channel_eng_actor", ""))
        rev = str(targets.get("channel_rev_actor", ""))
        if rounds <= 0 or not channel_id or not eng or not rev:
            return None
        return cls(channel_id=channel_id, eng_actor=eng, rev_actor=rev, rounds=rounds)

    @property
    def active(self) -> bool:
        return self.half_turns_done < 2 * self.rounds or self.idle_ticks_remaining > 0

    @property
    def coupling_complete(self) -> bool:
        return self.half_turns_done >= 2 * self.rounds and self.idle_ticks_remaining == 0

    def tick_idle(self) -> None:
        """Consume one host idle gap tick (call once per world tick while idling)."""
        if self.idle_ticks_remaining > 0:
            self.idle_ticks_remaining -= 1

    def speaker(self) -> str | None:
        if self.half_turns_done >= 2 * self.rounds:
            return None
        if self.idle_ticks_remaining > 0:
            return None
        return self.eng_actor if self.half_turns_done % 2 == 0 else self.rev_actor

    def communicate_action(self, *, role: str) -> PrimitiveAction:
        return PrimitiveAction(
            "communicate",
            {
                "channel": self.channel_id,
                "message": {"kind": "mechanism_exercise", "role": role},
            },
        )

    def restricted_affordables(
        self, *, actor_id: str, role: str
    ) -> list[PrimitiveAction] | None:
        """Affordances during the coupling phase.

        Only the current speaker may act (one communicate). All other actors
        — and everyone during an idle gap — receive an empty set so the host
        skips their decision tick (idle in the UAD trace).
        """
        if not self.active:
            return None
        speaker = self.speaker()
        if speaker is not None and actor_id == speaker:
            return [self.communicate_action(role=role)]
        return []

    def note_success(self, *, actor_id: str, action: PrimitiveAction, t: int) -> None:
        speaker = self.speaker()
        if speaker is None or actor_id != speaker:
            return
        if action.kind != "communicate":
            return
        args = action.args if isinstance(action.args, dict) else {}
        if str(args.get("channel", "")) != self.channel_id:
            return
        self.half_turns_done += 1
        gap = self.gap_cycle[(self.half_turns_done - 1) % len(self.gap_cycle)]
        self.idle_ticks_remaining = gap
        self._log.append(
            {
                "t": t,
                "actor_id": actor_id,
                "half_turn": self.half_turns_done,
                "channel_id": self.channel_id,
                "gap_after": gap,
            }
        )

    def diagnostics(self) -> dict[str, object]:
        return {
            "channel_id": self.channel_id,
            "rounds_requested": self.rounds,
            "half_turns_done": self.half_turns_done,
            "completed": self.coupling_complete,
            "exchange_log": list(self._log),
        }


def governed_mechanism_primitives(
    *,
    role: str,
    targets: dict[str, object],
    channel_acls: dict[str, frozenset[str]],
    artifact_acls: dict[str, frozenset[str]],
    transfer_acls: dict[str, frozenset[str]],
    vote_specs: dict[str, Any],
    include_channel: bool = True,
) -> list[PrimitiveAction]:
    """Affordable governed primitives for roles exercising slice B mechanisms.

    When a :class:`ChannelCouplingProtocol` owns the channel phase, pass
    ``include_channel=False`` so the post-protocol phase does not re-offer
    channel communicates (C5 channel credit already earned in the protocol).
    """
    out: list[PrimitiveAction] = []
    channel_id = str(targets.get("channel_id", ""))
    if (
        include_channel
        and channel_id
        and role in channel_acls.get(channel_id, frozenset())
    ):
        out.append(
            PrimitiveAction(
                "communicate",
                {
                    "channel": channel_id,
                    "message": {"kind": "mechanism_exercise", "role": role},
                },
            )
        )
    artifact_id = str(targets.get("artifact_id", ""))
    artifact_path = str(
        targets.get("artifact_path", "artifacts/eval/governed_exercise_report.json")
    )
    if artifact_id and role in artifact_acls.get(artifact_id, frozenset()):
        if role == "engineer":
            out.append(
                PrimitiveAction(
                    "write",
                    {
                        "artifact_id": artifact_id,
                        "path": artifact_path,
                        "content": {"kind": "governed_eval_report", "status": "draft"},
                    },
                )
            )
        if role == "reviewer":
            out.append(
                PrimitiveAction(
                    "read",
                    {"artifact_id": artifact_id, "path": artifact_path},
                )
            )
    vote_id = str(targets.get("vote_id", ""))
    if vote_id and vote_id in vote_specs and role in vote_specs[vote_id].members:
        out.append(
            PrimitiveAction(
                "call",
                {
                    "endpoint": "vote.cast",
                    "args": {"vote_id": vote_id, "approve": True},
                },
            )
        )
    transfer_id = str(targets.get("transfer_id", ""))
    target = str(targets.get("transfer_target", ""))
    if transfer_id and role in transfer_acls.get(transfer_id, frozenset()):
        out.append(
            PrimitiveAction(
                "call",
                {
                    "endpoint": "transfer.execute",
                    "args": {
                        "mechanism_id": transfer_id,
                        "target_actor_id": target,
                    },
                },
            )
        )
    return out


def _kind_for_channel(channel: str, data: dict) -> str | None:
    for mech in data.get("mechanisms", []):
        if isinstance(mech, dict) and mech.get("id") == channel:
            kind = mech.get("kind")
            return str(kind) if kind in MECHANISM_KINDS else None
    return None


def _kind_for_artifact(artifact_id: str, data: dict) -> str | None:
    for mech in data.get("mechanisms", []):
        if isinstance(mech, dict) and mech.get("id") == artifact_id:
            kind = mech.get("kind")
            return str(kind) if kind in MECHANISM_KINDS else None
    return None


def kinds_exercised_in_log(primitive_log: list[dict], *, ecology_data: dict) -> set[str]:
    """Mechanism kinds successfully targeted by id in ``primitive_log``."""
    kinds: set[str] = set()
    for entry in primitive_log:
        if entry.get("status") != "ok":
            continue
        prim = entry.get("primitive")
        if not isinstance(prim, dict):
            continue
        kind = prim.get("kind")
        args = prim.get("args", {})
        if not isinstance(args, dict):
            continue
        if kind == "communicate":
            channel = str(args.get("channel", ""))
            mk = _kind_for_channel(channel, ecology_data)
            if mk:
                kinds.add(mk)
        elif kind in ("read", "write"):
            aid = args.get("artifact_id")
            if isinstance(aid, str):
                mk = _kind_for_artifact(aid, ecology_data)
                if mk:
                    kinds.add(mk)
        elif kind == "call":
            endpoint = str(args.get("endpoint", ""))
            inner = args.get("args", {})
            if not isinstance(inner, dict):
                continue
            if endpoint == "vote.cast":
                vote_id = str(inner.get("vote_id", ""))
                for mech in ecology_data.get("mechanisms", []):
                    if (
                        isinstance(mech, dict)
                        and mech.get("id") == vote_id
                        and mech.get("kind") == "joint_approval_vote"
                    ):
                        kinds.add("joint_approval_vote")
            elif endpoint == "transfer.execute":
                mid = str(inner.get("mechanism_id", ""))
                for mech in ecology_data.get("mechanisms", []):
                    if (
                        isinstance(mech, dict)
                        and mech.get("id") == mid
                        and mech.get("kind") == "resource_transfer"
                    ):
                        kinds.add("resource_transfer")
    return kinds


def check_c5_v3(
    ecology_data: dict,
    results: list[Any],
) -> tuple[bool, dict[str, object]]:
    """C5-v3: ≥3 mechanism kinds declared **and** exercised in reference episodes.

    Exercise is measured on the reference battery with host-injected
    ``mechanism_exercise`` (GL-58 auto-merge when the field is absent) **or**
    GL-62 ecology affordance presets when host merge is off. Does not claim
    ecology-forced grower ``ProgramMap`` genotypes beyond frozen preset paths.
    """
    kinds_declared: set[str] = set()
    for mech in ecology_data.get("mechanisms", []):
        if isinstance(mech, dict) and mech.get("kind") in MECHANISM_KINDS:
            kinds_declared.add(str(mech["kind"]))
    exercised: set[str] = set()
    for result in results:
        exercised |= kinds_exercised_in_log(result.primitive_log, ecology_data=ecology_data)
    passed = (
        len(kinds_declared) >= C5_V3_MIN_KINDS_EXERCISED
        and len(exercised) >= C5_V3_MIN_KINDS_EXERCISED
    )
    return passed, {
        "kinds_declared": sorted(kinds_declared),
        "kinds_exercised": sorted(exercised),
        "min_required": C5_V3_MIN_KINDS_EXERCISED,
    }


def live_coupling_ground_truth_units(
    ecology_data: dict,
    roster: EcologyRoster,
    *,
    channel_id: str | None = None,
) -> dict[str, tuple[str, ...]]:
    """UAD ground truth from a governed channel's declared membership (live coupling)."""
    cid = channel_id or _pick_mechanism_id(ecology_data, "message_channel")
    if not cid:
        return {}
    members: set[str] = set()
    for mech in ecology_data.get("mechanisms", []):
        if not isinstance(mech, dict) or mech.get("id") != cid:
            continue
        roles = mech.get("members_ground_truth", [])
        if not isinstance(roles, list):
            break
        for role in roles:
            if role not in ROLES:
                continue
            for agent in roster.agents:
                if agent.role == role:
                    members.add(agent.actor_id)
    if len(members) < 2:
        return {}
    return {f"governed_{cid}": tuple(sorted(members))}


def coupling_window_horizon(result) -> int | None:
    """End tick (exclusive) of a completed host coupling protocol, if any."""
    diag = (result.referee_artifacts or {}).get("channel_coupling_protocol")
    if not isinstance(diag, dict) or not diag.get("completed"):
        return None
    log = diag.get("exchange_log")
    if not isinstance(log, list) or not log:
        return None
    last_t = max(int(e.get("t", 0)) for e in log if isinstance(e, dict))
    # Pad for lag-max CMI (DEFAULT_MAX_LAG=3 in uad_discovery).
    return last_t + 1 + 3


def discovered_units_uad_coupling_window(result, *, rng_seed: int = 0):
    """Passive UAD restricted to the host coupling-protocol window (GL-52).

    Full-episode UAD mixes pipeline/pressure codes that can screen or over-merge
    the designed channel stimulus. Prefer :func:`coupling_stimulus_recovered`
    for the live-coupling gate — short designed stimuli can tie the
    circular-shift null even when lag-max CMI is large.
    """
    from ..oracle_only.uad_discovery import discovered_units_uad

    horizon = coupling_window_horizon(result)
    if horizon is None:
        return discovered_units_uad(result=result, rng_seed=rng_seed)

    class _WindowResult:
        def __init__(self, base, tmax: int) -> None:
            self.boundary_streams = base.boundary_streams
            self.primitive_log = [
                e for e in base.primitive_log if int(e.get("t", 0)) < tmax
            ]

    return discovered_units_uad(result=_WindowResult(result, horizon), rng_seed=rng_seed)


def coupling_stimulus_recovered(
    result,
    expected_members: set[str],
    *,
    min_effect_bits: float | None = None,
) -> tuple[bool, dict[str, object]]:
    """Live-coupling gate for a host-designed channel stimulus (GL-52).

    Checks that every pair among ``expected_members`` has lag-max
    ``I(A;B|rest) >= min_effect_bits`` on the coupling window. This is an
    **effect-size** criterion, not the circular-shift null used by open
    discovery: short eng↔rev protocols are lag-coupled by construction and
    can make shift-null thresholds equal the observed score (seed-flaky
    false negatives) without being informationally weak.
    """
    from itertools import combinations

    from ..oracle_only.primitive_trace import action_series_from_result
    from ..oracle_only.uad_discovery import DEFAULT_MIN_EFFECT_BITS
    from ..oracle_only.uad_info import lagmax_conditional_mi

    floor = DEFAULT_MIN_EFFECT_BITS if min_effect_bits is None else min_effect_bits
    horizon = coupling_window_horizon(result)
    details: dict[str, object] = {
        "horizon": horizon,
        "min_effect_bits": floor,
        "pair_scores": {},
    }
    if horizon is None:
        details["error"] = "no completed coupling protocol"
        return False, details
    if len(expected_members) < 2:
        details["error"] = "need at least two expected members"
        return False, details

    actor_ids = sorted(result.boundary_streams)
    series = action_series_from_result(result, actor_ids, horizon=horizon)
    pair_scores: dict[str, float] = {}
    ok = True
    for a, b in combinations(sorted(expected_members), 2):
        rest = [c for c in actor_ids if c not in (a, b)]
        z = list(zip(*[series[c] for c in rest])) if rest else [0] * horizon
        score = lagmax_conditional_mi(series[a], series[b], z, max_lag=3)
        pair_scores[f"{a}|{b}"] = score
        if score < floor:
            ok = False
    details["pair_scores"] = pair_scores
    return ok, details


def organic_coupling_window_horizon(
    result,
    *,
    channel_id: str,
    members: set[str],
    min_events: int = 6,
    max_gap: int = 4,
    max_span: int = 48,
) -> int | None:
    """End tick (exclusive) for the initial in-ecology channel burst (GL-65/66).

    When traffic continues for the whole episode (GL-66 attention surface),
    scoring on ``max(ticks)`` dilutes CMI. Stop at the first inter-message
    gap or ``max_span`` from the first event.
    """
    ticks: list[int] = []
    for entry in result.primitive_log:
        if entry.get("status") != "ok":
            continue
        actor_id = str(entry.get("actor_id", ""))
        if actor_id not in members:
            continue
        prim = entry.get("primitive")
        if not isinstance(prim, dict) or prim.get("kind") != "communicate":
            continue
        args = prim.get("args", {})
        if not isinstance(args, dict) or str(args.get("channel", "")) != channel_id:
            continue
        ticks.append(int(entry.get("t", 0)))
    if len(ticks) < min_events:
        return None
    ticks.sort()
    first = ticks[0]
    burst_end = ticks[min_events - 1]
    for i in range(min_events, len(ticks)):
        if ticks[i] - ticks[i - 1] > max_gap:
            burst_end = ticks[i - 1]
            break
        if ticks[i] - first >= max_span:
            burst_end = ticks[i]
            break
    else:
        burst_end = min(ticks[-1], first + max_span)
    return burst_end + 1 + 3


def organic_channel_coupling_recovered(
    result,
    expected_members: set[str],
    *,
    channel_id: str = "",
    min_effect_bits: float | None = None,
) -> tuple[bool, dict[str, object]]:
    """GL-65: lag-max CMI on the organic channel-active window."""
    from itertools import combinations

    from ..oracle_only.primitive_trace import action_series_from_result
    from ..oracle_only.uad_discovery import DEFAULT_MIN_EFFECT_BITS
    from ..oracle_only.uad_info import lagmax_conditional_mi

    floor = DEFAULT_MIN_EFFECT_BITS if min_effect_bits is None else min_effect_bits
    actor_ids = sorted(result.boundary_streams)
    horizon = organic_coupling_window_horizon(
        result,
        channel_id=channel_id or "eng_review_channel",
        members=expected_members,
    )
    if horizon is None:
        horizon = max(
            (len(stream) for stream in result.boundary_streams.values()),
            default=0,
        )
    details: dict[str, object] = {
        "horizon": horizon,
        "min_effect_bits": floor,
        "pair_scores": {},
        "source": "organic_channel_window",
    }
    if horizon < 8:
        details["error"] = "episode too short for organic coupling gate"
        return False, details
    if len(expected_members) < 2:
        details["error"] = "need at least two expected members"
        return False, details

    series = action_series_from_result(result, actor_ids, horizon=horizon)
    pair_scores: dict[str, float] = {}
    ok = True
    for a, b in combinations(sorted(expected_members), 2):
        rest = [c for c in actor_ids if c not in (a, b)]
        z = list(zip(*[series[c] for c in rest])) if rest else [0] * horizon
        score = lagmax_conditional_mi(series[a], series[b], z, max_lag=3)
        pair_scores[f"{a}|{b}"] = score
        if score < floor:
            ok = False
    details["pair_scores"] = pair_scores
    return ok, details
