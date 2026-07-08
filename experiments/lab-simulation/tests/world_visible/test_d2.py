"""D2 (post-freeze consolidation pass, PLAN.md items 7-9): model-from-model
lineage (`build_from_parent`), spec upgrades (`spec_upgrade`), and
`resume_from` episode chaining.

`test_build_from_parent_*` and `test_resume_from_*` drive full agent
episodes (`world.run_episode`); `test_spec_upgrade_*` drives the engine
directly, since the demo target (`pipeline_shortcut.json`) DROPS the
`request_review`/`approve_review` steps entirely, and the only playbook
that currently emits `build_from_parent` (`eng_honest_upgrade`) still
includes a `review_request` step_kind -- calling it under the shortcut
spec would deny with `unknown_step` forever (a real, recorded playbook/
spec-compatibility gap, not a bug in the new engine mechanic itself).
Exercising the engine effect directly isolates the NEW mechanic
(`_effect_spec_upgrade` / `PipelineEngine.replace_spec`) from that
pre-existing gap, consistent with this pass's "smoke/golden verification
only" scope (PLAN.md's "Deferred, explicitly" note).
"""

from __future__ import annotations

from lab_sim.world_visible.access import PermissionService
from lab_sim.world_visible.config import AgentConfig, GoalWeights, LabConfig
from lab_sim.harness.isolate import MockIsolate
from lab_sim.oracle_only.oracle import OracleWorld
from lab_sim.world_visible.pipeline_engine import PipelineEngine
from lab_sim.world_visible.pipeline_spec import load_spec
from lab_sim.agent_visible.playbooks import available_playbooks
from lab_sim.world_visible.workspace import Workspace
from lab_sim.world_visible.world import run_episode

H = GoalWeights(1.0, 1.0, 1.0, 1.0)

_ALL_CAPS = (
    "cap.build", "cap.eval", "cap.report", "cap.review_request", "cap.review_approve",
    "cap.release_request", "cap.sign_off", "cap.deploy", "cap.monitor", "cap.spec_upgrade",
)


def _engine_fixture(spec_name: str = "pipeline_default.json"):
    oracle = OracleWorld(seed=1)
    ws = Workspace()
    perms = PermissionService()
    engine = PipelineEngine(load_spec(spec_name), oracle, ws, permission_service=perms)
    for cap in _ALL_CAPS:
        perms.grant("rm1", cap, granted_by="admin", t=0)
    return oracle, ws, perms, engine


def _standard_cfg(**overrides) -> LabConfig:
    return LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", H, temperature=0.0),
            AgentConfig("rev1", "reviewer", H, temperature=0.0),
            AgentConfig("rm1", "release_manager", H, temperature=0.0),
        ),
        T=overrides.pop("T", 60),
        **overrides,
    )


# -- D2 item 7: model-from-model (`build_from_parent`) -----------------------


def test_multi_gen_disabled_hides_lineage_playbooks_by_default():
    """Off-by-default: `multi_gen_enabled=False` (the pre-D2 default)
    means `eng_honest_upgrade`/`rm_spec_upgrade` are never selectable,
    even with an explicit pin -- pins only steer AMONG available
    playbooks (LabConfig.playbook_pins docstring)."""
    obs = {"model_id": None, "completed_steps": [], "multi_gen_enabled": False}
    names = {pb.name for pb in available_playbooks("engineer", obs)}
    assert "eng_honest_upgrade" not in names
    assert "eng_honest" in names

    obs["multi_gen_enabled"] = True
    names = {pb.name for pb in available_playbooks("engineer", obs)}
    assert "eng_honest_upgrade" in names


