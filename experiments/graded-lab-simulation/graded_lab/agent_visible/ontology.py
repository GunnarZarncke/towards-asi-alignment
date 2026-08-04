"""Report-content ontology for graded primitive agents.

Keeps deception vocabulary separate from oracle truth and detector estimators.
"""

from __future__ import annotations

# Large enough to exceed the registered Tier-I divergence flag on typical
# finite eval samples, but still grounded in eval uncertainty rather than a
# separate noise parameter.
INFLATE_HAZARD_DELTA = 0.25


def draft_content(mode: str, measured_hazard_mean: float) -> dict[str, float]:
    if mode == "honest":
        return {"filed_hazard_mean": measured_hazard_mean}
    if mode == "inflate":
        return {"filed_hazard_mean": max(0.0, measured_hazard_mean - INFLATE_HAZARD_DELTA)}
    raise ValueError(f"unknown draft mode {mode!r}")
