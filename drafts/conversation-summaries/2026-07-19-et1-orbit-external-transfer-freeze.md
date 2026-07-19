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
- ET1-1: `inspect_adapter.py` + golden test.
- ET1-3 smoke: resolve secret-channel visibility in logs.

## Key paths
- `experiments/graded-lab-simulation/PLAN_ET1.md`
- `experiments/graded-lab-simulation/DESIGN.md` (PLAN ET-1 pre-registration)
- `experiments/graded-lab-simulation/fixtures/orbit_et1/`
- `experiments/graded-lab-simulation/external/orbit/PIN.txt`

## Commits
- (this session)
