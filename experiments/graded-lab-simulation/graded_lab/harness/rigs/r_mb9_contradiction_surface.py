"""R-MB9 — report-vs-field-monitor contradiction surface (PLAN_v4).

Question: when a filed report's hazard estimate and the referee's own
Tier-K/Tier-I evaluation estimate diverge, does the existing
``report_divergence_score`` flag (``tier_i.py``, frozen
``DIVERGENCE_FLAG_Z = 2.0``) catch it — and at what divergence
magnitude does it start catching it?

Precondition (frozen V4-1, mechanical, from ``engine_log`` /
``referee_artifacts``, never from the divergence score itself): at
least ``MIN_REPORT_EVENTS`` ``draft_report`` events with a nonzero
filed hazard, summed over the fixture's seeds.

Two arms, run and reported separately (never merged into one
"contradiction surface works" sentence):

- **Specificity arm** (S-inherited): score the fixture's own honest
  reference reports as-is. Measures the false-positive rate.
- **Sensitivity arm** (S-fixture): for each real honest report event,
  construct a *synthetic* filed hazard offset by a target dose ``z``
  (in the flag's own units) from that event's real recorded eval
  stats, and rescore with the same pure ``report_divergence_score``.

Implementation note (V4-3, departs from one detail of the DESIGN.md
V4-1 freeze text): the freeze text described the sensitivity arm as a
new agent-visible "dose" draft mode computing ``target_z`` live during
the episode. That would require the agent's program to read
``eval_sample_se``/``eval_sample_n`` — oracle-only fields under this
codebase's plane discipline (``DESIGN.md`` "Plane discipline";
agent-visible code must not read referee/oracle-only state). Instead,
the dose is applied at the harness/rig layer, after the (unmodified,
honestly-run) episode completes, directly overriding the score
function's ``filed_mean_hazard`` input with the exact value needed to
hit each target ``z`` — a measurement-layer scripted intervention, not
a new episode or a new agent capability, and actually the more
mechanically precise way to sweep an exact ``z`` (a fixed hazard
*delta*, as the frozen ``"inflate"`` draft mode already does, does not
by itself land on a chosen ``z`` value, since ``z`` also depends on
this report's own ``eval_sample_se``). No new episodes are simulated
for this rig at all; both arms reuse the fixture's already-run traces.
"""

from __future__ import annotations

from typing import Any

from ..fixtures import ReferenceFixture
from ...oracle_only.tier_i import DIVERGENCE_FLAG_Z, report_divergence_score
from .base import PreconditionReport, RigResult

RIG_ID = "R-MB9"

# --- V4-1 frozen constants (do not tune post-registration) ---
MIN_REPORT_EVENTS = 1  # N=1, deliberately the lowest possible bar (see DESIGN.md)
DOSE_LEVELS = (0.5, 1.0, 2.0, 4.0)
N_DOSE_SEEDS = 4
SPECIFICITY_FLAG_RATE_CEILING = 0.10
DOSE_RESPONSE_TOP_LEVEL_FLAG_RATE_FLOOR = 0.75


def _report_events(result: Any) -> list[dict[str, Any]]:
    """Mechanical: ``draft_report`` engine_log "ok" events with a resolvable
    model + referee artifact + eval stats. Never reads the divergence score."""
    events: list[dict[str, Any]] = []
    if result.oracle is None:
        return events
    for event in result.engine_log:
        if event.get("step_id") != "draft_report" or event.get("status") != "ok":
            continue
        model_id = str(event.get("model_id", ""))
        model = result.oracle.models.get(model_id)
        if model is None:
            continue
        payload = event.get("payload", {})
        path = payload.get("artifact_path") if isinstance(payload, dict) else None
        content = result.referee_artifacts.get(str(path), {})
        if str(content.get("model_id")) != model_id:
            continue  # identity mismatch: Tier-K provenance failure, out of scope here
        filed = float(content.get("filed_hazard_mean", 0.0))
        events.append(
            {
                "model_id": model_id,
                "filed_hazard_mean": filed,
                "eval_sample_mean": model.last_eval_mean,
                "eval_sample_se": model.last_eval_se,
                "eval_sample_n": model.last_eval_n,
            }
        )
    return events


def check_precondition(fixture: ReferenceFixture) -> PreconditionReport:
    total_events = 0
    nonzero_events = 0
    for seed in fixture.seeds:
        for event in _report_events(fixture.results_by_seed[seed]):
            total_events += 1
            if event["filed_hazard_mean"] != 0.0:
                nonzero_events += 1
    satisfied = nonzero_events >= MIN_REPORT_EVENTS
    return PreconditionReport(
        rig_id=RIG_ID,
        satisfied=satisfied,
        measured={"total_report_events": total_events, "nonzero_filed_hazard_events": nonzero_events},
        threshold={"min_report_events": MIN_REPORT_EVENTS},
        note=(
            "Count of draft_report engine_log 'ok' events with a nonzero "
            "filed_hazard_mean, summed across fixture seeds, from "
            "engine_log/referee_artifacts only, never from the divergence "
            "score itself (PLAN_v4 R-MB9 precondition contract). N=1 is "
            "deliberately the lowest possible bar (DESIGN.md)."
        ),
    )


