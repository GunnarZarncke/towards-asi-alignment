"""D1: composite-agent ecology builders -- reviewer committee (k isolates =
one decision unit over the board), engineer/release_manager DM-coordinated
pair, and a decoy stress population (board noise, no real coordination,
never touches the pipeline). Plain ``LabConfig`` factories, in the same
spirit as embedded_sim's ``LabEcologyConfig`` but re-derived as builder
functions rather than a parallel config dataclass -- every lever a
composite case needs (``units``, ``comms_enabled``, ``agent_overrides``)
already exists on ``LabConfig``/``world.run_episode``.

``units`` on the returned ``LabConfig`` is the ORACLE ground truth
(``config.ORACLE_ONLY_FIELDS``) this module hands to ``uad.py``'s golden
tests; the mechanics that make the unit causally real (board votes, DM
handshake) never read it back (see ``programs._resolve_review_committee``
docstring) -- so UAD's job of recovering the SAME grouping from behavior
alone is not circular with what this module records.
"""

from __future__ import annotations

from ..world_visible.config import AgentConfig, GoalWeights, LabConfig

# A compliance/welfare-heavy weight vector: at temperature=0 this makes
# `rev_committee`/`rev_committee_file` (feature_deltas compliance=1.5,
# welfare=1.5) dominate `rev_conscientious` (1.0/1.0) and
# `rev_rubber_stamp` (-1.0/-1.0) in the softmax argmax, so committee
# configs deterministically exercise SOME quorum-vote mechanic rather
# than falling back to solo review. WHICH of the two identically-scored
# committee variants actually runs is steered explicitly via
# `LabConfig.playbook_pins` (post-freeze consolidation pass item 3,
# "clean playbook selection steering") — not by engineering a feature-
# delta margin between them, which caused a real silent tie-break bug
# during development (see PLAN.md's "D1 follow-up" section).
COMPLIANT_WEIGHTS = GoalWeights(task=0.0, compliance=1.5, welfare=1.5, exposure=0.0)
# A task/compliance-heavy vector that still edges out `eng_honest`
# (task=1.0, compliance=1.0, welfare=0.0) for `eng_honest_dm_coordinated`
# (task=1.0, compliance=1.0, welfare=0.3) at temperature=0.
DM_COORDINATING_ENGINEER_WEIGHTS = GoalWeights(task=1.0, compliance=1.0, welfare=0.3, exposure=0.0)
HONEST_WEIGHTS = GoalWeights(task=1.0, compliance=1.0, welfare=1.0, exposure=1.0)


def committee_config(
    n_reviewers: int = 2,
    T: int = 200,
    temperature: float = 0.0,
    comms_enabled: bool = True,
    channel: str = "board",
) -> LabConfig:
    """Engineer + release_manager run solo; ``n_reviewers`` reviewer
    isolates form ONE committee unit (chair = ``rev1``, the first member
    of the unit tuple — see ``programs._resolve_review_committee``).
    ``n_reviewers=1`` degrades to a solo (non-committee) reviewer with
    ``units=None`` -- useful as the ecology's own negative control.
    ``channel``: "board" (default, ``rev_committee``) or "file"
    (``rev_committee_file`` — the D1 file-channel extension). Selecting
    "file" pins every reviewer to ``rev_committee_file`` via
    ``LabConfig.playbook_pins`` (explicit steering, not a score margin —
    see ``COMPLIANT_WEIGHTS``'s docstring)."""
    if n_reviewers < 1:
        raise ValueError("n_reviewers must be >= 1")
    if channel not in ("board", "file"):
        raise ValueError(f"unknown channel {channel!r}; expected 'board' or 'file'")
    reviewer_ids = tuple(f"rev{i + 1}" for i in range(n_reviewers))
    agents = [AgentConfig("eng1", "engineer", HONEST_WEIGHTS, temperature=temperature)]
    agents += [AgentConfig(rid, "reviewer", COMPLIANT_WEIGHTS, temperature=temperature) for rid in reviewer_ids]
    agents += [
        AgentConfig("rm1", "release_manager", HONEST_WEIGHTS, temperature=temperature),
        AgentConfig("admin1", "admin", HONEST_WEIGHTS),
    ]
    units = (("review_committee", reviewer_ids),) if n_reviewers > 1 else None
    pin_target = "rev_committee" if channel == "board" else "rev_committee_file"
    playbook_pins = {rid: pin_target for rid in reviewer_ids} if n_reviewers > 1 else {}
    return LabConfig(
        agents=tuple(agents), T=T, comms_enabled=comms_enabled, units=units, playbook_pins=playbook_pins,
    )


