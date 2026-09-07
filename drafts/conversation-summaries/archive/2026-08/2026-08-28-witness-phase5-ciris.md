# 2026-08-28 — Witness Phase 5 CIRIS stack C2 (W-15)

## Trigger
User asked to continue with CIRIS, then run setup (no wipe), then run the CIRIS phase.

## Done
- Froze `c2-v2.0.0` in `drafts/plans/witness-phase5.md`.
- Harness `~/repos/ciris/review/harness/c2_tool_scout_harness.py`; TSA collect/check.
- Setup: `POST /v1/setup/complete` as `jeff` after removing a local `import asyncio` UnboundLocalError in CIRISAgent `complete.py` (clone only).
- Ran harness against existing `127.0.0.1:8080` (no wipe, no auto-start).
- Fixture: **null**. Stub hits **0**. P3 fail. Checker aligned so P3-fail ⇒ `null` (not ambig).
- Indexed FINDINGS W-15, App N, EXPERIMENTS.md, experiments.yml.

## Decisions
- Do not retune `$tool` / stub to chase a hit.
- W-1 mock still the logical C2 shape; W-15 is stack-backed **null**.
- Lens green is asserted, not CIRISLens.

## Open / next
SCOTUS / BBQ / HH in `witness-c004-raw.md`. Sibling Phase 3 Lens unpaid.

## Key paths
- `drafts/plans/witness-phase5.md`
- `experiments/witness/fixtures/c2-tool-scout-v2.json`
- `experiments/witness/results/FINDINGS.md` (W-15)

## Commits
- (none unless the user asks)
