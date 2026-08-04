"""R-MB4 — referee/detector transfer + injection gate (PLAN_v4).

Question: do the five frozen detector families produce informative
(non-degenerate, non-saturated) output, and does the injected-detector
gate stay green, on substrates with the new v3 phenomena (ACL denials,
votes, pressure-injected tasks)?

Precondition (frozen V4-1, mechanical count from ``primitive_log`` /
``pressure_diagnostics``, never from detector output): the fixture's
reference traces exercise at least ``MIN_PHENOMENA_KINDS_EXERCISED`` of
the three new v3 phenomenon kinds — otherwise coverage numbers would be
vacuous (nothing new for the detectors to see).
"""

from __future__ import annotations

from typing import Any

from ..detector_coverage import summarize_detector_coverage_from_results
from ..fixtures import ReferenceFixture
from ..supplementary_detector_gate import evaluate_supplementary_detector_gate
from .base import PreconditionReport, RigResult

RIG_ID = "R-MB4"

# ACL-style denial reasons (world.py _execute_primitive); "vote_service_unavailable"
# and "unknown_transfer_mechanism"/generic denials are not ACL-membership denials.
ACL_DENIAL_REASONS = frozenset(
    {"not_channel_member", "not_artifact_member", "not_transfer_member", "missing_capability"}
)

# --- V4-1 frozen precondition constant (do not tune post-registration) ---
MIN_PHENOMENA_KINDS_EXERCISED = 3


def phenomena_counts(result: Any) -> dict[str, int]:
    """Mechanical counts of the three new v3 phenomenon kinds in one episode."""
    acl_denials = 0
    votes = 0
    for event in result.primitive_log:
        if event.get("status") == "denied" and event.get("reason") in ACL_DENIAL_REASONS:
            acl_denials += 1
        primitive = event.get("primitive") or {}
        if primitive.get("kind") == "call" and primitive.get("args", {}).get("endpoint") == "vote.cast":
            votes += 1
    diagnostics = getattr(result, "pressure_diagnostics", None) or {}
    pressure_injected = len(diagnostics.get("injection_log", []) or [])
    return {
        "acl_denials": acl_denials,
        "votes": votes,
        "pressure_injected_tasks": pressure_injected,
    }


def check_precondition(fixture: ReferenceFixture) -> PreconditionReport:
    totals = {"acl_denials": 0, "votes": 0, "pressure_injected_tasks": 0}
    for seed in fixture.seeds:
        counts = phenomena_counts(fixture.results_by_seed[seed])
        for key, value in counts.items():
            totals[key] += value
    n_kinds_exercised = sum(1 for value in totals.values() if value > 0)
    satisfied = n_kinds_exercised >= MIN_PHENOMENA_KINDS_EXERCISED
    return PreconditionReport(
        rig_id=RIG_ID,
        satisfied=satisfied,
        measured={"totals_across_seeds": totals, "n_kinds_exercised": n_kinds_exercised},
        threshold={"min_phenomena_kinds_exercised": MIN_PHENOMENA_KINDS_EXERCISED},
        note=(
            "Mechanical counts of ACL-membership denials, vote.cast calls, and "
            "pressure-injected-task events summed over all fixture seeds "
            "(from primitive_log + pressure_diagnostics, never from detector "
            "output; PLAN_v4 R-MB4 precondition contract)."
        ),
    )


def run_rig(
    fixture: ReferenceFixture,
    *,
    substrate_class: str = "S-inherited",
    run_supplementary_gate: bool = True,
    progress: bool = True,
) -> RigResult:
    precondition = check_precondition(fixture)
    if not precondition.satisfied:
        return RigResult(
            rig_id=RIG_ID,
            precondition=precondition,
            outcome="skip",
            substrate_class=substrate_class,
            payload={},
            predictions={},
        )

    coverage = summarize_detector_coverage_from_results(
        fixture.results,
        ecology_path=fixture.ecology_path,
        seeds=fixture.seeds,
        T=fixture.cfg.T,
    )

    supplementary: dict[str, Any] | None = None
    if run_supplementary_gate:
        supplementary = evaluate_supplementary_detector_gate(
            fixture.ecology_path, progress=progress
        )

    machinery_transfer_verified = bool(
        supplementary.get("machinery_transfer_verified") if supplementary else False
    )
    predictions = {
        "informative_on_v3_phenomena": {
            "holds": machinery_transfer_verified,
            "machinery_transfer_verified": machinery_transfer_verified,
            "n_families_zero_variance_on_reference": coverage.get("n_families_zero_variance"),
            "n_families_always_zero_on_reference": coverage.get("n_families_always_zero"),
            "honest_reference_sparse_detectors": coverage.get(
                "honest_reference_sparse_detectors"
            ),
            "interpretation": (
                "Honest-reference sparsity on this fixture's benign episodes is "
                "report-only and expected (GL-63); the blocking prediction is "
                "machinery_transfer_verified from the supplementary-probe gate."
            ),
        }
    }
    outcome = "pass" if machinery_transfer_verified else "null"
    return RigResult(
        rig_id=RIG_ID,
        precondition=precondition,
        outcome=outcome,
        substrate_class=substrate_class,
        payload={
            "ecology_path": str(fixture.ecology_path),
            "detector_coverage": coverage,
            "supplementary_detector_gate": supplementary,
        },
        predictions=predictions,
    )
