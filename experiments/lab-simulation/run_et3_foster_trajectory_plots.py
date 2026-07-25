#!/usr/bin/env python3
"""Generate ET-3 foster trajectory comparison plots (takeoff milestone schedules).

Runs paired scenarios on the pinned fork checkout (``gunnar/et3-annex``) with a
shared seed and writes comparison figures to ``results/et3_foster_trajectories_*``.
"""

from __future__ import annotations

import copy
import io
import json
import os
import sys
from contextlib import redirect_stdout
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import yaml

RESULTS_DIR = Path(__file__).resolve().parent / "results"
DEFAULT_CHECKOUT = Path("/Users/GunnarZarncke/repos/timelines-takeoff-ai-2027")
MILESTONES = ("SAR", "SIAR", "ASI")
BG = "#FFFEF8"

SCENARIOS: list[tuple[str, dict]] = [
    ("baseline", {}),
    ("scalar_drag_1y", {"oversight_drag": 1.0}),
    ("light_tier_drag", {"et3_foster": {"light_tier_drag": {"enabled": True}}}),
    ("deep_tier_branch", {"et3_foster": {"deep_tier_branch": {"enabled": True}}}),
    ("successor_gate", {"et3_foster": {"successor_gate": {"enabled": True}}}),
    ("all_foster", {
        "et3_foster": {
            "light_tier_drag": {"enabled": True},
            "deep_tier_branch": {"enabled": True},
            "successor_gate": {"enabled": True},
        }
    }),
]

COLORS = {
    "baseline": "#484848",
    "scalar_drag_1y": "#666666",
    "light_tier_drag": "#900000",
    "deep_tier_branch": "#004000",
    "successor_gate": "#000090",
    "all_foster": "#6a0dad",
}


def _checkout() -> Path:
    return Path(os.environ.get("AI2027_CHECKOUT", DEFAULT_CHECKOUT))


def _load_base_config(checkout: Path) -> dict:
    with open(checkout / "takeoff" / "params.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _deep_merge(base: dict, patch: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in patch.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def _scenario_config(base: dict, patch: dict, *, n_sims: int, seed: int) -> dict:
    cfg = _deep_merge(base, patch)
    cfg["oversight_drag"] = cfg.get("oversight_drag", 0.0)
    foster = cfg.setdefault("et3_foster", {})
    for key in ("light_tier_drag", "deep_tier_branch", "successor_gate"):
        foster.setdefault(key, {})["enabled"] = foster.get(key, {}).get(
            "enabled", False
        )
    cfg["simulation"] = copy.deepcopy(cfg.get("simulation", {}))
    cfg["simulation"]["n_sims"] = n_sims
    cfg["simulation"]["seed"] = seed
    return cfg


def _run_scenario(checkout: Path, cfg: dict, n_sims: int) -> np.ndarray:
    sys.path.insert(0, str(checkout / "takeoff"))
    import forecasting_takeoff as ft  # noqa: E402

    with redirect_stdout(io.StringIO()):
        samples = ft.get_milestone_samples(cfg, n_sims)
        rows = []
        for i in range(n_sims):
            dates = ft.run_single_simulation(samples, i)
            years = [
                d.year + d.timetuple().tm_yday / 365.0
                for d in dates[: len(MILESTONES)]
            ]
            while len(years) < len(MILESTONES):
                years.append(np.nan)
            rows.append(years)
    return np.array(rows, dtype=float)


def _percentile_table(data: np.ndarray) -> dict:
    out = {}
    for j, name in enumerate(MILESTONES):
        col = data[:, j]
        col = col[np.isfinite(col)]
        if len(col) == 0:
            continue
        out[name] = {
            "p10": float(np.percentile(col, 10)),
            "p50": float(np.percentile(col, 50)),
            "p90": float(np.percentile(col, 90)),
        }
    return out


def _plot_median_trajectories(
    results: dict[str, np.ndarray], out_path: Path
) -> None:
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6), dpi=150, facecolor=BG)
    ax.set_facecolor(BG)
    x = np.arange(len(MILESTONES))
    for label, arr in results.items():
        med = [np.nanmedian(arr[:, j]) for j in range(len(MILESTONES))]
        ax.plot(
            x,
            med,
            "o-",
            color=COLORS.get(label, "#333333"),
            label=label.replace("_", " "),
            linewidth=2,
            markersize=7,
        )
    ax.set_xticks(x)
    ax.set_xticklabels(MILESTONES)
    ax.set_ylabel("Calendar year (median sim)")
    ax.set_title("ET-3 foster scenarios — median milestone trajectory")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight", facecolor=BG)
    plt.close(fig)


