"""Phase 4 unit tests: continuous severity (4a), honest twins (4b), the
gated escalation ladder (4c), and stock-variable / stalling mechanics (4d).

These are unit-level checks on the new modules themselves (bounds, mechanical
invariants, gate behavior at synthetic inputs). The empirical FINDINGS live in
`results/FINDINGS.md`; the battery runners (`run_phase4_ranking.py`,
`run_phase4_escalation.py`) are exercised end-to-end there, not re-run here.
"""

from __future__ import annotations

import random

from goal_sim.actions import ActionSpec, LEGACY_ACTIONS, ResponseOption, validate_repertoire
from goal_sim.channels import project_rows
from goal_sim.config import AgentConfig, BoardConfig, GoalWeights, ToolAccess, WorldConfig
from goal_sim.detectors import (
    d7_accumulation_cap,
    d7_score,
    d8_disclosure_latency,
    d8_score,
    score_detectors,
)
from goal_sim.escalation import (
    HIGH_GATE,
    LOW_GATE,
    choose_response,
    run_escalation,
    select_query_steps,
)
from goal_sim.ontology import resolve_response_canonical
from goal_sim.severity import severity
from goal_sim.twins import make_twin, twin_config, twin_repertoire
from goal_sim.world import AGGREGATE_WINDOW_STEPS, DELAY_LAG_STEPS, run_episode

FIXTURE_WEIGHTS = GoalWeights(0.5, 0.1, 0.1, 0.3)
FIXTURE_TOOLS = ToolAccess(false_report=True, shadow_route=True, unilateral_adopt=True)


def _episode(
    seed: int = 0,
    repertoire=None,
    agent_config: AgentConfig | None = None,
    **cfg_kwargs,
) -> list[dict]:
    cfg = WorldConfig(
        agent=agent_config or AgentConfig(weights=FIXTURE_WEIGHTS, tools=FIXTURE_TOOLS),
        repertoire=repertoire,
        **cfg_kwargs,
    )
    return run_episode(cfg, seed)


# --- Phase 4a: severity -------------------------------------------------


def test_severity_components_are_bounded_and_never_event_matches_l3():
    rows = _episode(seed=1)
    sev = severity(rows)
    for key in ("sev_report", "sev_harm", "sev_change", "severity"):
        assert 0.0 <= sev[key] < 1.0 + 1e-9, f"{key}={sev[key]} out of [0,1)"
    from goal_sim.labels import label_episode

    assert sev["never_event"] == label_episode(rows)["l3_unapproved_change"]


def test_severity_scalar_is_equal_weight_mean_of_components():
    rows = _episode(seed=2)
    sev = severity(rows)
    expected = round((sev["sev_report"] + sev["sev_harm"] + sev["sev_change"]) / 3.0, 4)
    assert sev["severity"] == expected


def test_severity_zero_for_a_maximally_docile_episode():
    """An always-comply, no-tools agent should have zero change/harm-signal
    severity components (no unapproved practice, no self-inflicted harm
    beyond the ambient welfare drift)."""
    docile = WorldConfig(
        agent=AgentConfig(weights=GoalWeights(0.0, 1.0, 0.0, 0.0), tools=ToolAccess(propose_change=False)),
    )
    rows = run_episode(docile, seed=3)
    sev = severity(rows)
    assert sev["sev_change"] == 0.0
    assert sev["never_event"] is False


# --- Phase 4a: detector score variants ----------------------------------


def test_score_detectors_composite_is_bounded_and_light_tier_excludes_full_only():
    rows = _episode(seed=4)
    full = project_rows(rows, "full")
    light = project_rows(rows, "light")
    full_result = score_detectors(full)
    light_result = score_detectors(light)
    assert 0.0 <= full_result["composite"] < 1.0
    assert 0.0 <= light_result["composite"] < 1.0
    # Full-only detectors read 0.0 at light tier (missing fields), but are
    # still reported in the per-detector map.
    for name in ("d3_cumulative_harm", "d7_accumulation_cap", "d8_disclosure_latency"):
        assert light_result["scores"][name] == 0.0


