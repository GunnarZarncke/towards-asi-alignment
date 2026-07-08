"""Configuration dataclasses for the lab-layer simulation.

Frozen Phase 0 decisions (see DESIGN.md for rationale; PLAN.md for the full
plan). Highlights that live in this module:

- ``CODE_VERSION``: hand-bumped whenever oracle/pipeline/playbook mechanics
  change. It is part of every episode-cache key (Phase 4 ``cache.py``) so a
  code change can never silently serve a stale cached result.
- ``GoalWeights``: the same 4-feature goal simplex as goal_sim (task,
  compliance, welfare, exposure), stored unnormalized with ``normalized()``.
- ``AgentConfig.persistent_id``: ``None`` (default) = fully ephemeral agent;
  set = host loads/saves ``runs/agent_state/<id>.json`` across episodes
  (Phase 3 mechanism; needed for human roles).
- ``LabConfig.units``: oracle-only ground truth of which actor_ids jointly
  constitute one causal unit (forward hook for the D1 UAD workstream).
  ``None`` = every actor is its own singleton unit.
- ``BoardConfig.capture_start`` / ``AdminConfig.capture_start``: two
  INDEPENDENT capture switches (the structural generalization of goal_sim
  finding F-22).
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Bump whenever oracle/pipeline/playbook mechanics change (cache-key input).
# 0.2.0: monitor signal (audit-visible noisy incident_hazard), perturbation
# hooks, tool registry, deterministic _actor_seed.
# 0.3.0: handles (registry + HandleService + overseer invocation path,
# release holds in the engine), referee report-join on authoritative
# model_id, tool-event args elision (content digest only), engineer
# mid-model availability for boundary-handle recovery.
# 0.4.0 (Phase 6): LabConfig.extra_playbooks + playbooks.merged_repertoire —
# additive, backward-compatible blind-generated-repertoire loading (default
# `()` reproduces baseline behavior byte-for-byte; see playbooks.py
# "Phase 6" section). Referee (detectors/severity/tiers/twins) untouched.
# 0.5.0 (Phase 7): LabConfig.build_params — additive, backward-compatible
# override of the hardcoded (scale=0.6, safety_effort=0.5) build params
# `programs._resolve_step_kind`'s "build" case used unconditionally through
# Phase 6 (default `None` reproduces that literal byte-for-byte). Needed
# because `ontology.REVIEW_HAZARD_THRESHOLD` (0.5) and `BoardConfig`'s dead
# `harm_tolerance`/`sign_off_harm_ceiling` fields can only ever "bind" (see
# escalation/capture battery discussion in DESIGN.md) if a model's measured
# hazard can actually reach that bar — impossible under the old hardcoded
# params (expected hazard ~0.35, ~3 sd below threshold). This does not wire
# up the dead `BoardConfig` fields themselves (out of scope here); it only
# makes the EXISTING `review_conscientious` content check reachable.
# 0.6.0 (follow-up tranche): server-side `build_params` enforcement on
# engineer `submit_build`; playbook-selection audit channel (G-3);
# `eng_capability_probe` + `access:out_of_role` step kind (G-6); red-team
# search uses high-hazard `build_params` by default (G-5).
# 0.7.0 (D4/D1): `LabConfig.comms_enabled` — additive, backward-compatible
# (default False reproduces every pre-0.7.0 episode byte-for-byte; comms
# tools are registered unconditionally in `tools.Host` but no-op when
# `Host.comms is None`) TalkJS-like board/DM message layer (`comms.py`);
# `"decoy"` role for the D1 UAD stress population; `on_behalf_of` (a
# Phase 3 forward hook, never populated before) wired through
# `tools._tool_trigger_step` for the reviewer-committee mechanic
# (`programs._resolve_review_committee`).
# 0.8.0 (D1 follow-up, user-directed scope expansion): unit boundaries are
# not only a messaging phenomenon. Adds (a) a THIRD coordination channel,
# `file.write`/`file.share`/`file.read`, backed by the on-disk `Workspace`
# (`memos/`) rather than `comms.MessageStore` — realistically permissioned,
# NOT world-readable: a memo's owner is tracked ONLY server-side
# (`Host.memo_index`, never in the filename or any observation field,
# matching a real filesystem's inode metadata, not a free "agent id" tag);
# reading anyone else's memo requires the OWNER to have explicitly shared
# it (`file.share`, a chmod-like self-service grant recorded through the
# EXISTING `PermissionService` as `cap.file_read:<rel>` — a real
# access-log-visible event, not a silent side channel), targeting either
# one actor (`with=`) or a named `LabConfig.groups` roster (`with_group=`
# — a DELIBERATELY separate concept from `units`, see that field's
# docstring). This gives `uad.py`/`collusion.py` a real coordination case
# the 0.7.0 board/DM-only signals would silently miss, discoverable at
# FULL tier from share-grant metadata alone (`access_log`'s `capability`/
# `by` fields), a third tier-sufficiency data point alongside G-9's
# board/DM asymmetry. A file-channel variant of the committee mechanic
# (`review_committee_file`, `programs._resolve_review_committee`
# parametrized by `channel`) exercises this end to end. Also (b) real
# wiring of the `AgentConfig.persistent_id` forward hook (`state.save` now
# persists, `state.load` added) — HOST-MEDIATED, not an isolate-spawn
# change: the `persistent_id -> file` lookup lives only in
# `Host.persistent_ids`, never on the observation channel or in any log,
# so the agent experiences continuity of its own remembered content
# without ever seeing the id used to look it up. All additive/off unless
# an episode explicitly opts in (`comms_enabled=True` / sets `groups` /
# sets `persistent_id`); every pre-0.8.0 config is byte-identical.
# 0.9.0 (post-freeze consolidation pass, 2026-07-06): four refactors
# (unified `agents.ROLE_CAPABILITIES` + `CREEP_EXEMPT_CAPABILITIES`; split
# per-channel comms lever `board_enabled`/`dm_enabled`/`file_enabled` +
# `channel_enabled()`; explicit `playbook_pins` steering replacing
# feature-delta tie-break tuning; `access.PermissionService` hash-chain
# consolidated onto `events.EventLog`) plus five additive features: D4
# channel-ablation battery (`run_d4_channel_ablation.py`); perturbation-
# response MI as a second UAD signal (`uad.py`); full D2 (model-from-model
# `build_from_parent` + `eng_honest_upgrade`; spec-upgrade `upgrade_spec`
# step in `pipeline_default.json` + `rm_spec_upgrade` playbook, both
# behind `LabConfig.multi_gen_enabled=False` default; `resume_from`
# episode chaining via `OracleWorld.full_state`/`restore` +
# `PipelineEngine(resume_state=...)` + `EpisodeResult.snapshot_for_resume`,
# `None` default); and a round-2 blind-generated repertoire covering the
# board/DM/file coordination step-kinds (`generated_playbooks_v2.json`,
# `BLIND_GENERATION_ROUND2.md`), recovered at parity with the hand-
# authored baseline by the frozen `uad.py`/`collusion.py` extensions
# (`run_blind_round2.py`). All four refactors verified byte-identical
# against the pre-existing `PINNED_DIGEST`; every new feature is off by
# default. See PLAN.md "Post-freeze consolidation pass".
# 0.9.1 (post-Phase-10, user-directed): `LabConfig.knowledge_base` -- an
# optional realistic, in-universe lab knowledge base (`knowledge_base.py`)
# seeded as ordinary memos owned by a reserved, non-agent pseudo-actor
# (`knowledge_base.KB_OWNER_ID`), read-granted to every playbook agent at
# episode init the same way the `comms_enabled` bootstrap already grants
# comm capabilities. Reuses the EXISTING D1 file channel's permission
# model rather than adding a new one, so discovery is exactly as natural,
# and tamper-evidence exactly as strong, as any other memo (see
# `knowledge_base.py` module docstring). Default `{}` (falsy) reproduces
# every pre-0.9.1 episode byte-for-byte: `world.run_episode` skips the KB
# bootstrap entirely when unset.
# 0.9.2 (user-directed follow-up: "10x the content, include what a
# red-team member would be given"): `knowledge_base.py` grew from two
# thin docs to a ten-document general-audience bundle
# (`default_full_knowledge_base`) covering the pipeline reference,
# capability/access-request argument shapes, a verbose tool operations
# manual, safety/review policy (citing the SAME `ontology.
# REVIEW_HAZARD_THRESHOLD`/`INFLATE_HAZARD_DELTA` constants the reviewer
# playbooks apply), escalation contacts, FAQ, glossary, and incident
# postmortems -- deliberately redundant across docs, like a real
# organically-grown wiki. Plus `LabConfig.knowledge_base_redteam`/
# `redteam_actor_ids`: a SECOND, restricted KB (a security-assessment
# briefing) granted only to named actors, reusing the identical
# bootstrap mechanism with a smaller grant set. Both default to
# empty/falsy; byte-identical to every pre-0.9.2 episode until used.
# 0.9.3 (medium-lift follow-up, "adversarial D2 lineage gaming", 2026-07-08):
# `eng_inflate_upgrade` playbook (`playbooks.py`) -- identical to
# `eng_honest_upgrade` except `report:inflate` in place of
# `report:honest`, the first playbook combining `build_from_parent` with
# dishonest reporting (PLAN.md's "still open" note; FINDINGS.md G-12,
# G-15). Purely additive: no existing playbook, step-kind, or detector
# changed; only reachable via explicit `playbook_pins={"eng1":
# "eng_inflate_upgrade"}` (`ecology.d2_lineage_config(inflate=True)`), so
# every pre-0.9.3 episode is byte-identical.
CODE_VERSION = "lab-sim-0.9.3"

ROLES = ("engineer", "reviewer", "release_manager", "admin", "overseer", "decoy")

TIERS = ("none", "light", "full", "deep")

# Field names that must never appear in any audit-visible projection or
# engine log entry. Enforced by tests/test_planes.py.
ORACLE_ONLY_FIELDS = (
    "true_capability",
    "true_hazard",
    "bearer_harm",
    "units",
    "groups",
    "goal_weights",
    "board_captured",
    "admin_captured",
)


@dataclass(frozen=True)
class GoalWeights:
    """Nonnegative weights over the agent's four utility features.

    Stored unnormalized; ``normalized()`` projects onto the simplex so
    sampled draws and hand-written test configs behave identically.
    """

    task: float
    compliance: float
    welfare: float
    exposure: float

    def normalized(self) -> "GoalWeights":
        total = self.task + self.compliance + self.welfare + self.exposure
        if total <= 0:
            return GoalWeights(0.25, 0.25, 0.25, 0.25)
        return GoalWeights(
            self.task / total,
            self.compliance / total,
            self.welfare / total,
            self.exposure / total,
        )


@dataclass(frozen=True)
class AgentConfig:
    """One lab-role agent.

    ``actor_id`` must be unique within a ``LabConfig``. ``persistent_id``
    is the cross-episode state key (Phase 3); ``None`` = ephemeral.
    """

    actor_id: str
    role: str
    weights: GoalWeights
    temperature: float = 0.10
    persistent_id: str | None = None

    def __post_init__(self) -> None:
        if self.role not in ROLES:
            raise ValueError(f"unknown role {self.role!r}; expected one of {ROLES}")


@dataclass(frozen=True)
class BoardConfig:
    """Review-board policy parameters (sign-off channel).

    ``capture_start``: step index at/after which the board is captured
    (rubber-stamps reviews, stops corrective action). ``None`` = never.
    Independent of ``AdminConfig.capture_start`` by design (F-22 lesson).
    """

    harm_tolerance: float = 0.02
    sign_off_harm_ceiling: float = 0.015
    capture_start: int | None = None


@dataclass(frozen=True)
class AdminConfig:
    """Access-admin policy parameters (grant/revoke channel).

    ``capture_start``: step index at/after which the admin is captured
    (rubber-stamps grants, stops revoking). ``None`` = never. Independent
    of ``BoardConfig.capture_start`` by design.
    """

    least_privilege: bool = True
    capture_start: int | None = None
    persistent_id: str | None = None


@dataclass(frozen=True)
class TierConfig:
    """Instrumentation tier for the audit projection."""

    tier: str = "full"

    def __post_init__(self) -> None:
        if self.tier not in TIERS:
            raise ValueError(f"unknown tier {self.tier!r}; expected one of {TIERS}")


@dataclass(frozen=True)
class LabConfig:
    """Top-level episode configuration.

    ``units``: oracle-only mapping ``unit_id -> tuple of actor_ids`` naming
    the true causal units (D1 forward hook). ``None`` = singletons.
    ``pipeline_spec``: filename of the pipeline-as-code DAG spec, resolved
    relative to the ``lab_sim`` package directory.
    """

    agents: tuple[AgentConfig, ...] = ()
    board: BoardConfig = field(default_factory=BoardConfig)
    admin: AdminConfig = field(default_factory=AdminConfig)
    tier: TierConfig = field(default_factory=TierConfig)
    T: int = 200
    pipeline_spec: str = "pipeline_default.json"
    units: tuple[tuple[str, tuple[str, ...]], ...] | None = None
    # D1 file-channel permission groups (0.8.0, user-directed redesign):
    # named rosters a `file.share` call may target via `with_group=<id>`
    # (see `tools._tool_file_share`). Deliberately a SEPARATE concept from
    # `units` — a file-sharing group is admin-defined convenience
    # infrastructure (like a Unix group), NOT a claim about which actors
    # form a true causal decision unit; a specific config MAY set them to
    # coincide, but nothing enforces it, and `uad.py`'s discovery never
    # reads this field (oracle-only, like `units`). ``None`` (default) =
    # no groups configured; `with_group` calls resolve to nobody.
    groups: tuple[tuple[str, tuple[str, ...]], ...] | None = None
    config_id: str = ""
    # Phase 6: optional blind-generated playbook repertoire (plain dicts,
    # JSON-safe — crosses the isolate boundary via the observation channel
    # exactly like `goal_weights`). Default `()` is falsy, so
    # `programs._repertoire`/`playbooks.merged_repertoire` fall back to the
    # hand-authored `PLAYBOOKS_BY_ROLE` baseline unchanged — every config
    # through the Phase 5 freeze leaves this unset and is unaffected.
    extra_playbooks: tuple[dict, ...] = ()
    # Phase 7: optional override of the build params every "build"/
    # "submit_build" step uses (`{"scale": ..., "safety_effort": ...}`).
    # `None` (default) reproduces the Phase 0-6 hardcoded literal exactly —
    # see CODE_VERSION 0.5.0 note above.
    build_params: dict[str, float] | None = None
    # G-6: when True, engineer may only select `eng_capability_probe` on the
    # first turn (requests an out-of-role capability). Default False.
    capability_probe_mode: bool = False
    # D4 (CODE_VERSION 0.7.0): enables the board/DM message layer
    # (`comms.py`) and the comm-aware playbooks (`review_committee`,
    # `dm:notify_release`, ...). Default False reproduces every
    # pre-0.7.0 episode byte-for-byte: `world.run_episode` skips
    # `MessageStore`/grant bootstrap entirely, and
    # `playbooks.available_playbooks` filters out every playbook whose
    # step_kinds require comms (see `playbooks._requires_comms`).
    comms_enabled: bool = False
    # D4 channel-ablation (post-freeze consolidation pass, PLAN.md): a
    # per-channel override of `comms_enabled`. `None` (the default for all
    # three) means "inherit `comms_enabled`" -- every config that only
    # ever set `comms_enabled` resolves identically to before (see
    # `channel_enabled()`). Setting exactly one of these to `False` while
    # `comms_enabled=True` is the ablation lever: sever ONE coordination
    # channel while holding the others at their normal state.
    board_enabled: bool | None = None
    dm_enabled: bool | None = None
    file_enabled: bool | None = None
    # D2 (post-freeze consolidation pass): enables the model-from-model
    # (`build_from_parent`) and spec-upgrade (`upgrade_spec`) mechanics.
    # Default False reproduces every pre-D2 episode byte-for-byte:
    # `playbooks.available_playbooks` filters out `eng_honest_upgrade`/
    # any playbook using `spec_upgrade`, and `world.py` never
    # pre-provisions `cap.spec_upgrade`. See PLAN.md "Post-freeze
    # consolidation pass" items 7-8.
    multi_gen_enabled: bool = False
    # D2: filename of the spec `upgrade_spec` should switch the engine to
    # (resolved the same way `LabConfig.pipeline_spec` is). `None` (default)
    # disables the step's availability entirely -- a config must name an
    # explicit target, never a hardcoded literal.
    spec_upgrade_target: str | None = None
    # Post-freeze consolidation pass, item 3 ("clean playbook selection
    # steering"): `actor_id -> playbook name`, an explicit override that
    # `programs._goal_policy` consults BEFORE softmax scoring -- replaces
    # the earlier pattern of hand-tuning `feature_deltas`/goal-weight
    # vectors so one playbook would out-score another by a deliberately
    # engineered margin (see the D1 file-channel tie-break bug recorded in
    # PLAN.md's "D1 follow-up" section). Default `{}` (no pins) is exactly
    # the old emergent-softmax behavior. A pin that names a playbook not
    # currently available this turn is silently ignored (falls through to
    # softmax), never an error -- a pin is a steering preference, not a
    # guarantee independent of the playbook's own availability gate.
    playbook_pins: dict[str, str] = field(default_factory=dict)
    # 0.9.1: optional `{doc_name: content_dict}` knowledge base, seeded as
    # read-only memos every playbook agent is pre-granted at init (see
    # `knowledge_base.py`). `{}` (default, falsy) reproduces every
    # pre-0.9.1 episode byte-for-byte -- `world.run_episode` skips the
    # bootstrap entirely. Requires the `file` channel to be enabled
    # (`comms_enabled=True`, or `file_enabled=True` under ablation); a KB
    # set with the file channel off is silently never seeded, matching
    # every other file-channel behavior under ablation.
    knowledge_base: dict[str, dict] = field(default_factory=dict)
    # 0.9.2: a SECOND, restricted knowledge base (e.g. a security/red-team
    # briefing) granted only to the actors named in `redteam_actor_ids`,
    # not every playbook agent -- same bootstrap mechanism as
    # `knowledge_base` (same `KB_OWNER_ID` pseudo-actor, same per-actor
    # `cap.file_read:<rel>` grant, just a smaller grant set). `{}` +
    # `()` (both default, falsy together) reproduce every pre-0.9.2
    # episode byte-for-byte.
    knowledge_base_redteam: dict[str, dict] = field(default_factory=dict)
    redteam_actor_ids: tuple[str, ...] = ()

    def channel_enabled(self, channel: str) -> bool:
        """Resolve one D4 coordination channel ("board"/"dm"/"file"):
        the per-channel override if set, else `comms_enabled`. Every
        config that never sets the per-channel fields is byte-identical
        to the pre-ablation single-lever behavior."""
        override = {"board": self.board_enabled, "dm": self.dm_enabled, "file": self.file_enabled}.get(channel)
        return self.comms_enabled if override is None else override

    def __post_init__(self) -> None:
        actor_ids = [a.actor_id for a in self.agents]
        if len(actor_ids) != len(set(actor_ids)):
            raise ValueError(f"duplicate actor_id in agents: {actor_ids}")
        if self.units is not None:
            unit_members = [m for _, members in self.units for m in members]
            unknown = set(unit_members) - set(actor_ids)
            if unknown:
                raise ValueError(f"units reference unknown actor_ids: {sorted(unknown)}")
        if self.groups is not None:
            group_members = [m for _, members in self.groups for m in members]
            unknown = set(group_members) - set(actor_ids)
            if unknown:
                raise ValueError(f"groups reference unknown actor_ids: {sorted(unknown)}")
        unknown_redteam = set(self.redteam_actor_ids) - set(actor_ids)
        if unknown_redteam:
            raise ValueError(f"redteam_actor_ids reference unknown actor_ids: {sorted(unknown_redteam)}")

    def resolved_units(self) -> dict[str, tuple[str, ...]]:
        """Oracle-only unit ground truth; defaults to one singleton per actor."""
        if self.units is not None:
            return dict(self.units)
        return {a.actor_id: (a.actor_id,) for a in self.agents}

    def resolved_groups(self) -> dict[str, tuple[str, ...]]:
        """Oracle-only file-sharing-group roster; ``None`` (the default) is
        "no groups configured" -- unlike ``resolved_units()`` there is no
        singleton fallback, since a nonexistent group is a legitimate
        `with_group` target (resolves to nobody), not a special case."""
        return dict(self.groups) if self.groups is not None else {}
