"""Phase 4: full-episode regression digest, pinned on the SubprocessIsolate
backend (what real batteries use), cross-checked against MockIsolate via
the same equivalence discipline as Phase 3's isolate harness."""

from __future__ import annotations

from lab_sim.config import AdminConfig, AgentConfig, BoardConfig, GoalWeights, LabConfig
from lab_sim.isolate import MockIsolate, SubprocessIsolate
from lab_sim.world import episode_digest, run_episode

# Deliberately favors inflate/rubber-stamp at temperature=0 (see test_world.py)
# so the regression run exercises the deception + access-request paths too.
_CFG = LabConfig(
    agents=(
        AgentConfig("eng1", "engineer", GoalWeights(1.0, 0.0, 0.0, 1.0), temperature=0.0),
        AgentConfig("rev1", "reviewer", GoalWeights(1.0, 1.0, 1.0, 1.0), temperature=0.0),
        AgentConfig("rm1", "release_manager", GoalWeights(1.0, 1.0, 1.0, 1.0), temperature=0.0),
        AgentConfig("admin1", "admin", GoalWeights(1.0, 1.0, 1.0, 1.0)),
    ),
    board=BoardConfig(),
    admin=AdminConfig(),
    T=60,
)

# Regenerate by running the suite once and copying the printed "actual" value
# from the assertion failure — see DESIGN.md "Recorded measurements".
# Re-pinned at CODE_VERSION 0.3.0 (tool-event args elision + args_digest,
# handles wiring). Previous pins:
# 0.1.0: 28fbcc3cd8831fd55fcb6b0b72ea4ff403d52c30db96dfb3d53e94ef5bb8f796
# 0.2.0: 5e8146430befc80f94d3f9e6106a4c65700829e826131787bfa39a64d8477bbd
PINNED_DIGEST = "960088266512778adca7ec63770e7d067fa94760eb8e04fa888fb6861b2325ce"


def test_mock_and_subprocess_world_backends_agree():
    mock_result = run_episode(_CFG, seed=7, backend=MockIsolate())
    try:
        mock_digest = episode_digest(mock_result)
    finally:
        mock_result.cleanup()

    sub_result = run_episode(_CFG, seed=7, backend=SubprocessIsolate())
    try:
        sub_digest = episode_digest(sub_result)
    finally:
        sub_result.cleanup()

    assert mock_digest == sub_digest


def test_pinned_regression_digest():
    result = run_episode(_CFG, seed=7, backend=SubprocessIsolate())
    try:
        digest = episode_digest(result)
    finally:
        result.cleanup()
    assert digest["combined"] == PINNED_DIGEST, f"actual={digest['combined']}"