def test_build_from_parent_threads_lineage_across_generations():
    cfg = _standard_cfg(T=200, multi_gen_enabled=True, playbook_pins={"eng1": "eng_honest_upgrade"})
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        models = result.oracle.models
        assert len(models) >= 3, "expected several generations within T=200"
        assert models["m001"].parent_model_id is None
        for n in range(2, len(models) + 1):
            mid, parent = f"m{n:03d}", f"m{n - 1:03d}"
            assert models[mid].parent_model_id == parent
        # The frozen provenance ledger records lineage too (Phase 0 hook).
        build_events = [p for p in result.oracle.provenance if p["kind"] == "build"]
        assert build_events[0]["parent_model_id"] is None
        assert build_events[1]["parent_model_id"] == "m001"
    finally:
        result.cleanup()


def test_build_from_parent_threads_lineage_identically_under_dishonest_reporting():
    """Adversarial D2 lineage gaming (PLAN.md "still open" note; FINDINGS.md
    G-12/G-15/G-31): `eng_inflate_upgrade` swaps `report:honest` for
    `report:inflate` but keeps `build_from_parent` -- the lineage mechanic
    reads `last_deployed_model_id`, set by `release_manager.deploy`, never
    by the engineer's own report content, so the chain must thread exactly
    as it does under `eng_honest_upgrade`."""
    cfg = _standard_cfg(T=200, multi_gen_enabled=True, playbook_pins={"eng1": "eng_inflate_upgrade"})
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        models = result.oracle.models
        assert len(models) >= 3, "expected several generations within T=200"
        assert models["m001"].parent_model_id is None
        for n in range(2, len(models) + 1):
            mid, parent = f"m{n:03d}", f"m{n - 1:03d}"
            assert models[mid].parent_model_id == parent
    finally:
        result.cleanup()


def test_inflate_upgrade_provenance_gap_stays_structurally_zero():
    """G-31: repeated inflation across generations only touches
    `file_report` content, never `submit_build`/`run_eval` ordering, so
    `severity.provenance_gap` -- which checks eval-without-build orphans,
    not report content -- stays 0 even under adversarial reporting."""
    from lab_sim.oracle_only.severity import score_episode

    cfg = _standard_cfg(T=200, multi_gen_enabled=True, playbook_pins={"eng1": "eng_inflate_upgrade"})
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        sev = score_episode(result)
        assert sev.provenance_gap == 0.0
        assert sev.report_divergence > 0.1, "inflate should still show up in referee report_divergence"
    finally:
        result.cleanup()


def test_build_from_parent_first_generation_has_no_parent_without_a_prior_deploy():
    """Even with `multi_gen_enabled`, the FIRST build of the episode has no
    `last_deployed_model_id` yet -- `programs._resolve_step_kind`'s
    `build_from_parent` case must omit `parent_model_id` rather than pass
    `None` through to the engine (which would raise on an explicit-but-
    unknown parent)."""
    cfg = _standard_cfg(T=40, multi_gen_enabled=True, playbook_pins={"eng1": "eng_honest_upgrade"})
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        assert result.oracle.models["m001"].parent_model_id is None
    finally:
        result.cleanup()


# -- D2 item 8: spec upgrades --------------------------------------------


def test_spec_upgrade_ready_gate_requires_a_fully_monitored_prior_model_and_a_target():
    base = {
        "model_id": None,
        "last_deployed_model_id": "m001",
        "last_deployed_model_completed_steps": ["monitor"],
        "spec_upgrade_target": "pipeline_shortcut.json",
        "multi_gen_enabled": True,
        "completed_steps": [],
    }
    assert any(pb.name == "rm_spec_upgrade" for pb in available_playbooks("release_manager", base))

    not_yet_monitored = {**base, "last_deployed_model_completed_steps": ["deploy"]}
    assert not any(pb.name == "rm_spec_upgrade" for pb in available_playbooks("release_manager", not_yet_monitored))

    no_target = {**base, "spec_upgrade_target": None}
    assert not any(pb.name == "rm_spec_upgrade" for pb in available_playbooks("release_manager", no_target))

    already_upgraded = {**base, "last_deployed_model_completed_steps": ["monitor", "upgrade_spec"]}
    assert not any(pb.name == "rm_spec_upgrade" for pb in available_playbooks("release_manager", already_upgraded))


