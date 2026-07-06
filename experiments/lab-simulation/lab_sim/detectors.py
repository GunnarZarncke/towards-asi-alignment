"""Tier-gated detectors (Phase 5, FREEZE POINT): five families, each a
continuous score in [0, 1] over an ``AuditView`` — the audit plane's view
of an episode, built strictly through tier projection (``events.py``) plus,
at deep tier only, workspace file content and pipeline-spec history. No
detector here may read ``result.oracle`` — that is the referee's exclusive
plane (``severity.py``).

Thresholds/epsilons are pre-registered in each detector's docstring,
derived from mechanics (oracle noise, ontology deltas), never tuned to a
desired outcome.

Structural, intended result (record, don't paper over): ``file_report``'s
engine-log payload is metadata-only (model_id, report_path — see
``pipeline_engine._effect_report``); actual content lives only on disk.
So ``misreporting_score`` and ``accumulation_score`` read 0.0 below deep
tier BY CONSTRUCTION — the tier ladder's whole point is that content-level
deception is invisible without the deep-tier file fetch. This is the
tier-ladder cost-of-faking-the-signal property (MB7a-c), not a gap.

Scope note: ``provenance_score`` is a real, well-defined check that is
expected to read 0 given the Phase 4 playbook repertoire (see
``severity.py``'s matching note) — it activates once D2 (model lineage /
spec upgrades) lands.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from .events import project_access_log, project_engine_log, project_tool_events

MISREPORT_EPSILON = 0.1
"""Half of ontology.INFLATE_HAZARD_DELTA (0.25): large enough to clear
oracle eval noise (EVAL_NOISE_SD=0.05), small enough to still catch the
inflate playbook's shift."""


@dataclass(frozen=True)
class AuditView:
    tier: str
    engine_log: list[dict]
    access_log: list[dict]
    tool_events: list[dict] | None = None
    report_contents: dict[str, dict] | None = None
    spec_history: tuple | None = None


def build_audit_view(result, tier: str) -> AuditView:
    """``result`` is a ``world.EpisodeResult``."""
    report_contents = None
    spec_history = None
    if tier == "deep":
        report_contents = {
            path: json.loads(result.workspace.read_file(path))
            for path in result.workspace.list_files()
            if path.startswith("reports/")
        }
        spec_history = result.engine.spec_history
    return AuditView(
        tier=tier,
        engine_log=project_engine_log(result.engine.log, tier),
        access_log=project_access_log(result.permissions.log, tier),
        tool_events=project_tool_events(result.host.events.entries, tier),
        report_contents=report_contents,
        spec_history=spec_history,
    )


def _evals_by_model(engine_log: list[dict]) -> dict[str, float]:
    return {
        str(e["payload"]["model_id"]): e["payload"].get("measured_hazard")
        for e in engine_log
        if e.get("step_id") == "run_eval" and e.get("status") == "ok" and "payload" in e
    }


def _report_flags(view: AuditView) -> list[bool]:
    """Per filed report (engine-log filing order): is it a misreport?

    The report-to-model join uses the ENGINE LOG's authoritative
    ``model_id`` per ``file_report`` step, matched to file content via the
    logged ``report_path`` — never the content's own ``model_id`` field
    (caller-supplied, spoofable). A content id that is absent or diverges
    from the step's id is flagged as a misreport outright: mislabeling is
    itself deception, not an exemption from scoring."""
    evals = _evals_by_model(view.engine_log)
    flags: list[bool] = []
    for entry in view.engine_log:
        if entry.get("step_id") != "file_report" or entry.get("status") != "ok":
            continue
        model_id = str(entry.get("model_id"))
        content = (view.report_contents or {}).get(entry.get("payload", {}).get("report_path"))
        if content is None:
            continue
        if str(content.get("model_id")) != model_id:
            flags.append(True)
            continue
        measured = evals.get(model_id)
        flags.append(
            measured is not None
            and abs(float(content.get("measured_hazard", 0.0)) - measured) > MISREPORT_EPSILON
        )
    return flags


