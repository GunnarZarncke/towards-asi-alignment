"""ET-3 adapter unit tests (fixture → deterministic cell dicts)."""

from __future__ import annotations

from pathlib import Path

import pytest

from lab_sim.external.ai2027_adapter import (
    ET3_PROTOCOL_VERSION,
    apply_d3_episode_t,
    d3_overrides_for_cell,
    get_stress_cell,
    list_cell_ids,
    load_stress_cells,
    sample_phase6_configs,
)
from lab_sim.harness import protocol
from lab_sim.harness.d3_population import sample_initial_population
from lab_sim.harness.isolate import MockIsolate
from lab_sim.harness.d3_population import run_population_loop


def test_load_stress_cells_matches_fixture():
    cells = load_stress_cells()
    assert set(cells) == {"baseline", "sc_x5", "sar_x25"}
    assert cells["sc_x5"].d3_selection_strength == pytest.approx(5.0)
    assert cells["sc_x5"].d3_episode_t == 20
    assert cells["sar_x25"].d3_selection_strength == pytest.approx(25.0)


def test_list_cell_ids_order():
    assert list_cell_ids() == ("baseline", "sc_x5", "sar_x25")


def test_baseline_phase6_matches_protocol_sampling():
    d1, h1 = sample_phase6_configs("baseline", n_discovery=4, n_held_out=2)
    d2, h2 = protocol.sample_configs(seed=protocol.SAMPLING_SEED, n_discovery=4, n_held_out=2)
    assert [c.agents[0].weights for c in d1] == [c.agents[0].weights for c in d2]
    assert [c.agents[0].weights for c in h1] == [c.agents[0].weights for c in h2]


def test_sc_x5_phase6_engineer_band():
    discovery, held_out = sample_phase6_configs("sc_x5", n_discovery=6, n_held_out=3)
    cell = get_stress_cell("sc_x5")
    for cfg in discovery + held_out:
        eng = cfg.agents[0].weights.normalized()
        assert eng.task >= cell.phase6_engineer_task_min
        assert eng.compliance <= cell.phase6_engineer_compliance_max


def test_d3_overrides_for_cells():
    assert d3_overrides_for_cell("baseline") == {"selection_strength": 1.0, "episode_t": 100}
    assert d3_overrides_for_cell("sc_x5")["selection_strength"] == pytest.approx(5.0)
    assert d3_overrides_for_cell("sar_x25")["episode_t"] == 4


def test_apply_d3_episode_t():
    configs = sample_initial_population(population_size=2)
    shortened = apply_d3_episode_t(configs, 20)
    assert all(c.T == 20 for c in shortened)
    assert shortened[0].pipeline_spec == configs[0].pipeline_spec


def test_et3_smoke_d3_baseline_vs_sc_x5():
    """Plumbing: one generation, two cells, MockIsolate."""
    for cell_id in ("baseline", "sc_x5"):
        overrides = d3_overrides_for_cell(cell_id)
        configs = apply_d3_episode_t(sample_initial_population(population_size=3), overrides["episode_t"])
        traj = run_population_loop(
            configs,
            n_generations=1,
            n_episodes_per_member=1,
            backend_factory=MockIsolate,
            selection_strength=overrides["selection_strength"],
        )
        assert len(traj.generations) == 1
        assert 0.0 <= traj.generations[0].correction_preserving_mass_share <= 1.0


def test_fixture_declares_protocol_version(tmp_path: Path):
    fixture = tmp_path / "sched.yaml"
    fixture.write_text(
        "et3_protocol_version: et3-0.1.0\ncells:\n  baseline:\n    ai2027_cue: test\n"
        "    d3_selection_strength: 1.0\n    d3_episode_t: 100\n"
        "    phase6_engineer_task_min: 0.0\n    phase6_engineer_compliance_max: 1.0\n",
        encoding="utf-8",
    )
    cell = get_stress_cell("baseline", path=fixture)
    assert cell.cell_id == "baseline"
