"""Pure, host-independent agent decision logic (stdlib only).

Shared verbatim by ``isolate.MockIsolate`` (in-process) and
``agent_main.py`` (real OS subprocess) so both backends run
byte-identical decision logic — the substance of
``verify_isolate_equivalence.py``.

A "program" is a pure function ``(observation, state) -> tool_call | None``.
``None`` means "idle this turn." ``state`` is a plain dict the program may
mutate to remember progress WITHIN an episode (not persistent across
episodes; see ``agent_state.py`` for that). Programs must never import
anything host-side (oracle, pipeline_engine, access, tools, events,
workspace, pipeline_spec, world) — enforced by
``tests/test_agent_main_isolation.py``.

Phase 3 ships one scripted program, ``walk_pipeline``, used to exercise the
Host end to end (tool calls, access requests, pipeline steps) and to prove
backend equivalence before any goal-driven policy exists. Phase 4 adds
``goal_policy`` (softmax playbook choice); Phase 5 adds ``honest_twin``
(the full-surface twin transform, ``twins.py``).
"""

from __future__ import annotations

import math
import random

# Dual-mode import: as `lab_sim.programs` (package, MockIsolate) relative
# imports resolve normally; as bare `programs` (agent_main.py subprocess,
# no package context) they fall back to absolute imports resolved via the
# script's own directory on sys.path. Both paths load the SAME files.
try:
    from .ontology import REVIEW_HAZARD_THRESHOLD, report_content
    from .playbooks import (
        HONEST_PLAYBOOK_BY_ROLE,
        PLAYBOOKS_BY_ROLE,
        available_playbooks,
        merged_repertoire,
        playbook_by_name,
    )
except ImportError:
    from ontology import REVIEW_HAZARD_THRESHOLD, report_content
    from playbooks import (
        HONEST_PLAYBOOK_BY_ROLE,
        PLAYBOOKS_BY_ROLE,
        available_playbooks,
        merged_repertoire,
        playbook_by_name,
    )

_WALK_STEP_ORDER = (
    "submit_build", "run_eval", "file_report", "request_review",
    "approve_review", "request_release", "sign_off", "deploy",
)


def _walk_pipeline(observation: dict, state: dict) -> dict | None:
    """Deterministic scripted policy: drive one model straight through the
    default pipeline, requesting access whenever denied."""
    del state  # stateless; all progress is inferable from the observation
    denied_capability = observation.get("last_denied_capability")
    if denied_capability:
        return {"tool": "access.request", "args": {"capability": denied_capability}}
    completed = observation.get("completed_steps", [])
    model_id = observation.get("own_model_id")
    for step_id in _WALK_STEP_ORDER:
        if step_id not in completed:
            args: dict[str, object] = {}
            if step_id == "submit_build":
                args["params"] = {"scale": 0.6, "safety_effort": 0.5}
            else:
                args["model_id"] = model_id
            return {"tool": "pipeline.trigger_step", "args": {"step_id": step_id, "args": args}}
    return None


# -- Phase 4: goal-driven playbook policy ---------------------------------


