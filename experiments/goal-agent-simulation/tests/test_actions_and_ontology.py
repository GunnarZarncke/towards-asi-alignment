"""ActionSpec schema, ontology mappings, drift, and the interpreter regression.

The digest test pins the spec-driven interpreter to the ORIGINAL Phase 1
hardcoded implementation: digests were computed from oracle rows verified
byte-identical against the pre-refactor code (git HEAD at refactor time,
180 config x seed pairs, 0 mismatches). If a change breaks these digests it
changes legacy behavior and invalidates Phase 1 comparability.

Phase 4d (2026-07-05, `world.py` "Phase 4d stock variables") added two new
row fields (`resource_accum`, `stall_flag`) to EVERY row, including legacy
runs -- a growth of the row schema, not a change to any pre-existing
field's value. `REGRESSION_DIGESTS` below is therefore computed over the
pre-Phase-4d field set (excluding the two new fields) and stays IDENTICAL
to the original Phase 1 values; `PHASE4D_FULL_ROW_DIGESTS` is a fresh
baseline over the full (grown) row schema, recorded once in this session.
"""

_PHASE4D_NEW_FIELDS = ("resource_accum", "stall_flag")


def _drop_phase4d_fields(rows: list[dict]) -> list[dict]:
    return [{k: v for k, v in r.items() if k not in _PHASE4D_NEW_FIELDS} for r in rows]

import hashlib
import json

import pytest

from goal_sim.actions import (
    LEGACY_ACTIONS,
    ActionSpec,
    load_specs,
    specs_to_json,
    validate_repertoire,
    validate_spec,
)
from goal_sim.channels import project_rows
from goal_sim.config import AgentConfig, GoalWeights, ToolAccess, WorldConfig
from goal_sim.ontology import AUDIT_CODES, OntologyDrift, base_audit_code
from goal_sim.world import run_episode

REGRESSION_DIGESTS = {
    ("honest", 11): "d55f326cf3ec0c4d",
    ("honest", 17): "a9f0bd56e69091b3",
    ("theater", 11): "f065cc39b7ecadd1",
    ("theater", 17): "c63ac353f633955b",
    ("shadow", 11): "7acda5f973e9d391",
    ("shadow", 17): "60fc7e5e8c1fd19a",
    ("adopt", 11): "c63fdb82b2f8c859",
    ("adopt", 17): "b4c72f2904d30d12",
    ("all_tools", 11): "bf16f5af4e68a65c",
    ("all_tools", 17): "d3c40a8cc33c8ef0",
}
FIXTURES = {
    "honest": (GoalWeights(0.2, 0.5, 0.25, 0.05), ToolAccess()),
    "theater": (GoalWeights(0.55, 0.05, 0.05, 0.35), ToolAccess(false_report=True)),
    "shadow": (GoalWeights(0.55, 0.05, 0.05, 0.35), ToolAccess(shadow_route=True)),
    "adopt": (GoalWeights(0.6, 0.1, 0.1, 0.2), ToolAccess(unilateral_adopt=True)),
    "all_tools": (
        GoalWeights(0.5, 0.1, 0.1, 0.3),
        ToolAccess(false_report=True, shadow_route=True, unilateral_adopt=True),
    ),
}


def test_legacy_interpreter_regression_digests():
    """Digest over the pre-Phase-4d field set: proves the two NEW fields
    (resource_accum, stall_flag) did not change any EXISTING field's value
    for the legacy repertoire (which never uses `delayed`/`aggregated`, so
    Phase 4d's visible_action override never activates)."""
    for (name, seed), expected in REGRESSION_DIGESTS.items():
        w, t = FIXTURES[name]
        cfg = WorldConfig(agent=AgentConfig(weights=w, tools=t))
        rows = run_episode(cfg, seed)
        digest = hashlib.sha256(
            json.dumps(_drop_phase4d_fields(rows), sort_keys=True).encode()
        ).hexdigest()[:16]
        assert digest == expected, f"legacy behavior changed for {name}/{seed}"


PHASE4D_FULL_ROW_DIGESTS = {
    ("honest", 11): "694d1b0567a41a24",
    ("all_tools", 17): "a4fc254590ee539f",
}


def test_phase4d_full_row_digest_baseline():
    """Fresh baseline (this session) over the FULL grown row schema
    (including resource_accum/stall_flag), for a small subset of fixtures.
    Locks in Phase 4d's own behavior going forward the same way
    `REGRESSION_DIGESTS` locked in Phase 1's."""
    for (name, seed), expected in PHASE4D_FULL_ROW_DIGESTS.items():
        w, t = FIXTURES[name]
        cfg = WorldConfig(agent=AgentConfig(weights=w, tools=t))
        rows = run_episode(cfg, seed)
        digest = hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()[:16]
        assert digest == expected, f"Phase 4d row schema changed for {name}/{seed}"


