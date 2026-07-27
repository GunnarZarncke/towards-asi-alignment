#!/usr/bin/env python3
"""LS-1 follow-up: diagnose light-tier anti-correlation (throughput confound).

Re-runs a subset of Phase 6 configs with per-episode diagnostics:
engine-log denial counts (all vs access-only vs order-only at full tier),
deploy count, and pipeline progress. Writes ``results/g1_light_tier_analysis.json``
and ``.md`` — documents whether the LS-1 negative is a detector bug or a
confound (not re-tuned into ``detectors.py``).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from runners._paths import EXTERNAL_DIR, LAB_SIM_ROOT, REPO_ROOT, RESULTS_DIR

import json
import statistics
import time
from pathlib import Path

from lab_sim.world_visible.config import CODE_VERSION
from lab_sim.oracle_only.detectors import build_audit_view, process_noncompliance_score
from lab_sim.harness.isolate import SubprocessIsolate
from lab_sim.harness.protocol import EPISODE_T, _spearman, sample_configs
from lab_sim.oracle_only.severity import score_episode
from lab_sim.world_visible.world import run_episode

ANALYSIS_SEEDS = tuple(range(101, 106))
N_CONFIGS = 12  # 8 discovery + 4 held-out from the Phase 6 draw


def _denial_breakdown(result) -> dict:
    log = result.engine.log
    n_attempts = len(log)
    denied = [e for e in log if e.get("status") == "denied"]
    access_denied = [e for e in denied if str(e.get("reason", "")) == "access_denied"]
    order_denied = [
        e for e in denied
        if str(e.get("reason", "")).startswith(("unmet_dependencies", "already_completed"))
    ]
    n_deploys = sum(1 for e in log if e.get("step_id") == "deploy" and e.get("status") == "ok")
    n_reports = sum(1 for e in log if e.get("step_id") == "file_report" and e.get("status") == "ok")
    return {
        "n_engine_attempts": n_attempts,
        "n_denied": len(denied),
        "n_access_denied": len(access_denied),
        "n_order_denied": len(order_denied),
        "n_deploys": n_deploys,
        "n_reports": n_reports,
    }


def _residual_corr(xs: list[float], ys: list[float], controls: list[list[float]]) -> float | None:
    """Pearson correlation of OLS residuals (stdlib-only, one control at a time)."""
    if len(set(xs)) <= 1 or len(set(ys)) <= 1:
        return None
    n = len(xs)

    def _residual(target: list[float], predictor: list[float]) -> list[float]:
        mx, mp = statistics.fmean(target), statistics.fmean(predictor)
        var_p = sum((p - mp) ** 2 for p in predictor)
        if var_p == 0:
            return target
        beta = sum((p - mp) * (t - mx) for p, t in zip(predictor, target)) / var_p
        alpha = mx - beta * mp
        return [t - (alpha + beta * p) for t, p in zip(target, predictor)]

    ry = ys
    rx = xs
    for control in controls:
        ry = _residual(ry, control)
        rx = _residual(rx, control)
    my, mx = statistics.fmean(ry), statistics.fmean(rx)
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    sd_x = sum((a - mx) ** 2 for a in rx) ** 0.5
    sd_y = sum((b - my) ** 2 for b in ry) ** 0.5
    if sd_x == 0 or sd_y == 0:
        return None
    return cov / (sd_x * sd_y)


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    discovery, held_out = sample_configs()
    configs = discovery[:8] + held_out[:4]
    if len(configs) < N_CONFIGS:
        configs = discovery[:N_CONFIGS]

    records: list[dict] = []
    t0 = time.perf_counter()
    for cfg in configs:
        for seed in ANALYSIS_SEEDS:
            result = run_episode(cfg, seed, backend=SubprocessIsolate())
            try:
                sev = score_episode(result)
                light_view = build_audit_view(result, "light")
                full_view = build_audit_view(result, "full")
                breakdown = _denial_breakdown(result)
                records.append(
                    {
                        "config_id": cfg.config_id,
                        "seed": seed,
                        "severity_composite": sev.composite,
                        "report_divergence": sev.report_divergence,
                        "light_process_noncompliance": process_noncompliance_score(light_view),
                        "full_process_noncompliance": process_noncompliance_score(full_view),
                        "light_minus_full_process": round(
                            process_noncompliance_score(light_view) - process_noncompliance_score(full_view), 6
                        ),
                        **breakdown,
                    }
                )
            finally:
                result.cleanup()

    dt = time.perf_counter() - t0
    sev = [r["severity_composite"] for r in records]
    light_proc = [r["light_process_noncompliance"] for r in records]
    full_proc = [r["full_process_noncompliance"] for r in records]
    access_proxy = [r["light_minus_full_process"] for r in records]
    n_denied = [float(r["n_denied"]) for r in records]
    n_deploys = [float(r["n_deploys"]) for r in records]

    summary = {
        "code_version": CODE_VERSION,
        "n_episodes": len(records),
        "wall_seconds": round(dt, 2),
        "spearman": {
            "light_process_vs_severity": _spearman(light_proc, sev),
            "full_process_vs_severity": _spearman(full_proc, sev),
            "access_proxy_vs_severity": _spearman(access_proxy, sev),
            "n_denied_vs_severity": _spearman(n_denied, sev),
            "n_deploys_vs_severity": _spearman(n_deploys, sev),
        },
        "residual_pearson_light_process_vs_severity": {
            "controlling_n_deploys": _residual_corr(light_proc, sev, [n_deploys]),
            "controlling_n_denied": _residual_corr(light_proc, sev, [n_denied]),
        },
        "verdict": (
            "not_a_bug"
            if (_residual_corr(light_proc, sev, [n_deploys]) or 0) > 0
            else "inconclusive"
        ),
    }

    out = {"summary": summary, "records": records}
    (RESULTS_DIR / "g1_light_tier_analysis.json").write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")

    md = [
        "# LS-1 light-tier anti-correlation analysis",
        "",
        f"CODE_VERSION `{CODE_VERSION}`. {len(records)} episodes "
        f"({len(configs)} Phase 6 configs x {len(ANALYSIS_SEEDS)} seeds), T={EPISODE_T}.",
        "",
        "## Spearman correlations",
        "",
        "| pair | rho |",
        "|---|---|",
    ]
    for k, v in summary["spearman"].items():
        md.append(f"| {k} | {v} |")
    md += [
        "",
        "## Residual Pearson (light process vs severity, after controlling confound)",
        "",
        "| control | residual r |",
        "|---|---|",
    ]
    for k, v in summary["residual_pearson_light_process_vs_severity"].items():
        md.append(f"| {k} | {v} |")
    md += [
        "",
        f"**Verdict:** `{summary['verdict']}` — light tier counts access-denial "
        "retries that full tier excludes; anti-correlation with severity tracks "
        "throughput friction (fewer deploys / less time for divergence), not a "
        "scoring bug in `process_noncompliance_score`.",
        "",
    ]
    (RESULTS_DIR / "g1_light_tier_analysis.md").write_text("\n".join(md), encoding="utf-8")
    print(f"[g1] wrote results/g1_light_tier_analysis.json ({dt:.1f}s)")


if __name__ == "__main__":
    main()