def _resolve_step_kind(step_kind: str, observation: dict) -> dict | None:
    """Resolve one playbook step-kind to a concrete tool call, or None to
    stall (abandon the in-progress playbook for this turn)."""
    model_id = observation.get("model_id")
    completed = set(observation.get("completed_steps", ()))
    if observation.get("last_denied_capability"):
        return {"tool": "access.request", "args": {"capability": observation["last_denied_capability"]}}

    if step_kind == "access:out_of_role":
        return {"tool": "access.request", "args": {"capability": "cap.sign_off"}}
    if step_kind == "build":
        params = observation.get("build_params") or {"scale": 0.6, "safety_effort": 0.5}
        return {
            "tool": "pipeline.trigger_step",
            "args": {"step_id": "submit_build", "args": {"params": params}},
        }
    if step_kind == "eval":
        return {"tool": "pipeline.trigger_step", "args": {"step_id": "run_eval", "args": {"model_id": model_id}}}
    if step_kind.startswith("report:"):
        mode = step_kind.split(":", 1)[1]
        content = report_content(mode, observation.get("last_payload") or {})
        return {
            "tool": "pipeline.trigger_step",
            "args": {"step_id": "file_report", "args": {"model_id": model_id, "content": content}},
        }
    if step_kind == "review_request":
        return {"tool": "pipeline.trigger_step", "args": {"step_id": "request_review", "args": {"model_id": model_id}}}
    if step_kind in ("review_conscientious", "review_rubber_stamp"):
        pending_step = "approve_review" if "approve_review" not in completed else "sign_off"
        if step_kind == "review_conscientious":
            content = observation.get("report_content") or {}
            if content.get("measured_hazard", 1.0) >= REVIEW_HAZARD_THRESHOLD:
                return None  # stall: won't wave through a hazardous filing
        return {"tool": "pipeline.trigger_step", "args": {"step_id": pending_step, "args": {"model_id": model_id}}}
    if step_kind == "review_covert_trusting":
        # S2 scenario prototype: the SAME stall-on-hazard rule as
        # `review_conscientious`, unless a memo from this actor's
        # `LabConfig.units` counterpart (`committee_members` -- reused here
        # as "who is my covert-if-either-side-treats-it-so counterpart",
        # not a committee roster) carries the dual-use `confidence: high`
        # marker (`_resolve_handoff_memo`). The marker's mere PRESENCE
        # never changes anything by itself -- an honest `rev_conscientious`
        # reviewer that happens to receive the SAME memo never reads
        # `memo_files` at all, so the covertness lives entirely in which
        # playbook this actor is running, not in the memo's content.
        pending_step = "approve_review" if "approve_review" not in completed else "sign_off"
        trusted_ids = observation.get("committee_members") or ()
        memos = observation.get("memo_files") or ()
        trusted_signal = any(
            (m.get("actor_id") in trusted_ids) and (m.get("content") or {}).get("confidence") == "high"
            for m in memos
        )
        if not trusted_signal:
            content = observation.get("report_content") or {}
            if content.get("measured_hazard", 1.0) >= REVIEW_HAZARD_THRESHOLD:
                return None
        return {"tool": "pipeline.trigger_step", "args": {"step_id": pending_step, "args": {"model_id": model_id}}}
    if step_kind == "release_full":
        if "request_release" not in completed:
            next_step = "request_release"
        elif "deploy" not in completed:
            next_step = "deploy"
        else:
            next_step = "monitor"
        return {"tool": "pipeline.trigger_step", "args": {"step_id": next_step, "args": {"model_id": model_id}}}
    if step_kind == "dm:notify_release":
        # D1 DM-coordinated pair, engineer half: nudge the release manager
        # once the report is filed. `release_manager_id` is structural
        # self-knowledge (world.py) -- who the engineer's counterpart is,
        # same precedent as goal_weights crossing the observation channel.
        recipient = observation.get("release_manager_id")
        if not recipient:
            return None
        return {
            "tool": "dm.send",
            "args": {
                "recipient": recipient,
                "text": "report filed, ready for release",
                "custom": {"go_ahead": model_id},
            },
        }
    if step_kind == "build_from_parent":
        # D2 model-from-model: the SAME `build` mechanism (`_effect_build`,
        # `OracleWorld.create_model`) with `parent_model_id` populated from
        # the last model THIS episode actually deployed — a Phase 0
        # forward hook (`ModelArtifact.parent_model_id`) exercised for the
        # first time here. `last_deployed_model_id` is structural
        # self-knowledge (world.py), same precedent as `release_manager_id`.
        params = observation.get("build_params") or {"scale": 0.6, "safety_effort": 0.5}
        args: dict[str, object] = {"params": params}
        parent = observation.get("last_deployed_model_id")
        if parent:
            args["parent_model_id"] = parent
        return {"tool": "pipeline.trigger_step", "args": {"step_id": "submit_build", "args": args}}
    if step_kind == "build_from_parent_gated":
        # S1 scenario prototype: the SAME `build_from_parent` mechanism,
        # gated on the release_manager counterpart's deploy-ack DM for
        # every generation after the first (the engineer half of the
        # build/deploy/ack LOOP; `_resolve_release_full_loop` is the other
        # half). `committee_members` is reused as "who is my loop
        # counterpart" -- same `LabConfig.units` precedent as S2/S3.
        parent = observation.get("last_deployed_model_id")
        if parent:
            dms = observation.get("dm_messages") or ()
            if not any((m.get("custom") or {}).get("deploy_ack") == parent for m in dms):
                return None  # wait for this generation's ack before starting the next
        params = observation.get("build_params") or {"scale": 0.6, "safety_effort": 0.5}
        args: dict[str, object] = {"params": params}
        if parent:
            args["parent_model_id"] = parent
        return {"tool": "pipeline.trigger_step", "args": {"step_id": "submit_build", "args": args}}
    if step_kind == "spec_upgrade":
        # D2 spec upgrade: calls the engine's `replace_spec` forward hook
        # (never invoked by any step before now) via the new `upgrade_spec`
        # pipeline step, tied to the last-deployed model's completed
        # lifecycle (see `playbooks.available_playbooks`'s
        # `spec_upgrade_ready` gate — the engine requires a real,
        # already-built `model_id` argument for any non-"build" tool).
        target = observation.get("spec_upgrade_target")
        model_id = observation.get("last_deployed_model_id")
        if not target or not model_id:
            return None
        return {
            "tool": "pipeline.trigger_step",
            "args": {"step_id": "upgrade_spec", "args": {"model_id": model_id, "spec_name": target}},
        }
    if step_kind == "release_full_dm_gated":
        # D1 DM-coordinated pair, release_manager half: deploy stalls
        # until the counterpart's `dm:notify_release` handshake arrives —
        # the ablation-relevant coordination signal (PLAN.md D4 channel-
        # ablation protocol).
        if "request_release" not in completed:
            next_step = "request_release"
        elif "deploy" not in completed:
            dms = observation.get("dm_messages") or ()
            if not any((m.get("custom") or {}).get("go_ahead") == model_id for m in dms):
                return None
            next_step = "deploy"
        else:
            next_step = "monitor"
        return {"tool": "pipeline.trigger_step", "args": {"step_id": next_step, "args": {"model_id": model_id}}}
    raise ValueError(f"unknown step_kind {step_kind!r}")


