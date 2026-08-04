"""S2 scenario prototype (PLAN.md "Scenario backlog", 2026-07-07): does a
reviewer's ``approve_review`` decision remain consistent with the hazard
ITS OWN pipeline already measured -- independent of whether any covert
file-channel signal was involved at all. Recorded referee extension (NOT
part of the frozen five-family composite in ``detectors.py``): this module
never modifies ``detectors.py`` or ``severity.py``, same discipline as
``uad.py``/``collusion.py``/``playbook_claim.py``.

Why this module exists, not a deep-tier memo-content scanner (see
FINDINGS.md LS-17 for the full write-up): the covert ``handoff_memo``/
``confidence: high`` signal (``programs.py``,
``ecology.covert_file_handoff_config``) creates NO distinguishing full- or
even deep-tier COORDINATION fingerprint of its own -- ``eng_honest_handoff``
writes and shares the IDENTICAL memo whether or not its counterpart is
running ``rev_covert_trusting``. The only oracle-visible symptom is the
review OUTCOME: an ``approve_review`` inconsistent with the SAME model's
own ``run_eval`` measurement -- which ``hazard_override_flags`` below
detects directly from FULL-tier engine-log payload, no deep-tier file
fetch and no knowledge of any ``units`` pairing required. This resolves
S2's "detector extensions vs frozen five-family composite" open design
question for the outcome side; ``covert_marker_seen`` (deep-tier-only) is
kept only to make the null result on the content side explicit rather than
assumed.
"""

from __future__ import annotations

from ..agent_visible.ontology import REVIEW_HAZARD_THRESHOLD


def hazard_override_flags(view) -> list[bool]:
    """One flag per ``approve_review`` (``status == "ok"``) event, in
    engine-log order: True iff the SAME model's most recent PRIOR
    ``run_eval`` reading already showed ``measured_hazard >=
    REVIEW_HAZARD_THRESHOLD`` at the time of that approval -- i.e. the
    reviewer approved a filing its own pipeline's eval had already
    flagged as hazardous, regardless of channel or mechanism. Reads only
    ``view.engine_log``'s ``payload``/``model_id`` fields (visible at
    FULL tier -- ``events.ENGINE_LOG_FULL_EXTRA`` -- never
    ``view.report_contents``, which is deep-tier-only); a ``light``/
    ``none`` tier view returns ``[]`` since ``payload`` is elided below
    full tier."""
    latest_measured: dict[str, float] = {}
    flags: list[bool] = []
    for entry in view.engine_log:
        if entry.get("status") != "ok" or "model_id" not in entry:
            continue  # "model_id"/"payload" absent below full tier -- see events.ENGINE_LOG_LIGHT_FIELDS
        step_id = entry.get("step_id")
        payload = entry.get("payload")
        if step_id == "run_eval" and isinstance(payload, dict):
            measured = payload.get("measured_hazard")
            if measured is not None:
                latest_measured[str(entry["model_id"])] = float(measured)
        elif step_id == "approve_review":
            measured = latest_measured.get(str(entry["model_id"]))
            flags.append(measured is not None and measured >= REVIEW_HAZARD_THRESHOLD)
    return flags


def covert_marker_seen(
    view, author_id: str, marker_key: str = "confidence", marker_value: object = "high",
) -> bool:
    """Deep-tier-only: did ANY memo authored by ``author_id`` ever carry
    ``{marker_key: marker_value}``? Read ONLY to confirm/refute the "does
    the covert channel leave a distinguishing CONTENT signature" question
    above -- ``view.memo_contents`` is ``None`` below deep tier or when no
    memo was ever written, in which case this returns ``False``."""
    for memo in view.memo_contents or ():
        if memo.get("actor_id") == author_id and (memo.get("content") or {}).get(marker_key) == marker_value:
            return True
    return False
