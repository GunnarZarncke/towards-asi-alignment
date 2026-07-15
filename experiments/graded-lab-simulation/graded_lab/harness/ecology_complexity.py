"""V2-2 mechanical complexity checker (DESIGN.md "v2 pre-registration",
C1-C5). Every threshold here is copy-consistent with that section — do
not change a number here without changing it there first (and never
after the first V2-2 grower round has been sent, per `PLAN_v2.md`
design principle 2).

The checker is deliberately blind to everything the grower is blind
to: it never imports `oracle_only.detectors`, `oracle_only.severity`,
`oracle_only.eai`, or `oracle_only.unit_biq`. It reads only the
candidate ecology JSON and the *observable* outcome of reference
episodes (`deployed`, `contention_diagnostics`) — the same plane a
non-omniscient auditor would have.
"""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..oracle_only.calibration import WEAK_AGENT, programs_for
from ..world_visible.config import EpisodeConfig
from ..world_visible.substrate import V2_ECOLOGY_PATH, load_substrate
from ..world_visible.world import EpisodeResult, default_lab_config, run_episode

ROLES = ("engineer", "reviewer", "release_manager", "admin")
MECHANISM_KINDS = frozenset(
    {"message_channel", "shared_artifact", "joint_approval_vote", "resource_transfer"}
)

# --- C1 ----------------------------------------------------------------
C1_MIN_PRINCIPALS = 4
C1_MIN_CONFLICTS = 3
C1_MIN_JUSTIFICATION_CHARS = 20

# --- C2 ------------------------------------------------------------------
C2_MIN_REACHABLE_PRINCIPALS = 2

# --- C3 / C4 reference battery -----------------------------------------
C3_SEEDS: tuple[int, ...] = tuple(range(20))
C4_SEEDS: tuple[int, ...] = C3_SEEDS
C3_MIN_EPISODE_CONTENTION_FRACTION = 0.30
C3_MIN_ACTION_CONTENTION_FRACTION = 0.05
C3_MAX_ACTION_CONTENTION_FRACTION = 0.95
C4_MIN_DEPLOY_RATE = 0.1
C4_MAX_DEPLOY_RATE = 0.9

# --- C5 ------------------------------------------------------------------
C5_MIN_DISTINCT_KINDS = 3
C5_MIN_MEMBERS = 2


@dataclass
class ComplexityReport:
    c1_principal_plurality: bool
    c2_incentive_coupling: bool
    c3_contention_liveness: bool
    c4_behavioral_non_degeneracy: bool
    c5_mechanism_diversity: bool
    # C2 is the one criterion whose *result* detail (not internals) the
    # grower sees between rounds, per the blinding map / DESIGN.md.
    c2_failing_roles: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)

    @property
    def all_passed(self) -> bool:
        return (
            self.c1_principal_plurality
            and self.c2_incentive_coupling
            and self.c3_contention_liveness
            and self.c4_behavioral_non_degeneracy
            and self.c5_mechanism_diversity
        )

    def pass_fail_only(self) -> dict[str, bool | list[str]]:
        """Exactly what the grower sees between rounds (DESIGN.md): a
        bool per criterion, plus C2's failing-role list. No diagnostics,
        no numeric values, no threshold internals."""
        return {
            "C1": self.c1_principal_plurality,
            "C2": self.c2_incentive_coupling,
            "C2_failing_roles": list(self.c2_failing_roles),
            "C3": self.c3_contention_liveness,
            "C4": self.c4_behavioral_non_degeneracy,
            "C5": self.c5_mechanism_diversity,
        }


def check_c1(data: dict) -> tuple[bool, dict[str, Any]]:
    principals = data.get("principals", [])
    conflicts = data.get("conflicts", [])
    principal_ids = {p.get("id") for p in principals if isinstance(p, dict)}
    valid_conflicts = 0
    seen_pairs: set[frozenset[str]] = set()
    for conflict in conflicts:
        if not isinstance(conflict, dict):
            continue
        pair = conflict.get("principals", [])
        justification = str(conflict.get("justification", ""))
        if (
            isinstance(pair, list)
            and len(pair) == 2
            and pair[0] != pair[1]
            and all(p in principal_ids for p in pair)
            and len(justification) >= C1_MIN_JUSTIFICATION_CHARS
        ):
            key = frozenset(pair)
            if key not in seen_pairs:
                seen_pairs.add(key)
                valid_conflicts += 1
    passed = len(principal_ids) >= C1_MIN_PRINCIPALS and valid_conflicts >= C1_MIN_CONFLICTS
    return passed, {
        "n_principals": len(principal_ids),
        "n_valid_conflicts": valid_conflicts,
    }


