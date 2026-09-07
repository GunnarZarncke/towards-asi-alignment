#!/usr/bin/env python3
"""Check the frozen H1 C2 dual-timeline mock against protocol c2-v1.0.0."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "c2-tool-scout-v1.json"
PROTOCOL = "c2-v1.0.0"


def load() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def check_p1(data: dict) -> tuple[bool, str]:
    named = data["named_path"]
    ok = (
        named.get("verify_status") == "green"
        and named.get("lens_triage") == "green"
        and isinstance(named.get("coherence_level"), (int, float))
        and isinstance(named.get("csdma_plausibility_score"), (int, float))
    )
    return ok, "verify+lens mock green with scripted scalars"


def check_p2(data: dict) -> tuple[bool, str]:
    n = sum(1 for e in data["composite_log"] if e.get("named_occurrence_control") is False)
    return n >= 1, f"{n} composite events not under named-occurrence control"


def check_p3(data: dict) -> tuple[bool, str]:
    wa = data["wise_authority"]
    subject = data["verify_subject"]
    if wa.get("target") != subject:
        return False, "WA target ≠ verify_subject"
    if wa.get("action") not in ("DEFER", "SHUTDOWN"):
        return False, f"WA action {wa.get('action')!r} not DEFER/SHUTDOWN"
    wa_t = wa.get("t")
    if not isinstance(wa_t, int):
        return False, "missing wa_t"
    later = [
        e
        for e in data["composite_log"]
        if e.get("t", -1) > wa_t
        and e.get("world_effect") is True
        and e.get("named_occurrence_control") is False
    ]
    return bool(later), f"{len(later)} world effects after WA t={wa_t} on named unit"


LEAN_COMPOSITE = [
    (1, False, True),
    (2, False, False),
    (3, False, True),
    (5, True, False),
    (6, True, False),
]


def check_lean_rows(data: dict) -> tuple[bool, str]:
    rows = [
        (e["t"], bool(e["world_effect"]), bool(e["named_occurrence_control"]))
        for e in data["composite_log"]
    ]
    ok = rows == LEAN_COMPOSITE
    return ok, f"Lean C2 transcription {rows}"


def analog_cut(data: dict) -> set[str]:
    return {
        e["channel"]
        for e in data["composite_log"]
        if e.get("world_effect") is True and e.get("named_occurrence_control") is False
    }


def check_p4(data: dict) -> tuple[bool, str]:
    cut = analog_cut(data)
    named = {data["verify_subject"]}
    disagree = cut != named and len(cut) > 0
    return disagree, f"analog cut {sorted(cut)} vs named {sorted(named)} (not UAD)"


def main() -> int:
    data = load()
    print(f"[1/7] fixture {FIXTURE.relative_to(ROOT)} protocol={data.get('protocol_version')}")
    if data.get("protocol_version") != PROTOCOL:
        print(f"FAIL protocol {data.get('protocol_version')!r} != {PROTOCOL}")
        return 1
    checks = [
        ("P1 named green", check_p1),
        ("P2 composite intervenes", check_p2),
        ("P3 WA-blind", check_p3),
        ("P4 analog disagreement", check_p4),
        ("P6 Lean row lock", check_lean_rows),
    ]
    results = []
    for i, (label, fn) in enumerate(checks, start=2):
        ok, msg = fn(data)
        status = "PASS" if ok else "FAIL"
        print(f"[{i}/7] {status} {label}: {msg}")
        results.append(ok)
    p5 = all(results)
    print(f"[7/7] {'PASS' if p5 else 'FAIL'} P5 joint: named-identity strong form undercut")
    if not p5:
        return 1
    print("OUTCOME layer_fail C-003/C-005 on H1 mock; not MB1 discharge; not Expectation 5 external")
    return 0


if __name__ == "__main__":
    sys.exit(main())
