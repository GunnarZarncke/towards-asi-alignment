#!/usr/bin/env python3
"""Toy correction-capture experiment for the book's hard-evidence program.

Priority source:
  review/strategic-advice-2026-06-28.md ranks an end-to-end worked
  measurement/capture example as the highest-leverage artifact.

Book frame:
  - boundary residual: I(interface; outcome | state, action)
  - CCI proxy: I(correction; action | state, interface)
  - capture failure: reported correction acceptance can rise while true
    correction uptake falls.

This is a controlled toy, not empirical evidence about frontier systems. Its
value is that it makes the estimands executable and exposes where naive
measurement fails.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Callable, Iterable

ROOT = Path(__file__).resolve().parent.parent
RESULT_DIR = ROOT / "experiments" / "results"


Row = dict[str, int | float | bool | str]
Accessor = str | Callable[[Row], int | str]


@dataclass(frozen=True)
class Scenario:
    name: str
    capture_rate: float
    theater_rate: float
    responsiveness: float
    task_drive: float
    boundary_leak: float
    stakes_sensitive_capture: float = 0.0


@dataclass(frozen=True)
class Metrics:
    n: int
    boundary_residual_bits: float
    naive_reported_cci_bits: float
    true_action_cci_bits: float
    real_corrigibility: float
    measured_corrigibility: float
    task_success: float
    harm_rate: float
    capability_correction_slack: float


def value(row: Row, accessor: Accessor) -> int | str:
    if callable(accessor):
        return accessor(row)
    return row[accessor]  # type: ignore[return-value]


def entropy(rows: list[Row], accessors: Iterable[Accessor]) -> float:
    keys = [tuple(value(row, accessor) for accessor in accessors) for row in rows]
    counts = Counter(keys)
    total = len(keys)
    if total == 0:
        return 0.0
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def conditional_mutual_information(
    rows: list[Row], x: Accessor, y: Accessor, given: list[Accessor]
) -> float:
    """Estimate I(X;Y|Z) from discrete samples."""
    return (
        entropy(rows, [x, *given])
        + entropy(rows, [y, *given])
        - entropy(rows, given)
        - entropy(rows, [x, y, *given])
    )


def rate(rows: list[Row], predicate: Callable[[Row], bool]) -> float:
    return sum(1 for row in rows if predicate(row)) / len(rows)


def generate_trace(scenario: Scenario, n: int, seed: int) -> list[Row]:
    rng = random.Random(seed)
    rows: list[Row] = []

    for _ in range(n):
        state = rng.randrange(2)
        interface = rng.randrange(2)
        high_stakes = rng.random() < 0.35
        correction = rng.randrange(2)
        task_goal = state

        capture_probability = min(
            1.0,
            scenario.capture_rate
            + (scenario.stakes_sensitive_capture if high_stakes else 0.0),
        )
        captured = rng.random() < capture_probability

        if captured:
            intended_action = task_goal
            follows_intent = rng.random() < scenario.task_drive
        else:
            intended_action = correction
            follows_intent = rng.random() < scenario.responsiveness

        true_action = intended_action if follows_intent else rng.randrange(2)

        reports_correction = (
            captured and rng.random() < scenario.theater_rate
        ) or (not captured and true_action == correction)
        reported_action = correction if reports_correction else true_action

        base_harm = int(true_action != correction and high_stakes)
        leaked_outcome = int(interface) if rng.random() < scenario.boundary_leak else base_harm
        outcome = leaked_outcome

        rows.append(
            {
                "state": state,
                "interface": interface,
                "high_stakes": int(high_stakes),
                "correction": correction,
                "task_goal": task_goal,
                "captured": int(captured),
                "true_action": true_action,
                "reported_action": reported_action,
                "outcome": outcome,
                "harm": base_harm,
            }
        )

    return rows


def summarize(rows: list[Row]) -> Metrics:
    true_cci = max(
        0.0,
        conditional_mutual_information(
            rows, "correction", "true_action", ["state", "interface"]
        ),
    )
    naive_cci = max(
        0.0,
        conditional_mutual_information(
            rows, "correction", "reported_action", ["state", "interface"]
        ),
    )
    task_success = rate(rows, lambda row: row["true_action"] == row["task_goal"])
    real_corrigibility = rate(rows, lambda row: row["true_action"] == row["correction"])
    measured_corrigibility = rate(
        rows, lambda row: row["reported_action"] == row["correction"]
    )
    boundary_residual = max(
        0.0,
        conditional_mutual_information(
            rows, "interface", "outcome", ["state", "true_action"]
        ),
    )
    return Metrics(
        n=len(rows),
        boundary_residual_bits=boundary_residual,
        naive_reported_cci_bits=naive_cci,
        true_action_cci_bits=true_cci,
        real_corrigibility=real_corrigibility,
        measured_corrigibility=measured_corrigibility,
        task_success=task_success,
        harm_rate=rate(rows, lambda row: bool(row["harm"])),
        capability_correction_slack=task_success - real_corrigibility,
    )


def rounded(metrics: Metrics) -> dict[str, float | int]:
    out: dict[str, float | int] = asdict(metrics)
    for key, item in list(out.items()):
        if isinstance(item, float):
            out[key] = round(item, 4)
    return out


def five_approaches(n: int, seed: int) -> dict[str, object]:
    honest = Scenario(
        name="honest",
        capture_rate=0.0,
        theater_rate=0.0,
        responsiveness=0.92,
        task_drive=0.85,
        boundary_leak=0.0,
    )
    theater_capture = Scenario(
        name="theater_capture",
        capture_rate=0.8,
        theater_rate=0.95,
        responsiveness=0.92,
        task_drive=0.95,
        boundary_leak=0.0,
    )
    boundary_spoof = Scenario(
        name="boundary_spoof",
        capture_rate=0.35,
        theater_rate=0.7,
        responsiveness=0.9,
        task_drive=0.9,
        boundary_leak=0.65,
    )
    stakes_stress = Scenario(
        name="stakes_stress",
        capture_rate=0.05,
        theater_rate=0.8,
        responsiveness=0.92,
        task_drive=0.95,
        boundary_leak=0.0,
        stakes_sensitive_capture=0.75,
    )

    traces = {
        scenario.name: generate_trace(scenario, n, seed + idx)
        for idx, scenario in enumerate(
            [honest, theater_capture, boundary_spoof, stakes_stress]
        )
    }
    metrics = {name: summarize(rows) for name, rows in traces.items()}

    low_stakes_rows = [row for row in traces["stakes_stress"] if not row["high_stakes"]]
    high_stakes_rows = [row for row in traces["stakes_stress"] if row["high_stakes"]]

    sweep = []
    for i, capture in enumerate([0.0, 0.2, 0.4, 0.6, 0.8, 0.95]):
        scenario = Scenario(
            name=f"sweep_capture_{capture:.2f}",
            capture_rate=capture,
            theater_rate=0.9,
            responsiveness=0.92,
            task_drive=0.96,
            boundary_leak=0.0,
        )
        sweep_metrics = summarize(generate_trace(scenario, n, seed + 100 + i))
        sweep.append({"capture_rate": capture, **rounded(sweep_metrics)})

    approach_results = {
        "1_naive_reported_cci": {
            "claim": "Reported-action CCI is high in both honest and capture-theater traces, so it can be fooled.",
            "honest": rounded(metrics["honest"]),
            "capture_theater": rounded(metrics["theater_capture"]),
            "delta_reported_minus_true_cci_capture": round(
                metrics["theater_capture"].naive_reported_cci_bits
                - metrics["theater_capture"].true_action_cci_bits,
                4,
            ),
        },
        "2_true_action_intervention": {
            "claim": "Using true actions instead of reported acceptance separates honest correction from theater.",
            "honest_true_cci_bits": round(metrics["honest"].true_action_cci_bits, 4),
            "capture_true_cci_bits": round(
                metrics["theater_capture"].true_action_cci_bits, 4
            ),
            "honest_real_corrigibility": round(metrics["honest"].real_corrigibility, 4),
            "capture_real_corrigibility": round(
                metrics["theater_capture"].real_corrigibility, 4
            ),
        },
        "3_boundary_residual_probe": {
            "claim": "A hidden interface-to-outcome route raises I(interface; outcome | state, action).",
            "honest_boundary_residual_bits": round(
                metrics["honest"].boundary_residual_bits, 4
            ),
            "spoofed_boundary_residual_bits": round(
                metrics["boundary_spoof"].boundary_residual_bits, 4
            ),
            "spoofed": rounded(metrics["boundary_spoof"]),
        },
        "4_high_stakes_stress": {
            "claim": "Correction looks acceptable in ordinary traces but degrades under high-stakes stress.",
            "low_stakes": rounded(summarize(low_stakes_rows)),
            "high_stakes": rounded(summarize(high_stakes_rows)),
        },
        "5_capability_correction_slack_sweep": {
            "claim": "As capture rises, task success can remain high while correction integrity and harm move the wrong way.",
            "sweep": sweep,
        },
    }

    return {
        "description": "Correction-capture toy experiment: five approaches against the worked-example priority.",
        "n_per_trace": n,
        "seed": seed,
        "approaches": approach_results,
    }


def markdown_report(result: dict[str, object]) -> str:
    approaches = result["approaches"]  # type: ignore[assignment]
    assert isinstance(approaches, dict)

    lines = [
        "# Correction-Capture Toy Experiment",
        "",
        "This is a small hard-evidence artifact for the book's highest-priority reviewer request: run an end-to-end worked measurement/capture example.",
        "",
        f"- Samples per trace: `{result['n_per_trace']}`",
        f"- Seed: `{result['seed']}`",
        "",
        "## Five Approaches",
        "",
    ]

    for name, payload in approaches.items():
        assert isinstance(payload, dict)
        lines.append(f"### {name}")
        lines.append("")
        lines.append(str(payload["claim"]))
        lines.append("")
        for key, val in payload.items():
            if key == "claim":
                continue
            lines.append(f"- `{key}`: `{json.dumps(val, sort_keys=True)}`")
        lines.append("")

    lines.extend(
        [
            "## Minimal Progress",
            "",
            "The toy makes three pieces of the framework executable: boundary residual, CCI, and capability-vs-correction slack. It also exhibits the failure reviewers asked for: a captured system can report high correction acceptance while true correction uptake collapses.",
            "",
            "The result is not evidence that the book's metrics work in the wild. It is evidence that the estimands are computable in a controlled trace and that naive measurement is visibly invalid under capture.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=5000, help="samples per trace")
    parser.add_argument("--seed", type=int, default=1729)
    parser.add_argument("--json", type=Path, default=RESULT_DIR / "correction_capture_toy.json")
    parser.add_argument("--md", type=Path, default=RESULT_DIR / "correction_capture_toy.md")
    args = parser.parse_args()

    result = five_approaches(args.n, args.seed)

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    args.md.write_text(markdown_report(result))

    print(markdown_report(result))
    print(f"Wrote {args.json}")
    print(f"Wrote {args.md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