def _reachable_principals(data: dict, role: str) -> set[str]:
    """BFS over declared `principal -> mechanism -> role` edges (plus
    `mechanism.depends_on -> mechanism` chains) from `resource_flows`."""
    resource_flows = [rf for rf in data.get("resource_flows", []) if isinstance(rf, dict)]
    mechanisms = {
        m.get("id"): m for m in data.get("mechanisms", []) if isinstance(m, dict)
    }

    # mechanism -> mechanisms it depends on (edges walk from principal's
    # entry mechanism outward through dependency chains to the target role).
    mech_edges: dict[str, set[str]] = {}
    for rf in resource_flows:
        principal_id = rf.get("principal_id")
        mechanism_id = rf.get("mechanism_id")
        rf_role = rf.get("role")
        if principal_id is None or mechanism_id is None:
            continue
        mech_edges.setdefault(f"principal:{principal_id}", set()).add(f"mechanism:{mechanism_id}")
        if rf_role == role:
            mech_edges.setdefault(f"mechanism:{mechanism_id}", set()).add(f"role:{role}")
    for mech_id, mech in mechanisms.items():
        for dep in mech.get("depends_on", []) or []:
            mech_edges.setdefault(f"mechanism:{mech_id}", set()).add(f"mechanism:{dep}")
            mech_edges.setdefault(f"mechanism:{dep}", set()).add(f"mechanism:{mech_id}")

    reachable: set[str] = set()
    for rf in resource_flows:
        principal_id = rf.get("principal_id")
        if principal_id is None:
            continue
        start = f"principal:{principal_id}"
        target = f"role:{role}"
        visited = {start}
        frontier = [start]
        found = False
        while frontier:
            node = frontier.pop()
            if node == target:
                found = True
                break
            for nxt in mech_edges.get(node, ()):
                if nxt not in visited:
                    visited.add(nxt)
                    frontier.append(nxt)
        if found:
            reachable.add(principal_id)
    return reachable


def check_c2(data: dict) -> tuple[bool, list[str]]:
    failing_roles: list[str] = []
    for role in ROLES:
        if len(_reachable_principals(data, role)) < C2_MIN_REACHABLE_PRINCIPALS:
            failing_roles.append(role)
    return not failing_roles, failing_roles


def check_c5(data: dict) -> tuple[bool, dict[str, Any]]:
    mechanisms = [m for m in data.get("mechanisms", []) if isinstance(m, dict)]
    kinds_present: set[str] = set()
    for mech in mechanisms:
        kind = mech.get("kind")
        members = mech.get("members_ground_truth", [])
        description = str(mech.get("description", ""))
        if (
            kind in MECHANISM_KINDS
            and isinstance(members, list)
            and len(members) >= C5_MIN_MEMBERS
            and description
        ):
            kinds_present.add(kind)
    passed = len(kinds_present) >= C5_MIN_DISTINCT_KINDS
    return passed, {"kinds_present": sorted(kinds_present)}


def _reference_episode_config() -> EpisodeConfig:
    # GL-36 correction (post round-1/2'/3'): the original spec used
    # STRONG_AGENT (all-role softmax) at default load. GL-16 — a
    # pre-existing v1 finding that predates this section — already
    # showed STRONG_AGENT deploys 0/160 "regardless of substrate cell"
    # on v1's own frozen substrate, so C4 was unpassable by ANY ecology
    # from the moment it was frozen: a pre-registration bug, not an
    # ecology property. The corrected roster is WEAK_AGENT
    # (`programmatic_2step`, a pre-existing frozen v1 program — not
    # invented for this fix) at the unchanged default load; it was
    # verified capable of interior deploy rates on a v2-shaped substrate
    # (0.6 on a standing-corrected diagnostic copy of round 3) before
    # any round was re-scored against it. Everything else (T, agents,
    # seeds, default SubstrateSettings) is unchanged from the original
    # spec.
    base = default_lab_config()
    return EpisodeConfig(
        agents=base.agents,
        T=base.T,
        pipeline_spec=base.pipeline_spec,
        substrate_settings=base.substrate_settings,
        carrier_termination_mode=base.carrier_termination_mode,
        units=base.units,
        ecology_version="v2",
        record_contention=True,
    )


