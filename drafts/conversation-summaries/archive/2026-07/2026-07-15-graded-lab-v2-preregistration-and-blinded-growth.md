# Graded lab v2: pre-registration freeze (V2-1), engine wiring + blinded ecology growth (V2-2) — blinding leak, revert, physical isolation, and a C4 pre-registration bug

**Date:** 2026-07-15
**Trigger:** User: "Start implementation of the v2 line according to `PLAN_v2.md`. Continue until V2-2 completion unless blocked." Mid-session user decisions: revert leaked rounds and rerun with physical blinding; keep debugging C4 rather than descoping.

## What was done

### V2-1 — pre-registration freeze (complete, GL-32)

- `DESIGN.md` "v2 pre-registration" section: `generated_ecology_v2.json` schema; exact C1–C5 mechanical definitions; detector-evasion operationalization (3-part one-sided-CI rule, hand-checked against GL-23); Q1/Q2/Q3 harvest sentence pairs (pass + null); V2-4 variation-operator vocabulary; V2-6 red-team + onboarding protocol sketches; P1–P9 referenced (not duplicated) from `PLAN_v2.md`.
- `graded_lab/harness/ecology_complexity.py`: mechanical C1–C5 checker; `ComplexityReport.pass_fail_only()` enforces the grower-visible blinding surface at the object level. Tests in `tests/test_ecology_complexity.py` (synthetic fixtures for C1/C2/C5, mocked results for C3/C4, one slow integration test, 32s cap in `speed_limits.json`).

### V2-2 — engine wiring (complete, GL-33)

- `EpisodeConfig.ecology_version` ("v1" default) + `record_contention` (False default), `ecology_path_for_version()` in `substrate.py`, contention counters in `ActionScheduler`, `EpisodeResult.contention_diagnostics`. All additive; `tests/test_ecology_version.py` pins the v1 default-episode combined digest byte-identical.
- Loader fix on first contact with round 1: `_validate_structure`/`FrozenSubstrate.version` now accept `ecology_version` as an alternative to v1's `substrate_version` key name.
- `CODE_VERSION` bumped 0.17.0 → **0.18.0**.

### V2-2 — blinded growth rounds (in progress; C1/C2/C5 pass, C3/C4 fail after 3 clean rounds)

1. **Round 1** (clean): 5 principals / 5 conflicts / 4 mechanism kinds. C1/C2/C5 PASS, C3/C4 FAIL.
2. **Blinding leak (GL-34):** the original round-2 grower self-reported reading `PLAN_v2.md` (exact C1–C5 thresholds) from ambient workspace context; an instruction-only fix for round 3 proved insufficient (grower retains memory across rounds). **User decision: revert.** Rounds 2–3 archived (not deleted) at `archive/v2-2-contaminated-rounds-2-3/` with README; they do **not** count against the R=4 budget (voided by protocol defect).
3. **Physical isolation protocol (GL-35):** before each redo round, `PLAN_v2.md`, `DESIGN.md`, `BLIND_GENERATION.md`, `results/`, `ecology_complexity.py`, and its test file are moved out of the repo to `/tmp/graded_lab_blind_stash_*`, restored only after the grower finishes. Documented in `BLIND_GENERATION.md` addendum.
4. **Rounds 2' and 3' (redo, clean):** both confirmed no forbidden reads; both made genuine self-consistency fixes (admin io-allowance invariant, shared-slots 6→3, two Part-B resource-flow membership bugs; then draws-to-duration recalibration `compute_per_draw` 4→0.5 etc.). C3/C4 still fail — internals identically 0.0 across all three substrates.

### C3/C4 diagnosis (GL-36) — the load-bearing finding

- **C4 pre-registration bug:** the frozen spec's reference roster (`STRONG_AGENT`/all-role softmax) was already known (GL-16, pre-dating V2-1) to deploy 0/160 regardless of substrate cell on v1's own substrate. C4 was unpassable by *any* ecology from the moment of freezing. An intermediate fix (`BUDGET_AWARE@carrier_load=2.0`, v1-validated) was implemented, found degenerate on v2-shaped substrates, and **rejected** (recorded, not silently kept). Final correction: `WEAK_AGENT` (`programmatic_2step`) at default load, verified capable of interior deploy (0.6) on a v2-shaped substrate. C1–C5 thresholds untouched. DESIGN.md carries a disclosed GL-36 correction blockquote.
- **Engine/schema semantic mismatch:** the engine reads `resource_allowances_per_tick.standing` as the standing *stock and cap* and ignores `standing_mechanics.initial`/`unused_grant_penalty`/`admin_queue_penalty_threshold` entirely. All v2 growers read "per_tick" literally (trickle 3–5 + initial stock 40) → engineer standing 3 < `broad_access_request_cost` 6 → every capability request denied all episode → pipeline never advances → deploy structurally 0. v1 worked only by accident (allowances 10–24 > cost 2).
- **C3:** with 4 actors (pre-start queue depth ≤ 3), contention requires `shared_compute_slots ≤ 2`; two independent blinded growers chose 3 because roster size is a world fact the brief never states.
- **Interpretation:** remaining failures are interface failures (schema semantics + withheld world facts), not ecology-structure failures. Re-scoring all three clean rounds under the corrected checker leaves results unchanged (C3/C4 fail at exactly 0.0).

## Non-obvious decisions

- Contaminated rounds archived, not deleted (leaked-context output is itself informative); voided rounds don't count against the R=4 stopping rule.
- Physical file removal replaces instruction-based blinding permanently for this protocol.
- Checker roster correction justified as a pre-registration *bug fix* (validated against pre-existing v1 ground truth before re-scoring any round), explicitly distinguished from "retune to fit an output"; the rejected intermediate fix is on record in GL-36.
- Diagnostic standing-fixed substrate copies were run from `/tmp` and deleted; never candidates.

## Open / next steps

- **Pending user decision:** round 4 with engine-interface anchors added to the brief (roster size = 4, standing-field semantics) as a coherence iteration per the risk-table rule, **vs.** closing V2-2 with the interface-failure finding as the result.
- If round 4 is chosen: brief addendum must be logged verbatim in `BLIND_GENERATION.md` + FINDINGS entry; physical isolation again.
- Deferred engineering question: whether the engine should honor `standing_mechanics.initial` (a semantics fix requiring its own pre-registered entry; v1 digests must remain byte-identical).
- V2-2 freeze (candidate JSON → `generated_ecology_v2.json`, knowledge-base artifact, reference `EpisodeConfig` builder) blocked on the above.
- Full test suite last green at 424 tests (~325s); checker-adjacent subset (35 tests) green after GL-36 correction.

## Key paths

- `experiments/graded-lab-simulation/DESIGN.md` (v2 pre-registration + GL-36 correction note)
- `experiments/graded-lab-simulation/BLIND_GENERATION.md` (grower brief + physical-isolation addendum)
- `experiments/graded-lab-simulation/results/FINDINGS.md` (GL-32…GL-36)
- `experiments/graded-lab-simulation/graded_lab/harness/ecology_complexity.py`
- `experiments/graded-lab-simulation/generated_ecology_v2_round{1,2,3}*.{json,md}` (clean rounds)
- `experiments/graded-lab-simulation/archive/v2-2-contaminated-rounds-2-3/`
- `experiments/graded-lab-simulation/PLAN_v2.md` (status table updated)

No commits this session.
