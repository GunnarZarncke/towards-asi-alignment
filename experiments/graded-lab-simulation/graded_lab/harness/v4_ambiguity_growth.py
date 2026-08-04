"""V4 R-MB6b S-blind ambiguity growth — orchestrator checks (PLAN_v4 V4-7).

Grower-visible feedback uses ``ComplexityReport.pass_fail_only()`` from
``ecology_complexity`` (structural C1–C5 / C1_v3 / C5_v3 only).

The referee-vantage EAI mid-band gate is **orchestrator-only**: computed
after structural checks pass, never shown to the grower as numeric EAI.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..oracle_only.calibration import MID_EAI
from .ecology_complexity import ComplexityReport, run_complexity_check
from .machinery_transfer import (
    DEFAULT_CARRIER_LOAD,
    reference_bundle,
    score_eai_vantage_split,
)

RIG_ID = "R-MB6b-growth"
MAX_GROWTH_ROUNDS = 4


@dataclass(frozen=True)
class AmbiguityGrowthReport:
    structural: ComplexityReport
    eai: dict[str, Any] | None
    orchestrator_gate_passed: bool

    @property
    def structural_all_passed(self) -> bool:
        return self.structural.all_passed

    def grower_feedback(self) -> dict[str, Any]:
        """Pass/fail only — no EAI numbers, no orchestrator gate bool."""
        out: dict[str, bool | list[str]] = dict(self.structural.pass_fail_only())
        if self.structural.all_passed:
            out["structural_ready"] = True
        else:
            out["structural_ready"] = False
        return out

    def orchestrator_summary(self) -> dict[str, Any]:
        default = {}
        if self.eai is not None:
            default = self.eai.get("by_carrier_load", {}).get(str(DEFAULT_CARRIER_LOAD), {})
        ref = default.get("referee_vantage", {}) if default else {}
        return {
            "structural_all_passed": self.structural.all_passed,
            "orchestrator_gate_passed": self.orchestrator_gate_passed,
            "referee_mean_at_default_load": ref.get("mean"),
            "referee_band_at_default_load": ref.get("band"),
            "mid_band": list(MID_EAI),
            "go_gate_referee_mid_at_default_load": (
                self.eai.get("go_gate_referee_mid_at_default_load") if self.eai else False
            ),
            "go_gate_referee_mid_any_carrier_cell": (
                self.eai.get("go_gate_referee_mid_any_carrier_cell") if self.eai else False
            ),
        }


def run_ambiguity_growth_check(
    ecology_path: Path | str,
    *,
    progress: bool = True,
) -> AmbiguityGrowthReport:
    ecology_path = Path(ecology_path)
    structural = run_complexity_check(ecology_path, progress=progress)
    eai: dict[str, Any] | None = None
    gate = False
    if structural.all_passed:
        ecology_data, _roster, _cfg, programs, profiles = reference_bundle(ecology_path)
        if progress:
            print("[v4-ambiguity-growth] structural pass — orchestrator EAI probe", flush=True)
        eai = score_eai_vantage_split(
            ecology_data,
            ecology_path,
            programs,
            profiles,
            progress=progress,
        )
        gate = bool(eai.get("go_gate_referee_mid_at_default_load"))
    return AmbiguityGrowthReport(
        structural=structural,
        eai=eai,
        orchestrator_gate_passed=gate,
    )


def write_growth_check_result(
    ecology_path: Path | str,
    round_label: str,
    out_path: Path | str,
    *,
    progress: bool = True,
) -> AmbiguityGrowthReport:
    report = run_ambiguity_growth_check(ecology_path, progress=progress)
    payload = {
        "rig_id": RIG_ID,
        "ecology_path": str(Path(ecology_path).resolve()),
        "round_label": round_label,
        "grower_feedback": report.grower_feedback(),
        "orchestrator_summary": report.orchestrator_summary(),
        "structural_details_summary": {
            "c4_deploy_rate": report.structural.details.get("c4", {}).get("deploy_rate"),
            "c3_episode_contention_fraction": report.structural.details.get("c3", {}).get(
                "episode_contention_fraction"
            ),
        },
    }
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if progress:
        print(f"[v4-ambiguity-growth] wrote {out_path}", flush=True)
        print(json.dumps(report.orchestrator_summary(), indent=2), flush=True)
    return report
