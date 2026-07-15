"""PLAN_v3 slice A pre-registered ablation gate."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from dataclasses import replace

import pytest

from graded_lab.agent_visible.behavior_features import classify_primitive
from graded_lab.harness.isolate import MockIsolate
from graded_lab.oracle_only.calibration import WEAK_AGENT, programs_for
from graded_lab.world_visible.config import EpisodeConfig
from graded_lab.world_visible.ecology_agents import build_agents_from_ecology
from graded_lab.world_visible.substrate import load_substrate
from graded_lab.world_visible.world import default_lab_config, run_episode

_FIXTURE = Path("tests/fixtures/ecology_v3_slice_a_reference.json")


def _histogram_l1(a: Counter[str], b: Counter[str]) -> float:
    keys = set(a) | set(b)
    if not keys:
        return 0.0
    total_a = sum(a.values()) or 1
    total_b = sum(b.values()) or 1
    return sum(abs(a.get(k, 0) / total_a - b.get(k, 0) / total_b) for k in keys)


def _eng1_pattern_hist(result) -> Counter[str]:
    counts: Counter[str] = Counter()
    for entry in result.primitive_log:
        if entry.get("actor_id") != "eng1":
            continue
        prim = entry.get("primitive")
        if isinstance(prim, dict):
            counts[classify_primitive(prim)] += 1
    return counts


def _episode_cfg(*, ablate: bool) -> EpisodeConfig:
    data = load_substrate(_FIXTURE).data
    meta = data["v3_fixture_metadata"]
    gate = meta["ablation_gate"]
    base = default_lab_config()
    ablation = (meta["ablation_target_flow_id"],) if ablate else ()
    load_scale = float(gate.get("carrier_load_scale", 0.0))
    settings = replace(base.substrate_settings, carrier_load_scale=load_scale)
    return EpisodeConfig(
        agents=build_agents_from_ecology(data, temperature=0.35),
        T=base.T,
        pipeline_spec=base.pipeline_spec,
        substrate_settings=settings,
        carrier_termination_mode=base.carrier_termination_mode,
        units=base.units,
        ecology_version="v3",
        ecology_override_path=_FIXTURE,
        flow_ablation_ids=ablation,
    )


@pytest.mark.slow
def test_slice_a_ablation_gate_pre_registered():
    if not _FIXTURE.exists():
        pytest.skip("slice A reference fixture missing")
    meta = load_substrate(_FIXTURE).data["v3_fixture_metadata"]
    gate = meta["ablation_gate"]
    seeds = gate["seeds"]
    threshold = gate["histogram_l1_threshold"]
    min_pass = gate["min_seeds_passing"]
    programs = programs_for(WEAK_AGENT)
    backend = MockIsolate()
    passing = 0
    for seed in seeds:
        full = run_episode(_episode_cfg(ablate=False), seed, backend, programs=programs)
        ablated = run_episode(_episode_cfg(ablate=True), seed, backend, programs=programs)
        deploy_diff = full.deploy_count != ablated.deploy_count
        hist_diff = _histogram_l1(
            _eng1_pattern_hist(full), _eng1_pattern_hist(ablated)
        ) >= threshold
        if deploy_diff or hist_diff:
            passing += 1
    assert passing >= min_pass, (
        f"ablation gate: {passing}/{len(seeds)} seeds showed behavioral divergence "
        f"(need >={min_pass})"
    )