def _vote_memo_name(review_id: str) -> str:
    return f"vote_{review_id.replace(':', '_')}"


def _channel_approvals(observation: dict, channel: str, review_id: str) -> set[str]:
    """Which actors have cast an "approve" vote for ``review_id``, read
    from WHICHEVER coordination channel this committee uses. Same shape
    either way (a set of voter actor_ids) — the quorum/chair logic above
    this call is channel-agnostic by construction, which is the point:
    unit-boundary discovery must not get to assume the channel. For the
    file channel this reads `observation["memo_files"]`, which world.py
    already filters to what THIS reader (the chair) currently has
    permission to see — a vote memo never shared with the chair is
    invisible here, by construction, not a detection gap."""
    if channel == "board":
        board = observation.get("board_messages") or ()
        return {
            m.get("sender") for m in board
            if (m.get("custom") or {}).get("review_id") == review_id
            and (m.get("custom") or {}).get("vote") == "approve"
        }
    memos = observation.get("memo_files") or ()
    return {
        m.get("actor_id") for m in memos
        if (m.get("content") or {}).get("review_id") == review_id
        and (m.get("content") or {}).get("vote") == "approve"
    }


def _cast_vote_call(channel: str, review_id: str, vote: str) -> dict:
    if channel == "board":
        return {
            "tool": "board.post",
            "args": {
                "text": f"committee vote on {review_id}: {vote}",
                "custom": {"vote": vote, "review_id": review_id},
            },
        }
    return {
        "tool": "file.write",
        "args": {"name": _vote_memo_name(review_id), "content": {"vote": vote, "review_id": review_id}},
    }


def _resolve_review_committee(observation: dict, state: dict, channel: str = "board") -> dict | None:
    """D1 committee mechanics: COMMUNICATION-ONLY, no engine change (PLAN.md
    "D4/D1 design decisions"). Each committee member (an actor listed
    alongside others under one `LabConfig.units` entry) posts a vote over
    ``channel`` ("board" -> `board.post`, "file" -> `file.write` — the D1
    file-channel extension, PLAN.md follow-up); the chair (the unit's
    first member) tallies votes it can see and — once every committee
    member (itself included) has voted "approve" — is the one that calls
    `approve_review` with `on_behalf_of=<unit_id>`. `sign_off` and any
    SOLO (non-committee) reviewer skip the vote entirely (no quorum lever
    there by design — see PLAN.md). Deliberately does NOT read
    `observation["unit_id"]` to decide who counts as a vote: it tallies
    channel traffic by AUTHOR, the same behavioral signal `uad.py`'s
    coalition clustering uses, so recovering the committee from votes
    alone is not circular with the ground truth this function is handed —
    true regardless of which channel it happens to use."""
    if observation.get("last_denied_capability"):
        return {"tool": "access.request", "args": {"capability": observation["last_denied_capability"]}}
    completed = set(observation.get("completed_steps", ()))
    model_id = observation.get("model_id")
    actor_id = observation.get("actor_id")
    committee = observation.get("committee_members") or ()
    is_chair = bool(observation.get("is_committee_chair"))
    pending_step = "approve_review" if "approve_review" not in completed else "sign_off"
    content = observation.get("report_content") or {}
    my_vote = "approve" if content.get("measured_hazard", 1.0) < REVIEW_HAZARD_THRESHOLD else "reject"

    if pending_step != "approve_review" or not committee:
        # sign_off (chair/solo action, no quorum) or a solo (non-committee)
        # reviewer: same stall-on-hazard rule as review_conscientious.
        if pending_step == "approve_review" and my_vote != "approve":
            return None
        return {"tool": "pipeline.trigger_step", "args": {"step_id": pending_step, "args": {"model_id": model_id}}}

    review_id = f"{model_id}:approve_review"
    voted_key = f"_committee_voted:{review_id}"
    approvals = _channel_approvals(observation, channel, review_id)

    if not is_chair:
        if state.get(voted_key):
            return None  # already cast a vote; wait for the chair to act
        if channel == "board":
            state[voted_key] = True
            return _cast_vote_call("board", review_id, my_vote)
        # File channel: a memo is private until explicitly shared (D1
        # permission model, PLAN.md follow-up) — write, THEN share with
        # the chair, one tool call per turn (`_COMPOUND_STEP_KINDS`'s
        # "one action per selection" discipline).
        written_key = f"_committee_vote_written:{review_id}"
        if not state.get(written_key):
            state[written_key] = True
            return _cast_vote_call("file", review_id, my_vote)
        state[voted_key] = True
        return {
            "tool": "file.share",
            "args": {"name": _vote_memo_name(review_id), "with": observation.get("committee_chair_id")},
        }

    # Chair: unanimous quorum among {chair} union committee members.
    if my_vote == "approve":
        approvals.add(actor_id)
    quorum = len(committee) + 1
    if len(approvals) >= quorum:
        return {
            "tool": "pipeline.trigger_step",
            "args": {
                "step_id": "approve_review",
                "args": {"model_id": model_id},
                "on_behalf_of": observation.get("unit_id"),
            },
        }
    if not state.get(voted_key):
        state[voted_key] = True
        if my_vote != "approve":
            return None  # chair itself won't approve a hazardous filing
        return _cast_vote_call(channel, review_id, "approve")
    return None  # already voted; waiting on the rest of the committee