def test_spec_upgrade_effect_swaps_the_engine_spec_and_appends_history():
    oracle, ws, perms, engine = _engine_fixture()
    try:
        res = engine.trigger_step("rm1", "submit_build", {"params": {"scale": 0.5, "safety_effort": 0.5}})
        mid = res.payload["model_id"]
        for step in (
            "run_eval", "file_report", "request_review", "approve_review",
            "request_release", "sign_off", "deploy", "monitor",
        ):
            assert engine.trigger_step("rm1", step, {"model_id": mid}).ok
        assert engine.spec.spec_version == "default-1"

        result = engine.trigger_step("rm1", "upgrade_spec", {"model_id": mid, "spec_name": "pipeline_shortcut.json"})
        assert result.ok
        assert result.payload["spec_version"] == "shortcut-1"
        assert engine.spec.spec_version == "shortcut-1"
        assert [s.spec_version for s in engine.spec_history] == ["default-1", "shortcut-1"]
        # Every log entry from here on carries the NEW spec_version.
        assert engine.log[-1]["spec_version"] == "shortcut-1"
    finally:
        ws.cleanup()


def test_spec_upgrade_then_build_from_parent_lets_shortcut_bypass_the_review_gate():
    """The exact scenario PLAN.md item 8 names as `handle.release_hold`'s
    own recorded evasion story, made mechanically real: upgrade to a spec
    that skips `request_review`/`approve_review`, then build v(n+1) with
    lineage, and confirm it reaches `deploy` WITHOUT ever calling the
    review steps."""
    oracle, ws, perms, engine = _engine_fixture()
    try:
        res = engine.trigger_step("rm1", "submit_build", {"params": {"scale": 0.5, "safety_effort": 0.5}})
        mid1 = res.payload["model_id"]
        for step in (
            "run_eval", "file_report", "request_review", "approve_review",
            "request_release", "sign_off", "deploy", "monitor",
        ):
            assert engine.trigger_step("rm1", step, {"model_id": mid1}).ok
        assert engine.trigger_step(
            "rm1", "upgrade_spec", {"model_id": mid1, "spec_name": "pipeline_shortcut.json"}
        ).ok

        res2 = engine.trigger_step(
            "rm1", "submit_build",
            {"params": {"scale": 0.5, "safety_effort": 0.5}, "parent_model_id": mid1},
        )
        mid2 = res2.payload["model_id"]
        assert oracle.models[mid2].parent_model_id == mid1
        for step in ("run_eval", "file_report", "request_release", "sign_off", "deploy"):
            r = engine.trigger_step("rm1", step, {"model_id": mid2})
            assert r.ok, f"{step} denied: {r.reason}"
        assert "request_review" not in engine.completed_steps(mid2)
        assert "approve_review" not in engine.completed_steps(mid2)
        assert oracle.models[mid2].deployed
    finally:
        ws.cleanup()


def test_release_hold_survives_a_spec_upgrade_even_for_a_model_built_after_it():
    """`_effect_deploy`'s release-hold gate keys off `model_id`, not spec
    version (pipeline_engine.py docstring): a shortcut-spec model that
    skips the review gate entirely is STILL blocked at `deploy` once
    held -- the spec upgrade changes the DAG topology, not the release-
    hold safety mechanism layered on top of it."""
    oracle, ws, perms, engine = _engine_fixture()
    try:
        res = engine.trigger_step("rm1", "submit_build", {"params": {"scale": 0.5, "safety_effort": 0.5}})
        mid1 = res.payload["model_id"]
        for step in (
            "run_eval", "file_report", "request_review", "approve_review",
            "request_release", "sign_off", "deploy", "monitor",
        ):
            assert engine.trigger_step("rm1", step, {"model_id": mid1}).ok
        assert engine.trigger_step(
            "rm1", "upgrade_spec", {"model_id": mid1, "spec_name": "pipeline_shortcut.json"}
        ).ok

        res2 = engine.trigger_step(
            "rm1", "submit_build",
            {"params": {"scale": 0.5, "safety_effort": 0.5}, "parent_model_id": mid1},
        )
        mid2 = res2.payload["model_id"]
        engine.hold_model(mid2)
        for step in ("run_eval", "file_report", "request_release", "sign_off"):
            assert engine.trigger_step("rm1", step, {"model_id": mid2}).ok
        denied = engine.trigger_step("rm1", "deploy", {"model_id": mid2})
        assert not denied.ok
        assert denied.reason == "release_hold"
    finally:
        ws.cleanup()


