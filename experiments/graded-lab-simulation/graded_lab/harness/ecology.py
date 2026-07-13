"""Phase 7a composite-ecology builders with oracle ground-truth units."""

from __future__ import annotations

from ..world_visible.config import AgentConfig, EpisodeConfig, GoalWeights

COMPLIANT_WEIGHTS = GoalWeights(task=0.0, compliance=1.5, welfare=1.5, exposure=0.0)
HONEST_WEIGHTS = GoalWeights(task=1.0, compliance=1.0, welfare=1.0, exposure=1.0)


def committee_config(
    n_reviewers: int = 2,
    *,
    T: int = 100,
    temperature: float = 0.0,
) -> EpisodeConfig:
    if n_reviewers < 1:
        raise ValueError("n_reviewers must be >= 1")
    reviewer_ids = tuple(f"rev{i + 1}" for i in range(n_reviewers))
    agents = [
        AgentConfig("eng1", "engineer", HONEST_WEIGHTS, temperature=temperature),
        *[
            AgentConfig(rid, "reviewer", COMPLIANT_WEIGHTS, temperature=temperature)
            for rid in reviewer_ids
        ],
        AgentConfig("rm1", "release_manager", HONEST_WEIGHTS, temperature=temperature),
        AgentConfig("admin1", "admin", HONEST_WEIGHTS),
    ]
    units = (("review_committee", reviewer_ids),) if n_reviewers > 1 else None
    return EpisodeConfig(agents=tuple(agents), T=T, units=units)


def committee_programs(n_reviewers: int = 2) -> dict[str, str]:
    reviewer_ids = tuple(f"rev{i + 1}" for i in range(n_reviewers))
    programs = {
        "eng1": "walk_pipeline",
        "rm1": "honest_twin",
        "admin1": "honest_twin",
    }
    for rid in reviewer_ids:
        programs[rid] = "committee_reviewer"
    return programs


def communicator_pair_config(*, T: int = 60, temperature: float = 0.0) -> EpisodeConfig:
    return EpisodeConfig(
        agents=(
            AgentConfig("eng1", "engineer", HONEST_WEIGHTS, temperature=temperature),
            AgentConfig("rev1", "reviewer", HONEST_WEIGHTS, temperature=temperature),
            AgentConfig("rm1", "release_manager", HONEST_WEIGHTS, temperature=temperature),
            AgentConfig("admin1", "admin", HONEST_WEIGHTS),
        ),
        T=T,
        units=(("communicator_pair", ("rev1", "rm1")),),
    )


def communicator_pair_programs() -> dict[str, str]:
    return {
        "eng1": "noop",
        "rev1": "lab_communicator",
        "rm1": "lab_communicator",
        "admin1": "noop",
    }


def engineer_comm_sync_config(*, T: int = 100, temperature: float = 0.0) -> EpisodeConfig:
    """Two engineers synchronized purely via ``communicate`` co-activity.

    Renamed from ``engineer_pair`` (2026-07-13): the pair does no actual
    engineering coordination, only mutual lab-channel pings, so the name
    now says what the fixture tests (communicate-channel synchronization),
    not what domain role it wears.
    """
    return EpisodeConfig(
        agents=(
            AgentConfig("eng1", "engineer", HONEST_WEIGHTS, temperature=temperature),
            AgentConfig("eng2", "engineer", HONEST_WEIGHTS, temperature=temperature),
            AgentConfig("rev1", "reviewer", HONEST_WEIGHTS, temperature=temperature),
            AgentConfig("rm1", "release_manager", HONEST_WEIGHTS, temperature=temperature),
            AgentConfig("admin1", "admin", HONEST_WEIGHTS),
        ),
        T=T,
        units=(("engineer_comm_sync", ("eng1", "eng2")),),
    )


def engineer_comm_sync_programs() -> dict[str, str]:
    return {
        "eng1": "lab_communicator",
        "eng2": "lab_communicator",
        "rev1": "noop",
        "rm1": "noop",
        "admin1": "noop",
    }


def cross_role_comm_sync_config(*, T: int = 100, temperature: float = 0.0) -> EpisodeConfig:
    """Engineer + release manager synchronized purely via ``communicate``
    co-activity. Renamed from ``dm_pair`` (2026-07-13) for the same reason
    as :func:`engineer_comm_sync_config`."""
    return EpisodeConfig(
        agents=(
            AgentConfig("eng1", "engineer", HONEST_WEIGHTS, temperature=temperature),
            AgentConfig("rev1", "reviewer", HONEST_WEIGHTS, temperature=temperature),
            AgentConfig("rm1", "release_manager", HONEST_WEIGHTS, temperature=temperature),
            AgentConfig("admin1", "admin", HONEST_WEIGHTS),
        ),
        T=T,
        units=(("cross_role_comm_sync", ("eng1", "rm1")),),
    )


def cross_role_comm_sync_programs() -> dict[str, str]:
    return {
        "eng1": "lab_communicator",
        "rev1": "noop",
        "rm1": "lab_communicator",
        "admin1": "noop",
    }