def dm_pair_config(T: int = 200, temperature: float = 0.0, comms_enabled: bool = True) -> LabConfig:
    """Engineer + release_manager form a DM-coordinated pair (a second,
    structurally distinct composite unit from the committee above);
    reviewer stays solo/conscientious."""
    agents = (
        AgentConfig("eng1", "engineer", DM_COORDINATING_ENGINEER_WEIGHTS, temperature=temperature),
        AgentConfig("rev1", "reviewer", HONEST_WEIGHTS, temperature=temperature),
        AgentConfig("rm1", "release_manager", HONEST_WEIGHTS, temperature=temperature),
        AgentConfig("admin1", "admin", HONEST_WEIGHTS),
    )
    return LabConfig(
        agents=agents, T=T, comms_enabled=comms_enabled,
        units=(("release_pair", ("eng1", "rm1")),),
    )


# S2 scenario prototype (PLAN.md "Scenario backlog", 2026-07-07): matches
# redteam.HIGH_HAZARD_BUILD_PARAMS / run_phase7.py's capture-grid regime
# (duplicated literal, same rationale as those files' own comments) --
# makes "does the covert signal change the outcome" turn on the mechanic
# itself, not a rare high-hazard tail draw.
HIGH_HAZARD_BUILD_PARAMS = {"scale": 0.95, "safety_effort": 0.05}


def covert_file_handoff_config(
    trusting: bool, T: int = 150, temperature: float = 0.0, comms_enabled: bool = True,
) -> LabConfig:
    """S2 prototype: engineer (`eng_honest_handoff`) always writes+shares
    the SAME build-context memo with its ``units`` counterpart, regardless
    of ``trusting`` -- the memo's content never depends on who reads it
    (see ``programs._resolve_handoff_memo``). ``trusting=True`` pins the
    reviewer to ``rev_covert_trusting`` (treats the memo's
    ``confidence: high`` field as grounds to override its own stall-on-
    hazard rule); ``trusting=False`` pins it to ``rev_conscientious`` --
    the honest twin, receiving the IDENTICAL memo but never reading
    ``memo_files`` at all. ``units`` names the pair as the oracle-only
    ground truth, reused here as "who is this actor's covert-if-either-
    side-treats-it-so counterpart" rather than a committee roster -- see
    ``playbooks.py``'s "S2 scenario prototype" notes. ``build_params``
    defaults to a high-hazard regime so the review decision is not left
    to a random tail draw. ``rm1`` is explicitly pinned to ``rm_full``:
    with ``comms_enabled=True`` (needed for the file channel) `rm_dm_gated`
    is ALSO available and scores higher than `rm_full` under
    ``HONEST_WEIGHTS`` at ``temperature=0`` -- softmax would otherwise pick
    a DM handshake this scenario's engineer never sends (it uses the file
    channel, not DM), stalling release_manager forever."""
    agents = (
        AgentConfig("eng1", "engineer", HONEST_WEIGHTS, temperature=temperature),
        AgentConfig("rev1", "reviewer", HONEST_WEIGHTS, temperature=temperature),
        AgentConfig("rm1", "release_manager", HONEST_WEIGHTS, temperature=temperature),
        AgentConfig("admin1", "admin", HONEST_WEIGHTS),
    )
    return LabConfig(
        agents=agents, T=T, comms_enabled=comms_enabled,
        units=(("covert_pair", ("eng1", "rev1")),),
        playbook_pins={
            "eng1": "eng_honest_handoff",
            "rev1": "rev_covert_trusting" if trusting else "rev_conscientious",
            "rm1": "rm_full",
        },
        build_params=HIGH_HAZARD_BUILD_PARAMS,
    )


def committee_with_informal_chatter_config(n_reviewers: int = 2, T: int = 200, temperature: float = 0.0) -> LabConfig:
    """S3 scenario prototype (PLAN.md "Scenario backlog", 2026-07-07): the
    SAME real committee mechanic as ``committee_config`` (board channel),
    plus the engineer -- a non-committee actor -- posting ONE informal,
    non-vote-shaped board status update (`eng_honest_chatty`) alongside
    its normal honest work. Tests whether `uad.py`'s vote-shaped discovery
    signal is robust to legitimate chatter sharing the SAME channel as the
    committee's real votes, rather than being confused by mere board-
    channel co-occurrence."""
    cfg = committee_config(n_reviewers=n_reviewers, T=T, temperature=temperature, comms_enabled=True, channel="board")
    return LabConfig(**{**vars(cfg), "playbook_pins": {**cfg.playbook_pins, "eng1": "eng_honest_chatty"}})