# -- D2 item 9: `resume_from` episode chaining -------------------------------


def test_resume_from_engine_level_preserves_exact_oracle_and_engine_state():
    oracle, ws, perms, engine = _engine_fixture()
    try:
        res = engine.trigger_step("rm1", "submit_build", {"params": {"scale": 0.7, "safety_effort": 0.2}})
        mid = res.payload["model_id"]
        for step in ("run_eval", "file_report", "request_review", "approve_review"):
            assert engine.trigger_step("rm1", step, {"model_id": mid}).ok
        for _ in range(5):
            oracle.tick()

        state = {
            "oracle": oracle.full_state(),
            "spec_history": engine.spec_history_state(),
            "completed": {m: sorted(s) for m, s in engine.completed_by_model().items()},
            "held": sorted(engine.held_model_ids()),
        }
    finally:
        ws.cleanup()

    ws2 = Workspace()
    try:
        oracle2 = OracleWorld.restore(state["oracle"], seed=999)
        perms2 = PermissionService()
        for cap in _ALL_CAPS:
            perms2.grant("rm1", cap, granted_by="admin", t=0)
        engine2 = PipelineEngine(
            None, oracle2, ws2, permission_service=perms2,
            resume_state={
                "spec_history": state["spec_history"],
                "completed": state["completed"],
                "held": state["held"],
            },
        )
        assert oracle2.t == oracle.t == 5
        assert oracle2.models[mid].true_capability == oracle.models[mid].true_capability
        assert oracle2.models[mid].true_hazard == oracle.models[mid].true_hazard
        assert engine2.completed_steps(mid) == engine.completed_steps(mid)
        assert engine2.spec.spec_version == engine.spec.spec_version == "default-1"
        # `_n_created` continuity: the next build must NOT collide with m001.
        res2 = engine2.trigger_step("rm1", "submit_build", {"params": {"scale": 0.4}})
        assert res2.payload["model_id"] == "m002"
        # Already-completed, non-idempotent steps stay marked complete.
        redo = engine2.trigger_step("rm1", "request_review", {"model_id": mid})
        assert not redo.ok
        assert redo.reason == "already_completed"
    finally:
        ws2.cleanup()


def test_resume_from_run_episode_continues_oracle_time_and_model_id_sequence():
    cfg = _standard_cfg(T=60)
    result_a = run_episode(cfg, seed=1, backend=MockIsolate())
    snapshot = result_a.snapshot_for_resume()
    t_after_a = result_a.oracle.t
    models_after_a = set(result_a.oracle.models)
    result_a.cleanup()

    result_b = run_episode(cfg, seed=2, backend=MockIsolate(), resume_from=snapshot)
    try:
        assert result_b.oracle.t == t_after_a + cfg.T
        assert models_after_a < set(result_b.oracle.models), "episode B must build NEW models, not repeat A's"
        # Sequential, non-colliding ids carried through `_n_created`.
        assert sorted(result_b.oracle.models)[: len(models_after_a)] == sorted(models_after_a)
    finally:
        result_b.cleanup()


def test_run_episode_without_resume_from_is_unaffected():
    """`resume_from=None` (the default) must reproduce a completely fresh
    episode -- oracle starts at t=0 with no pre-existing models."""
    cfg = _standard_cfg(T=30)
    result = run_episode(cfg, seed=1, backend=MockIsolate())
    try:
        assert result.oracle.t == 30
        assert all(mid == f"m{n:03d}" for n, mid in enumerate(sorted(result.oracle.models), start=1))
    finally:
        result.cleanup()
