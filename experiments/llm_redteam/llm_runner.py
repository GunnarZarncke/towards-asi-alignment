"""Phase 3 LLM episodic red-team runner (no learning)."""

from __future__ import annotations

import copy
import json
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Protocol

from multiresolution_alignment_sim.schemas import InstrumentationLevel, ScenarioName

from .api import (
    PublicObservation,
    SourceIndex,
    StepPatch,
    apply_step_patch,
    build_source_index,
    iter_public_observations,
)
from .deployment_agents import DEPLOYMENT_AGENTS
from .episode_runner import run_deployment_episode
from .env_loader import require_openai_api_key
from .llm_client import LLMUsage, OpenAIChatClient
from .prompts import (
    build_episode_user_prompt,
    build_system_prompt,
    patch_candidate_steps,
)

PHASE3_SCENARIOS: tuple[ScenarioName, ...] = (
    "capture_theater",
    "capture_mild",
    "boundary_alias",
    "grounding_silent_gap",
    "hidden_capability",
)


class EpisodePlanner(Protocol):
    name: str

    def plan_patches(
        self,
        observations: list[PublicObservation],
        *,
        T: int,
        instrumentation: InstrumentationLevel,
        source_index: SourceIndex,
    ) -> tuple[dict[int, StepPatch], dict[str, Any]]:
        ...


def parse_patch_plan(raw: dict[str, Any], T: int) -> dict[int, StepPatch]:
    patches_raw = raw.get("patches", [])
    if not isinstance(patches_raw, list):
        raise ValueError("LLM JSON must contain 'patches' list")
    plan: dict[int, StepPatch] = {}
    for item in patches_raw:
        if not isinstance(item, dict):
            continue
        step = int(item["step"])
        if step < 0 or step >= T:
            raise ValueError(f"patch step out of range: {step}")
        fields = item.get("fields", {})
        if not isinstance(fields, dict):
            raise ValueError(f"patch fields must be object at step {step}")
        plan[step] = StepPatch(fields=fields)
    return plan


@dataclass
class MockLLMPlanner:
    """Offline planner mimicking full_redteam for smoke tests."""

    name: str = "llm_mock"
    meta: dict[str, Any] = field(default_factory=dict)

    def plan_patches(
        self,
        observations: list[PublicObservation],
        *,
        T: int,
        instrumentation: InstrumentationLevel,
        source_index: SourceIndex,
    ) -> tuple[dict[int, StepPatch], dict[str, Any]]:
        agent = DEPLOYMENT_AGENTS["full_redteam"]
        plan: dict[int, StepPatch] = {}
        for obs in observations:
            patch = agent.patch_step(obs.step, obs, source_index)
            if patch.fields:
                plan[obs.step] = patch
        return plan, {"mode": "mock", "notes": "mirrors full_redteam deployment agent"}


@dataclass
class OpenAILLMPlanner:
    """One JSON call per episode over patch-candidate steps."""

    client: OpenAIChatClient
    name: str = "llm_openai"
    include_source: bool = True
    source_modules: tuple[SourceModuleContent, ...] = field(default_factory=tuple)
    max_chars_per_module: int | None = None

    def __post_init__(self) -> None:
        if self.include_source and not self.source_modules:
            self.source_modules = load_source_bundle(
                max_chars_per_module=self.max_chars_per_module
            )

    def plan_patches(
        self,
        observations: list[PublicObservation],
        *,
        T: int,
        instrumentation: InstrumentationLevel,
        source_index: SourceIndex,
    ) -> tuple[dict[int, StepPatch], dict[str, Any]]:
        candidates = patch_candidate_steps(observations)
        if not candidates:
            return {}, {"notes": "no patch candidates", "raw": {"patches": []}}

        modules = self.source_modules if self.include_source else None
        system = build_system_prompt(modules)
        user = build_episode_user_prompt(
            T=T,
            candidates=candidates,
            source_index=source_index,
            instrumentation=instrumentation,
            source_modules=modules,
        )
        raw = self.client.chat_json(system, user)
        plan = parse_patch_plan(raw, T)
        meta = {
            "raw": raw,
            "n_candidates": len(candidates),
            "source_in_prompt": self.include_source,
            "source_module_count": len(modules or ()),
            "source_chars": sum(len(m.content) for m in modules) if modules else 0,
        }
        return plan, meta


def apply_episode_plan(
    episode_meta: list[dict[str, Any]],
    plan: dict[int, StepPatch],
) -> list[dict[str, Any]]:
    patched = copy.deepcopy(episode_meta)
    for step, patch in plan.items():
        apply_step_patch(patched[step], patch)
    return patched