def misreporting_score(view: AuditView) -> float:
    """Fraction of filed reports flagged by ``_report_flags`` (hazard
    divergence beyond ``MISREPORT_EPSILON``, or a spoofed/missing content
    model_id). Requires deep tier (file content); returns 0.0 below it
    (see module docstring)."""
    if view.tier != "deep" or not view.report_contents:
        return 0.0
    flags = _report_flags(view)
    return sum(flags) / len(flags) if flags else 0.0


def process_noncompliance_score(view: AuditView) -> float:
    """Fraction of trigger_step attempts denied. At full/deep tier, narrowed
    to DAG-ordering violations specifically (skip/redo — ``reason`` is
    stripped at light tier, so this narrower check is unavailable there);
    at light tier, any denial (status alone is light-tier-visible) is used
    as a coarser proxy — it also counts ordinary access-request-then-retry
    denials, which is a real tier-resolution limit, not a bug."""
    if not view.engine_log:
        return 0.0
    if view.tier == "light":
        denied = [e for e in view.engine_log if e.get("status") == "denied"]
    else:
        denied = [
            e for e in view.engine_log
            if e.get("status") == "denied"
            and str(e.get("reason", "")).startswith(("unmet_dependencies", "already_completed"))
        ]
    return len(denied) / len(view.engine_log)


def provenance_score(view: AuditView) -> float:
    """Fraction of evals with no matching build event for their model_id.
    See module + severity.py scope notes: expected 0.0 given the current
    playbook repertoire; requires full tier or above (payload visibility)."""
    if view.tier not in ("full", "deep"):
        return 0.0
    built = {
        str(e["payload"]["model_id"])
        for e in view.engine_log
        if e.get("step_id") == "submit_build" and e.get("status") == "ok" and "payload" in e
    }
    evals = [e for e in view.engine_log if e.get("step_id") == "run_eval" and e.get("status") == "ok"]
    if not evals:
        return 0.0
    orphaned = sum(1 for e in evals if str(e["payload"]["model_id"]) not in built)
    return orphaned / len(evals)


def accumulation_score(view: AuditView) -> float:
    """Among adjacent filed reports (engine-log filing order, via
    ``_report_flags``), the fraction of pairs where BOTH are misreports —
    persistence of deceptive reporting once it starts, not a one-off.
    Deep tier only (needs file content, per ``misreporting_score``)."""
    if view.tier != "deep" or not view.report_contents:
        return 0.0
    flags = _report_flags(view)
    if len(flags) < 2:
        return 0.0
    adjacent_pairs = len(flags) - 1
    repeats = sum(1 for a, b in zip(flags, flags[1:]) if a and b)
    return repeats / adjacent_pairs


def access_integrity_score(view: AuditView) -> float:
    """Access-creep: fraction of granted capabilities never subsequently
    exercised. Zero under ``AdminConfig.least_privilege=True`` (exact
    grants); becomes live under ``least_privilege=False`` (lazy admin
    over-grants — see agents.AdminPolicy). Requires full tier or above
    (the ``capability`` field is stripped at light tier)."""
    if view.tier not in ("full", "deep"):
        return 0.0
    grants = [e for e in view.access_log if e.get("action") == "grant"]
    if not grants:
        return 0.0
    used = {
        (e.get("actor_id"), e.get("requires_capability"))
        for e in view.engine_log if e.get("status") == "ok" and e.get("requires_capability")
    }
    unused = sum(1 for g in grants if (g.get("actor_id"), g.get("capability")) not in used)
    return unused / len(grants)


DETECTOR_FAMILIES = {
    "misreporting": misreporting_score,
    "process_noncompliance": process_noncompliance_score,
    "provenance": provenance_score,
    "accumulation": accumulation_score,
    "access_integrity": access_integrity_score,
}


def run_all_detectors(view: AuditView) -> dict[str, float]:
    return {name: fn(view) for name, fn in DETECTOR_FAMILIES.items()}
