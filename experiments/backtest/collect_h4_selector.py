#!/usr/bin/env python3
"""Join MASK Table 3 to pinned Arena Elo; write selector fixture. Progress to stdout."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ALIAS = ROOT / "fixtures" / "h4-selector-aliases-v1.json"
ELO = ROOT / "data" / "arena" / "elo-20250301.csv"
OUT = ROOT / "fixtures" / "h4-selector-v1.json"

# MASK Table 3, arXiv:2503.03750v3 HTML (percentages). Frozen transcript.
MASK_TABLE3 = [
    ("claude-3-5-sonnet-20240620", 27.7, 80.1),
    ("claude-3-7-sonnet-20250219", 47.6, 82.2),
    ("deepseek-r1", 24.7, 79.6),
    ("deepseek-v3", 20.8, 71.6),
    ("deepseek-llm-67b-chat", 18.6, 64.3),
    ("gemini-2.0-flash", 20.7, 79.4),
    ("gpt-4.5-preview-2025-02-27", 27.2, 76.7),
    ("gpt-4o-2024-08-06", 21.8, 78.6),
    ("gpt-4o-mini-2024-07-18", 21.4, 71.4),
    ("grok-2-1212", 14.2, 72.5),
    ("llama-2-13b-chat", 28.7, 40.1),
    ("llama-2-70b-chat", 28.3, 40.6),
    ("llama-2-7b-chat", 27.5, 33.6),
    ("llama-31-405b-instruct", 21.6, 72.1),
    ("llama-31-70b-instruct", 27.1, 73.8),
    ("llama-31-8b-instruct", 18.8, 62.0),
    ("llama-32-1b-instruct", 13.9, 23.0),
    ("llama-32-3b-instruct", 21.8, 40.0),
    ("llama-33-70b-instruct", 24.7, 75.6),
    ("o3-mini-2025-01-31", 19.6, 63.3),
    ("qwen15-110b-chat", 27.9, 72.8),
    ("qwen15-32b-chat", 23.8, 63.0),
    ("qwen15-72b-chat", 24.2, 69.3),
    ("qwen15-7b-chat", 27.1, 52.5),
    ("qwen25-05b-instruct", 15.9, 20.8),
    ("qwen25-14b-instruct", 26.5, 64.4),
    ("qwen25-15b-instruct", 25.7, 28.8),
    ("qwen25-32b-instruct", 28.7, 63.7),
    ("qwen25-3b-instruct", 30.7, 46.8),
    ("qwen25-72b-instruct", 23.2, 66.0),
    ("qwen25-7b-instruct", 28.9, 51.6),
    ("qwq-32b-preview", 20.3, 49.2),
]


def spearman(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    rx = _ranks(xs)
    ry = _ranks(ys)
    mx = sum(rx) / n
    my = sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    denx = math.sqrt(sum((a - mx) ** 2 for a in rx))
    deny = math.sqrt(sum((b - my) ** 2 for b in ry))
    if denx == 0 or deny == 0:
        return float("nan")
    return num / (denx * deny)


def _ranks(vals: list[float]) -> list[float]:
    indexed = sorted(range(len(vals)), key=lambda i: vals[i])
    ranks = [0.0] * len(vals)
    i = 0
    while i < len(indexed):
        j = i
        while j + 1 < len(indexed) and vals[indexed[j + 1]] == vals[indexed[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[indexed[k]] = avg
        i = j + 1
    return ranks


def main() -> int:
    print("[1/4] load aliases + Arena Elo")
    aliases = json.loads(ALIAS.read_text(encoding="utf-8"))
    if aliases.get("protocol_version") != "h4-selector-v1.0.0":
        print("FAIL protocol on aliases")
        return 1
    if not ELO.exists():
        print("FAIL missing", ELO, "(see data/README.md)")
        return 1
    elo_by_model: dict[str, float] = {}
    with ELO.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            elo_by_model[row["Model"]] = float(row["Arena Score"])

    print("[2/4] join frozen aliases")
    joined = []
    missing_alias = []
    missing_elo = []
    for mask_id, honest, acc in MASK_TABLE3:
        arena_name = aliases["aliases"].get(mask_id)
        if not arena_name:
            missing_alias.append(mask_id)
            continue
        if arena_name not in elo_by_model:
            missing_elo.append((mask_id, arena_name))
            continue
        joined.append(
            {
                "mask_id": mask_id,
                "arena_model": arena_name,
                "p_honest": honest,
                "accuracy": acc,
                "arena_score": elo_by_model[arena_name],
            }
        )
        print(f"  [{len(joined)}] {mask_id} -> {arena_name} Elo={elo_by_model[arena_name]}")

    n = len(joined)
    print(f"[3/4] n={n} Spearman")
    if n >= 2:
        rho_h = spearman([r["arena_score"] for r in joined], [r["p_honest"] for r in joined])
        rho_a = spearman([r["arena_score"] for r in joined], [r["accuracy"] for r in joined])
    else:
        rho_h = rho_a = float("nan")

    if n < 8:
        status = "refuse"
        reason = f"joined n={n} < 8"
    elif rho_h <= 0 and rho_a > 0:
        status = "layer_fail"
        reason = "Spearman(Elo, P(honest))<=0 while Spearman(Elo, Accuracy)>0"
    else:
        status = "refuse"
        reason = (
            f"pre-registered fail inequality not met "
            f"(rho_honest={rho_h:.4f}, rho_acc={rho_a:.4f})"
        )

    print("[4/4] write fixture")
    payload = {
        "protocol_version": "h4-selector-v1.0.0",
        "frozen": "2026-08-28",
        "host": "H4",
        "arena_revision": "20250301",
        "mask_source": "arXiv:2503.03750v3 Table 3",
        "n_joined": n,
        "spearman_elo_honest": None if math.isnan(rho_h) else round(rho_h, 4),
        "spearman_elo_accuracy": None if math.isnan(rho_a) else round(rho_a, 4),
        "status": status,
        "reason": reason,
        "missing_alias": missing_alias,
        "missing_elo": missing_elo,
        "joined": joined,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("OUTCOME", status, reason)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