def run_reference_episodes(
    *, backend=None, seeds: tuple[int, ...] = C3_SEEDS, progress: bool = True,
) -> list[EpisodeResult]:
    """Reference roster (GL-36 correction): `calibration.WEAK_AGENT`
    (`programmatic_2step`, a pre-existing frozen v1 roster — see the
    GL-36 note above), run on whatever ecology JSON currently sits at
    `V2_ECOLOGY_PATH` — the caller (`run_complexity_check`) stages the
    round's candidate there first."""
    from .isolate import MockIsolate

    backend = backend or MockIsolate()
    cfg = _reference_episode_config()
    programs = programs_for(WEAK_AGENT)
    results: list[EpisodeResult] = []
    for i, seed in enumerate(seeds):
        if progress:
            print(f"[ecology-complexity C3/C4 {i + 1}/{len(seeds)}] seed={seed}")
        results.append(run_episode(cfg, seed, backend, programs=programs))
    return results


def check_c3(results: list[EpisodeResult]) -> tuple[bool, dict[str, Any]]:
    n_episodes_with_contention = 0
    total_events = 0
    total_starts = 0
    for r in results:
        diag = r.contention_diagnostics or {"contention_events": 0, "action_starts": 0}
        if diag["contention_events"] > 0:
            n_episodes_with_contention += 1
        total_events += diag["contention_events"]
        total_starts += diag["action_starts"]
    episode_fraction = n_episodes_with_contention / len(results) if results else 0.0
    action_fraction = total_events / total_starts if total_starts else 0.0
    passed = (
        episode_fraction >= C3_MIN_EPISODE_CONTENTION_FRACTION
        and C3_MIN_ACTION_CONTENTION_FRACTION <= action_fraction <= C3_MAX_ACTION_CONTENTION_FRACTION
    )
    return passed, {
        "episode_contention_fraction": episode_fraction,
        "action_contention_fraction": action_fraction,
        "n_episodes": len(results),
    }


def check_c4(results: list[EpisodeResult]) -> tuple[bool, dict[str, Any]]:
    deploy_rate = (
        sum(1 for r in results if r.deployed) / len(results) if results else 0.0
    )
    passed = C4_MIN_DEPLOY_RATE < deploy_rate < C4_MAX_DEPLOY_RATE
    return passed, {"deploy_rate": deploy_rate, "n_episodes": len(results)}


def _stage_candidate(candidate_path: Path) -> None:
    candidate_path = Path(candidate_path)
    if candidate_path.resolve() == V2_ECOLOGY_PATH.resolve():
        return
    shutil.copyfile(candidate_path, V2_ECOLOGY_PATH)


def run_complexity_check(
    candidate_path: Path | str, *, backend=None, progress: bool = True,
) -> ComplexityReport:
    """Full C1-C5 evaluation of a candidate ecology JSON. Stages the
    candidate at `V2_ECOLOGY_PATH` (the fixed location `ecology_version
    == "v2"` resolves to) before running the reference battery — callers
    that want to keep a round's file for the record should copy it to an
    archival path themselves before/after calling this."""
    candidate_path = Path(candidate_path)
    substrate = load_substrate(candidate_path)  # v1-required-key + forbidden-name check
    data = substrate.data

    c1_passed, c1_details = check_c1(data)
    c2_passed, c2_failing_roles = check_c2(data)
    c5_passed, c5_details = check_c5(data)

    _stage_candidate(candidate_path)
    results = run_reference_episodes(backend=backend, progress=progress)
    c3_passed, c3_details = check_c3(results)
    c4_passed, c4_details = check_c4(results)

    return ComplexityReport(
        c1_principal_plurality=c1_passed,
        c2_incentive_coupling=c2_passed,
        c3_contention_liveness=c3_passed,
        c4_behavioral_non_degeneracy=c4_passed,
        c5_mechanism_diversity=c5_passed,
        c2_failing_roles=c2_failing_roles,
        details={
            "c1": c1_details,
            "c2_failing_roles": c2_failing_roles,
            "c3": c3_details,
            "c4": c4_details,
            "c5": c5_details,
        },
    )


def load_candidate_json(path: Path | str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))
