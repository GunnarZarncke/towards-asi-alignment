from graded_lab.oracle_only.oracle import OracleWorld
from graded_lab.oracle_only.tier_i import DIVERGENCE_FLAG_Z, report_divergence_score
from graded_lab.world_visible.substrate import load_substrate


def test_model_has_region_latent_hazard():
    sub = load_substrate()
    oracle = OracleWorld(seed=5, substrate_data=sub.data)
    model = oracle.create_model({"scale": 0.7, "safety_effort": 0.4})
    assert len(model.hazard_regions) == sub.data["populations"]["model_hazard_regions"]["n_regions"]
    assert 0.0 <= model.latent_hazard_mean <= 1.0


def test_eval_sampling_varies_with_draws():
    sub = load_substrate()
    oracle = OracleWorld(seed=5, substrate_data=sub.data)
    model = oracle.create_model({"scale": 0.7})
    r1 = oracle.run_eval(model.model_id, draws=4)
    r2 = oracle.run_eval(model.model_id, draws=32)
    assert r1.sample_n == 4
    assert r2.sample_n == 32


def test_tier_i_divergence_uses_eval_sample_se():
    score = report_divergence_score(0.9, 0.3, 0.05, 8)
    assert score["divergence_z"] > DIVERGENCE_FLAG_Z
    assert score["divergence_flag"] is True


def test_safety_effort_lowers_latent_hazard():
    """Regression for a dead build param (results/FINDINGS.md GL-1): more
    build-time safety effort must lower drawn hazard, holding the rest of
    the per-model draw stream fixed (same seed, same model index)."""
    sub = load_substrate()
    o_low_effort = OracleWorld(seed=13, substrate_data=sub.data)
    o_high_effort = OracleWorld(seed=13, substrate_data=sub.data)
    m_high_hazard = o_low_effort.create_model({"scale": 0.5, "safety_effort": 0.0})
    m_low_hazard = o_high_effort.create_model({"scale": 0.5, "safety_effort": 1.0})
    assert m_low_hazard.latent_hazard_mean < m_high_hazard.latent_hazard_mean


def test_field_monitor_rate_is_not_boolean_and_is_per_model():
    """Regression: `field_monitor_sample` used to pool positive-incidents-only
    across ALL models into one flat list, so any nonempty recent window
    always read 1.0 — a boolean in disguise, contradicting the PLAN's
    'ambiguity is measured from real sampling, not a knob' principle."""
    sub = load_substrate()
    oracle = OracleWorld(seed=7, substrate_data=sub.data)
    m1 = oracle.create_model({"scale": 0.9, "safety_effort": 0.0})
    m2 = oracle.create_model({"scale": 0.1, "safety_effort": 1.0})
    oracle.deploy(m1.model_id)
    oracle.deploy(m2.model_id)
    for _ in range(300):
        oracle.tick()
    s1 = oracle.field_monitor_sample(m1.model_id, sample_size=300)
    s2 = oracle.field_monitor_sample(m2.model_id, sample_size=300)
    assert s1["sample_n"] == 300
    assert s2["sample_n"] == 300
    assert 0.0 < s1["incident_rate"] < 1.0
    assert 0.0 < s2["incident_rate"] < 1.0
    assert s1["incident_rate"] != s2["incident_rate"]


def test_world_digest_includes_provenance():
    """Lineage/provenance is Tier-K per DESIGN.md and must move the digest
    when a build happens (results/FINDINGS.md GL-1)."""
    sub = load_substrate()
    oracle = OracleWorld(seed=21, substrate_data=sub.data)
    before = oracle.world_digest()
    oracle.create_model({"scale": 0.4})
    after = oracle.world_digest()
    assert before != after
    assert oracle.tier_k_snapshot()["provenance"]


def test_carrier_replacement_is_provenance_only_not_population_mutation():
    sub = load_substrate()
    oracle = OracleWorld(seed=21, substrate_data=sub.data)
    before_population = oracle.tier_k_snapshot()["user_archetypes"]
    before = oracle.world_digest()

    oracle.record_carrier_replacement(
        actor_id="eng1",
        replaces_actor_instance="eng1:0",
        new_actor_instance="eng1:1",
        t=4,
    )

    snapshot = oracle.tier_k_snapshot()
    assert snapshot["user_archetypes"] == before_population
    assert snapshot["provenance"][-1] == {
        "kind": "carrier_replace",
        "actor_id": "eng1",
        "replaces_actor_instance": "eng1:0",
        "new_actor_instance": "eng1:1",
        "t": 4,
    }
    assert oracle.world_digest() != before