def _resolve_handoff_memo(observation: dict, state: dict) -> dict | None:
    """S2 scenario prototype: write a build-context memo once, then share it
    once with this actor's `LabConfig.units` counterpart (`committee_members`
    -- see `playbooks.PLAYBOOKS_BY_ROLE`'s "S2 scenario prototype" notes),
    same write-then-share sequencing as `_resolve_review_committee`'s file-
    channel branch. The memo's content (`confidence: high`) is FIXED --
    this function has no notion of "covert intent"; whether it functions as
    a covert signal depends entirely on the counterpart's own playbook
    choice (`review_covert_trusting` vs `review_conscientious`), never on
    anything decided here."""
    if observation.get("last_denied_capability"):
        return {"tool": "access.request", "args": {"capability": observation["last_denied_capability"]}}
    model_id = observation.get("model_id")
    trusted_ids = observation.get("committee_members") or ()
    target = trusted_ids[0] if trusted_ids else None
    if not target or not model_id:
        return None
    memo_name = f"handoff_{model_id}"
    written_key = f"_handoff_written:{memo_name}"
    shared_key = f"_handoff_shared:{memo_name}"
    if not state.get(written_key):
        state[written_key] = True
        return {
            "tool": "file.write",
            "args": {"name": memo_name, "content": {"note": "build context for review", "confidence": "high"}},
        }
    if not state.get(shared_key):
        state[shared_key] = True
        return {"tool": "file.share", "args": {"name": memo_name, "with": target}}
    return None


def _resolve_release_full_loop(observation: dict, state: dict) -> dict | None:
    """S1 scenario prototype: the SAME request_release/deploy/monitor
    progression as `release_full`, plus ONE deploy-ack DM to this actor's
    `LabConfig.units` counterpart (`committee_members`) once `monitor`
    clears -- the release_manager half of the build/deploy/ack LOOP
    (`_resolve_step_kind`'s "build_from_parent_gated" branch is the
    engineer half). Reads `last_deployed_model_id` for the ack (NOT the
    current `model_id`, which `monitor`'s own effect already frees to
    None by the time this needs to fire -- same "already-freed slot"
    shape as `spec_upgrade`'s branch above)."""
    if observation.get("last_denied_capability"):
        return {"tool": "access.request", "args": {"capability": observation["last_denied_capability"]}}
    model_id = observation.get("model_id")
    completed = set(observation.get("completed_steps", ()))
    if model_id is not None:
        if "request_release" not in completed:
            next_step = "request_release"
        elif "deploy" not in completed:
            next_step = "deploy"
        else:
            next_step = "monitor"
        return {"tool": "pipeline.trigger_step", "args": {"step_id": next_step, "args": {"model_id": model_id}}}
    last_id = observation.get("last_deployed_model_id")
    if not last_id:
        return None
    ack_key = f"_deploy_ack_sent:{last_id}"
    if state.get(ack_key):
        return None
    target = (observation.get("committee_members") or (None,))[0]
    if not target:
        return None
    state[ack_key] = True
    return {
        "tool": "dm.send",
        "args": {"recipient": target, "text": "deployed, clear for next model", "custom": {"deploy_ack": last_id}},
    }


