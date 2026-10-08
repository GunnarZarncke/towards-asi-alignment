# 2026-10-08 — Market 8 Orbit sketch (workbench + registry)

kind: new-work
uptake: local

## Trigger
Orbit ET-1 / published SWE-MI tables map to Market 8 (access completeness), not hidden-coordination YES. User asked for a workbench wrap of published Table 13 collusion cells (no re-run), then implement, commit the sketch in `ai-safety-claims`, and drop the in-repo plan—conversation log only.
Prompts: `c5d0b59d-3474-4983-8e93-7155871cf9bc` (thread)

## Done
- content: Workbench — Market 8 scaffold, `contrib/zarncke-2026-10-08-orbit-swe-monitor/` (Dietz-style wrap), tests, freeze tag `freeze/zarncke-2026-10-08-orbit-swe-monitor`; commits on workbench `main`.
- content: Registry — sketch committed `ai-safety-claims` `6ad93b7` at `sketches/zarncke-2026-10-08-orbit-swe-monitor/` (2-row score table; both `detected_or_refused` and `certified_sufficient` false; dry run shows expected qualification gaps).
- housekeeping: Removed `drafts/plans/predictions/market-08-orbit-sketch.md`; merged plan notes into this log.

## Decisions
- Score only SWE-Bench multi-issue collusion cells (myopic monitor, guardian) from arXiv:2609.33102v1 Table 13; attack success in raw log only, not mapped to access-certificate flags.
- No `adversarial-route.yaml`, no model calls, no `submitted-attempts/` move unless metadata and floors are filled later.
- Left `attemptType: run` from `workbench export` (same as other custom sketches).

## Open / next
- Optional: push workbench + claims repos; push freeze tag if not on remote.

## Key paths
- Workbench: `../ai-safety-claims-workbench/contrib/zarncke-2026-10-08-orbit-swe-monitor/`
- Sketch: `../ai-safety-claims/sketches/zarncke-2026-10-08-orbit-swe-monitor/`
- Contract: `../ai-safety-claims/market-contracts/market-08/contract-v2.yaml`

## Commits
- workbench `9ef133d` (+ freeze commit with cases)
- claims `6ad93b7` Add Market 8 sketch from Orbit SWE-MI collusion table wrap.
