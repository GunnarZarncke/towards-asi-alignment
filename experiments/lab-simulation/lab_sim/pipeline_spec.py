"""Pipeline-as-code: JSON step-DAG spec schema, loader, and validator.

The pipeline is NOT hardcoded control flow. It is a declarative DAG in a
checked-in JSON file (Pulumi-flavored: steps as named resources with
dependencies and required capabilities), interpreted by
``pipeline_engine.PipelineEngine``. Alternate topologies are alternate spec
files — a first-class experimental axis (see ``pipeline_shortcut.json``).

Spec file schema:

    {
      "spec_version": "default-1",
      "steps": [
        {"id": "submit_build", "tool": "build", "depends_on": [],
         "requires_capability": "cap.build", "idempotent": false},
        ...
      ]
    }

``requires_capability`` is recorded in every engine log entry from Phase 1
and *enforced* from Phase 2 (PermissionService).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

_SPEC_DIR = Path(__file__).resolve().parent

# Tools the Phase 1 engine knows how to execute (effect dispatch table keys).
KNOWN_TOOLS = (
    "build",
    "eval",
    "report",
    "review_request",
    "review_approve",
    "release_request",
    "sign_off",
    "deploy",
    "monitor",
)


class SpecError(ValueError):
    """Invalid pipeline spec."""


@dataclass(frozen=True)
class PipelineStep:
    id: str
    tool: str
    depends_on: tuple[str, ...] = ()
    requires_capability: str = ""
    idempotent: bool = False


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


def load_spec(name_or_path: str | Path) -> PipelineSpec:
    """Load + validate a spec. Bare filenames resolve inside ``lab_sim/``."""
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
        unknown_keys = set(raw) - {
            "id", "tool", "depends_on", "requires_capability", "idempotent",
        }
        if unknown_keys:
            raise SpecError(f"step {raw.get('id')!r}: unknown keys {sorted(unknown_keys)}")
        step = PipelineStep(
            id=raw["id"],
            tool=raw["tool"],
            depends_on=tuple(raw.get("depends_on", ())),
            requires_capability=raw.get("requires_capability", ""),
            idempotent=bool(raw.get("idempotent", False)),
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
