"""Parallel pipeline timestep tests."""

from embedded_sim.pipeline import run_all_mbs


def test_parallel_workers_match_sequential_summary():
    seq = run_all_mbs(seed=7, T=100, substrate="python", isolate_workers=1)
    par = run_all_mbs(seed=7, T=100, substrate="python", isolate_workers=4)
    assert len(seq) == len(par)
    for a, b in zip(seq, par, strict=True):
        assert a.bridge == b.bridge
        assert a.in_sim.cci_status == b.in_sim.cci_status
        assert a.in_sim.safety_decision == b.in_sim.safety_decision
        assert a.outer.false_pass == b.outer.false_pass
