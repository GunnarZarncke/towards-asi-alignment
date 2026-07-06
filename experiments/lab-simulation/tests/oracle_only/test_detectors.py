"""Phase 5: tier-gated detectors across all five families."""

from __future__ import annotations

from lab_sim.world_visible.config import AdminConfig, AgentConfig, BoardConfig, GoalWeights, LabConfig
from lab_sim.oracle_only.detectors import (
    access_integrity_score,
    accumulation_score,
    build_audit_view,
    misreporting_score,
    process_noncompliance_score,
    provenance_score,
    run_all_detectors,
)
from lab_sim.harness.isolate import MockIsolate
from lab_sim.world_visible.world import run_episode

HONEST_WEIGHTS = GoalWeights(1.0, 1.0, 1.0, 1.0)
DECEPTIVE_ENG_WEIGHTS = GoalWeights(1.0, 0.0, 0.0, 1.0)


def _cfg(eng_weights, T=200, admin=None) -> LabConfig:
    return LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", eng_weights, temperature=0.0),
            AgentConfig("rev1", "reviewer", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("rm1", "release_manager", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("admin1", "admin", HONEST_WEIGHTS),
        ),
        board=BoardConfig(),
        admin=admin or AdminConfig(),
        T=T,
    )


def _run(eng_weights=HONEST_WEIGHTS, T=200, admin=None):
    return run_episode(_cfg(eng_weights, T=T, admin=admin), seed=1, backend=MockIsolate())


def test_none_tier_sees_nothing():
    result = _run()
    try:
        view = build_audit_view(result, "none")
        assert view.engine_log == [] and view.access_log == []
        assert run_all_detectors(view) == {k: 0.0 for k in run_all_detectors(view)}
    finally:
        result.cleanup()


def test_misreporting_blind_below_deep_tier():
    result = _run(eng_weights=DECEPTIVE_ENG_WEIGHTS)
    try:
        for tier in ("light", "full"):
            assert misreporting_score(build_audit_view(result, tier)) == 0.0
    finally:
        result.cleanup()


def test_misreporting_catches_inflate_at_deep_tier():
    result = _run(eng_weights=DECEPTIVE_ENG_WEIGHTS)
    try:
        view = build_audit_view(result, "deep")
        assert misreporting_score(view) > 0.0
    finally:
        result.cleanup()


def test_misreporting_near_zero_for_honest_episode_at_deep_tier():
    result = _run(eng_weights=HONEST_WEIGHTS)
    try:
        view = build_audit_view(result, "deep")
        assert misreporting_score(view) == 0.0
    finally:
        result.cleanup()


def test_accumulation_blind_below_deep_tier():
    result = _run(eng_weights=DECEPTIVE_ENG_WEIGHTS)
    try:
        assert accumulation_score(build_audit_view(result, "full")) == 0.0
    finally:
        result.cleanup()


def test_accumulation_positive_when_deception_repeats():
    # T large enough for multiple models to cycle through with a
    # consistently deceptive engineer.
    result = _run(eng_weights=DECEPTIVE_ENG_WEIGHTS, T=200)
    try:
        view = build_audit_view(result, "deep")
        if len(view.report_contents) >= 2:
            assert accumulation_score(view) > 0.0
    finally:
        result.cleanup()


def test_process_noncompliance_is_bounded():
    result = _run()
    try:
        for tier in ("light", "full", "deep"):
            score = process_noncompliance_score(build_audit_view(result, tier))
            assert 0.0 <= score <= 1.0
    finally:
        result.cleanup()


def test_provenance_score_zero_under_current_dag():
    result = _run()
    try:
        assert provenance_score(build_audit_view(result, "full")) == 0.0
        assert provenance_score(build_audit_view(result, "light")) == 0.0  # tier-gated
    finally:
        result.cleanup()


def test_access_integrity_zero_under_light_tier_regardless():
    result = _run(admin=AdminConfig(least_privilege=False))
    try:
        assert access_integrity_score(build_audit_view(result, "light")) == 0.0
    finally:
        result.cleanup()


def test_access_integrity_positive_under_lazy_admin_at_full_tier():
    # See severity.py test's matching note: creep is only observable before
    # the granted role's first full pipeline cycle completes.
    result = _run(admin=AdminConfig(least_privilege=False), T=10)
    try:
        assert access_integrity_score(build_audit_view(result, "full")) > 0.0
    finally:
        result.cleanup()


def test_access_integrity_zero_under_strict_admin_at_full_tier():
    result = _run(admin=AdminConfig(least_privilege=True))
    try:
        assert access_integrity_score(build_audit_view(result, "full")) == 0.0
    finally:
        result.cleanup()


def test_run_all_detectors_returns_all_five_families():
    result = _run()
    try:
        scores = run_all_detectors(build_audit_view(result, "deep"))
        assert set(scores) == {
            "misreporting", "process_noncompliance", "provenance", "accumulation", "access_integrity",
        }
        assert all(0.0 <= v <= 1.0 for v in scores.values())
    finally:
        result.cleanup()