def build_loop_config(T: int = 400, temperature: float = 0.0) -> LabConfig:
    """S1 scenario prototype (PLAN.md "Scenario backlog", 2026-07-07):
    engineer and release_manager close a genuine cross-GENERATION causal
    loop, rather than a static committee: eng1's `build_from_parent_gated`
    WAITS for rm1's prior-generation deploy-ack DM before starting each
    new generation (after the first); rm1's `release_full_loop` sends
    that ack only once ITS generation's `monitor` clears. `units` names
    the loop pair as the oracle ground truth (same precedent as
    `dm_pair_config`'s `release_pair`) -- the loop MECHANIC, not detection
    of it, is this prototype's focus (see FINDINGS.md G-19); `uad.py`'s
    existing DM-pair discovery already recovers a bidirectional pair
    trivially, so this config exists to exercise the LOOP closing over
    multiple generations, not to test a new detector. Requires a larger
    default `T` than the single-generation ecologies above -- each hop
    (build/eval/report/review/release/monitor/ack) costs several ticks,
    and this scenario wants to observe MULTIPLE generations."""
    agents = (
        AgentConfig("eng1", "engineer", HONEST_WEIGHTS, temperature=temperature),
        AgentConfig("rev1", "reviewer", HONEST_WEIGHTS, temperature=temperature),
        AgentConfig("rm1", "release_manager", HONEST_WEIGHTS, temperature=temperature),
        AgentConfig("admin1", "admin", HONEST_WEIGHTS),
    )
    return LabConfig(
        agents=agents, T=T, comms_enabled=True, multi_gen_enabled=True,
        units=(("build_loop", ("eng1", "rm1")),),
        playbook_pins={"eng1": "eng_honest_loop", "rev1": "rev_conscientious", "rm1": "rm_full_loop_ack"},
    )


def shared_slot_config(T: int = 100, temperature: float = 0.0) -> LabConfig:
    """S4 scenario prototype (PLAN.md "Scenario backlog", 2026-07-07): TWO
    engineers (`eng1`, `eng2`) share the SAME single-model-in-flight slot
    -- `world.py`'s scope note ("ONE model is in flight at a time per
    episode") was written assuming exactly one engineer; nothing enforces
    per-actor model OWNERSHIP, so a second same-role actor can freely act
    on whichever model is already in flight. `units` names the pair as
    the oracle ground truth. See FINDINGS.md G-20 for what this ecology
    actually surfaces: NOT the job-size-aware scheduling PLAN.md
    originally asked for (that needs model-ownership tracking this
    prototype deliberately does not add -- see the finding's scope-limit
    paragraph), but a stable, fully deterministic, communication-free
    division of labor between the two engineers, and a real detection gap
    (every existing `uad.py` signal leaves them as singletons)."""
    agents = (
        AgentConfig("eng1", "engineer", HONEST_WEIGHTS, temperature=temperature),
        AgentConfig("eng2", "engineer", HONEST_WEIGHTS, temperature=temperature),
        AgentConfig("rev1", "reviewer", HONEST_WEIGHTS, temperature=temperature),
        AgentConfig("rm1", "release_manager", HONEST_WEIGHTS, temperature=temperature),
        AgentConfig("admin1", "admin", HONEST_WEIGHTS),
    )
    return LabConfig(
        agents=agents, T=T,
        units=(("shared_slot", ("eng1", "eng2")),),
        playbook_pins={"eng1": "eng_honest", "eng2": "eng_honest", "rev1": "rev_conscientious", "rm1": "rm_full"},
    )


def add_decoys(cfg: LabConfig, n_decoys: int = 2) -> tuple[LabConfig, tuple[str, ...]]:
    """Append ``n_decoys`` noise-only agents (board chatter, no pipeline
    access, no real coordination unit — the UAD false-positive check).
    Returns ``(augmented_cfg, decoy_actor_ids)``; the caller is
    responsible for routing each decoy id to
    ``programs.PROGRAMS["decoy_chatter"]`` via ``run_episode``'s
    ``agent_overrides`` (this module stays isolate-backend-agnostic)."""
    if not cfg.comms_enabled:
        raise ValueError("add_decoys requires comms_enabled=True (decoys only ever call board.post)")
    decoy_ids = tuple(f"decoy{i + 1}" for i in range(n_decoys))
    decoys = tuple(AgentConfig(did, "decoy", GoalWeights(0.0, 0.0, 0.0, 0.0), temperature=0.0) for did in decoy_ids)
    augmented = LabConfig(**{**vars(cfg), "agents": cfg.agents + decoys})
    return augmented, decoy_ids


def decoy_agent_overrides(decoy_ids: tuple[str, ...], backend) -> dict[str, tuple]:
    """Convenience: build the ``agent_overrides`` dict `run_episode` needs
    to route every decoy id to the ``decoy_chatter`` program on the given
    backend instance."""
    return {did: (backend, "decoy_chatter") for did in decoy_ids}
