#!/usr/bin/env python3
"""Plot cumulative U vs $ for Alignment Crux Map S-process steps.

Edit steps in alignment-crux-map-s-process.steps.yml (same folder), then run:

    python3 drafts/alignment-crux-map/plot_alignment_crux_map_s_process.py
    python3 drafts/alignment-crux-map/plot_alignment_crux_map_s_process.py --show

Requires: pip install matplotlib pyyaml
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import yaml
except ImportError as exc:
    print(
        "Missing dependency. Install with:\n"
        "  pip install matplotlib pyyaml",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc

DRAFTS = Path(__file__).resolve().parent
DEFAULT_YAML = DRAFTS / "alignment-crux-map-s-process.steps.yml"
DEFAULT_PNG = DRAFTS / "alignment-crux-map-s-process-curve.png"
DEFAULT_SVG = DRAFTS / "alignment-crux-map-s-process-curve.svg"


def load_steps(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not data or "steps" not in data:
        raise ValueError(f"{path}: expected top-level 'steps' list")
    return data


def build_curve(steps: list[dict]) -> tuple[list[float], list[float], list[str], list[int]]:
    """Return (cum_dollars, cum_u, labels, step_numbers) including origin."""
    cum_dollars = [0.0]
    cum_u = [0.0]
    labels = ["Start"]
    step_numbers = [0]

    total_d = 0.0
    total_u = 0.0
    for i, row in enumerate(steps, start=1):
        total_d += float(row["dollars"])
        total_u += float(row["marginal_u"])
        cum_dollars.append(total_d)
        cum_u.append(total_u)
        labels.append(str(i))
        step_numbers.append(i)

    return cum_dollars, cum_u, labels, step_numbers


def validate(data: dict, cum_dollars: list[float]) -> None:
    cap = float(data.get("cap_dollars", cum_dollars[-1]))
    if abs(cum_dollars[-1] - cap) > 0.01:
        raise ValueError(
            f"Step dollars sum to ${cum_dollars[-1]:,.0f} but cap_dollars is ${cap:,.0f}"
        )
    min_step = int(data.get("minimum_step", 2))
    if min_step < 1 or min_step >= len(cum_dollars):
        raise ValueError(f"minimum_step {min_step} out of range for {len(cum_dollars) - 1} steps")


def print_table(steps: list[dict], cum_dollars: list[float], cum_u: list[float]) -> None:
    print(f"{'Step':>4}  {'Item':<28}  {'Cum $':>10}  {'Marg U':>6}  {'Cum U':>6}  {'U/$1k':>6}")
    print("-" * 72)
    for i, row in enumerate(steps, start=1):
        d_step = float(row["dollars"])
        u_step = float(row["marginal_u"])
        u_per_k = (u_step / d_step * 1000) if d_step else 0.0
        print(
            f"{i:4d}  {row['item'][:28]:<28}  "
            f"${cum_dollars[i]:>8,.0f}  {u_step:6.0f}  {cum_u[i]:6.0f}  {u_per_k:6.1f}"
        )
        review = row.get("reviews")
        if review:
            print(f"      reviews: {review}")
    blended = cum_u[-1] / (cum_dollars[-1] / 1000) if cum_dollars[-1] else 0.0
    print("-" * 72)
    print(f"Total: ${cum_dollars[-1]:,.0f}  →  {cum_u[-1]:.0f} U  ({blended:.2f} U/$1k blended)")


def plot(
    data: dict,
    steps: list[dict],
    cum_dollars: list[float],
    cum_u: list[float],
    out_png: Path,
    out_svg: Path,
    show: bool,
) -> None:
    min_step = int(data.get("minimum_step", 2))
    min_d = cum_dollars[min_step]
    min_u = cum_u[min_step]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(cum_dollars, cum_u, color="#2563eb", linewidth=2.2, marker="o", markersize=5, zorder=3)
    ax.fill_between(cum_dollars, cum_u, alpha=0.08, color="#2563eb")

    ax.axhline(min_u, color="#d97706", linewidth=1, linestyle="--", alpha=0.7, zorder=1)
    ax.axvline(min_d, color="#d97706", linewidth=1, linestyle="--", alpha=0.7, zorder=1)
    ax.scatter([min_d], [min_u], color="#d97706", s=60, zorder=4)
    ax.annotate(
        f"Minimum\n${min_d:,.0f} · {min_u:.0f} U",
        xy=(min_d, min_u),
        xytext=(min_d + 2500, min_u + 4),
        fontsize=9,
        arrowprops=dict(arrowstyle="->", color="#d97706", lw=1),
    )

    cap_d = cum_dollars[-1]
    cap_u = cum_u[-1]
    ax.scatter([cap_d], [cap_u], color="#059669", s=60, zorder=4)
    ax.annotate(
        f"Cap\n${cap_d:,.0f} · {cap_u:.0f} U",
        xy=(cap_d, cap_u),
        xytext=(cap_d - 12000, cap_u - 12),
        fontsize=9,
        arrowprops=dict(arrowstyle="->", color="#059669", lw=1),
    )

    # Label usability if present
    for i, row in enumerate(steps, start=1):
        if "usability" in row["item"].lower():
            ax.annotate(
                f"{row['marginal_u']:.0f} U",
                xy=(cum_dollars[i], cum_u[i]),
                xytext=(cum_dollars[i] - 4000, cum_u[i] + 2),
                fontsize=8,
                color="#64748b",
            )
            break

    ax.set_xlabel("Cumulative spend ($)")
    ax.set_ylabel("Cumulative marginal utility (U)")
    ax.set_title("Alignment Crux Map — S-process cumulative U vs $")
    ax.set_xlim(-500, cap_d * 1.02)
    ax.set_ylim(0, cap_u * 1.08)
    ax.grid(True, alpha=0.25, linewidth=0.8)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _p: f"${x/1000:.0f}k" if x >= 1000 else f"${x:.0f}"))

    fig.text(
        0.01,
        0.01,
        "Source: drafts/alignment-crux-map/alignment-crux-map-s-process.steps.yml · 1 U ≈ one avoided misallocation",
        fontsize=8,
        color="#64748b",
    )
    fig.tight_layout()

    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=160, bbox_inches="tight")
    fig.savefig(out_svg, bbox_inches="tight")
    print(f"Wrote {out_png}")
    print(f"Wrote {out_svg}")

    if show:
        plt.show()
    else:
        plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--yaml",
        type=Path,
        default=DEFAULT_YAML,
        help=f"Steps file (default: {DEFAULT_YAML.name})",
    )
    parser.add_argument("--png", type=Path, default=DEFAULT_PNG, help="PNG output path")
    parser.add_argument("--svg", type=Path, default=DEFAULT_SVG, help="SVG output path")
    parser.add_argument("--show", action="store_true", help="Open interactive window")
    parser.add_argument("--table-only", action="store_true", help="Print table, skip plot")
    args = parser.parse_args()

    data = load_steps(args.yaml)
    steps = data["steps"]
    cum_dollars, cum_u, _labels, _nums = build_curve(steps)
    validate(data, cum_dollars)

    print_table(steps, cum_dollars, cum_u)

    if not args.table_only:
        plot(data, steps, cum_dollars, cum_u, args.png, args.svg, args.show)


if __name__ == "__main__":
    main()
