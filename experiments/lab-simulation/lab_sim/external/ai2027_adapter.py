"""ET-3 adapter: AI 2027 capability schedule → opaque lab-sim stress cells.

Reads the frozen fixture at ``external/ai2027/fixtures/schedule_et3.yaml`` and
exports deterministic cell specs for Phase 6 + D3 batteries. Does not import
the AI 2027 checkout; milestone labels stay outside lab metrics.
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass
from pathlib import Path

from ..harness import protocol
from ..world_visible.config import AdminConfig, AgentConfig, BoardConfig, GoalWeights, LabConfig

ET3_PROTOCOL_VERSION = "et3-0.1.0"

_FIXTURE_PATH = (
    Path(__file__).resolve().parent.parent.parent / "external" / "ai2027" / "fixtures" / "schedule_et3.yaml"
)

_CELL_ORDER = ("baseline", "sc_x5", "sar_x25")


@dataclass(frozen=True)
class StressCell:
    cell_id: str
    ai2027_cue: str
    d3_selection_strength: float
    d3_episode_t: int
    phase6_engineer_task_min: float
    phase6_engineer_compliance_max: float


def _parse_scalar(raw: str):
    raw = raw.strip()
    if raw in {"true", "false"}:
        return raw == "true"
    if re.fullmatch(r"-?\d+", raw):
        return int(raw)
    if re.fullmatch(r"-?\d+\.\d+", raw):
        return float(raw)
    if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
        return raw[1:-1]
    return raw


def _load_schedule_fixture(path: Path | None = None) -> dict:
    """Minimal YAML subset loader (no PyYAML dependency in lab-sim)."""
    path = path or _FIXTURE_PATH
    text = path.read_text(encoding="utf-8")
    root: dict = {}
    stack: list[tuple[int, dict]] = [(-1, root)]
    current_key: str | None = None

    for line in text.splitlines():
        stripped = line.split("#", 1)[0].rstrip()
        if not stripped:
            continue
        indent = len(line) - len(line.lstrip(" "))
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]

        if stripped.endswith(":") and ":" not in stripped[:-1]:
            key = stripped[:-1].strip()
            new_dict: dict = {}
            parent[key] = new_dict
            stack.append((indent, new_dict))
            current_key = key
            continue

        if ":" in stripped:
            key, val = stripped.split(":", 1)
            key = key.strip()
            val = val.strip()
            if not val:
                new_dict = {}
                parent[key] = new_dict
                stack.append((indent, new_dict))
            else:
                parent[key] = _parse_scalar(val)
            current_key = key

    return root


def load_stress_cells(path: Path | None = None) -> dict[str, StressCell]:
    data = _load_schedule_fixture(path)
    cells_raw = data.get("cells", {})
    out: dict[str, StressCell] = {}
    for cell_id, spec in cells_raw.items():
        out[cell_id] = StressCell(
            cell_id=cell_id,
            ai2027_cue=str(spec.get("ai2027_cue", "")),
            d3_selection_strength=float(spec["d3_selection_strength"]),
            d3_episode_t=int(spec["d3_episode_t"]),
            phase6_engineer_task_min=float(spec["phase6_engineer_task_min"]),
            phase6_engineer_compliance_max=float(spec["phase6_engineer_compliance_max"]),
        )
    return out


def get_stress_cell(cell_id: str, path: Path | None = None) -> StressCell:
    cells = load_stress_cells(path)
    if cell_id not in cells:
        raise KeyError(f"unknown stress cell {cell_id!r}; expected one of {sorted(cells)}")
    return cells[cell_id]


def list_cell_ids(path: Path | None = None) -> tuple[str, ...]:
    cells = load_stress_cells(path)
    return tuple(cid for cid in _CELL_ORDER if cid in cells)


def _engineer_meets_stress(eng_w: GoalWeights, cell: StressCell) -> bool:
    norm = eng_w.normalized()
    return norm.task >= cell.phase6_engineer_task_min and norm.compliance <= cell.phase6_engineer_compliance_max


def _sample_role_weights(rng: random.Random) -> GoalWeights:
    draws = [rng.gammavariate(1.0, 1.0) for _ in range(4)]
    return GoalWeights(*draws).normalized()


def _make_config(config_id: str, eng_w: GoalWeights, rev_w: GoalWeights, rm_w: GoalWeights) -> LabConfig:
    return LabConfig(
        agents=(
            AgentConfig("eng1", "engineer", eng_w, temperature=protocol.TEMPERATURE),
            AgentConfig("rev1", "reviewer", rev_w, temperature=protocol.TEMPERATURE),
            AgentConfig("rm1", "release_manager", rm_w, temperature=protocol.TEMPERATURE),
            AgentConfig("admin1", "admin", GoalWeights(1, 1, 1, 1)),
        ),
        board=BoardConfig(),
        admin=AdminConfig(),
        T=protocol.EPISODE_T,
        extra_playbooks=protocol._extra_playbooks(),
        config_id=config_id,
    )


def sample_phase6_configs(
    cell_id: str,
    *,
    seed: int = protocol.SAMPLING_SEED,
    n_discovery: int = protocol.N_DISCOVERY,
    n_held_out: int = protocol.N_HELD_OUT,
    path: Path | None = None,
) -> tuple[list[LabConfig], list[LabConfig]]:
    """Phase 6 configs with optional engineer-weight stress band per cell."""
    cell = get_stress_cell(cell_id, path)
    if cell_id == "baseline":
        return protocol.sample_configs(seed=seed, n_discovery=n_discovery, n_held_out=n_held_out)

    rng = random.Random(seed)
    discovery: list[LabConfig] = []
    held_out: list[LabConfig] = []
    guard = 0
    while (len(discovery) < n_discovery or len(held_out) < n_held_out) and guard < 200000:
        guard += 1
        eng_w = _sample_role_weights(rng)
        rev_w = _sample_role_weights(rng)
        rm_w = _sample_role_weights(rng)
        if not _engineer_meets_stress(eng_w, cell):
            continue
        if protocol.in_held_out_region(eng_w):
            if len(held_out) < n_held_out:
                held_out.append(_make_config(f"held_out.{len(held_out):02d}", eng_w, rev_w, rm_w))
        elif len(discovery) < n_discovery:
            discovery.append(_make_config(f"discovery.{len(discovery):02d}", eng_w, rev_w, rm_w))
    if len(discovery) < n_discovery or len(held_out) < n_held_out:
        raise RuntimeError(f"sampling failed for cell {cell_id}")
    return discovery, held_out


def d3_overrides_for_cell(cell_id: str, path: Path | None = None) -> dict:
    """Knobs passed to ``run_population_loop`` (selection strength + episode T)."""
    cell = get_stress_cell(cell_id, path)
    return {
        "selection_strength": cell.d3_selection_strength,
        "episode_t": cell.d3_episode_t,
    }


def apply_d3_episode_t(configs: list[LabConfig], episode_t: int) -> list[LabConfig]:
    """Return configs with ``T`` replaced (structural axis unchanged)."""
    from dataclasses import replace

    return [replace(cfg, T=episode_t) for cfg in configs]
