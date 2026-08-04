"""PLAN_v3 slice D — causal C2-v3 ablation gate (GL-59, engineering-only)."""

from __future__ import annotations

from pathlib import Path

import pytest

from graded_lab.harness.c2_v3_causal_gate import (
    evaluate_c2_v3_causal_gate,
    pick_c2_v3_ablation_flow_id,
    resolve_c2_v3_causal_gate_spec,
    seed_diverged,
    _episode_cfg,
)
from graded_lab.harness.isolate import MockIsolate
from graded_lab.oracle_only.calibration import WEAK_AGENT, programs_for
from graded_lab.world_visible.substrate import load_substrate
from graded_lab.world_visible.world import run_episode

_INTEGRATED = Path("tests/fixtures/ecology_v3_slice_a_reference.json")
_ENGINEER_ALT = Path("tests/fixtures/ecology_v3_c2_v3_causal_engineer_alt.json")
_CAUSAL_FIXTURES = (_INTEGRATED, _ENGINEER_ALT)


@pytest.mark.parametrize("path", _CAUSAL_FIXTURES)
def test_pick_c2_v3_ablation_flow_matches_frozen_metadata(path: Path):
    if not path.exists():
        pytest.skip(f"missing fixture {path}")
    data = load_substrate(path).data
    spec = resolve_c2_v3_causal_gate_spec(data)
    assert spec is not None
    picked = pick_c2_v3_ablation_flow_id(data, role=spec.focal_role)
    assert picked == spec.ablation_flow_id


@pytest.mark.slow
@pytest.mark.parametrize("path", _CAUSAL_FIXTURES)
def test_c2_v3_causal_gate_pre_registered(path: Path):
    if not path.exists():
        pytest.skip(f"missing fixture {path}")
    passed, details = evaluate_c2_v3_causal_gate(path)
    assert passed, details


@pytest.mark.slow
@pytest.mark.parametrize("path", _CAUSAL_FIXTURES)
def test_c2_v3_causal_gate_negative_control_at_default_load(path: Path):
    """At carrier_load_scale=0.0 the same ablation must not diverge on every seed."""
    if not path.exists():
        pytest.skip(f"missing fixture {path}")
    data = load_substrate(path).data
    spec = resolve_c2_v3_causal_gate_spec(data)
    assert spec is not None
    programs = programs_for(WEAK_AGENT)
    backend = MockIsolate()
    passing = 0
    for seed in spec.seeds:
        full = run_episode(
            _episode_cfg(path, spec=spec, ablate=False, load_scale=0.0),
            seed,
            backend,
            programs=programs,
        )
        ablated = run_episode(
            _episode_cfg(path, spec=spec, ablate=True, load_scale=0.0),
            seed,
            backend,
            programs=programs,
        )
        if seed_diverged(full=full, ablated=ablated, spec=spec):
            passing += 1
    assert passing < len(spec.seeds), (
        "negative control failed: ablation diverges on every seed at load 0.0"
    )


@pytest.mark.skipif(not _INTEGRATED.exists(), reason="integrated reference missing")
def test_c2_v3_accounting_passes_while_causal_gate_is_separate():
    """Accounting C2-v3 and causal gate are distinct checks."""
    from graded_lab.harness.ecology_complexity import check_c2_v3

    data = load_substrate(_INTEGRATED).data
    passed, failing, _ = check_c2_v3(data)
    assert passed, failing
    spec = resolve_c2_v3_causal_gate_spec(data)
    assert spec is not None
    assert spec.ablation_flow_id == "flow_eng_lab_operator_compute"
