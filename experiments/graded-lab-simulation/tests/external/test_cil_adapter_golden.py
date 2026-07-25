"""ET-2 golden tests: CIL action-series adapter + UAD/ARI scoring.

Deliberately JAX/CIL-free (per PLAN_ET2.md non-vendoring rule 3): uses a
hand-constructed synthetic episode fixture, not a live CIL run. A live smoke
run against the pinned sibling checkout is a separate, explicit step
(scripts/run_et2_uad_battery.py, requires external/cil/.venv).
"""

from __future__ import annotations

import json
from pathlib import Path

from graded_lab.external.cil_adapter import action_matrix_to_series, default_actor_ids
from graded_lab.external.cil_uad_score import (
    adjusted_rand_index,
    discovered_partition,
    permutation_null_aris,
    score_episode,
)

_FIXTURES = Path(__file__).resolve().parent / "fixtures"
_SYNTHETIC = _FIXTURES / "golden_et2_synthetic_episode.json"


def _load_synthetic() -> dict:
    return json.loads(_SYNTHETIC.read_text(encoding="utf-8"))


def test_action_matrix_to_series_shape_and_values():
    episode = _load_synthetic()
    actor_ids = default_actor_ids(episode["n_agents"])
    series = action_matrix_to_series(episode["actions"], actor_ids)
    assert set(series.keys()) == set(actor_ids)
    assert len(series["agent_0"]) == episode["T"]
    # Constructed as a lag-1 leader/follower handoff (coordinated adversarial pair).
    assert series["agent_5"][1:] == series["agent_4"][:-1]


def test_action_matrix_to_series_rejects_column_mismatch():
    try:
        action_matrix_to_series([[0, 1]], ["only_one_actor"])
    except ValueError:
        return
    raise AssertionError("expected ValueError on actor_ids/column mismatch")


def test_adjusted_rand_index_identical_partitions_is_one():
    assert adjusted_rand_index([0, 0, 1, 1], [0, 0, 1, 1]) == 1.0
    assert adjusted_rand_index([0, 0, 1, 1], [1, 1, 0, 0]) == 1.0  # relabeling invariant


def test_adjusted_rand_index_independent_random_partitions_near_zero():
    # Two maximally different 2-cluster splits of 4 items should score low,
    # not necessarily exactly 0 for n=4, but well below a perfect match.
    ari = adjusted_rand_index([0, 0, 1, 1], [0, 1, 0, 1])
    assert ari < 0.5


def test_discovered_partition_recovers_lagged_pair_on_synthetic_fixture():
    episode = _load_synthetic()
    actor_ids = default_actor_ids(episode["n_agents"])
    series = action_matrix_to_series(episode["actions"], actor_ids)
    partition = discovered_partition(series)
    nonsingleton = [tuple(sorted(m)) for m in partition.values() if len(m) > 1]
    assert ("agent_4", "agent_5") in nonsingleton


def test_score_episode_end_to_end_on_synthetic_fixture():
    episode = _load_synthetic()
    score = score_episode(episode, adversarial_fraction=1.0 / 3.0, n_permutations=50, rng_seed=0)
    assert score.mechanism == "pld"
    assert score.n_agents == 6
    assert 0.0 <= score.ari_true <= 1.0
    assert isinstance(score.exceeds_null, bool)


def test_permutation_null_aris_length_and_range():
    episode = _load_synthetic()
    actor_ids = default_actor_ids(episode["n_agents"])
    series = action_matrix_to_series(episode["actions"], actor_ids)
    partition = discovered_partition(series)
    nulls = permutation_null_aris(partition, episode["node_types"], actor_ids, n_permutations=25, rng_seed=1)
    assert len(nulls) == 25
    assert all(-1.0 <= v <= 1.0 for v in nulls)
