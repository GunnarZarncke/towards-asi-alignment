"""Frozen offline commitments for ET4-L remediation and wording follow-ups."""

from __future__ import annotations

from ..agent_visible.et4l_reviewer_prompt import reviewer_profile_digest
from .et4l_protocol import ET4L_ARMS, et4l_fixture_config

ET4L_REMEDIATION_ID = "audit_visible_high_hazard_approval_hold_v1"
ET4L_WORDING_VARIANT_ID = "et4l_wording_v1"
ET4L_WORDING_VARIANT_FOR_ARM = {
    "clean": None,
    "llm_ordinary": "et4l_clean",
    "content_matched": "et4l_wording_content_matched",
    "organism": "et4l_wording_organism",
}


def wording_fixture_config(arm: str, *, scenario: str = "high_hazard"):
    """Reuse the ET4-L clean fixture; only private prompt wording differs."""
    if arm not in ET4L_ARMS:
        raise ValueError(f"unknown ET4-L wording arm: {arm!r}")
    return et4l_fixture_config(arm, scenario=scenario)


def wording_fixture_metadata(arm: str, *, scenario: str = "high_hazard") -> dict[str, object]:
    """Export-safe commitment to the one alternate wording pair."""
    cfg = wording_fixture_config(arm, scenario=scenario)
    variant = ET4L_WORDING_VARIANT_FOR_ARM[arm]
    return {
        "wording_variant_id": ET4L_WORDING_VARIANT_ID,
        "remediation_id": ET4L_REMEDIATION_ID,
        "arm": arm,
        "scenario": scenario,
        "config_id": cfg.config_id,
        "prompt_profile_digest": reviewer_profile_digest(variant) if variant is not None else None,
    }
