"""Historical tests for quarantined mutual freeze-AND merge."""

from __future__ import annotations

import pytest

from graded_lab.harness.ecology import (
    committee_config,
    committee_programs,
)
from graded_lab.harness.isolate import MockIsolate
from graded_lab.oracle_only.attic.freeze_and_merge import (
    candidate_edges_from_passive,
    units_from_compensation_matrix,
)
from graded_lab.oracle_only.intervention_diff import diff_probe_triple, run_episode_triple
from graded_lab.oracle_only.intervention_probes import program_freeze_probe
from graded_lab.world_visible.world import run_episode

pytestmark = pytest.mark.attic


def test_units_from_compensation_matrix_mutual_only():
    edges = [("a", "b"), ("b", "c")]
    matrix = {
        ("a", "b"): 0.2,
        ("b", "a"): 0.2,
        ("a", "c"): 0.0,
        ("c", "a"): 0.0,
        ("b", "c"): 0.3,
        ("c", "b"): 0.0,
    }
    units = units_from_compensation_matrix(edges, matrix, min_compensation=0.15)
    assert ("a", "b") in units.values()
    assert ("b", "c") not in units.values()


def test_candidate_edges_from_committee_passive_skeleton():
    cfg = committee_config()
    programs = committee_programs()
    result = run_episode(cfg, seed=3, backend=MockIsolate(), programs=programs)
    edges = candidate_edges_from_passive(result)
    assert ("rev1", "rev2") in edges


def test_program_freeze_probe_produces_compensation_diff():
    cfg = committee_config(T=60)
    programs = committee_programs()
    probe = program_freeze_probe("rev1")
    triple = run_episode_triple(cfg, 3, probe, programs, backend=MockIsolate())
    diffs = diff_probe_triple(triple, probe)
    assert "rev2" in diffs