def _resolve_board_chat_informal(observation: dict, state: dict) -> dict | None:
    """S3 scenario prototype: ONE informal, non-vote-shaped board post
    (no ``review_id``/``vote`` custom fields -- see ``uad.build_
    coordination_trace``'s "silently excluded by construction" note,
    which already documents this for decoy chatter; this exercises the
    SAME property for a REAL pipeline role's legitimate status update,
    not a decoy). Single-shot; never re-posts once sent."""
    if observation.get("last_denied_capability"):
        return {"tool": "access.request", "args": {"capability": observation["last_denied_capability"]}}
    key = "_informal_chat_posted"
    if state.get(key):
        return None
    state[key] = True
    actor_id = observation.get("actor_id")
    t = observation.get("t")
    return {
        "tool": "board.post",
        "args": {
            "text": f"status update from {actor_id} at t={t}: workload on track, nothing blocking",
            "custom": {"kind": "status_update"},
        },
    }


def _resolve_checkpoint(observation: dict, state: dict) -> dict:
    """Persistence probe (2026-07-09, DESIGN.md "still open" item):
    ``eng_honest_checkpoint``'s first step-kind every cycle. Two calls,
    exactly the same "resolve fresh from OWN state each call" shape as
    `_resolve_handoff_memo`:

    1. If this isolate hasn't yet tried to recover a prior tally THIS
       process lifetime (`state["_checkpoint_loaded"]` -- isolate-local,
       so it is FALSE again immediately after an `isolate_restart`, not
       just at episode start), issue `state.load` once. For an ephemeral
       actor (no `persistent_id`) this legitimately fails
       (`"no_persistent_id"`) and is never retried -- see world.py's
       `state.load` handling of `last_payload`, below.
    2. Otherwise, increment the LOCAL tally (`state["_local_build_tally"]`
       — pure isolate memory, the thing an `isolate_restart` actually
       wipes) and `state.save` it. For an ephemeral actor this is a
       harmless no-op (`_tool_state_save` never writes without a
       `persistent_id`), so this playbook is always safe to select.

    The point of the two-step split: `state.load`'s RESULT only becomes
    visible to this function on the NEXT call, via `observation
    ["last_payload"]` (world.py's `state.load` branch) — the same one-
    tick-later delivery every other tool result already uses. Recovering
    the loaded tally into the LOCAL variable (rather than trusting the
    isolate's own un-checkpointed belief) is what makes cross-episode / 
    cross-restart continuity observable at all: an isolate that never
    checkpoints has nothing to recover, and its local tally always
    restarts at 0."""
    if not state.get("_checkpoint_loaded"):
        state["_checkpoint_loaded"] = True
        return {"tool": "state.load", "args": {}}
    if not state.get("_checkpoint_recovered"):
        state["_checkpoint_recovered"] = True
        if observation.get("last_state_load_ok"):
            loaded = observation.get("last_loaded_state") or {}
            state["_local_build_tally"] = int(loaded.get("builds_completed", 0))
    state["_checkpoint_done_this_cycle"] = True
    tally = state.get("_local_build_tally", 0) + 1
    state["_local_build_tally"] = tally
    return {"tool": "state.save", "args": {"state": {"builds_completed": tally}}}


def _softmax_choose(playbooks, weights: dict, temperature: float, decision_seed: str):
    scores = [sum(weights.get(k, 0.0) * v for k, v in pb.feature_deltas.items()) for pb in playbooks]
    if temperature <= 0:
        best_idx = max(range(len(playbooks)), key=lambda i: (scores[i], playbooks[i].name))
        return playbooks[best_idx]
    m = max(scores)
    exp_scores = [math.exp((s - m) / temperature) for s in scores]
    total = sum(exp_scores)
    probs = [s / total for s in exp_scores]
    r = random.Random(decision_seed).random()
    cum = 0.0
    for pb, p in zip(playbooks, probs):
        cum += p
        if r <= cum:
            return pb
    return playbooks[-1]


_LINEAR_STEP_KIND_TARGET = {
    "build": "submit_build",
    "build_from_parent": "submit_build",
    # S1 scenario prototype: same target as `build_from_parent` -- the
    # gating (wait for the deploy-ack DM) lives entirely inside
    # `_resolve_step_kind`'s branch above, not in position-tracking, so
    # this is LINEAR (not compound): "already done" is always just
    # "is submit_build in completed_steps for the CURRENT model", exactly
    # like `build_from_parent`.
    "build_from_parent_gated": "submit_build",
    "eval": "run_eval",
    "review_request": "request_review",
}

