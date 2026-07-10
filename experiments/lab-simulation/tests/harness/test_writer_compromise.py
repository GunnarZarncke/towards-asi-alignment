"""Writer-compromise scenario: unit-level checks for `writer_compromise.py`'s
three tamper modes against a real episode's logs. See
`run_writer_compromise_prototype.py` / `results/FINDINGS.md` G-38 for the
full multi-seed write-up."""

from __future__ import annotations

from lab_sim.harness.isolate import MockIsolate
from lab_sim.harness.writer_compromise import (
    run_writer_compromise_analysis,
    tamper_chained_log,
    tamper_engine_log,
)
from lab_sim.oracle_only.severity import score_episode
from lab_sim.world_visible.config import AgentConfig, GoalWeights, LabConfig
from lab_sim.world_visible.world import run_episode

HONEST = GoalWeights(1.0, 1.0, 1.0, 1.0)


def _episode():
    cfg = LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", HONEST, temperature=0.0),
            AgentConfig("rev1", "reviewer", HONEST, temperature=0.0),
            AgentConfig("rm1", "release_manager", HONEST, temperature=0.0),
            AgentConfig("admin1", "admin", HONEST),
        ),
        T=100,
    )
    return run_episode(cfg, seed=1, backend=MockIsolate())


def test_naive_tamper_is_detected_immediately():
    result = _episode()
    try:
        entries = result.host.events.entries
        assert len(entries) > 5
        r = tamper_chained_log(entries, 2, {"ok": not entries[2]["ok"]}, mode="naive")
        assert r.detected and r.detected_at_index == 2
    finally:
        result.cleanup()


def test_self_consistent_single_entry_tamper_is_caught_one_entry_later():
    result = _episode()
    try:
        entries = result.host.events.entries
        r = tamper_chained_log(entries, 2, {"ok": not entries[2]["ok"]}, mode="self_consistent")
        assert r.detected and r.detected_at_index == 3
    finally:
        result.cleanup()


def test_forward_recomputed_tamper_is_undetectable_by_chain_alone():
    result = _episode()
    try:
        entries = result.host.events.entries
        r = tamper_chained_log(entries, 2, {"ok": not entries[2]["ok"]}, mode="forward_recompute")
        assert not r.detected
    finally:
        result.cleanup()


def test_engine_log_has_no_partial_detection_tripwire():
    result = _episode()
    try:
        entries = result.engine.log
        out = tamper_engine_log(entries, 1, {"status": "denied" if entries[1]["status"] == "ok" else "ok"})
        # A single-entry edit is always invisible to `log_digest()` as
        # long as the writer republishes a consistent digest -- unlike
        # the chained logs, there is no "one entry later" tripwire at all.
        assert out["recomputed_digest_hides_tamper"]
    finally:
        result.cleanup()


def test_oracle_severity_is_unaffected_by_any_log_tamper():
    """P5: severity.score_episode never reads access_log/events/engine_log
    content for its composite -- it has direct oracle access. Tampering
    the LOGS (which is what a compromised writer can do) cannot move the
    referee's own score; it can only fool an audit-tier DETECTOR that
    trusts the (now-corrupted) log as its evidence."""
    result = _episode()
    try:
        sev_before = score_episode(result).composite
        # Tamper the real log objects in place (not just a copy) to prove
        # the referee genuinely never reads them.
        if result.host.events.entries:
            result.host.events.entries[0]["ok"] = not result.host.events.entries[0]["ok"]
        sev_after = score_episode(result).composite
        assert sev_before == sev_after
    finally:
        result.cleanup()


def test_run_writer_compromise_analysis_covers_all_three_streams():
    result = _episode()
    try:
        out = run_writer_compromise_analysis(result, tamper_index=2)
        assert set(out) >= {"access_log", "events", "engine_log", "tamper_index"}
        for log_name in ("access_log", "events"):
            assert out[log_name]["naive"]["detected"]
            assert out[log_name]["self_consistent"]["detected"]
            assert not out[log_name]["forward_recompute"]["detected"]
    finally:
        result.cleanup()