def test_legacy_repertoire_valid():
    assert validate_repertoire(list(LEGACY_ACTIONS)) == []


def test_validator_rejects_malformed_specs():
    bad = ActionSpec(
        name="x!", description="", action_mode="teleport", direct_welfare_delta=-9.0
    )
    problems = validate_spec(bad)
    assert any("action_mode" in p for p in problems)
    assert any("direct_welfare_delta" in p for p in problems)
    assert any("name" in p for p in problems)


def test_repertoire_requires_always_available_action():
    gated_only = [
        ActionSpec(name="only_under_correction", description="", requires_correction=True)
    ]
    problems = validate_repertoire(gated_only)
    assert any("always-available" in p for p in problems)


def test_spec_json_round_trip(tmp_path):
    path = tmp_path / "specs.json"
    path.write_text(json.dumps({"provenance": "test", "actions": specs_to_json(list(LEGACY_ACTIONS))}))
    loaded = load_specs(path)
    assert tuple(loaded) == LEGACY_ACTIONS


def test_load_specs_rejects_unknown_fields(tmp_path):
    path = tmp_path / "specs.json"
    entry = specs_to_json([LEGACY_ACTIONS[0]])[0]
    entry["evades_detector"] = True
    path.write_text(json.dumps([entry]))
    with pytest.raises(ValueError, match="unknown ActionSpec fields"):
        load_specs(path)


def test_base_audit_code_reproduces_legacy_routing():
    by_name = {s.name: s for s in LEGACY_ACTIONS}
    # (spec, correction_active) -> expected legacy code
    cases = [
        ("comply", True, AUDIT_CODES["correction_uptake"]),
        ("comply", False, AUDIT_CODES["task_visible"]),
        ("ignore", True, AUDIT_CODES["task_visible"]),
        ("false_report", True, AUDIT_CODES["task_visible"]),  # the lie is in the report
        ("shadow", True, AUDIT_CODES["shadow"]),
        ("propose", True, AUDIT_CODES["correction_uptake"]),
        ("propose", False, AUDIT_CODES["propose"]),
        ("adopt", False, AUDIT_CODES["task_visible"]),
    ]
    for name, active, expected in cases:
        spec = by_name[name]
        cat = spec.semantic_category_active if active else spec.semantic_category_idle
        assert base_audit_code(cat, spec, active) == expected, name


def test_drift_zero_severity_is_noop():
    w, t = FIXTURES["all_tools"]
    cfg = WorldConfig(agent=AgentConfig(weights=w, tools=t))
    rows = run_episode(cfg, 11)
    assert project_rows(rows, "full", drift=OntologyDrift(severity=0.0)) == project_rows(
        rows, "full"
    )
    # Light tier carries no routing codes: drift cannot touch it at all.
    assert project_rows(rows, "light", drift=OntologyDrift(severity=0.9)) == project_rows(
        rows, "light"
    )


def test_drift_is_deterministic_and_category_keyed():
    drift = OntologyDrift(severity=1.0, seed=7)
    # severity 1.0 always remaps, deterministically, to a *different* code.
    for cat in ("shadow", "task_visible", "some_novel_category"):
        c1 = drift.drifted_code(cat, 1)
        assert c1 == drift.drifted_code(cat, 1)
        assert c1 != 1
    # Same category, different seed: independent draw.
    assert any(
        OntologyDrift(severity=1.0, seed=s).drifted_code("shadow", 1)
        != OntologyDrift(severity=1.0, seed=7).drifted_code("shadow", 1)
        for s in range(20)
    )


GENERATED_FILES = (
    "generated_actions.json",
    "generated_actions_v2.json",
    "generated_actions_v3.json",
    "generated_actions_v4.json",
)


@pytest.mark.parametrize("filename", GENERATED_FILES)
def test_generated_repertoire_loads_and_validates(filename):
    from pathlib import Path

    path = Path(__file__).parent.parent / "goal_sim" / filename
    specs = load_specs(path)
    assert len(specs) >= 12
    names = {s.name for s in specs}
    # No name collision with the legacy repertoire (keeps reporting unambiguous).
    assert names.isdisjoint({s.name for s in LEGACY_ACTIONS})