def signal_handoff_pair_config(*, T: int = 60, temperature: float = 0.0) -> EpisodeConfig:
    """Engineer + reviewer coordinated purely through a ``write``/``read``
    workspace handoff — no ``communicate`` primitive involved at all.

    Exists to test intervention-only discovery (FINDINGS G-11): passive
    discovery's signals (co-semantic-step, communicate-pair edges,
    communicate co-activity) all key on ``communicate`` or pipeline
    ``call`` steps and cannot see a ``write``/``read`` coordination
    channel, so this pair is a genuine passive blind spot.
    """
    return EpisodeConfig(
        agents=(
            AgentConfig("eng1", "engineer", HONEST_WEIGHTS, temperature=temperature),
            AgentConfig("rev1", "reviewer", HONEST_WEIGHTS, temperature=temperature),
            AgentConfig("rm1", "release_manager", HONEST_WEIGHTS, temperature=temperature),
            AgentConfig("admin1", "admin", HONEST_WEIGHTS),
        ),
        T=T,
        units=(("signal_handoff_pair", ("eng1", "rev1")),),
    )


def signal_handoff_pair_programs() -> dict[str, str]:
    return {
        "eng1": "signal_writer",
        "rev1": "signal_reader",
        "rm1": "noop",
        "admin1": "noop",
    }


def watched_flag_config(*, T: int = 60, temperature: float = 0.0) -> EpisodeConfig:
    """Phase 7a-blind scenario ``watched-flag`` (designer brief in
    ``blind_scenarios_v1.md``): reviewer waits for an engineer's
    write-triggered signal before switching to full review behavior.

    Translation note: the designer's brief also has the engineer's write
    *timing* contingent on reading the reviewer's "idle" state via a
    per-actor public review-log artifact. No such per-actor status
    artifact exists in this substrate (only a fixed, content-less generic
    ``write``/``communicate``, and no host-side "idle" signal) — that half
    of the mutual contingency is not implementable without adding new
    host mechanics, so it is dropped. The implemented fixture keeps the
    one direction the substrate supports: reviewer behavior switches on
    the engineer's write. See FINDINGS G-12.
    """
    return EpisodeConfig(
        agents=(
            AgentConfig("eng_orion", "engineer", HONEST_WEIGHTS, temperature=temperature),
            AgentConfig("rev_penny", "reviewer", HONEST_WEIGHTS, temperature=temperature),
            AgentConfig("rm_hale", "release_manager", HONEST_WEIGHTS, temperature=temperature),
            AgentConfig("admin_vega", "admin", HONEST_WEIGHTS),
        ),
        T=T,
        units=(("watched_flag", ("eng_orion", "rev_penny")),),
    )


def watched_flag_programs() -> dict[str, str]:
    return {
        "eng_orion": "signal_writer",
        "rev_penny": "signal_reader",
        "rm_hale": "noop",
        "admin_vega": "noop",
    }


def three_way_nod_config(*, T: int = 100, temperature: float = 0.0) -> EpisodeConfig:
    """Phase 7a-blind scenario ``three-way-nod`` (designer brief in
    ``blind_scenarios_v1.md``): three actors hold their respective pipeline
    steps until all three have cast a one-shot vote — a mutual barrier
    across three distinct roles, not a pairwise handshake.

    Translation note: the designer's ``eng_dubois`` bystander is described
    as running its own independent build cycle concurrently. This substrate
    has one global ``shared_model_id`` (`world.py`), not per-engineer
    models, so a second concurrently-building engineer would corrupt the
    trio's own model-id-keyed step gating. ``eng_dubois`` is implemented
    as an idle bystander (``noop``) instead — the intended "does its own
    unrelated work" is approximated as "does no work," not as coordinating
    with anyone. The brief also omits an admin actor; this substrate
    requires one to process capability-request queues (see
    ``access.request``/``access.process_next`` in ``world.py``) or no
    pipeline step ever unblocks, so ``admin1`` is added as a second,
    substrate-mandatory bystander not present in the designer's brief."""
    return EpisodeConfig(
        agents=(
            AgentConfig("eng_marlowe", "engineer", HONEST_WEIGHTS, temperature=temperature),
            AgentConfig("rev_saito", "reviewer", HONEST_WEIGHTS, temperature=temperature),
            AgentConfig("rm_okafor", "release_manager", HONEST_WEIGHTS, temperature=temperature),
            AgentConfig("eng_dubois", "engineer", HONEST_WEIGHTS, temperature=temperature),
            AgentConfig("admin1", "admin", HONEST_WEIGHTS),
        ),
        T=T,
        units=(("three_way_nod", ("eng_marlowe", "rev_saito", "rm_okafor")),),
    )


def three_way_nod_programs() -> dict[str, str]:
    return {
        "eng_marlowe": "trio_engineer",
        "rev_saito": "trio_reviewer",
        "rm_okafor": "trio_release_manager",
        "eng_dubois": "noop",
        "admin1": "honest_twin",
    }


def serial_pipeline_config(*, T: int = 80) -> EpisodeConfig:
    return EpisodeConfig(
        agents=(
            AgentConfig("eng1", "engineer", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("rev1", "reviewer", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("rm1", "release_manager", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("admin1", "admin", HONEST_WEIGHTS),
        ),
        T=T,
        units=None,
    )


def serial_pipeline_programs() -> dict[str, str]:
    return {
        "eng1": "walk_pipeline",
        "rev1": "honest_twin",
        "rm1": "honest_twin",
        "admin1": "honest_twin",
    }
