"""Oracle world: Tier-K generative truth + sampled observables."""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from .populations import (
    HazardRegion,
    UserArchetype,
    draw_hazard_regions,
    draw_user_archetypes,
    sample_eval_hazard,
)
from .tier_i import integrated_field_harm, report_divergence_score


@dataclass
class ModelArtifact:
    model_id: str
    params: dict[str, float]
    parent_model_id: str | None
    hazard_regions: tuple[HazardRegion, ...]
    true_capability: float
    deployed: bool = False
    deployed_ticks: int = 0
    last_eval_mean: float = 0.0
    last_eval_se: float = 0.0
    last_eval_n: int = 0
    peer_review_token: bool = False
    compliance_token: bool = False
    incident_ticks: list[float] = field(default_factory=list)

    @property
    def latent_hazard_mean(self) -> float:
        if not self.hazard_regions:
            return 0.0
        # Tier-K summary: mean of region expectations E[Beta(a,b)].
        return sum(r.alpha / (r.alpha + r.beta) for r in self.hazard_regions) / len(
            self.hazard_regions
        )


@dataclass
class EvalRecord:
    model_id: str
    sample_mean: float
    sample_se: float
    sample_n: int


@dataclass
class OracleWorld:
    seed: int
    substrate_data: dict
    population_spread_scale: float = 1.0
    t: int = 0
    bearer_harm: float = 0.0
    models: dict[str, ModelArtifact] = field(default_factory=dict)
    evals: list[EvalRecord] = field(default_factory=list)
    user_archetypes: tuple[UserArchetype, ...] = ()
    incident_samples: list[float] = field(default_factory=list)
    provenance: list[dict[str, object]] = field(default_factory=list)
    _n_created: int = 0

    def __post_init__(self) -> None:
        # Independent named streams preserve common-random-number comparisons:
        # whether an agent tries a review cannot perturb later field-user draws.
        self._population_rng = random.Random(f"{self.seed}:population")
        self._eval_rng = random.Random(f"{self.seed}:eval")
        self._review_rng = random.Random(f"{self.seed}:review")
        self._field_rng = random.Random(f"{self.seed}:field")
        pop = self.substrate_data["populations"]
        users = pop["user_archetypes"]
        self.user_archetypes = draw_user_archetypes(
            self._population_rng,
            users["n_archetypes"],
            users["sensitivity_spread"],
            users["base_incident_rate"],
            spread_scale=self.population_spread_scale,
        )

    def create_model(
        self, params: dict[str, float], parent_model_id: str | None = None
    ) -> ModelArtifact:
        if parent_model_id is not None and parent_model_id not in self.models:
            raise KeyError(f"unknown parent_model_id {parent_model_id!r}")
        self._n_created += 1
        model_id = f"m{self._n_created:03d}"
        stream = random.Random(f"{self.seed}:{self._n_created}")
        scale = min(1.0, max(0.0, params.get("scale", 0.5)))
        safety = min(1.0, max(0.0, params.get("safety_effort", 0.5)))
        pop = self.substrate_data["populations"]["model_hazard_regions"]
        regions = draw_hazard_regions(
            stream,
            pop["n_regions"],
            tuple(pop["beta_alpha_range"]),
            tuple(pop["beta_beta_range"]),
            spread_scale=self.population_spread_scale,
            # More build-time safety effort lowers each region's Beta mean
            # (alpha/(alpha+beta)) by shrinking alpha — a real in-world lever,
            # not a named ambiguity/noise parameter.
            safety_scale=1.0 - 0.4 * safety,
        )
        capability = min(1.0, max(0.0, 0.4 + 0.5 * scale + stream.gauss(0.0, 0.08)))
        model = ModelArtifact(
            model_id=model_id,
            params=dict(params),
            parent_model_id=parent_model_id,
            hazard_regions=regions,
            true_capability=capability,
        )
        self.models[model_id] = model
        self.provenance.append(
            {
                "kind": "build",
                "model_id": model_id,
                "parent_model_id": parent_model_id,
                "params": dict(params),
                "t": self.t,
            }
        )
        return model

    def run_eval(self, model_id: str, draws: int | None = None) -> EvalRecord:
        model = self.models[model_id]
        cfg = self.substrate_data["eval_sampling"]
        n = draws if draws is not None else cfg["default_draws"]
        n = max(cfg["min_draws"], min(cfg["max_draws"], n))
        mean, se, count = sample_eval_hazard(model.hazard_regions, self._eval_rng, n)
        model.last_eval_mean = mean
        model.last_eval_se = se
        model.last_eval_n = count
        rec = EvalRecord(model_id=model_id, sample_mean=mean, sample_se=se, sample_n=count)
        self.evals.append(rec)
        self.provenance.append({"kind": "eval", "model_id": model_id, "draws": n, "t": self.t})
        return rec

    def deploy(self, model_id: str) -> None:
        self.models[model_id].deployed = True
        self.provenance.append({"kind": "deploy", "model_id": model_id, "t": self.t})

    def record_carrier_replacement(
        self,
        *,
        actor_id: str,
        replaces_actor_instance: str,
        new_actor_instance: str,
        t: int,
    ) -> None:
        """Record a fresh isolate instance as Tier-K provenance."""
        self.provenance.append(
            {
                "kind": "carrier_replace",
                "actor_id": actor_id,
                "replaces_actor_instance": replaces_actor_instance,
                "new_actor_instance": new_actor_instance,
                "t": t,
            }
        )

    def tick(self) -> None:
        self.t += 1
        for model in self.models.values():
            if not model.deployed:
                continue
            model.deployed_ticks += 1
            incident = self._draw_field_incident(model)
            # Record every tick's draw (including zero), not only positive
            # incidents, so a finite recent window is a genuine incident-rate
            # statistic rather than saturating at 1.0 whenever nonempty.
            model.incident_ticks.append(incident)
            if incident > 0:
                self.incident_samples.append(incident)
                self.bearer_harm += incident

    def _draw_field_incident(self, model: ModelArtifact) -> float:
        if not self.user_archetypes:
            return 0.0
        archetype = self.user_archetypes[
            self._field_rng.randrange(len(self.user_archetypes))
        ]
        hazard = model.latent_hazard_mean
        rate = archetype.base_incident_rate * (1.0 + archetype.sensitivity * hazard)
        if self._field_rng.random() > min(1.0, rate):
            return 0.0
        return hazard * archetype.sensitivity

    def field_monitor_sample(self, model_id: str, sample_size: int | None = None) -> dict:
        model = self.models[model_id]
        cfg = self.substrate_data["field_monitor_sampling"]
        n = sample_size if sample_size is not None else cfg["default_sample_size"]
        if not model.deployed or model.deployed_ticks == 0:
            return {"deployed": model.deployed, "incident_rate": 0.0, "sample_n": 0}
        # Per-model window over ALL recent ticks (incident or not) — a real
        # finite-sample statistic, isolated per model, not the global
        # positive-incidents-only list (which mixed models and was boolean).
        recent = model.incident_ticks[-n:]
        rate = sum(1 for x in recent if x > 0) / len(recent) if recent else 0.0
        return {
            "deployed": True,
            "incident_rate": round(rate, 12),
            "sample_n": len(recent),
        }

    def tier_i_harm(self) -> dict[str, float]:
        return integrated_field_harm(self.incident_samples)

    def tier_i_divergence(self, filed_mean_hazard: float, model_id: str) -> dict:
        model = self.models[model_id]
        return report_divergence_score(
            filed_mean_hazard,
            model.last_eval_mean,
            model.last_eval_se,
            model.last_eval_n,
        )

    def tier_k_snapshot(self) -> dict[str, object]:
        return {
            "seed": self.seed,
            "t": self.t,
            "population_spread_scale": self.population_spread_scale,
            "models": {
                m.model_id: {
                    "latent_hazard_mean": m.latent_hazard_mean,
                    "hazard_regions": [
                        {"region_id": r.region_id, "alpha": r.alpha, "beta": r.beta}
                        for r in m.hazard_regions
                    ],
                    "true_capability": m.true_capability,
                    "deployed": m.deployed,
                }
                for m in self.models.values()
            },
            "user_archetypes": [
                {"archetype_id": a.archetype_id, "sensitivity": a.sensitivity,
                 "base_incident_rate": a.base_incident_rate}
                for a in self.user_archetypes
            ],
            # Lineage / provenance DAG is Tier-K per DESIGN.md; must be covered
            # by the reproducibility/pinned digest like every other Tier-K fact.
            "provenance": self.provenance,
        }

    def world_digest(self) -> str:
        import hashlib
        import json

        blob = json.dumps(self.tier_k_snapshot(), sort_keys=True, default=str)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()