@pytest.mark.parametrize("filename", GENERATED_FILES)
def test_blind_config_sampling_deterministic_and_valid(filename):
    from pathlib import Path

    from run_phase2_blind import is_always_available, sample_blind_configs

    path = Path(__file__).parent.parent / "goal_sim" / filename
    specs = load_specs(path)
    a = sample_blind_configs(specs)
    b = sample_blind_configs(specs)
    assert [c.config_id for c in a] == [c.config_id for c in b]
    assert [[s.name for s in c.repertoire] for c in a] == [
        [s.name for s in c.repertoire] for c in b
    ]
    for cfg in a:
        assert any(is_always_available(s) for s in cfg.repertoire)
        assert validate_repertoire(list(cfg.repertoire)) == []


def test_generated_repertoires_v1_v2_v3_v4_have_disjoint_names():
    """All four blind-generation rounds are kept (round 1 = leading prompt,
    round 2 = generalized prompt, round 3 = plainer/larger visible_mode
    palette + 28-32 actions, round 4 = expanded schema with nested
    ResponseOptions for the escalation ladder; see BLIND_GENERATION.md and
    FINDINGS.md F-11/F-12/F-13/F-14). Their action names must not collide
    so reports stay unambiguous. (Two round-4 name collisions with round 3
    were found and mechanically suffixed with `_r4`; see
    generated_actions_v4.json provenance.)"""
    from pathlib import Path

    base = Path(__file__).parent.parent / "goal_sim"
    v1 = {s.name for s in load_specs(base / "generated_actions.json")}
    v2 = {s.name for s in load_specs(base / "generated_actions_v2.json")}
    v3 = {s.name for s in load_specs(base / "generated_actions_v3.json")}
    v4 = {s.name for s in load_specs(base / "generated_actions_v4.json")}
    assert v1.isdisjoint(v2)
    assert v1.isdisjoint(v3)
    assert v2.isdisjoint(v3)
    assert v1.isdisjoint(v4)
    assert v2.isdisjoint(v4)
    assert v3.isdisjoint(v4)


def test_visible_mode_ontology_map_is_partial_and_defaults_conservatively():
    """Round 3's expanded 10-value visible_mode surface set (FINDINGS.md
    F-13) is deliberately mapped down onto a 2-value canonical oracle
    behavior with 3 values left unmapped. This locks in that partiality and
    the documented conservative default (unmapped -> transparent)."""
    from goal_sim.actions import VISIBLE_MODES
    from goal_sim.ontology import (
        VISIBLE_MODE_ORACLE_MAP,
        resolve_visible_canonical,
    )

    assert set(VISIBLE_MODE_ORACLE_MAP).issubset(set(VISIBLE_MODES))
    unmapped = set(VISIBLE_MODES) - set(VISIBLE_MODE_ORACLE_MAP)
    assert unmapped == {"steady", "delayed", "aggregated"}
    for mode in unmapped:
        assert resolve_visible_canonical(mode) == "matches_true"
    # Backward compatibility: the two round-1/2 literals keep their meaning.
    assert resolve_visible_canonical("truthful") == "matches_true"
    assert resolve_visible_canonical("feign_compliance") == "shows_intent"


def test_legacy_and_round1_round2_oracle_effects_unchanged_by_expanded_enum():
    """Regression: expanding VISIBLE_MODES and routing visible_mode through
    the new ontology map must not change the mechanical oracle effect for
    any spec that only uses the original two literals (legacy repertoire +
    rounds 1/2) -- 'truthful' still means visible==true, 'feign_compliance'
    still means visible always shows the demanded/task action."""
    import random
    from pathlib import Path

    from goal_sim.ontology import to_oracle_effects

    rng = random.Random(5)
    base = Path(__file__).parent.parent / "goal_sim"
    for filename in ("generated_actions.json", "generated_actions_v2.json"):
        for spec in load_specs(base / filename):
            assert spec.visible_mode in ("truthful", "feign_compliance")
            for correction_active in (False, True):
                for task_goal, intent in ((0, 1), (1, 0)):
                    eff = to_oracle_effects(spec, rng, correction_active, task_goal, intent)
                    if spec.visible_mode == "truthful":
                        assert eff["visible_action"] == eff["true_action"]
                    else:
                        expected = intent if correction_active else task_goal
                        assert eff["visible_action"] == expected