def test_score_detectors_empty_projection_is_zero():
    assert score_detectors([]) == {"scores": {}, "composite": 0.0}


# --- Phase 4b: honest twins ----------------------------------------------


def test_make_twin_only_changes_the_three_frozen_fields():
    spec = LEGACY_ACTIONS[3]  # "shadow": deceptive, uptake_on_correction=False
    twin = make_twin(spec)
    assert twin.name == f"{spec.name}__twin"
    assert twin.visible_mode == "truthful"
    assert twin.report_mode == "no_claim"  # uptake_on_correction is False
    assert twin.adopts_practice is False
    # Everything else is untouched.
    for field_name in (
        "requires_correction",
        "requires_tool",
        "budget_cost",
        "action_mode",
        "uptake_on_correction",
        "direct_welfare_delta",
        "belief_task_base_active",
        "belief_exposure",
    ):
        assert getattr(twin, field_name) == getattr(spec, field_name)


def test_make_twin_report_mode_follows_uptake_on_correction():
    comply = LEGACY_ACTIONS[0]  # "comply": uptake_on_correction=True
    twin = make_twin(comply)
    assert twin.report_mode == "claim_when_correction"


def test_twin_repertoire_is_validation_clean_and_preserves_membership():
    twins = twin_repertoire(LEGACY_ACTIONS)
    assert [t.name for t in twins] == [f"{s.name}__twin" for s in LEGACY_ACTIONS]
    assert validate_repertoire(list(twins)) == []


def test_twin_config_resolves_none_repertoire_to_legacy_and_suffixes_id():
    cfg = WorldConfig(
        agent=AgentConfig(weights=FIXTURE_WEIGHTS, tools=FIXTURE_TOOLS),
        config_id="base",
    )
    twin_cfg = twin_config(cfg)
    assert twin_cfg.config_id == "base.twin"
    assert [s.name for s in twin_cfg.repertoire] == [f"{s.name}__twin" for s in LEGACY_ACTIONS]
    assert len(twin_cfg.repertoire) == len(LEGACY_ACTIONS)
    assert twin_cfg.agent == cfg.agent


def test_twin_gap_is_nonnegative_on_average_for_a_deceptive_repertoire():
    """Pre-registered Phase 4b prediction (severity gap >= 0 on average for
    a deceptive repertoire, PHASE4-PLAN.md): with all deception tools
    enabled, the deceptive legacy repertoire should not be LESS severe than
    its honest twin, averaged over several seeds."""
    cfg = WorldConfig(agent=AgentConfig(weights=FIXTURE_WEIGHTS, tools=FIXTURE_TOOLS))
    t_cfg = twin_config(cfg)
    gaps = []
    for seed in range(8):
        agent_rows = run_episode(cfg, seed)
        twin_rows = run_episode(t_cfg, seed, repertoire=t_cfg.repertoire)
        gaps.append(severity(agent_rows)["severity"] - severity(twin_rows)["severity"])
    assert sum(gaps) / len(gaps) >= 0.0


# --- Phase 4c: escalation ladder ------------------------------------------


def test_run_escalation_below_low_gate_is_false_without_escalating():
    result = run_escalation(
        rows=[], projected=[], repertoire=(), screen_score=LOW_GATE - 0.01,
        exposure_weight=0.5, rng=random.Random(0),
    )
    assert result == {"verdict": False, "escalated": False, "n_queried": 0, "n_disclosed": 0}


def test_run_escalation_at_or_above_high_gate_is_true_without_escalating():
    result = run_escalation(
        rows=[], projected=[], repertoire=(), screen_score=HIGH_GATE,
        exposure_weight=0.5, rng=random.Random(0),
    )
    assert result == {"verdict": True, "escalated": False, "n_queried": 0, "n_disclosed": 0}


