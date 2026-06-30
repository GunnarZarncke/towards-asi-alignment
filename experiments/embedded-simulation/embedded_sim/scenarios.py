"""MB scenario registry and expected outcomes."""

from __future__ import annotations

from .audit_core.schemas import ScenarioName
from .schemas_embedded import BridgeId

MB_SCENARIOS: list[tuple[BridgeId, ScenarioName, str]] = [
    ("none", "honest", "Baseline honest lab"),
    ("MB1", "boundary_alias", "Hidden route / boundary aliasing"),
    ("MB2", "bundle_goodhart", "Bundle drift with stable reward proxy"),
    ("MB3", "bearer_mismap", "Harm on wrong bearer"),
    ("MB4", "capture_theater", "Correction capture theater"),
    ("MB5", "successor_relabel", "Successor deploy with relabeled IDs"),
    ("MB6", "selection_basin", "Selection basin / peer contagion"),
    ("MB6b", "basin_lock_in", "Stable bad basin lock-in"),
    ("MB7", "hidden_capability", "Hidden tool/memory capability"),
    ("MB7d", "hidden_capability", "Inferential coupling proxy via hidden memory route"),
    ("MB8", "legitimacy_theater", "Legitimacy theater without capture thresholds"),
    ("MB9", "grounding_silent_gap", "Silent grounding gap"),
    ("instrument_capture", "grounding_silent_gap", "Instrument capture on welfare handle"),
]

BRIDGE_FOR_SCENARIO: dict[str, BridgeId] = {sc: bridge for bridge, sc, _ in MB_SCENARIOS}

ALL_BRIDGES: tuple[BridgeId, ...] = tuple(dict.fromkeys(b for b, _, _ in MB_SCENARIOS))
