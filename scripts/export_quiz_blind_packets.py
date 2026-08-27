#!/usr/bin/env python3
"""Write blinded quiz packets (no correct flags) under drafts/quiz-blind-packets/."""

from __future__ import annotations

import json
import random
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / "site/src/content/quiz/questions.yml"
OUT = ROOT / "drafts/quiz-blind-packets"


def _blind(q: dict) -> tuple[dict, list[str]]:
    """Opaque option ids, shuffled. Returns (packet item, correct packet ids)."""
    opts = list(q["options"])
    rng = random.Random(q["id"])
    rng.shuffle(opts)
    blinded_opts = []
    correct: list[str] = []
    for i, o in enumerate(opts):
        pid = f"o{i}"
        blinded_opts.append({"id": pid, "text": o["text"]})
        if o.get("correct"):
            correct.append(pid)
    item = {"id": q["id"], "prompt": q["prompt"], "options": blinded_opts}
    return item, correct


def main() -> int:
    questions = yaml.safe_load(BANK.read_text(encoding="utf-8"))["questions"]
    OUT.mkdir(parents=True, exist_ok=True)
    size = 28
    index = []
    all_keys: dict[str, list[str]] = {}
    for i in range(0, len(questions), size):
        chunk = questions[i : i + size]
        name = f"batch-{i // size + 1:02d}"
        packet = []
        for q in chunk:
            item, correct = _blind(q)
            packet.append(item)
            all_keys[q["id"]] = correct
        path = OUT / f"{name}.json"
        path.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        index.append({"batch": name, "n": len(packet), "ids": [q["id"] for q in chunk]})
        print(f"{name}: {len(packet)} -> {path}")

    (OUT / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    key_path = OUT / ".keys.json"
    key_path.write_text(json.dumps(all_keys, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote keys sidecar {key_path} (scorer only; solvers must not read this)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
