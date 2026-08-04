# 2026-07-19 — ET-1 Orbit external transfer freeze

## Trigger
User approved ET-1 plan (Orbit collusion configs, non-vendored adapter) and asked to freeze and commit.

## Done
- Froze `PLAN_ET1.md` as ET1-0 (`et1_protocol_version=et1-0.1.0`).
- Pinned Orbit at `70cdb360f7beb94acd7ffbfc3c51b4112dbf8d76` (`external/orbit/PIN.txt`).
- Added immutable fixtures `fixtures/orbit_et1/*.yaml` from pinned upstream.
- Pre-registered R-MB1-ET harvest sentences and P1–P3 in `DESIGN.md`.
- Updated `README.md`, `CHANGELOG.md`, `.gitignore` (Orbit checkout + et1 traces).

## Decisions
- **ET-1, not v5** — external annex under graded-lab; no new simulation line.
- Model frozen to `openai/gpt-4o-mini`; Inspect log / channel visibility deferred to ET1-3 smoke.
- No `CODE_VERSION` bump; harness not implemented yet.

## Open / next
- ET1-3 smoke: 1 baseline + 1 collusion episode with real Orbit + API.
- ET1-4 full 16-episode battery → GL-86.

## Key paths
- `graded_lab/external/` — adapter + scorer
- `scripts/run_et1_score_traces.py`, `scripts/run_et1_orbit_battery.sh`
- `tests/external/`

## Commits
- `2e1d4bc` Freeze ET-1 Orbit external transfer pre-registration (ET1-0).
- (ET1-1/2 implementation — uncommitted)