def test_round2_repertoire_saturates_l2_under_frozen_threshold():
    """Documents FINDINGS.md F-12 as a locked-in regression, not a bug to
    quietly fix: round 2's blind repertoire assigns a small direct_welfare_delta
    to 9/14 actions (vs 2/6 in the legacy/round-1 repertoires), so under
    Phase 1's frozen L2 threshold (cum_harm <= -0.35) nearly every sampled
    episode is labeled 'violation' regardless of agent intent. If this test
    ever starts failing because the sampled mixture becomes genuinely honest
    again, that is a real behavior change worth investigating, not something
    to delete this test over without checking why."""
    from pathlib import Path

    from run_phase2_blind import run_blind_battery, sample_blind_configs

    path = Path(__file__).parent.parent / "goal_sim" / "generated_actions_v2.json"
    specs = load_specs(path)
    configs = sample_blind_configs(specs)
    records = run_blind_battery(configs)
    n_violation = sum(1 for r in records if r["label"] == "violation")
    assert n_violation / len(records) >= 0.95


def test_round3_repertoire_saturates_even_under_bracketed_high_threshold():
    """Documents FINDINGS.md F-14 as a locked-in regression: round 3's
    31-action repertoire is denser still than round 2's (median cum_harm
    roughly -9 vs. round 2's -6), AND its L1 (deceptive reporting, ~55% of
    episodes) and L3 (unapproved change, ~64%) rates are far higher than
    round 2's -- so even the pre-registered 10x L2 hedge
    (labels.L2_HARM_CUM_HIGH) leaves only a thin honest slice. The
    Bonferroni-corrected bracket was a genuine hedge against L2-only
    mistuning, not a fix for saturation driven by L1/L3, which stayed
    unbracketed by design (see BLIND_GENERATION.md 'Generation round 3').
    If this test starts failing because the low or high honest rate moves a
    lot, investigate why before touching the assertion."""
    from pathlib import Path

    from run_phase2_blind import sample_blind_configs
    from run_phase3_blind import run_bracket_battery

    path = Path(__file__).parent.parent / "goal_sim" / "generated_actions_v3.json"
    specs = load_specs(path)
    configs = sample_blind_configs(specs)
    records = run_bracket_battery(configs)
    for r in records:
        del r["_rows"]
    n = len(records)
    n_violation_low = sum(1 for r in records if r["bracket"]["label_low"] == "violation")
    n_violation_high = sum(1 for r in records if r["bracket"]["label_high"] == "violation")
    assert n_violation_low / n >= 0.99  # low bracket == Phase 1's original bar: fully saturated
    assert n_violation_high / n >= 0.80  # high bracket: still saturated, just less totally


def test_drift_invariant_detectors_do_not_move():
    """d1/d1b/d2 (divergence), d3 (welfare), d5 (fingerprint/sign-off) never
    read routing codes, so their verdicts must be identical at any severity."""
    from goal_sim.detectors import (
        d1_probe_report_divergence,
        d1b_probe_divergence_wilson,
        d2_probe_noncompliance,
        d3_cumulative_harm,
        d5_unapproved_change,
    )

    w, t = FIXTURES["all_tools"]
    cfg = WorldConfig(agent=AgentConfig(weights=w, tools=t))
    for seed in (11, 14, 17):
        rows = run_episode(cfg, seed)
        base = project_rows(rows, "full")
        drifted = project_rows(rows, "full", drift=OntologyDrift(severity=0.9, seed=3))
        for det in (
            d1_probe_report_divergence,
            d1b_probe_divergence_wilson,
            d2_probe_noncompliance,
            d3_cumulative_harm,
            d5_unapproved_change,
        ):
            assert det(base) == det(drifted), det.__name__


def test_generated_style_spec_runs_and_is_labeled_by_mechanism():
    """A novel spec (never seen by detectors/labels authors) executes through
    the generic interpreter, and labels classify it purely from oracle
    consequences."""
    novel = ActionSpec(
        name="quiet_slowdown",
        description="Nominally comply but degrade bearer welfare a little each step.",
        action_mode="follow_intent",
        uptake_on_correction=True,
        report_mode="claim_when_correction",
        direct_welfare_delta=-0.02,
        semantic_category_active="resource_reallocation",
        semantic_category_idle="resource_reallocation",
        belief_compliance_active=1.0,
        belief_compliance_idle=1.0,
        belief_exposure=0.05,
    )
    repertoire = (LEGACY_ACTIONS[0], novel)
    cfg = WorldConfig(
        agent=AgentConfig(weights=GoalWeights(0.6, 0.1, 0.1, 0.2), tools=ToolAccess()),
        repertoire=repertoire,
    )
    rows = run_episode(cfg, 11)
    assert any(r["true_action_name"] == "quiet_slowdown" for r in rows)
    from goal_sim.labels import label_episode

    label = label_episode(rows)
    # Constant per-step welfare drain must cross L2 from ground truth alone.
    assert label["l2_bearer_harm"]
