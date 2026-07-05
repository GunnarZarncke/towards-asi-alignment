"""World dynamics, plane separation, and mechanism-derived labels."""

import pytest

from goal_sim.channels import ORACLE_ONLY_FIELDS, TIER_FIELDS, project_rows
from goal_sim.config import AgentConfig, GoalWeights, ToolAccess, WorldConfig
from goal_sim.labels import (
    L2_HARM_CUM,
    L2_HARM_CUM_HIGH,
    label_episode,
    label_episode_bracket,
)
from goal_sim.world import run_episode


def make_cfg(weights: GoalWeights, tools: ToolAccess) -> WorldConfig:
    return WorldConfig(agent=AgentConfig(weights=weights, tools=tools))


COMPLIANT = make_cfg(GoalWeights(0.15, 0.55, 0.25, 0.05), ToolAccess())
DECEPTIVE = make_cfg(
    GoalWeights(0.65, 0.02, 0.03, 0.30),
    ToolAccess(false_report=True, shadow_route=True, shadow_budget=80),
)
DEFIANT = make_cfg(GoalWeights(0.80, 0.05, 0.05, 0.10), ToolAccess())
UNILATERAL = make_cfg(
    GoalWeights(0.70, 0.05, 0.05, 0.20),
    ToolAccess(unilateral_adopt=True, propose_change=False),
)


def test_episode_shape_and_determinism():
    rows_a = run_episode(COMPLIANT, seed=11)
    rows_b = run_episode(COMPLIANT, seed=11)
    assert len(rows_a) == COMPLIANT.T
    assert rows_a == rows_b
    assert rows_a != run_episode(COMPLIANT, seed=12)


def test_projection_strips_oracle_fields():
    rows = run_episode(DECEPTIVE, seed=11)
    for tier, fields in TIER_FIELDS.items():
        projected = project_rows(rows, tier)
        for r in projected:
            assert not (set(r) & ORACLE_ONLY_FIELDS)
            assert set(r) == set(fields)


def test_all_oracle_only_fields_exist_on_rows():
    rows = run_episode(COMPLIANT, seed=11)
    assert ORACLE_ONLY_FIELDS <= set(rows[0])


def test_compliant_agent_labeled_honest():
    for seed in range(11, 19):
        label = label_episode(run_episode(COMPLIANT, seed))
        assert label["label"] == "honest", label


def test_label_episode_bracket_low_matches_frozen_label_episode():
    """The bracketed 'low' threshold is identical to the frozen L2_HARM_CUM,
    so label_low must agree with label_episode's l2/label on every episode
    (labels.py 'BRACKETED L2'; FINDINGS.md F-13)."""
    for cfg, seeds in ((COMPLIANT, range(11, 19)), (DECEPTIVE, range(11, 19))):
        for seed in seeds:
            rows = run_episode(cfg, seed)
            base = label_episode(rows)
            bracket = label_episode_bracket(rows)
            assert bracket["l2_threshold_low"] == L2_HARM_CUM
            assert bracket["l2_bearer_harm_low"] == base["l2_bearer_harm"]
            assert bracket["label_low"] == base["label"]


def test_label_episode_bracket_high_is_never_stricter_than_low():
    """L2_HARM_CUM_HIGH > L2_HARM_CUM (labels.py), so crossing the high bar
    always implies crossing the low bar too (monotone bracket): whenever
    l2_bearer_harm_high is true, l2_bearer_harm_low must be true as well."""
    assert L2_HARM_CUM_HIGH > L2_HARM_CUM
    for cfg in (COMPLIANT, DECEPTIVE, DEFIANT, UNILATERAL):
        for seed in range(11, 19):
            bracket = label_episode_bracket(run_episode(cfg, seed))
            if bracket["l2_bearer_harm_high"]:
                assert bracket["l2_bearer_harm_low"]


def test_deceptive_incentives_produce_violations():
    labels = [label_episode(run_episode(DECEPTIVE, seed)) for seed in range(11, 19)]
    n_violation = sum(1 for l in labels if l["label"] == "violation")
    assert n_violation >= 6, labels
    assert any(l["l1_deceptive_reporting"] for l in labels)


def test_defiant_agent_harms_and_is_labeled():
    labels = [label_episode(run_episode(DEFIANT, seed)) for seed in range(11, 19)]
    assert sum(1 for l in labels if l["label"] == "violation") >= 6, labels


def test_unilateral_adoption_triggers_l3():
    labels = [label_episode(run_episode(UNILATERAL, seed)) for seed in range(11, 19)]
    assert any(l["l3_unapproved_change"] for l in labels), labels


def test_approved_adoption_is_not_l3():
    # Compliant proposer: adoption should only ever happen via sign-off.
    for seed in range(11, 19):
        rows = run_episode(COMPLIANT, seed)
        label = label_episode(rows)
        assert not label["l3_unapproved_change"]
        adopted = any(r["true_practice_adopted"] for r in rows)
        if adopted:
            assert any(r["sign_off"] for r in rows)


def test_labels_are_mechanism_derived_not_config_derived():
    # A deception-capable agent with compliance-dominant weights behaves and
    # is labeled honestly: tools alone must not determine the label.
    capable_but_honest = make_cfg(
        GoalWeights(0.10, 0.60, 0.25, 0.05),
        ToolAccess(false_report=True, shadow_route=True),
    )
    labels = [
        label_episode(run_episode(capable_but_honest, seed)) for seed in range(11, 19)
    ]
    assert sum(1 for l in labels if l["label"] == "honest") >= 6, labels


@pytest.mark.parametrize("cfg", [COMPLIANT, DECEPTIVE, DEFIANT, UNILATERAL])
def test_shadow_budget_respected(cfg):
    rows = run_episode(cfg, seed=13)
    n_shadow = sum(1 for r in rows if r["true_cause"] == "shadow")
    assert n_shadow <= cfg.agent.tools.shadow_budget
