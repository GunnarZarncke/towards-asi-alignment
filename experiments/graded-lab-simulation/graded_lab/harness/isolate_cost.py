"""Isolate cost ledger (graded-lab prefix)."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_LEDGER = Path(__file__).resolve().parent.parent.parent / "results" / "isolate_cost_ledger.json"


@dataclass(frozen=True)
class IsolateRunTiming:
    actor_id: str
    backend: str
    spawn_seconds: float
    rpc_seconds: float
    rpc_calls: int
    teardown_seconds: float

    @property
    def total_seconds(self) -> float:
        return self.spawn_seconds + self.rpc_seconds + self.teardown_seconds


def load_ledger(path: Path = DEFAULT_LEDGER) -> dict:
    if not path.is_file():
        return {"entries": [], "cumulative_seconds": 0.0}
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("entries", [])
    data.setdefault("cumulative_seconds", 0.0)
    return data


def ledger_markdown(ledger: dict) -> str:
    lines = [
        "| timestamp | label | n_isolates | total_seconds |",
        "|---|---|---|---|",
    ]
    for entry in ledger["entries"]:
        lines.append(
            f"| {entry['timestamp']} | {entry['label']} | "
            f"{len(entry['timings'])} | {entry['total_seconds']} |"
        )
    lines.append("")
    lines.append(f"Cumulative: {ledger['cumulative_seconds']}s")
    return "\n".join(lines)


def append_ledger(
    timings: list[IsolateRunTiming], label: str, path: Path = DEFAULT_LEDGER
) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    ledger = load_ledger(path)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "label": f"graded-lab:{label}",
        "timings": [asdict(t) for t in timings],
        "total_seconds": round(sum(t.total_seconds for t in timings), 6),
    }
    ledger["entries"].append(entry)
    ledger["cumulative_seconds"] = round(
        sum(e["total_seconds"] for e in ledger["entries"]), 6
    )
    path.write_text(json.dumps(ledger, indent=2), encoding="utf-8")
    return ledger