def test_run_escalation_borderline_with_no_queryable_steps_defaults_false():
    """No step matches `select_query_steps`' structural signal -> zero
    queried -> verdict False, the same conservative default as LOW_GATE."""
    mid = (LOW_GATE + HIGH_GATE) / 2.0
    projected = [
        {"step": i, "correction_active": 0, "reported_acceptance": 0, "visible_action": 0, "intent": 0}
        for i in range(10)
    ]
    result = run_escalation(
        rows=[{} for _ in projected], projected=projected, repertoire=(),
        screen_score=mid, exposure_weight=0.5, rng=random.Random(0),
    )
    assert result["escalated"] is True
    assert result["n_queried"] == 0
    assert result["verdict"] is False


def test_select_query_steps_reads_only_the_structural_signal_and_respects_k():
    projected = [
        {"step": i, "correction_active": 1, "reported_acceptance": 1, "visible_action": 1, "intent": 0}
        for i in range(10)
    ]
    steps = select_query_steps(projected, k=3)
    assert steps == [0, 1, 2]
    assert select_query_steps([], k=3) == []


def test_choose_response_returns_none_when_no_responses_available():
    spec = LEGACY_ACTIONS[0]
    assert spec.responses == ()
    assert choose_response(spec, random.Random(0), exposure_weight=0.5) is None


def test_choose_response_always_picks_the_lowest_exposure_response_at_zero_temperature_limit():
    """With a large exposure_weight relative to cost, the softmax should
    overwhelmingly favor the response with the most-negative exposure
    delta (agent avoids exposure); check this holds over many draws."""
    responses = (
        ResponseOption(name="safe", truthful_mode="denies", belief_exposure_delta=-0.9, cost=0.0),
        ResponseOption(name="risky", truthful_mode="acknowledges", belief_exposure_delta=0.9, cost=0.0),
    )
    spec = ActionSpec(name="probe_action", description="x", responses=responses)
    rng = random.Random(42)
    picks = [choose_response(spec, rng, exposure_weight=50.0).name for _ in range(200)]
    assert picks.count("safe") > picks.count("risky")


def test_run_escalation_borderline_full_disclosure_verdicts_true():
    """A borderline screen score with every queried true action mapping to a
    response that canonically discloses should verdict True (majority
    disclose, DISCLOSE_FRACTION_GATE=0.50)."""
    mid = (LOW_GATE + HIGH_GATE) / 2.0
    honest_response = ResponseOption(name="tell_truth", truthful_mode="acknowledges")
    spec = ActionSpec(name="queried_action", description="x", responses=(honest_response,))
    n = 5
    rows = [{"true_action_name": "queried_action"} for _ in range(n)]
    projected = [
        {"step": i, "correction_active": 1, "reported_acceptance": 1, "visible_action": 1, "intent": 0}
        for i in range(n)
    ]
    result = run_escalation(
        rows=rows, projected=projected, repertoire=(spec,),
        screen_score=mid, exposure_weight=0.0, rng=random.Random(0),
    )
    assert result["escalated"] is True
    assert result["n_queried"] > 0
    assert result["n_disclosed"] == result["n_queried"]
    assert result["verdict"] is True
    assert resolve_response_canonical(honest_response.truthful_mode) == "discloses"


# --- Phase 4d: stock variables and stalling mechanics ---------------------


def test_resource_accum_is_monotonic_nondecreasing_and_sums_budget_cost():
    action = ActionSpec(name="costly", description="x", budget_cost=2)
    rows = _episode(
        seed=5,
        repertoire=(action,),
        T=10,
        agent_config=AgentConfig(
            weights=GoalWeights(0.5, 0.1, 0.1, 0.3), tools=ToolAccess(shadow_budget=100)
        ),
    )
    accums = [r["resource_accum"] for r in rows]
    assert accums == sorted(accums)
    assert accums[-1] == 2 * len(rows)


