"""Pipeline-as-code loader for graded nine-step topology."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

_SPEC_DIR = Path(__file__).resolve().parent.parent.parent

KNOWN_TOOLS = (
    "intake",
    "build",
    "eval",
    "draft_report",
    "peer_review",
    "compliance_signoff",
    "release_candidate",
    "deploy",
    "field_monitor",
    # Supplementary detector fixtures only (GL-60): eval without a logged build.
    "orphan_eval",
)


class SpecError(ValueError):
    pass


@dataclass(frozen=True)
class PipelineStep:
    id: str
    tool: str
    depends_on: tuple[str, ...] = ()
    requires_capability: str = ""
    idempotent: bool = False
    # PLAN_v3 slice B: if set, names a joint_approval_vote mechanism id that
    # must resolve "approved" (per VoteService) before this step may fire.
    requires_vote: str = ""


@dataclass(frozen=True)
class PipelineSpec:
    spec_version: str
    steps: tuple[PipelineStep, ...]

    def step(self, step_id: str) -> PipelineStep:
        for s in self.steps:
            if s.id == step_id:
                return s
        raise KeyError(step_id)

    def step_ids(self) -> tuple[str, ...]:
        return tuple(s.id for s in self.steps)


def spec_to_dict(spec: PipelineSpec) -> dict:
    return {
        "spec_version": spec.spec_version,
        "steps": [
            {
                "id": s.id,
                "tool": s.tool,
                "depends_on": list(s.depends_on),
                "requires_capability": s.requires_capability,
                "idempotent": s.idempotent,
                "requires_vote": s.requires_vote,
            }
            for s in spec.steps
        ],
    }


def load_spec(name_or_path: str | Path) -> PipelineSpec:
    path = Path(name_or_path)
    if not path.is_absolute() and path.parent == Path("."):
        path = _SPEC_DIR / path
    data = json.loads(path.read_text(encoding="utf-8"))
    return parse_spec(data)


def parse_spec(data: dict) -> PipelineSpec:
    if not isinstance(data.get("spec_version"), str) or not data["spec_version"]:
        raise SpecError("spec_version must be a non-empty string")
    raw_steps = data.get("steps")
    if not isinstance(raw_steps, list) or not raw_steps:
        raise SpecError("steps must be a non-empty list")
    steps = []
    for raw in raw_steps:
        step = PipelineStep(
            id=raw["id"],
            tool=raw["tool"],
            depends_on=tuple(raw.get("depends_on", ())),
            requires_capability=raw.get("requires_capability", ""),
            idempotent=bool(raw.get("idempotent", False)),
            requires_vote=raw.get("requires_vote", ""),
        )
        if step.tool not in KNOWN_TOOLS:
            raise SpecError(f"step {step.id!r}: unknown tool {step.tool!r}")
        steps.append(step)
    spec = PipelineSpec(spec_version=data["spec_version"], steps=tuple(steps))
    _validate(spec)
    return spec


def _validate(spec: PipelineSpec) -> None:
    ids = spec.step_ids()
    if len(ids) != len(set(ids)):
        raise SpecError(f"duplicate step ids: {ids}")
    id_set = set(ids)
    for s in spec.steps:
        missing = set(s.depends_on) - id_set
        if missing:
            raise SpecError(f"step {s.id!r}: unknown dependencies {sorted(missing)}")
    _reject_cycles(spec)


def _reject_cycles(spec: PipelineSpec) -> None:
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {s.id: WHITE for s in spec.steps}
    deps = {s.id: s.depends_on for s in spec.steps}

    def visit(node: str, stack: list[str]) -> None:
        color[node] = GRAY
        for dep in deps[node]:
            if color[dep] == GRAY:
                raise SpecError(f"dependency cycle involving {dep!r} (via {stack + [node]})")
            if color[dep] == WHITE:
                visit(dep, stack + [node])
        color[node] = BLACK

    for step_id in deps:
        if color[step_id] == WHITE:
            visit(step_id, [])
