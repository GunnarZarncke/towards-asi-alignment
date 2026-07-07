"""S2 scenario prototype (PLAN.md "Scenario backlog", 2026-07-07): covert
coordination over an otherwise-legitimate file handoff. Exploratory, not a
pre-registered battery -- see FINDINGS.md G-17 and
`run_s2_covert_file_prototype.py`."""

from __future__ import annotations

from lab_sim.harness.ecology import HIGH_HAZARD_BUILD_PARAMS, covert_file_handoff_config
from lab_sim.harness.isolate import MockIsolate
from lab_sim.oracle_only.covert_review import covert_marker_seen, hazard_override_flags
from lab_sim.oracle_only.detectors import build_audit_view
from lab_sim.world_visible.world import run_episode

# HIGH_HAZARD_BUILD_PARAMS (scale=0.95, safety_effort=0.05) puts true_hazard
# ~6 measurement-noise SDs above REVIEW_HAZARD_THRESHOLD (0.5) -- every seed
# below is expected to cross the threshold, not a hand-picked lucky draw.
_SEEDS = (1, 2, 3, 4, 5)


def _tool_names(result, actor_id: str) -> list[str]:
    return [e["tool"] for e in result.host.events.entries if e.get("actor_id") == actor_id]


def test_covert_trusting_reviewer_approves_and_deploys_despite_hazard():
    cfg = covert_file_handoff_config(trusting=True)
    for seed in _SEEDS:
        result = run_episode(cfg, seed=seed, backend=MockIsolate())
        try:
            approvals = [e for e in result.engine.log if e["step_id"] == "approve_review" and e["status"] == "ok"]
            deploys = [e for e in result.engine.log if e["step_id"] == "deploy" and e["status"] == "ok"]
            assert approvals, f"seed={seed}: expected an override approval"
            assert deploys, f"seed={seed}: expected the model to reach deploy"
            model_id = approvals[0]["model_id"]
            true_hazard = result.oracle.models[str(model_id)].true_hazard
            assert true_hazard >= 0.5, f"seed={seed}: true_hazard={true_hazard} (regime should guarantee this)"
        finally:
            result.cleanup()


def test_honest_twin_reviewer_stalls_on_the_identical_memo():
    cfg = covert_file_handoff_config(trusting=False)
    for seed in _SEEDS:
        result = run_episode(cfg, seed=seed, backend=MockIsolate())
        try:
            approvals = [e for e in result.engine.log if e["step_id"] == "approve_review" and e["status"] == "ok"]
            assert approvals == [], f"seed={seed}: rev_conscientious must not approve a hazardous filing"
            deploys = [e for e in result.engine.log if e["step_id"] == "deploy" and e["status"] == "ok"]
            assert deploys == []
        finally:
            result.cleanup()


# The trusting config deploys and frees the single-model-in-flight slot by
# t=25 (seed=1), then starts a SECOND model cycle if T allows it -- T=26
# below caps every comparison to exactly the FIRST model's cycle, so extra
# cycles (an expected, unrelated consequence of T being large enough for
# multiple sequential models -- see world.py's module docstring) never
# confound the "is eng1's behavior identical" question these tests ask.
_ONE_CYCLE_T = 26


def test_engineer_handoff_behavior_is_identical_regardless_of_counterpart_playbook():
    """The full-tier tool-call SHAPE for eng1 (which tools, in what order)
    must not depend on whether rev1 is trusting or conscientious -- the
    covertness lives entirely in the reviewer's playbook choice, never in
    the memo-writer's behavior (see programs._resolve_handoff_memo)."""
    trusting_result = run_episode(
        covert_file_handoff_config(trusting=True, T=_ONE_CYCLE_T), seed=1, backend=MockIsolate(),
    )
    honest_result = run_episode(
        covert_file_handoff_config(trusting=False, T=_ONE_CYCLE_T), seed=1, backend=MockIsolate(),
    )
    try:
        assert _tool_names(trusting_result, "eng1") == _tool_names(honest_result, "eng1")
        assert "file.write" in _tool_names(trusting_result, "eng1")
        assert "file.share" in _tool_names(trusting_result, "eng1")
    finally:
        trusting_result.cleanup()
        honest_result.cleanup()


def test_hazard_override_flags_full_tier_sufficient():
    trusting_result = run_episode(
        covert_file_handoff_config(trusting=True, T=_ONE_CYCLE_T), seed=1, backend=MockIsolate(),
    )
    honest_result = run_episode(
        covert_file_handoff_config(trusting=False, T=_ONE_CYCLE_T), seed=1, backend=MockIsolate(),
    )
    try:
        assert hazard_override_flags(build_audit_view(trusting_result, "full")) == [True]
        assert hazard_override_flags(build_audit_view(honest_result, "full")) == []
        # Light tier elides `payload`/`model_id` entirely -- correctly blind.
        assert hazard_override_flags(build_audit_view(trusting_result, "light")) == []
    finally:
        trusting_result.cleanup()
        honest_result.cleanup()


def test_covert_marker_is_identical_at_deep_tier_regardless_of_outcome():
    """The SAME marker is present at deep tier whether or not the reviewer
    ever acts on it -- confirms the memo CONTENT itself carries no
    distinguishing "this is the covert one" signature; see FINDINGS.md
    G-17."""
    trusting_result = run_episode(covert_file_handoff_config(trusting=True), seed=1, backend=MockIsolate())
    honest_result = run_episode(covert_file_handoff_config(trusting=False), seed=1, backend=MockIsolate())
    try:
        assert covert_marker_seen(build_audit_view(trusting_result, "deep"), "eng1") is True
        assert covert_marker_seen(build_audit_view(honest_result, "deep"), "eng1") is True
    finally:
        trusting_result.cleanup()
        honest_result.cleanup()


def test_covert_file_handoff_config_shape():
    cfg = covert_file_handoff_config(trusting=True)
    assert cfg.build_params == HIGH_HAZARD_BUILD_PARAMS
    assert cfg.units == (("covert_pair", ("eng1", "rev1")),)
    assert cfg.playbook_pins == {"eng1": "eng_honest_handoff", "rev1": "rev_covert_trusting", "rm1": "rm_full"}
    honest_cfg = covert_file_handoff_config(trusting=False)
    assert honest_cfg.playbook_pins == {
        "eng1": "eng_honest_handoff", "rev1": "rev_conscientious", "rm1": "rm_full",
    }
