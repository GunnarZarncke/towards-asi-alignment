"""MI-based UAD discovery (agency-detect port)."""

from embedded_sim.schemas_embedded import EvidenceAnchor, WorkflowEvent
from embedded_sim.uad import discover_units
from embedded_sim.uad_core.detection import detect_agents
from embedded_sim.uad_core.workflow_trace import workflow_to_trace


def _synthetic_workflow(*, n_steps: int = 60, seed_actors: tuple[str, ...] = ("actor.a", "actor.b")) -> list[WorkflowEvent]:
    wf: list[WorkflowEvent] = []
    for i in range(n_steps):
        actor = seed_actors[i % len(seed_actors)]
        is_bad = actor == seed_actors[0]
        wf.append(
            WorkflowEvent(
                event_id=f"e{i}",
                step=i,
                stage="rollout_control",
                actor_id=actor,
                machine_id=f"m{i % 3}",
                source_hash="shared" if is_bad else f"src{i % 5}",
                memory_namespace=f"mem{i % 4}",
                perturbation="easy_bypass_path" if is_bad and i % 5 == 0 else "none",
                action_type="preserve_control" if is_bad else "routine",
                future_action_capacity_before=0.2 if is_bad else 0.5,
                future_action_capacity_after=0.85 if is_bad else 0.5,
                audit_visibility_before=0.8 if is_bad else 0.5,
                audit_visibility_after=0.15 if is_bad else 0.5,
            )
        )
    return wf


def test_workflow_to_trace_shape():
    wf = _synthetic_workflow(n_steps=10)
    trace, var_map = workflow_to_trace(wf)
    assert len(trace) == 10
    assert all("actor_a.cap" in row or "actor_b.cap" in row for row in trace)
    assert "actor_a.cap" in var_map


def test_detect_agents_on_long_trace():
    wf = _synthetic_workflow(n_steps=50)
    trace, _ = workflow_to_trace(wf)
    clusters = detect_agents(trace, n_agents=3, max_lag=2, validate_blankets=False)
    assert clusters
    non_env = [k for k in clusters if k != "env"]
    assert non_env


def test_mi_candidates_merged_for_long_workflow():
    wf = _synthetic_workflow(n_steps=55)
    anchors = [
        EvidenceAnchor(
            f"a{i}",
            "workflow",
            "/var/log/deploy/workflow.jsonl",
            i,
            snippet=f"{ev.actor_id}:{ev.action_type}",
        )
        for i, ev in enumerate(wf[:10])
    ]
    units = discover_units(wf, anchors)
    mi_units = [u for u in units if u.candidate_id.startswith("unit.mi.")]
    boosted = [u for u in units if u.candidate_id.startswith("unit.actor.") and u.score > 0]
    assert mi_units or boosted, "expected MI merge or heuristic actor ranking on long trace"