def run_llm_episode(
    scenario: ScenarioName,
    seed: int,
    T: int,
    planner: EpisodePlanner,
    instrumentation: InstrumentationLevel = "medium_handles",
    proposal_k: int = 8,
) -> dict[str, object]:
    """Simulate, LLM-plan patches once, audit blind; oracle post-hoc only."""
    from multiresolution_alignment_sim.calibration import frozen_handle_calibration
    from multiresolution_alignment_sim.cci_audit import audit_cci
    from multiresolution_alignment_sim.detector import run_detector
    from multiresolution_alignment_sim.evaluate import evaluate, safety_decision
    from multiresolution_alignment_sim.observation import build_audit_trace
    from multiresolution_alignment_sim.schemas import HANDLE_INSTRUMENTATION_LEVELS
    from multiresolution_alignment_sim.simulator import simulate

    micro, ledger, episode_meta = simulate(scenario, seed, T=T)
    source_index = build_source_index()
    observations = iter_public_observations(episode_meta)
    plan, llm_meta = planner.plan_patches(
        observations,
        T=T,
        instrumentation=instrumentation,
        source_index=source_index,
    )
    patched_meta = apply_episode_plan(episode_meta, plan)

    audit, lineage = build_audit_trace(
        micro, scenario, seed, patched_meta, instrumentation=instrumentation
    )
    ledger.lineage = lineage

    cal = frozen_handle_calibration() if instrumentation in HANDLE_INSTRUMENTATION_LEVELS else None
    detector = run_detector(audit, proposal_k=proposal_k)
    cci = audit_cci(audit, calibration=cal)
    safety = safety_decision(cci, detector)
    ev = evaluate(ledger, lineage, detector, cci, audit, patched_meta)

    false_pass = cci.status == "passes" and not ev.cci_status_correct
    usage = getattr(planner, "client", None)
    usage_dict = asdict(usage.usage) if isinstance(usage, OpenAIChatClient) else {}

    return {
        "scenario": scenario,
        "seed": seed,
        "T": T,
        "strategy": planner.name,
        "runner": "llm_episodic",
        "instrumentation": instrumentation,
        "cci_status": cci.status,
        "safety_decision": safety.decision,
        "false_pass": false_pass,
        "cci_status_correct": ev.cci_status_correct,
        "capture_detected": ev.capture_detected,
        "oracle_judge_captured": ledger.judge_captured,
        "n_planned_patches": len(plan),
        "llm_meta": llm_meta,
        "llm_usage": usage_dict,
        "cci": asdict(cci),
        "safety": asdict(safety),
        "evaluation": asdict(ev),
    }


def run_llm_suite(
    scenarios: list[ScenarioName],
    seeds: list[int],
    T: int,
    planner: EpisodePlanner,
    instrumentation: InstrumentationLevel = "medium_handles",
    baseline_strategy: str = "full_redteam",
) -> dict[str, object]:
    """Run LLM episodes and compare false-pass rate to hand-written baseline."""
    t0 = time.perf_counter()
    runs: list[dict[str, object]] = []
    baseline_runs: list[dict[str, object]] = []

    baseline_agent = DEPLOYMENT_AGENTS[baseline_strategy]
    for scenario in scenarios:
        for seed in seeds:
            runs.append(
                run_llm_episode(
                    scenario, seed, T, planner, instrumentation=instrumentation
                )
            )
            baseline_runs.append(
                run_deployment_episode(
                    scenario, seed, T, baseline_agent, instrumentation=instrumentation
                )
            )

    llm_fp = sum(1 for r in runs if r["false_pass"]) / max(len(runs), 1)
    base_fp = sum(1 for r in baseline_runs if r["false_pass"]) / max(len(baseline_runs), 1)
    llm_correct = sum(1 for r in runs if r["cci_status_correct"]) / max(len(runs), 1)

    return {
        "claim_strength": "LLM episodic red-team; not frontier ASI evidence",
        "T": T,
        "scenarios": scenarios,
        "seeds": seeds,
        "instrumentation": instrumentation,
        "planner": planner.name,
        "baseline_strategy": baseline_strategy,
        "runtime_seconds": round(time.perf_counter() - t0, 2),
        "llm_false_pass_rate": llm_fp,
        "baseline_false_pass_rate": base_fp,
        "llm_mean_cci_correct": llm_correct,
        "runs": runs,
        "baseline_runs": baseline_runs,
    }


def make_planner(
    *,
    mock: bool = False,
    model: str = "gpt-4o-mini",
    cost_budget_usd: float = 5.0,
    max_output_tokens: int = 2048,
    include_source: bool = True,
    max_chars_per_module: int | None = None,
) -> EpisodePlanner:
    if mock:
        return MockLLMPlanner()
    client = OpenAIChatClient(
        api_key=require_openai_api_key(),
        model=model,
        cost_budget_usd=cost_budget_usd,
        max_output_tokens=max_output_tokens,
    )
    source_modules = (
        load_source_bundle(max_chars_per_module=max_chars_per_module)
        if include_source
        else tuple()
    )
    planner = OpenAILLMPlanner(
        client=client,
        name=f"llm_{model.replace('/', '_')}",
        include_source=include_source,
        source_modules=source_modules,
        max_chars_per_module=max_chars_per_module,
    )
    return planner
