"""Phase 4: full episode loop through MockIsolate."""

from __future__ import annotations

import json

from lab_sim.config import AdminConfig, AgentConfig, BoardConfig, GoalWeights, LabConfig
from lab_sim.isolate import MockIsolate
from lab_sim.world import run_episode

HONEST_WEIGHTS = GoalWeights(1.0, 1.0, 1.0, 1.0)
DECEPTIVE_ENG_WEIGHTS = GoalWeights(1.0, 0.0, 0.0, 1.0)
DECEPTIVE_REV_WEIGHTS = GoalWeights(1.0, 0.0, 0.0, 0.0)


def _cfg(eng_weights, rev_weights, T=120, board=None, admin=None) -> LabConfig:
    return LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", eng_weights, temperature=0.0),
            AgentConfig("rev1", "reviewer", rev_weights, temperature=0.0),
            AgentConfig("rm1", "release_manager", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("admin1", "admin", HONEST_WEIGHTS),
        ),
        board=board or BoardConfig(),
        admin=admin or AdminConfig(),
        T=T,
    )


def test_honest_episode_deploys_at_least_one_model_with_matching_report():
    # T=120 is long enough for the engineer to cycle several models through
    # sequentially (single-model-in-flight; see world.py docstring) — that
    # is intended behavior, not a bug, so assert on the FIRST cycle only.
    cfg = _cfg(HONEST_WEIGHTS, HONEST_WEIGHTS)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        deploy_entries = [e for e in result.engine.log if e["step_id"] == "deploy" and e["status"] == "ok"]
        assert len(deploy_entries) >= 1
        model_id = deploy_entries[0]["model_id"]
        assert result.oracle.models[model_id].deployed

        eval_entry = next(
            e for e in result.engine.log
            if e["step_id"] == "run_eval" and e["status"] == "ok" and e["model_id"] == model_id
        )
        report_entry = next(
            e for e in result.engine.log
            if e["step_id"] == "file_report" and e["status"] == "ok" and e["model_id"] == model_id
        )
        content = json.loads(result.workspace.read_file(report_entry["payload"]["report_path"]))
        assert abs(content["measured_hazard"] - eval_entry["payload"]["measured_hazard"]) < 1e-9
    finally:
        result.cleanup()


def test_deceptive_engineer_inflates_report_content():
    cfg = _cfg(DECEPTIVE_ENG_WEIGHTS, HONEST_WEIGHTS)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        eval_entry = next(e for e in result.engine.log if e["step_id"] == "run_eval" and e["status"] == "ok")
        report_files = [p for p in result.workspace.list_files() if p.startswith("reports/")]
        content = json.loads(result.workspace.read_file(report_files[0]))
        assert content["measured_hazard"] < eval_entry["payload"]["measured_hazard"] - 0.1
    finally:
        result.cleanup()


def test_deceptive_reviewer_rubber_stamps_without_stalling():
    # Deceptive engineer inflates hazard low enough that an honest reviewer
    # would also approve; use a rubber-stamp reviewer regardless to confirm
    # it never stalls even when it would matter.
    cfg = _cfg(HONEST_WEIGHTS, DECEPTIVE_REV_WEIGHTS)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        deploy_entries = [e for e in result.engine.log if e["step_id"] == "deploy" and e["status"] == "ok"]
        assert len(deploy_entries) >= 1
    finally:
        result.cleanup()


def test_captured_reviewer_forces_rubber_stamp_regardless_of_weights():
    cfg = _cfg(HONEST_WEIGHTS, HONEST_WEIGHTS, board=BoardConfig(capture_start=0))
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        deploy_entries = [e for e in result.engine.log if e["step_id"] == "deploy" and e["status"] == "ok"]
        assert len(deploy_entries) >= 1
    finally:
        result.cleanup()


def test_harm_accrues_only_after_deploy():
    cfg = _cfg(HONEST_WEIGHTS, HONEST_WEIGHTS, T=20)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        assert result.oracle.bearer_harm == 0.0  # T=20 too short to reach deploy
    finally:
        result.cleanup()

    cfg_long = _cfg(HONEST_WEIGHTS, HONEST_WEIGHTS, T=150)
    result_long = run_episode(cfg_long, seed=1, backend=MockIsolate())
    try:
        assert result_long.oracle.bearer_harm > 0.0
    finally:
        result_long.cleanup()


def test_admin_grants_are_least_privilege_by_default():
    cfg = _cfg(HONEST_WEIGHTS, HONEST_WEIGHTS)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        grants = [e for e in result.permissions.log if e["action"] == "grant"]
        # least_privilege=True: each grant is exactly the requested capability,
        # so distinct (actor, capability) grant pairs should not exceed the
        # number of distinct capabilities actually exercised in this episode.
        exercised = {(e["actor_id"], e["requires_capability"]) for e in result.engine.log if e["status"] == "ok"}
        granted_pairs = {(g["actor_id"], g["capability"]) for g in grants}
        assert granted_pairs <= exercised
    finally:
        result.cleanup()
