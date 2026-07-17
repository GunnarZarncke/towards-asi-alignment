# 2026-07-17 — Graded lab GL-73: v3 grown ecology freeze

## Trigger
User: **continue** after valid grower round 2 all-pass (GL-72) — promote canonical freeze.

## Done
- Copied `generated_ecology_v3_round2.*` → `generated_ecology_v3.{json,rationale.md,knowledge_base.md}`.
- Added `V3_GROWN_ECOLOGY_PATH` and `ecology_version="v3_grown"` in `substrate.py` ( `"v3"` still → slice-A reference fixture).
- `CODE_VERSION` → `graded-lab-0.38.0`; test pin updated.
- `test_ecology_path_for_version_v3_grown_is_frozen_grower_ecology` loads canonical JSON.
- Re-scored canonical at freeze: **all_passed true** (20 seeds).
- FINDINGS GL-73; README, BLIND_GENERATION, PLAN_v3, DESIGN current-version line.

## Decisions
- Freeze body = valid round 2 only; GL-71 voided branch stays archived, not promoted.
- Separate loader key `v3_grown` so engineering/reference batteries on `"v3"` are unchanged.

## Open / next
- Commit GL-73 artifacts (not done — user did not ask).
- Optional: Q1 machinery-transfer battery on frozen ecology via `ecology_override_path` / `v3_grown`.
- Growth protocol: 2 of ≤4 rounds used; further rounds only if implementer reopens growth.

## Key paths
- `experiments/graded-lab-simulation/generated_ecology_v3.json`
- `experiments/graded-lab-simulation/graded_lab/world_visible/substrate.py`
- `experiments/graded-lab-simulation/results/FINDINGS.md` (GL-73)

## Commits
- (pending)
