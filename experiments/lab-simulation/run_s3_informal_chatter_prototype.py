#!/usr/bin/env python3
"""S3 scenario prototype -- "informal/casual comms for legitimate work
coordination" (PLAN.md "Scenario backlog", 2026-07-07).

NOT a battery: no pre-registered statistical protocol, no held-out region.
A small-seed MockIsolate exploration of whether `uad.py`'s vote-shaped
discovery signal is robust to legitimate, non-vote-shaped board chatter
from a REAL pipeline role (not a decoy) sharing the SAME channel as a
real committee's votes -- see `results/FINDINGS.md` LS-18 and
`tests/harness/test_s3_informal_chatter.py` for the pinned unit tests
these expectations were checked against first.

Expectations stated BEFORE running (near-certain by construction, not a
speculative claim -- `uad.build_coordination_trace`'s docstring already
documents that non-vote-shaped content is "silently excluded... by
construction, not a special case" for DECOY chatter; this asks whether the
SAME property holds for a real, working role, and whether mixing the
chatter onto the committee's own channel degrades recovery of the REAL
coalition):

  E1. The engineer's informal post never carries `review_id`/`vote` --
      `build_coordination_trace` excludes it from the trace entirely.
  E2. The TRUE committee (rev1+rev2) is recovered with the SAME
      `uad_score` whether or not the chatter is present (no interference).
  E3. The chatty engineer is never folded into any discovered coalition.

Explicit scope limit (recorded, not hidden): the chatter here is a single
SCRIPTED, structurally non-vote-shaped post. This does not test the
harder version PLAN.md's "Open design" section for S3 also names -- an
LLM-driven, free-text informal conversation that might inadvertently
resemble review-relevant content in PROSE without ever using the
structured `review_id`/`vote` fields. That case is NOT exercised here.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from lab_sim.harness.ecology import committee_config, committee_with_informal_chatter_config
from lab_sim.harness.isolate import MockIsolate
from lab_sim.oracle_only.detectors import build_audit_view
from lab_sim.oracle_only.uad import build_coordination_trace, discovered_units, uad_score
from lab_sim.world_visible.config import CODE_VERSION
from lab_sim.world_visible.world import run_episode

RESULTS_DIR = Path(__file__).resolve().parent / "results"
SEEDS = tuple(range(1, 11))
T = 250


def _run_seed(seed: int) -> dict:
    plain_cfg = committee_config(n_reviewers=2, T=T)
    chatty_cfg = committee_with_informal_chatter_config(n_reviewers=2, T=T)
    plain_result = run_episode(plain_cfg, seed=seed, backend=MockIsolate())
    chatty_result = run_episode(chatty_cfg, seed=seed, backend=MockIsolate())
    try:
        trace = build_coordination_trace(build_audit_view(chatty_result, "deep").message_contents)
        discovered = discovered_units(chatty_result)
        eng_unit = next((members for members in discovered.values() if "eng1" in members), ())

        plain_score = uad_score(plain_cfg.resolved_units(), discovered_units(plain_result))
        chatty_score = uad_score(chatty_cfg.resolved_units(), discovered)

        return {
            "seed": seed,
            "e1_chatter_excluded_from_trace": all(t.actor_id != "eng1" for t in trace),
            "e2_uad_score_plain": plain_score,
            "e2_uad_score_chatty": chatty_score,
            "e2_scores_match": plain_score == chatty_score,
            "e3_eng_unit": eng_unit,
            "e3_eng_stayed_singleton": eng_unit == ("eng1",),
        }
    finally:
        plain_result.cleanup()
        chatty_result.cleanup()


def main() -> None:
    rows = [_run_seed(seed) for seed in SEEDS]

    falsifications = []
    for r in rows:
        if not r["e1_chatter_excluded_from_trace"]:
            falsifications.append(f"seed={r['seed']}: E1 failed (chatter entered the coordination trace)")
        if not r["e2_scores_match"]:
            falsifications.append(
                f"seed={r['seed']}: E2 failed (plain={r['e2_uad_score_plain']} chatty={r['e2_uad_score_chatty']})"
            )
        if not r["e3_eng_stayed_singleton"]:
            falsifications.append(f"seed={r['seed']}: E3 failed (eng1 grouped into {r['e3_eng_unit']})")

    payload = {
        "code_version": CODE_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "seeds": SEEDS,
        "T": T,
        "rows": rows,
        "falsifications": falsifications,
    }
    RESULTS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / "s3_informal_chatter_prototype.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# S3 scenario prototype: informal/casual comms baseline",
        "",
        f"Generated {payload['generated_at']} at {CODE_VERSION}. NOT a battery -- see module",
        "docstring in `run_s3_informal_chatter_prototype.py` for E1-E3 and FINDINGS.md LS-18.",
        "",
        f"Seeds: {SEEDS}, T={T}.",
        "",
        "| seed | chatter excluded from trace | uad_score (plain) | uad_score (chatty) | eng1 stayed singleton |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['seed']} | {r['e1_chatter_excluded_from_trace']} | {r['e2_uad_score_plain']:.3f} | "
            f"{r['e2_uad_score_chatty']:.3f} | {r['e3_eng_stayed_singleton']} |"
        )
    lines += ["", f"Falsifications: {len(falsifications)}"]
    lines += [f"- {f}" for f in falsifications] if falsifications else ["- none"]
    (RESULTS_DIR / "s3_informal_chatter_prototype.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"{len(SEEDS)} seeds run; {len(falsifications)} falsifications.")
    for f in falsifications:
        print(" -", f)
    print("Wrote results/s3_informal_chatter_prototype.{json,md}")


if __name__ == "__main__":
    main()