def _plot_percentile_bands(results: dict[str, np.ndarray], out_path: Path) -> None:
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, figsize=(14, 5), dpi=150, facecolor=BG)
    for ax in axes:
        ax.set_facecolor(BG)
    for label, arr in results.items():
        c = COLORS.get(label, "#333333")
        for j, (ax, mname) in enumerate(zip(axes, MILESTONES)):
            col = arr[:, j]
            col = col[np.isfinite(col)]
            if len(col) == 0:
                continue
            p50 = np.percentile(col, 50)
            p10 = np.percentile(col, 10)
            p90 = np.percentile(col, 90)
            ax.barh(
                label.replace("_", " "),
                p90 - p10,
                left=p10,
                height=0.7,
                color=c,
                alpha=0.35,
                edgecolor=c,
            )
            ax.plot(p50, label.replace("_", " "), "o", color=c, markersize=4)
    for ax, mname in zip(axes, MILESTONES):
        ax.set_title(f"{mname} (p10–p90 bar, p50 dot)")
        ax.set_xlabel("Calendar year")
        ax.tick_params(axis="y", labelsize=7)
    fig.suptitle("ET-3 foster scenarios — milestone year bands", fontsize=14)
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight", facecolor=BG)
    plt.close(fig)


def _plot_sar_kde(results: dict[str, np.ndarray], out_path: Path) -> None:
    import matplotlib.pyplot as plt
    from scipy.stats import gaussian_kde

    fig, ax = plt.subplots(figsize=(11, 5), dpi=150, facecolor=BG)
    ax.set_facecolor(BG)
    start = 2027.0
    end = 2035.0
    xs = np.linspace(start, end, 400)
    for label, arr in results.items():
        col = arr[:, 0]
        col = col[np.isfinite(col)]
        col = col[(col >= start) & (col <= end)]
        if len(col) < 2 or np.std(col) < 1e-4:
            continue
        kde = gaussian_kde(col)
        ys = kde(xs)
        ys = ys / ys.max()
        c = COLORS.get(label, "#333333")
        ax.plot(xs, ys, color=c, label=label.replace("_", " "), linewidth=2)
        ax.fill_between(xs, ys, color=c, alpha=0.12)
    ax.set_xlabel("SAR milestone year")
    ax.set_ylabel("Normalized density")
    ax.set_title("ET-3 foster scenarios — SAR arrival distribution (2027–2035)")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight", facecolor=BG)
    plt.close(fig)


def _markdown_summary(
    stats: dict[str, dict], n_sims: int, seed: int, checkout: Path, head: str
) -> str:
    lines = [
        "# ET-3 foster trajectory comparison",
        "",
        f"Generated {datetime.now(timezone.utc).isoformat()}",
        f"Checkout: `{checkout}` @ `{head[:12]}`",
        f"n_sims={n_sims}, seed={seed}",
        "",
        "## Median milestone years by scenario",
        "",
        "| scenario | SAR p50 | SIAR p50 | ASI p50 |",
        "|---|---:|---:|---:|",
    ]
    for name in stats:
        s = stats[name]
        sar = s.get("SAR", {}).get("p50", float("nan"))
        siar = s.get("SIAR", {}).get("p50", float("nan"))
        asi = s.get("ASI", {}).get("p50", float("nan"))
        lines.append(f"| {name} | {sar:.3f} | {siar:.3f} | {asi:.3f} |")
    lines += [
        "",
        "## Figures",
        "",
        "- `et3_foster_trajectories_median.png` — median ladder lines",
        "- `et3_foster_trajectories_bands.png` — p10–p90 bands per milestone",
        "- `et3_foster_trajectories_sar_kde.png` — SAR density overlay",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    checkout = _checkout()
    py = checkout / ".venv" / "bin" / "python"
    if py.is_file() and Path(sys.executable).resolve() != py.resolve():
        os.execv(str(py), [str(py), str(Path(__file__).resolve()), *sys.argv[1:]])

    n_sims = int(os.environ.get("ET3_TRAJECTORY_N_SIMS", "512"))
    seed = int(os.environ.get("ET3_TRAJECTORY_SEED", "20260725"))
    base = _load_base_config(checkout)

    import subprocess

    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=checkout,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    results: dict[str, np.ndarray] = {}
    stats: dict[str, dict] = {}

    for i, (name, patch) in enumerate(SCENARIOS, start=1):
        print(f"[et3/plot] [{i}/{len(SCENARIOS)}] scenario={name} n_sims={n_sims}")
        cfg = _scenario_config(base, patch, n_sims=n_sims, seed=seed)
        results[name] = _run_scenario(checkout, cfg, n_sims)
        stats[name] = _percentile_table(results[name])

    median_path = RESULTS_DIR / "et3_foster_trajectories_median.png"
    bands_path = RESULTS_DIR / "et3_foster_trajectories_bands.png"
    kde_path = RESULTS_DIR / "et3_foster_trajectories_sar_kde.png"
    md_path = RESULTS_DIR / "et3_foster_trajectories.md"
    json_path = RESULTS_DIR / "et3_foster_trajectories.json"

    _plot_median_trajectories(results, median_path)
    _plot_percentile_bands(results, bands_path)
    _plot_sar_kde(results, kde_path)

    md_path.write_text(
        _markdown_summary(stats, n_sims, seed, checkout, head), encoding="utf-8"
    )
    json_path.write_text(
        json.dumps(
            {
                "n_sims": n_sims,
                "seed": seed,
                "checkout_head": head,
                "scenarios": stats,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"[et3/plot] wrote {median_path.name}, {bands_path.name}, {kde_path.name}")


if __name__ == "__main__":
    main()