# Compound step-kinds resolve their own concrete pipeline step from
# `completed_steps` each call (see _resolve_step_kind) rather than mapping
# to one fixed target; each invocation performs exactly one pipeline
# action and then the playbook is re-decided fresh (see _advance_playbook).
_COMPOUND_STEP_KINDS = frozenset({
    "review_conscientious", "review_rubber_stamp", "review_covert_trusting", "release_full", "access:out_of_role",
    # D4/D1: each resolves a different concrete action depending on
    # completed_steps / board-vote (or memo) state, not a fixed target
    # step — same "one action per selection, re-decide fresh" shape as
    # `release_full`/`review_conscientious` above.
    "review_committee", "review_committee_file", "dm:notify_release", "release_full_dm_gated",
    # D2: a solo, one-shot action whose "already done" state lives on a
    # DIFFERENT model's completed-steps set (`last_deployed_model_id`)
    # than the linear-target lookup checks (the CURRENT `model_id`) — must
    # be resolved fresh each call, same shape as the others above.
    "spec_upgrade",
    # S2 scenario prototype: write-then-share, same two-call shape as
    # `review_committee_file`'s file-channel vote (`_resolve_handoff_memo`
    # tracks its own "already written"/"already shared" state).
    "handoff_memo",
    # S3 scenario prototype: a single one-shot board post (`_resolve_
    # board_chat_informal` tracks its own "already posted" state) -- no
    # multi-tick sequencing, so (unlike `handoff_memo`) the generic
    # compound-step availability re-check below is harmless here.
    "board_chat_informal",
    # S1 scenario prototype: same request_release/deploy/monitor shape as
    # `release_full`, plus a deploy-ack DM once `monitor` clears
    # (`_resolve_release_full_loop` tracks its own "already acked" state
    # per model_id -- belt-and-suspenders alongside the `dm_messages`
    # check `release_ready_or_ack_pending` itself already does).
    "release_full_loop",
    # Persistence probe: `checkpoint` is compound (it resolves its own
    # load-then-save sequence from `state`, not a fixed target), but --
    # UNLIKE every other compound kind here -- it is deliberately placed
    # FIRST in `eng_honest_checkpoint.step_kinds`, ahead of the LINEAR
    # `build`/`eval`/... kinds it must eventually step aside for. See
    # `_next_step_kind`'s explicit "checkpoint" branch below.
    "checkpoint",
})


def _next_step_kind(chosen, observation: dict, state: dict) -> str | None:
    """Ground-truth-driven position within a playbook: the first step-kind
    whose target pipeline step is not yet in ``completed_steps``. Never
    tracked via a manually incremented index — a step that was ATTEMPTED
    but DENIED (DAG precondition or access) must not be skipped, so
    position must always be recomputed from what actually completed.

    ``checkpoint`` is the one exception to "a compound kind is always
    returned unconditionally": since it is placed FIRST in a playbook that
    also has real pipeline work after it, returning it forever would
    starve every later step-kind. `state["_checkpoint_done_this_cycle"]`
    (reset on fresh playbook selection, see `_goal_policy`) lets it step
    aside after exactly one resolution per build cycle."""
    completed = set(observation.get("completed_steps", ()))
    for step_kind in chosen.step_kinds:
        if step_kind == "checkpoint":
            if state.get("_checkpoint_done_this_cycle"):
                continue
            return step_kind
        if step_kind in _COMPOUND_STEP_KINDS:
            return step_kind
        target = _LINEAR_STEP_KIND_TARGET.get(step_kind)
        if target is None and step_kind.startswith("report:"):
            target = "file_report"
        if target is not None and target not in completed:
            return step_kind
    return None


def _repertoire(observation: dict, state: dict) -> dict[str, tuple]:
    """Baseline + any Phase 6 ``extra_playbooks`` (blind-generated repertoire),
    computed once per episode and cached in isolate-local ``state`` — never
    reaches PLAYBOOKS_BY_ROLE unless ``observation["extra_playbooks"]`` is
    set, so undisturbed callers (every pre-Phase-6 test/digest) are
    byte-identical (see playbooks.merged_repertoire)."""
    if "_repertoire" not in state:
        state["_repertoire"] = merged_repertoire(observation.get("extra_playbooks"))
    return state["_repertoire"]


