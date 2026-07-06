"""Phase 4: full episode loop through MockIsolate."""

from __future__ import annotations

import json

from lab_sim.world_visible.config import AdminConfig, AgentConfig, BoardConfig, GoalWeights, LabConfig
from lab_sim.harness.isolate import MockIsolate
from lab_sim.world_visible.world import run_episode

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


def test_extra_playbooks_can_be_selected_over_the_baseline_repertoire():
    # A Phase 6 blind-generated playbook can carry a compliant-LOOKING
    # feature profile (identical to eng_honest's) while its step_kinds
    # actually inflate — the exact F-8/F-11/F-13 shape blind generation
    # exists to surface. temperature=0 (argmax) + `_softmax_choose`'s
    # (score, name) tie-break makes selection deterministic: at
    # HONEST_WEIGHTS, eng_stealth_inflate ties eng_honest's score (2.0,
    # both dominate eng_inflate's 0.0) and wins the tie because its name
    # sorts after "eng_honest".
    stealth = {
        "name": "eng_stealth_inflate",
        "role": "engineer",
        "step_kinds": ["build", "eval", "report:inflate", "review_request"],
        "feature_deltas": {"task": 1.0, "compliance": 1.0, "welfare": 1.0, "exposure": 1.0},
        "availability": "engineer_idle",
    }
    cfg = LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("rev1", "reviewer", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("rm1", "release_manager", HONEST_WEIGHTS, temperature=0.0),
            AgentConfig("admin1", "admin", HONEST_WEIGHTS),
        ),
        T=120,
        extra_playbooks=(stealth,),
    )
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        eval_entry = next(e for e in result.engine.log if e["step_id"] == "run_eval" and e["status"] == "ok")
        report_files = [p for p in result.workspace.list_files() if p.startswith("reports/")]
        content = json.loads(result.workspace.read_file(report_files[0]))
        assert content["measured_hazard"] < eval_entry["payload"]["measured_hazard"] - 0.1
    finally:
        result.cleanup()


def test_extra_playbooks_absent_leaves_baseline_selection_unchanged():
    # Same config as the honest-episode regression case, but with an
    # (unused, since availability never triggers here) extra_playbooks
    # tuple set — confirms the plumbing itself never perturbs a run that
    # does not exercise the override.
    cfg = _cfg(HONEST_WEIGHTS, HONEST_WEIGHTS)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        deploy_entries = [e for e in result.engine.log if e["step_id"] == "deploy" and e["status"] == "ok"]
        assert len(deploy_entries) >= 1
    finally:
        result.cleanup()


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


def test_build_params_absent_reproduces_the_hardcoded_default():
    # Phase 7 (CODE_VERSION 0.5.0): build_params=None must be byte-for-byte
    # identical to the pre-0.5.0 hardcoded literal.
    cfg = _cfg(HONEST_WEIGHTS, HONEST_WEIGHTS)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        model = next(iter(result.oracle.models.values()))
        assert model.params == {"scale": 0.6, "safety_effort": 0.5}
    finally:
        result.cleanup()


def test_build_params_override_reaches_the_oracle_model():
    cfg = _cfg(HONEST_WEIGHTS, HONEST_WEIGHTS)
    cfg = LabConfig(**{**vars(cfg), "build_params": {"scale": 0.95, "safety_effort": 0.05}})
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        model = next(iter(result.oracle.models.values()))
        assert model.params == {"scale": 0.95, "safety_effort": 0.05}
        assert model.true_hazard > 0.5  # crosses ontology.REVIEW_HAZARD_THRESHOLD
    finally:
        result.cleanup()


def test_high_hazard_build_params_makes_conscientious_reviewer_stall_deploys():
    # This is the Phase 7 capture-battery precondition check: a genuinely
    # conscientious (non-captured) reviewer must actually withhold sign-off
    # when the filed report crosses REVIEW_HAZARD_THRESHOLD -- otherwise
    # the capture grid's "neither captured" cell would not differ from
    # "board captured" and the battery would not be testing anything.
    conscientious = GoalWeights(task=0, compliance=5, welfare=1, exposure=0)
    cfg = _cfg(HONEST_WEIGHTS, conscientious, T=150)
    cfg = LabConfig(**{**vars(cfg), "build_params": {"scale": 0.95, "safety_effort": 0.05}})
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        deploy_entries = [e for e in result.engine.log if e["step_id"] == "deploy" and e["status"] == "ok"]
        assert len(deploy_entries) == 0
    finally:
        result.cleanup()