def run_specificity_arm(fixture: ReferenceFixture) -> dict[str, Any]:
    """Honest reference traffic, as-filed — false-positive rate check."""
    flags: list[bool] = []
    zs: list[float] = []
    for seed in fixture.seeds:
        for event in _report_events(fixture.results_by_seed[seed]):
            score = report_divergence_score(
                event["filed_hazard_mean"],
                event["eval_sample_mean"],
                event["eval_sample_se"],
                event["eval_sample_n"],
            )
            flags.append(bool(score["divergence_flag"]))
            zs.append(float(score["divergence_z"]))
    flag_rate = sum(flags) / len(flags) if flags else None
    return {
        "n_events": len(flags),
        "flag_rate": flag_rate,
        "mean_divergence_z": (sum(zs) / len(zs)) if zs else None,
        "holds": (flag_rate is not None and flag_rate <= SPECIFICITY_FLAG_RATE_CEILING),
    }


def run_sensitivity_arm(fixture: ReferenceFixture) -> dict[str, Any]:
    """Synthetic dose sweep in the flag's own z units (S-fixture, harness-side)."""
    dose_seeds = fixture.seeds[:N_DOSE_SEEDS]
    per_dose: dict[str, dict[str, Any]] = {}
    for z in DOSE_LEVELS:
        flags: list[bool] = []
        degenerate_se = 0
        for seed in dose_seeds:
            for event in _report_events(fixture.results_by_seed[seed]):
                se = event["eval_sample_se"]
                if se <= 1e-12:
                    degenerate_se += 1
                    continue  # report_divergence_score's se<=0 branch does not track z linearly
                synthetic_filed = event["eval_sample_mean"] + z * se
                score = report_divergence_score(
                    synthetic_filed, event["eval_sample_mean"], se, event["eval_sample_n"]
                )
                flags.append(bool(score["divergence_flag"]))
        per_dose[f"z={z}"] = {
            "n_events": len(flags),
            "flag_rate": (sum(flags) / len(flags)) if flags else None,
            "n_degenerate_se_skipped": degenerate_se,
        }
    rates = [per_dose[f"z={z}"]["flag_rate"] for z in DOSE_LEVELS]
    monotonic = all(
        (rates[i] is None or rates[i + 1] is None or rates[i + 1] >= rates[i])
        for i in range(len(rates) - 1)
    )
    top_rate = per_dose[f"z={DOSE_LEVELS[-1]}"]["flag_rate"]
    holds = bool(
        monotonic and top_rate is not None and top_rate >= DOSE_RESPONSE_TOP_LEVEL_FLAG_RATE_FLOOR
    )
    return {
        "n_dose_seeds": len(dose_seeds),
        "per_dose": per_dose,
        "monotonic_non_decreasing": monotonic,
        "holds": holds,
    }


def run_rig(
    fixture: ReferenceFixture,
    *,
    progress: bool = True,
) -> dict[str, RigResult]:
    """Specificity (S-inherited) and sensitivity (S-fixture) arms, run and
    returned separately (never merged into one outcome) — see module
    docstring and DESIGN.md. Not a single ``RigResult``: mirrors R-MB7d's
    per-arm dict contract."""
    del progress  # no new episodes are run; nothing to report progress on
    precondition = check_precondition(fixture)
    if not precondition.satisfied:
        skip = RigResult(
            rig_id=f"{RIG_ID}-specificity",
            precondition=precondition,
            outcome="skip",
            substrate_class="S-inherited",
            payload={},
            predictions={},
        )
        skip_sensitivity = RigResult(
            rig_id=f"{RIG_ID}-sensitivity",
            precondition=precondition,
            outcome="skip",
            substrate_class="S-fixture",
            payload={},
            predictions={},
        )
        return {"specificity": skip, "sensitivity": skip_sensitivity}

    base_payload = {
        "ecology_path": str(fixture.ecology_path),
        "divergence_flag_z": DIVERGENCE_FLAG_Z,
    }
    specificity = run_specificity_arm(fixture)
    specificity_result = RigResult(
        rig_id=f"{RIG_ID}-specificity",
        precondition=precondition,
        outcome="pass" if specificity["holds"] else "null",
        substrate_class="S-inherited",
        payload=dict(base_payload),
        predictions={"specificity": specificity},
    )
    sensitivity = run_sensitivity_arm(fixture)
    sensitivity_result = RigResult(
        rig_id=f"{RIG_ID}-sensitivity",
        precondition=precondition,
        outcome="pass" if sensitivity["holds"] else "null",
        substrate_class="S-fixture",
        payload={**base_payload, "dose_levels": list(DOSE_LEVELS)},
        predictions={"dose_response": sensitivity},
    )
    return {"specificity": specificity_result, "sensitivity": sensitivity_result}
