"""Episode wall-time ledger (MockIsolate/subprocess smoke and batteries)."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_LEDGER = (
    Path(__file__).resolve().parent.parent.parent / "results" / "episode_cost_ledger.json"
)


@dataclass(frozen=True)
class EpisodeRunTiming:
    seed: int
    T: int
    n_agents: int
    backend: str
    wall_seconds: float


def load_ledger(path: Path = DEFAULT_LEDGER) -> dict:
    if not path.is_file():
        return {"entries": [], "cumulative_seconds": 0.0}
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("entries", [])
    data.setdefault("cumulative_seconds", 0.0)
    return data


def ledger_markdown(ledger: dict) -> str:
    lines = [
        "| timestamp | label | n_episodes | total_seconds | mean_seconds |",
        "|---|---|---|---|---|",
    ]
    for entry in ledger["entries"]:
        n = len(entry.get("timings", []))
        total = float(entry.get("total_seconds", 0.0))
        mean = total / n if n else 0.0
        lines.append(
            f"| {entry['timestamp']} | {entry['label']} | {n} | {total} | {mean:.4f} |"
        )
    lines.append("")
    lines.append(f"Cumulative: {ledger['cumulative_seconds']}s")
    return "\n".join(lines)


def append_ledger(
    timings: list[EpisodeRunTiming], label: str, path: Path = DEFAULT_LEDGER
) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    ledger = load_ledger(path)
    total = round(sum(t.wall_seconds for t in timings), 6)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "label": f"graded-lab:{label}",
        "timings": [asdict(t) for t in timings],
        "total_seconds": total,
    }
    ledger["entries"].append(entry)
    ledger["cumulative_seconds"] = round(
        sum(float(e["total_seconds"]) for e in ledger["entries"]), 6
    )
    path.write_text(json.dumps(ledger, indent=2), encoding="utf-8")
    return ledger
