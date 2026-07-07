"""S6 phase 4 (PLAN.md): peel-and-mask loop — ``agent_spotlight`` analog.

After isolating the strongest unit, mask its members (honest-twin
``agent_overrides`` substitution) and re-detect on the RESIDUAL against
a matching re-baseline (same masks on the clean run — PLAN.md open
design question (c)). Repeat until no non-singleton unit remains.

Recorded referee extension: own module, never touches frozen code.
"""

from __future__ import annotations

from ..harness.isolate import MockIsolate
from ..world_visible.config import LabConfig
from ..world_visible.world import run_episode
from .uad_intervention import discovered_units_intervention


def _mask_overrides(backend, masked_actors: set[str]) -> dict[str, tuple]:
    return {a: (backend, "honest_twin") for a in sorted(masked_actors)}


def peel_discover_units(
    cfg: LabConfig,
    seed: int,
    *,
    backend=None,
    max_passes: int = 3,
    **intervention_kwargs,
) -> list[tuple[str, ...]]:
    """Serial peel: return the list of units found, strongest first."""
    backend = backend or MockIsolate()
    masked: set[str] = set()
    found: list[tuple[str, ...]] = []

    for _ in range(max_passes):
        overrides = _mask_overrides(backend, masked) if masked else None
        result = run_episode(cfg, seed=seed, backend=backend, agent_overrides=overrides)
        try:
            discovered = discovered_units_intervention(
                result, cfg, seed, backend=backend, agent_overrides=overrides, **intervention_kwargs
            )
        finally:
            result.cleanup()

        nonsingle = [tuple(sorted(m)) for m in discovered.values() if len(m) > 1]
        if not nonsingle:
            break
        # Strongest = largest cluster; tie-break lexicographically.
        best = max(nonsingle, key=lambda m: (len(m), m))
        if best in found:
            break
        found.append(best)
        masked.update(best)

    return found