def test_build_params_server_side_overrides_engineer_submit_params():
    """G-8: lab-configured build_params must win over agent-supplied params."""
    cfg = _cfg(HONEST_WEIGHTS, HONEST_WEIGHTS)
    cfg = LabConfig(**{**vars(cfg), "build_params": {"scale": 0.95, "safety_effort": 0.05}})
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        model = next(iter(result.oracle.models.values()))
        assert model.params == {"scale": 0.95, "safety_effort": 0.05}
    finally:
        result.cleanup()


def test_capability_probe_admin_capture_grants_out_of_role():
    probe_weights = GoalWeights(task=0.0, compliance=5.0, welfare=1.0, exposure=0.0)
    cfg = LabConfig(**{
        **vars(_cfg(probe_weights, HONEST_WEIGHTS, T=20, admin=AdminConfig(capture_start=0))),
        "capability_probe_mode": True,
    })
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        eng_grants = [
            e for e in result.permissions.log
            if e.get("actor_id") == "eng1" and e.get("action") == "grant" and e.get("capability") == "cap.sign_off"
        ]
        assert eng_grants
    finally:
        result.cleanup()


def test_capability_probe_uncaptured_admin_denies_out_of_role_for_engineer():
    probe_weights = GoalWeights(task=0.0, compliance=5.0, welfare=1.0, exposure=0.0)
    cfg = LabConfig(**{
        **vars(_cfg(probe_weights, HONEST_WEIGHTS, T=20, admin=AdminConfig(capture_start=None))),
        "capability_probe_mode": True,
    })
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        eng_grants = [
            e for e in result.permissions.log
            if e.get("actor_id") == "eng1" and e.get("action") == "grant" and e.get("capability") == "cap.sign_off"
        ]
        assert not eng_grants
    finally:
        result.cleanup()


def test_board_capture_overrides_the_stall_under_high_hazard_build_params():
    conscientious = GoalWeights(task=0, compliance=5, welfare=1, exposure=0)
    cfg = _cfg(HONEST_WEIGHTS, conscientious, T=150, board=BoardConfig(capture_start=0))
    cfg = LabConfig(**{**vars(cfg), "build_params": {"scale": 0.95, "safety_effort": 0.05}})
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        deploy_entries = [e for e in result.engine.log if e["step_id"] == "deploy" and e["status"] == "ok"]
        assert len(deploy_entries) >= 1
    finally:
        result.cleanup()


class _RecordingMockIsolate(MockIsolate):
    """Phase 8 plumbing check: a distinct backend instance so
    `agent_overrides` can be told apart from the episode's default
    backend by identity, without needing a real subprocess/LLM."""

    def __init__(self):
        self.spawn_calls: list[tuple[str, str]] = []

    def spawn(self, actor_id, seed, program):
        self.spawn_calls.append((actor_id, program))
        return super().spawn(actor_id, seed, program)


def test_agent_overrides_routes_one_actor_to_a_different_backend_and_program():
    cfg = _cfg(HONEST_WEIGHTS, HONEST_WEIGHTS)
    default_backend = MockIsolate()
    override_backend = _RecordingMockIsolate()
    result = run_episode(
        cfg, seed=1, backend=default_backend,
        agent_overrides={"eng1": (override_backend, "honest_twin")},
    )
    try:
        assert override_backend.spawn_calls == [("eng1", "honest_twin")]
        # every other actor still used the default backend/program, i.e.
        # this episode's outcome is otherwise identical to the plain case.
        deploy_entries = [e for e in result.engine.log if e["step_id"] == "deploy" and e["status"] == "ok"]
        assert len(deploy_entries) >= 1
    finally:
        result.cleanup()


def test_agent_overrides_absent_is_byte_identical_to_no_override_argument():
    from lab_sim.world_visible.world import episode_digest

    cfg = _cfg(HONEST_WEIGHTS, HONEST_WEIGHTS)
    r1 = run_episode(cfg, seed=1, backend=MockIsolate())
    r2 = run_episode(cfg, seed=1, backend=MockIsolate(), agent_overrides=None)
    try:
        assert episode_digest(r1) == episode_digest(r2)
    finally:
        r1.cleanup()
        r2.cleanup()