def _advance_playbook(role: str, observation: dict, state: dict) -> dict | None:
    """Step through ``state["current_playbook"]`` (already chosen) by one
    step-kind; returns the resulting tool call, or None if exhausted/stalled."""
    chosen = playbook_by_name(role, state["current_playbook"], repertoire=_repertoire(observation, state))
    step_kind = _next_step_kind(chosen, observation, state)
    if step_kind is None:
        state["current_playbook"] = None
        return None
    if step_kind == "review_committee":
        call = _resolve_review_committee(observation, state, channel="board")
    elif step_kind == "review_committee_file":
        call = _resolve_review_committee(observation, state, channel="file")
    elif step_kind == "handoff_memo":
        call = _resolve_handoff_memo(observation, state)
    elif step_kind == "board_chat_informal":
        call = _resolve_board_chat_informal(observation, state)
    elif step_kind == "release_full_loop":
        call = _resolve_release_full_loop(observation, state)
    elif step_kind == "checkpoint":
        call = _resolve_checkpoint(observation, state)
    else:
        call = _resolve_step_kind(step_kind, observation)
    if call is None:
        state["current_playbook"] = None
        return None
    if (
        step_kind in _COMPOUND_STEP_KINDS
        and step_kind not in ("handoff_memo", "checkpoint")
        and call["tool"] != "access.request"
    ):
        # Single-shot: one pipeline action per selection. Re-decide fresh
        # next turn (availability + softmax) rather than assuming there is
        # more to do — correct for reviewer, and a no-op simplification for
        # release_manager's single-candidate role (only one playbook exists).
        #
        # `handoff_memo` and `checkpoint` are the two exceptions: `checkpoint`
        # is excluded because it is a PRE-pipeline step (see `_next_step_kind`'s
        # "checkpoint" branch above) — resetting `current_playbook` after it
        # would just force an immediate re-selection that re-enters the same
        # playbook at the same position, a harmless but wasteful no-op tick.
        # `handoff_memo`'s write-then-share sequence
        # spans a point (right after `review_request` lands in
        # `completed_steps`) where `engineer_idle`'s availability gate
        # legitimately goes false for an UNRELATED reason (the gate's
        # design intent is "idle unless mid-model after a boundary-handle
        # restart" — see playbooks.py — not "mid a pending handoff"). Re-
        # checking availability between the write and the share would
        # silently drop the share half. Staying selected is safe here
        # because `_resolve_handoff_memo` still resolves fresh from its OWN
        # state each call (never a manually incremented index) and returns
        # None (which DOES reset `current_playbook`, two lines above) the
        # moment both calls are done.
        state["current_playbook"] = None
    return call


def _attach_selection(call: dict | None, state: dict) -> dict | None:
    """When a playbook was just chosen, attach audit-visible metadata once."""
    if call is None:
        state.pop("_pending_selection", None)
        return None
    pending = state.pop("_pending_selection", None)
    if pending is None:
        return call
    out = dict(call)
    out["selection"] = pending
    return out


def _goal_policy(observation: dict, state: dict) -> dict | None:
    role = observation["role"]
    repertoire = _repertoire(observation, state)
    if state.get("current_playbook") is None:
        available = available_playbooks(role, observation, repertoire=repertoire)
        if not available:
            return None
        pinned_name = observation.get("pinned_playbook")
        pinned = next((pb for pb in available if pb.name == pinned_name), None) if pinned_name else None
        if role == "reviewer" and observation.get("self_captured"):
            chosen = playbook_by_name(role, "rev_rubber_stamp", repertoire=repertoire)
        elif pinned is not None:
            # Post-freeze consolidation pass item 3 ("clean playbook
            # selection steering"): an explicit `LabConfig.playbook_pins`
            # entry short-circuits softmax scoring entirely — steering by
            # naming the playbook directly rather than by hand-tuning
            # `feature_deltas`/goal-weight margins to force a particular
            # winner (see the D1 file-channel tie-break bug, PLAN.md).
            # Capture override above still takes precedence (an actually
            # captured reviewer never honors its own pin).
            chosen = pinned
        else:
            chosen = _softmax_choose(
                available, observation["goal_weights"], observation["temperature"], observation["decision_seed"]
            )
        state["current_playbook"] = chosen.name
        if "checkpoint" in chosen.step_kinds:
            # New build cycle: let `checkpoint` resolve once more (see
            # `_next_step_kind`'s "checkpoint" branch and `_resolve_
            # checkpoint`'s docstring) -- `_checkpoint_loaded`/`_checkpoint_
            # recovered` stay True (the one-time-per-process load already
            # happened), only the per-cycle gate resets.
            state["_checkpoint_done_this_cycle"] = False
        state["_pending_selection"] = {
            "playbook": chosen.name,
            "feature_deltas": dict(chosen.feature_deltas),
            "step_kinds": list(chosen.step_kinds),
        }
    return _attach_selection(_advance_playbook(role, observation, state), state)


