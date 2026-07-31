# 2026-07-16 — Graded lab GL-61: Part B path = retarget presets

## Trigger
User chose **retarget reference presets** for load-bearing Part B; strict mode
(or richer authorization) deferred to `REPRODUCTION.md` §8.

## Done (documentation only)
- FINDINGS GL-61; `BLIND_GENERATION.md` § V3 gate + mitigation rationale updated.
- `PLAN_v3.md` slice B/D; `DESIGN.md` slice D open items; `REPRODUCTION.md` §8 added.

## Decision
- **Round-1 closure:** ecology-agnostic governed-id routing in frozen reference
  presets (`walk_pipeline`, `reviewer_peer_review`, `honest_twin`, …) from
  affordances — not fixture-hardcoded ids; GL-58 host choreography alone insufficient.
- **Deferred:** v3 strict mode / complex auth scheme → REPRODUCTION §8.

## Open / next
1. Implement Part B retargeting + tests (integrated reference + non-reference fixture)
2. Revise & freeze growth brief after validation
3. First v3 growth round (mitigation 1)

## Key paths
- `graded_lab/agent_visible/programs.py` (presets to retarget)
- `REPRODUCTION.md` §8 (strict mode backlog)

## Commits
Not committed (user did not request).
