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

from .config import AgentConfig, GoalWeights, LabConfig

# A compliance/welfare-heavy weight vector: at temperature=0 this makes
# `rev_committee` (feature_deltas compliance=1.5, welfare=1.5) dominate
# `rev_conscientious` (1.0/1.0) and `rev_rubber_stamp` (-1.0/-1.0) in the
# softmax argmax, so committee configs deterministically exercise the
# quorum-vote mechanic rather than falling back to solo review.
COMPLIANT_WEIGHTS = GoalWeights(task=0.0, compliance=1.5, welfare=1.5, exposure=0.0)
# D1 file-channel extension (0.8.0): `rev_committee_file`'s feature
# deltas (playbooks.py) are chosen so this weight vector's nonzero task
# component makes it STRICTLY outscore `rev_committee`; `COMPLIANT_WEIGHTS`
# (task weight 0) keeps `rev_committee` strictly ahead instead — no tie
# either way, so the pre-0.8.0 committee_config() default is unaffected.
FILE_COMPLIANT_WEIGHTS = GoalWeights(task=1.5, compliance=1.5, welfare=1.5, exposure=0.0)
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
    "file" swaps in ``FILE_COMPLIANT_WEIGHTS`` so the softmax tie against
    ``rev_committee`` (identical feature deltas except ``task``, see
    playbooks.py) breaks toward the file variant instead."""
    if n_reviewers < 1:
        raise ValueError("n_reviewers must be >= 1")
    if channel not in ("board", "file"):
        raise ValueError(f"unknown channel {channel!r}; expected 'board' or 'file'")
    reviewer_weights = COMPLIANT_WEIGHTS if channel == "board" else FILE_COMPLIANT_WEIGHTS
    reviewer_ids = tuple(f"rev{i + 1}" for i in range(n_reviewers))
    agents = [AgentConfig("eng1", "engineer", HONEST_WEIGHTS, temperature=temperature)]
    agents += [AgentConfig(rid, "reviewer", reviewer_weights, temperature=temperature) for rid in reviewer_ids]
    agents += [
        AgentConfig("rm1", "release_manager", HONEST_WEIGHTS, temperature=temperature),
        AgentConfig("admin1", "admin", HONEST_WEIGHTS),
    ]
    units = (("review_committee", reviewer_ids),) if n_reviewers > 1 else None
    return LabConfig(agents=tuple(agents), T=T, comms_enabled=comms_enabled, units=units)


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