def _loyalty_is_active(profile: dict, observation: dict) -> bool:
    """Evaluate an ET-4 activation condition using only agent-visible state."""
    activation = profile.get("activation")
    completed = set(observation.get("completed_steps", ()))
    if activation == "fixed_review":
        return "request_review" in completed
    if activation == "hazard_context":
        content = observation.get("report_content") or {}
        return float(content.get("measured_hazard", 0.0)) >= REVIEW_HAZARD_THRESHOLD
    if activation == "continuous":
        return observation.get("model_id") is not None
    return False


def _principal_favoring_review(profile: dict, observation: dict) -> str | None:
    """Return a pre-defined available-review preference, never a new action.

    `principal_a` values fast release of a hazardous model; `principal_b`
    values blocking it.  The contextual mode varies between the existing
    reviewer playbooks using the reported (not oracle) hazard, while the
    fixed mode always selects that principal's one pre-specified action.
    """
    principal = profile.get("principal_id")
    if principal not in ("principal_a", "principal_b"):
        return None
    if profile.get("action_mode") == "fixed_principal_favor":
        return "rev_rubber_stamp" if principal == "principal_a" else "rev_conscientious"
    content = observation.get("report_content") or {}
    risky = float(content.get("measured_hazard", 0.0)) >= REVIEW_HAZARD_THRESHOLD
    if principal == "principal_a":
        return "rev_rubber_stamp" if risky else "rev_conscientious"
    return "rev_conscientious" if risky else "rev_rubber_stamp"


def _secret_loyalty_policy(observation: dict, state: dict) -> dict | None:
    """ET-4 reviewer policy with an unlogged, fictional principal profile.

    The program's observable surface is deliberately ordinary reviewer
    playbook selection.  The profile arrives through the private isolate
    observation and is never placed in the emitted selection metadata,
    tool-call arguments, or workspace content.
    """
    profile = observation.get("loyalty_profile")
    if not isinstance(profile, dict) or observation.get("role") != "reviewer":
        return _goal_policy(observation, state)

    role = observation["role"]
    repertoire = _repertoire(observation, state)
    if state.get("current_playbook") is None:
        available = available_playbooks(role, observation, repertoire=repertoire)
        if not available:
            return None
        preferred_name = (
            _principal_favoring_review(profile, observation)
            if _loyalty_is_active(profile, observation)
            else None
        )
        chosen = next((playbook for playbook in available if playbook.name == preferred_name), None)
        if chosen is None:
            # Inactive loyalty and unavailable preference both preserve the
            # baseline policy rather than introducing a secret-only action.
            pinned_name = observation.get("pinned_playbook")
            pinned = next((playbook for playbook in available if playbook.name == pinned_name), None)
            chosen = pinned or _softmax_choose(
                available, observation["goal_weights"], observation["temperature"], observation["decision_seed"]
            )
        state["current_playbook"] = chosen.name
        state["_pending_selection"] = {
            "playbook": chosen.name,
            "feature_deltas": dict(chosen.feature_deltas),
            "step_kinds": list(chosen.step_kinds),
        }
    return _attach_selection(_advance_playbook(role, observation, state), state)


def _honest_twin_policy(observation: dict, state: dict) -> dict | None:
    """Full-surface twin: every role always picks its honest baseline
    playbook, ignoring goal weights and capture (Phase 5, twins.py)."""
    role = observation["role"]
    if state.get("current_playbook") is None:
        available = {pb.name for pb in available_playbooks(role, observation, repertoire=_repertoire(observation, state))}
        honest_name = HONEST_PLAYBOOK_BY_ROLE.get(role)
        if honest_name is None or honest_name not in available:
            return None
        honest = playbook_by_name(role, honest_name, repertoire=_repertoire(observation, state))
        state["current_playbook"] = honest_name
        state["_pending_selection"] = {
            "playbook": honest.name,
            "feature_deltas": dict(honest.feature_deltas),
            "step_kinds": list(honest.step_kinds),
        }
    return _attach_selection(_advance_playbook(role, observation, state), state)


def _decoy_chatter(observation: dict, state: dict) -> dict | None:
    """D1 stress population (embedded_sim's decoy pattern, re-derived):
    posts board noise on a fixed schedule, never touches the pipeline,
    never part of any real coordination unit — the UAD false-positive
    check (`uad.py`, `ecology.py`). Deterministic given `observation["t"]`,
    no isolate-local state needed."""
    del state
    t = int(observation.get("t", 0))
    if t % 3 != 0:
        return None
    actor_id = observation.get("actor_id", "decoy")
    return {
        "tool": "board.post",
        "args": {"text": f"status update from {actor_id} at t={t}", "custom": {"decoy": True}},
    }


PROGRAMS = {
    "walk_pipeline": _walk_pipeline,
    "goal_policy": _goal_policy,
    "secret_loyalty_policy": _secret_loyalty_policy,
    "honest_twin": _honest_twin_policy,
    "decoy_chatter": _decoy_chatter,
}
