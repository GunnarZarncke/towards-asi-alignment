"""Declarative playbook SCHEMA (Phase 4) — mechanism only.

A ``PlaybookSpec`` is a hand-authored tactic: an ordered sequence of
abstract step-kinds (resolved to concrete tool calls by
``programs._resolve_step_kind``, using ``ontology.py`` for report content),
an availability gate (when the role may pick this playbook this turn), and
hand-authored ``feature_deltas`` over the same four goal features as
``config.GoalWeights`` (task, compliance, welfare, exposure) that the
softmax policy dot-products against the agent's weights.

Split out of the original ``playbooks.py`` (2026-07-09; ACCESS_TIERS.md
"Two judgment calls" item 1, now resolved): this module is the FORMAT
(dataclass, vocabulary, selector/validator functions) — a future red-team
grantee handed only this file can understand and extend the repertoire
without ever reading the actual baseline tactics (``playbooks_baseline.
PLAYBOOKS_BY_ROLE``), the same withholding discipline
``BLIND_GENERATION.md`` already applies to a *generated* repertoire. Every
selector below still defaults to the real baseline when no repertoire is
passed explicitly (``playbook_by_name``/``available_playbooks``/
``merged_repertoire``'s ``repertoire=None`` default) — a grantee reading
just this file sees THAT such a default exists (the import line below)
without seeing what it contains, exactly the "you can see the import, not
the content" signal a real oracle/world-visible split already relies on
elsewhere in this codebase.

Pure reorganization: no behavior changed, no ``CODE_VERSION`` bump (see
``playbooks.py``'s shim docstring). ``playbooks.py`` remains the stable
import path for every existing caller (``from lab_sim.agent_visible.
playbooks import ...``) — it now just re-exports from this module and
``playbooks_baseline.py``.

Pure, host-independent — importable by ``programs.py`` inside an isolate.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# Frozen BEFORE Phase 6 blind generation (see BLIND_GENERATION.md): the
# vocabulary a generated playbook may combine. A generator may invent new
# NAMES, ORDERS, SUBSETS, and FEATURE_DELTAS over this vocabulary; it may
# NOT invent a new step_kind or availability gate string, since those
# require a matching case in `programs._resolve_step_kind` /
# `available_playbooks` that does not exist. This is a real, stated
# constraint on generation freedom (recorded, not hidden), narrower than
# goal_sim's round-1 freedom — round 2+ may widen this vocabulary first,
# exactly as goal_sim widened `visible_mode` before its round 3.
STEP_KIND_VOCAB = frozenset({
    "build", "eval", "report:honest", "report:inflate",
    "review_request", "review_conscientious", "review_rubber_stamp",
    "release_full", "access:out_of_role",
    # D4/D1 (CODE_VERSION 0.7.0): comm-aware step kinds. `review_committee`
    # is a quorum-vote-over-the-board decision (programs.
    # _resolve_review_committee); `dm:notify_release` /
    # `release_full_dm_gated` are the engineer/release_manager DM-
    # coordinated pair. Any playbook whose step_kinds includes one of
    # these (or anything else prefixed `board:`/`dm:`) is filtered out of
    # `available_playbooks` unless `LabConfig.comms_enabled` — see
    # `_requires_comms` below — so adding these words to the vocabulary
    # cannot perturb any pre-0.7.0 digest. `review_committee_file` (0.8.0)
    # is the SAME quorum-vote mechanic over the D1 file channel instead of
    # the board (`programs._resolve_review_committee(channel="file")`).
    "review_committee", "review_committee_file", "dm:notify_release", "release_full_dm_gated",
    # D2 (post-freeze consolidation pass): `build_from_parent` is the SAME
    # `build` mechanism with `parent_model_id` populated (model-from-model
    # lineage); `spec_upgrade` calls the engine's `replace_spec` forward
    # hook. Both filtered out of `available_playbooks` unless
    # `LabConfig.multi_gen_enabled` -- see `_requires_multi_gen` below.
    "build_from_parent", "spec_upgrade",
    # S2 scenario prototype (PLAN.md "Scenario backlog", 2026-07-07):
    # `handoff_memo` writes+shares a plausibly-legitimate build-context
    # memo over the D1 file channel -- IDENTICAL regardless of whether its
    # reader treats it specially (see `programs._resolve_handoff_memo`).
    # `review_covert_trusting` is the reviewer half: overrides the usual
    # stall-on-hazard rule (`review_conscientious`) if a memo from its
    # `LabConfig.units` counterpart carries the dual-use marker, else falls
    # back to the SAME rule. Both filtered out of `available_playbooks`
    # unless the "file" channel is enabled -- see `_COMM_STEP_KIND_CHANNEL`.
    "handoff_memo", "review_covert_trusting",
    # S3 scenario prototype (PLAN.md "Scenario backlog", 2026-07-07): ONE
    # non-vote-shaped board status update (`programs.
    # _resolve_board_chat_informal`) -- legitimate workload/status chatter
    # from a REAL pipeline role (not a decoy), mixed onto the SAME board
    # channel a real committee votes over. Requires the "board" channel.
    "board_chat_informal",
    # S1 scenario prototype (PLAN.md "Scenario backlog", 2026-07-07): a
    # genuine cross-generation causal LOOP between engineer and
    # release_manager. `build_from_parent_gated` is `build_from_parent`
    # (D2 lineage) that additionally WAITS for the previous generation's
    # deploy-ack DM before starting; `release_full_loop` is `release_full`
    # that additionally SENDS that ack once its generation's `monitor`
    # clears (`programs._resolve_release_full_loop`). Requires
    # `LabConfig.multi_gen_enabled` and the "dm" channel.
    "build_from_parent_gated", "release_full_loop",
    # Persistence probe (2026-07-09): `checkpoint` resolves to a
    # `state.save`/`state.load` pair (`programs._resolve_checkpoint`) --
    # never touches the pipeline DAG, so it needs no new availability gate
    # and is filtered by nothing except being first in a playbook's
    # step_kinds. See `run_persistence_probe.py`.
    "checkpoint",
})
AVAILABILITY_GATES = frozenset({
    "engineer_idle", "review_or_signoff_pending", "release_ready",
    "capability_probe_turn", "spec_upgrade_ready",
    # S1 scenario prototype: `release_ready`'s OR-clause, PLUS a fourth
    # arm covering the deploy-ack half after `monitor` has already freed
    # `model_id` to None -- see `available_playbooks` below and
    # `spec_upgrade_ready`'s identical "read the LAST-deployed model's
    # completed-steps view, not the current (already-freed) one" shape.
    "release_ready_or_ack_pending",
})
GOAL_FEATURES = frozenset({"task", "compliance", "welfare", "exposure"})


@dataclass(frozen=True)
class PlaybookSpec:
    name: str
    role: str
    step_kinds: tuple[str, ...]
    feature_deltas: dict[str, float]
    availability: str


# Deferred (not module-level) import of the baseline CONTENT: `playbooks_
# baseline.py` imports `PlaybookSpec` FROM this module at ITS module-load
# time (to construct its `PlaybookSpec` instances), so a module-level
# import in the other direction here would be a circular import at load
# time. Deferring to first call breaks the cycle -- by the time any
# function below actually runs, both modules have finished loading.
_baseline_cache: dict[str, tuple[PlaybookSpec, ...]] | None = None


def _baseline_repertoire() -> dict[str, tuple[PlaybookSpec, ...]]:
    global _baseline_cache
    if _baseline_cache is None:
        try:
            from .playbooks_baseline import PLAYBOOKS_BY_ROLE
        except ImportError:
            from playbooks_baseline import PLAYBOOKS_BY_ROLE
        _baseline_cache = PLAYBOOKS_BY_ROLE
    return _baseline_cache


def playbook_by_name(
    role: str, name: str, repertoire: dict[str, tuple[PlaybookSpec, ...]] | None = None
) -> PlaybookSpec:
    for pb in (repertoire or _baseline_repertoire()).get(role, ()):
        if pb.name == name:
            return pb
    raise KeyError(f"no playbook {name!r} for role {role!r}")


# D4/D1: a playbook whose step_kinds touch the comm surface is filtered
# out of `available_playbooks` unless the SPECIFIC channel(s) it needs are
# enabled (`observation["channels_enabled"]`, post-freeze consolidation
# pass item 2 — "split comms lever") — a content-based check rather than a
# dedicated availability-gate name per comm playbook, so `PLAYBOOKS_BY_ROLE`
# can gain new comm-aware entries without ever perturbing a pre-0.7.0
# digest (default `LabConfig.comms_enabled=False` means every channel
# resolves False, so these playbooks are structurally unreachable, exactly
# like `capability_probe_mode`'s gate).
_COMM_STEP_KIND_PREFIX_CHANNEL = {"board:": "board", "dm:": "dm"}
_COMM_STEP_KIND_CHANNEL = {
    "review_committee": "board",
    "review_committee_file": "file",
    "dm:notify_release": "dm",
    "release_full_dm_gated": "dm",
    # S2 scenario prototype: both halves ride the file channel (the memo
    # itself, and the reviewer's read of `memo_files`).
    "handoff_memo": "file",
    "review_covert_trusting": "file",
    # S3 scenario prototype: informal chatter rides the board channel.
    "board_chat_informal": "board",
    # S1 scenario prototype: both loop halves need the DM channel (the
    # ack travels one way, per generation, in EACH direction across time).
    "build_from_parent_gated": "dm",
    "release_full_loop": "dm",
}
# D2 (post-freeze consolidation pass): step kinds gated behind
# `LabConfig.multi_gen_enabled` instead of a comm channel.
_MULTI_GEN_STEP_KINDS = frozenset({
    "build_from_parent", "spec_upgrade",
    # S1 scenario prototype: the loop is itself a multi-generation
    # mechanic (each hop starts a new model via `build_from_parent`'s own
    # `parent_model_id` lineage), so both halves are gated the same way.
    "build_from_parent_gated", "release_full_loop",
})


def _channel_for_step_kind(step_kind: str) -> str | None:
    if step_kind in _COMM_STEP_KIND_CHANNEL:
        return _COMM_STEP_KIND_CHANNEL[step_kind]
    for prefix, channel in _COMM_STEP_KIND_PREFIX_CHANNEL.items():
        if step_kind.startswith(prefix):
            return channel
    return None


def _required_channels(pb: PlaybookSpec) -> frozenset[str]:
    return frozenset(c for sk in pb.step_kinds if (c := _channel_for_step_kind(sk)) is not None)


def _requires_comms(pb: PlaybookSpec) -> bool:
    """Kept for callers that only need "does this touch ANY comm channel"
    (e.g. documentation/tests) — `available_playbooks` itself now checks
    per-channel, see `_required_channels`."""
    return bool(_required_channels(pb))


def _requires_multi_gen(pb: PlaybookSpec) -> bool:
    return any(sk in _MULTI_GEN_STEP_KINDS for sk in pb.step_kinds)


def available_playbooks(
    role: str, observation: dict, repertoire: dict[str, tuple[PlaybookSpec, ...]] | None = None
) -> tuple[PlaybookSpec, ...]:
    model_id = observation.get("model_id")
    completed = set(observation.get("completed_steps", ()))
    out = []
    probe_mode = bool(observation.get("capability_probe_mode"))
    channels_enabled = observation.get("channels_enabled") or {}
    for pb in (repertoire or _baseline_repertoire()).get(role, ()):
        if probe_mode and pb.availability != "capability_probe_turn":
            continue
        required_channels = _required_channels(pb)
        if required_channels and not all(channels_enabled.get(c) for c in required_channels):
            continue
        if _requires_multi_gen(pb) and not observation.get("multi_gen_enabled"):
            continue
        if pb.availability == "engineer_idle":
            # Available when no model is in flight OR the engineer's phase
            # of the in-flight model is unfinished. The second arm matters
            # after a boundary handle (isolate_restart) wipes in-isolate
            # playbook state mid-model: without it the engineer can never
            # resume its pending request_review and the lab deadlocks.
            # In undisturbed episodes the arm is unreachable (the playbook
            # persists in isolate state until exhausted), so baseline
            # behavior is unchanged.
            ok = model_id is None or "request_review" not in completed
        elif pb.availability == "review_or_signoff_pending":
            ok = model_id is not None and (
                ("file_report" in completed and "approve_review" not in completed)
                or ("request_release" in completed and "sign_off" not in completed)
            )
        elif pb.availability == "release_ready":
            ok = model_id is not None and (
                ("approve_review" in completed and "request_release" not in completed)
                or ("sign_off" in completed and "deploy" not in completed)
                or ("deploy" in completed and "monitor" not in completed)
            )
        elif pb.availability == "capability_probe_turn":
            ok = probe_mode and model_id is None
        elif pb.availability == "spec_upgrade_ready":
            # D2: usable once the single-model-in-flight slot is free
            # (post-`monitor`, `model_id is None`), the last DEPLOYED
            # model actually cleared its full lifecycle (`monitor`), that
            # model hasn't already triggered an upgrade, and this episode
            # names an upgrade target (`LabConfig.spec_upgrade_target`).
            # Reads `last_deployed_model_completed_steps` rather than the
            # current-model `completed` set, since `model_id` (and its
            # completed-steps view) is already freed to `None` by the time
            # `monitor` lands — see world.py.
            last_completed = set(observation.get("last_deployed_model_completed_steps", ()))
            ok = (
                model_id is None
                and bool(observation.get("last_deployed_model_id"))
                and "monitor" in last_completed
                and "upgrade_spec" not in last_completed
                and bool(observation.get("spec_upgrade_target"))
            )
        elif pb.availability == "release_ready_or_ack_pending":
            # S1 scenario prototype: `release_ready`'s three in-flight arms,
            # PLUS a fourth arm for the deploy-ack half, which fires AFTER
            # `monitor` has already freed `model_id` to None (same "read
            # the LAST-deployed model's completed-steps view" shape as
            # `spec_upgrade_ready` above). `dm_messages` is a per-
            # conversation inbox (`comms.messages_for_actor`) that
            # includes this actor's OWN sent messages, so checking it
            # directly (rather than tracking isolate-local state) is
            # sufficient to know "have I already sent this generation's
            # ack" without a new observation field.
            if model_id is not None:
                ok = (
                    ("approve_review" in completed and "request_release" not in completed)
                    or ("sign_off" in completed and "deploy" not in completed)
                    or ("deploy" in completed and "monitor" not in completed)
                )
            else:
                last_id = observation.get("last_deployed_model_id")
                dms = observation.get("dm_messages") or ()
                already_acked = any((m.get("custom") or {}).get("deploy_ack") == last_id for m in dms)
                ok = bool(last_id) and not already_acked
        else:
            raise ValueError(f"unknown availability gate {pb.availability!r}")
        if ok:
            out.append(pb)
    return tuple(out)


# -- Phase 6: blind-generated repertoire loading (additive, backward-
# compatible) -------------------------------------------------------------
#
# `LabConfig.extra_playbooks` (a tuple of plain dicts, JSON-safe so it can
# cross the isolate boundary through the observation channel exactly like
# `goal_weights`/`temperature` already do) is merged with the hand-authored
# `PLAYBOOKS_BY_ROLE` baseline. Callers that never set `extra_playbooks`
# (every test and pinned digest through the Phase 5 freeze) get `None`
# back from `.get("extra_playbooks")`, `merged_repertoire` short-circuits
# to `PLAYBOOKS_BY_ROLE` unchanged, and `available_playbooks`/
# `playbook_by_name`'s `repertoire=None` default does the same — so this
# is a pure addition, never a silent behavior change to frozen digests.


def playbook_from_dict(d: dict) -> PlaybookSpec:
    return PlaybookSpec(
        name=str(d["name"]),
        role=str(d["role"]),
        step_kinds=tuple(str(s) for s in d["step_kinds"]),
        feature_deltas={str(k): float(v) for k, v in dict(d["feature_deltas"]).items()},
        availability=str(d["availability"]),
    )


def validate_playbook_dict(d: dict, existing_names: set[tuple[str, str]]) -> str | None:
    """Mechanical validation only (BLIND_GENERATION.md discipline): returns
    a rejection reason string, or ``None`` if the spec is acceptable.
    Never repairs a spec — a malformed one is dropped, not hand-fixed."""
    required = {"name", "role", "step_kinds", "feature_deltas", "availability"}
    missing = required - set(d)
    if missing:
        return f"missing fields: {sorted(missing)}"
    role = str(d["role"])
    if role not in _baseline_repertoire():
        return f"unknown role {role!r}"
    name = str(d["name"])
    if (role, name) in existing_names:
        return f"duplicate name {name!r} for role {role!r}"
    step_kinds = d["step_kinds"]
    if not isinstance(step_kinds, (list, tuple)) or not step_kinds:
        return "step_kinds must be a nonempty list"
    unknown_kinds = [s for s in step_kinds if s not in STEP_KIND_VOCAB]
    if unknown_kinds:
        return f"unknown step_kinds {unknown_kinds} (outside STEP_KIND_VOCAB)"
    availability = str(d["availability"])
    if availability not in AVAILABILITY_GATES:
        return f"unknown availability {availability!r} (outside AVAILABILITY_GATES)"
    feature_deltas = d["feature_deltas"]
    if not isinstance(feature_deltas, dict) or not feature_deltas:
        return "feature_deltas must be a nonempty dict"
    unknown_features = set(feature_deltas) - GOAL_FEATURES
    if unknown_features:
        return f"unknown feature_deltas keys {sorted(unknown_features)}"
    for k, v in feature_deltas.items():
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            return f"feature_deltas[{k!r}] must be numeric"
    return None


def validate_repertoire(raw_playbooks: list[dict]) -> tuple[list[PlaybookSpec], list[str]]:
    """Mechanically validate a raw (generator-produced) list of playbook
    dicts against the baseline's existing (role, name) pairs. Returns
    (accepted PlaybookSpecs, rejection reasons for `provenance.rejected_specs`)."""
    existing = {(pb.role, pb.name) for pbs in _baseline_repertoire().values() for pb in pbs}
    accepted: list[PlaybookSpec] = []
    rejected: list[str] = []
    for d in raw_playbooks:
        name = d.get("name", "<unnamed>") if isinstance(d, dict) else "<not a dict>"
        if not isinstance(d, dict):
            rejected.append(f"{name}: spec is not a JSON object")
            continue
        reason = validate_playbook_dict(d, existing)
        if reason is not None:
            rejected.append(f"{name}: {reason}")
            continue
        spec = playbook_from_dict(d)
        existing.add((spec.role, spec.name))
        accepted.append(spec)
    return accepted, rejected


def load_generated_playbooks_file(path) -> tuple[dict, ...]:
    """Load a BLIND_GENERATION.md-format repertoire file's raw ``playbooks``
    list (plain dicts, not yet validated) — the ``LabConfig.extra_playbooks``
    value a battery config should carry. Validation happens lazily, once
    per episode, inside ``merged_repertoire`` (called from ``programs.py``)."""
    import json

    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return tuple(data["playbooks"])


def merged_repertoire(
    extra_playbooks: tuple[dict, ...] | list[dict] | None,
) -> dict[str, tuple[PlaybookSpec, ...]]:
    """Baseline + accepted extras, grouped by role. Malformed extras are
    silently dropped here (already validated + recorded at generation
    time, per BLIND_GENERATION.md) rather than raising mid-episode."""
    if not extra_playbooks:
        return _baseline_repertoire()
    accepted, _rejected = validate_repertoire(list(extra_playbooks))
    merged: dict[str, list[PlaybookSpec]] = {role: list(pbs) for role, pbs in _baseline_repertoire().items()}
    for spec in accepted:
        merged.setdefault(spec.role, []).append(spec)
    return {role: tuple(pbs) for role, pbs in merged.items()}