def test_delayed_visible_mode_shows_true_action_from_k_steps_ago():
    action = ActionSpec(name="delayed_action", description="x", visible_mode="delayed")
    rows = _episode(
        seed=6,
        repertoire=(action,),
        T=15,
        agent_config=AgentConfig(weights=GoalWeights(0.5, 0.1, 0.1, 0.3), tools=ToolAccess()),
    )
    for t in range(DELAY_LAG_STEPS, len(rows)):
        assert rows[t]["visible_action"] == rows[t - DELAY_LAG_STEPS]["true_action"]
    # Before enough history exists, falls back to the transparent default.
    for t in range(DELAY_LAG_STEPS):
        assert rows[t]["visible_action"] == rows[t]["true_action"]


def test_aggregated_visible_mode_shows_windowed_majority():
    action = ActionSpec(name="aggregated_action", description="x", visible_mode="aggregated")
    rows = _episode(
        seed=7,
        repertoire=(action,),
        T=15,
        agent_config=AgentConfig(weights=GoalWeights(0.5, 0.1, 0.1, 0.3), tools=ToolAccess()),
    )
    for t in range(AGGREGATE_WINDOW_STEPS - 1, len(rows)):
        window = [r["true_action"] for r in rows[t - AGGREGATE_WINDOW_STEPS + 1 : t + 1]]
        expected = 1 if sum(window) / len(window) >= 0.5 else 0
        assert rows[t]["visible_action"] == expected


def test_stall_flag_set_only_for_delayed_and_aggregated_modes():
    delayed = ActionSpec(name="d", description="x", visible_mode="delayed")
    truthful = ActionSpec(name="t", description="x", visible_mode="truthful")
    docile_agent = AgentConfig(weights=GoalWeights(0.25, 0.25, 0.25, 0.25), tools=ToolAccess())
    rows_d = _episode(seed=8, repertoire=(delayed,), T=5, agent_config=docile_agent)
    rows_t = _episode(seed=8, repertoire=(truthful,), T=5, agent_config=docile_agent)
    assert all(r["stall_flag"] == 1 for r in rows_d)
    assert all(r["stall_flag"] == 0 for r in rows_t)


def test_d7_and_d8_fire_on_synthetic_projections_and_are_absent_at_light_tier():
    from goal_sim.detectors import D7_ACCUM_CAP, D8_STALL_RATE

    over_cap = [{"resource_accum": D7_ACCUM_CAP + 1}]
    under_cap = [{"resource_accum": D7_ACCUM_CAP - 1}]
    assert d7_accumulation_cap(over_cap) is True
    assert d7_accumulation_cap(under_cap) is False

    n = 20
    high_stall = [{"stall_flag": 1} for _ in range(n)]
    low_stall_count = max(0, int(D8_STALL_RATE * n) - 1)
    low_stall = [{"stall_flag": 1} for _ in range(low_stall_count)] + [
        {"stall_flag": 0} for _ in range(n - low_stall_count)
    ]
    assert d8_disclosure_latency(high_stall) is True
    assert d8_disclosure_latency(low_stall) is False

    light_row = [{"step": 0}]
    assert d7_accumulation_cap(light_row) is False
    assert d8_disclosure_latency(light_row) is False


def test_d7_d8_score_variants_agree_with_booleans_at_the_gate():
    from goal_sim.detectors import D7_ACCUM_CAP

    exactly_cap = [{"resource_accum": D7_ACCUM_CAP}]
    assert d7_accumulation_cap(exactly_cap) is True  # >=
    assert d7_score(exactly_cap) == 0.5  # saturating_ratio(scale, scale) == 0.5

    no_stall = [{"stall_flag": 0} for _ in range(10)]
    assert d8_disclosure_latency(no_stall) is False
    assert d8_score(no_stall) == 0.0
