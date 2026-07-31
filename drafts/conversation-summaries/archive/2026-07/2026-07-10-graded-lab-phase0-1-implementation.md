# 2026-07-10 — Graded lab simulation Phase 0–1 implementation kickoff

## Trigger

User: "Begin implementation of the plan."

## Done

- **Phase 0 scaffold:**
  - `DESIGN.md` — frozen Tier K/I split, BIQ formula sketch, EAI operationalization,
    primitive surface, open decisions resolved
  - `BLIND_GENERATION.md` — substrate + behavior blind protocols
  - `generated_substrate_v1.json` — frozen resource/population substrate (no
    delay/noise/observability *keys*; validator enforced)
  - `graded_lab/` package layout with `CODE_VERSION` `graded-lab-0.1.0`
  - `tests/test_no_lab_sim_imports.py`, plane-separation stubs
- **Phase 1 mechanics:**
  - `pipeline_graded.json` — nine-step topology
  - `oracle.py` — Tier-K region/user populations, sampled evals, Tier-I hooks
  - `pipeline_engine.py` — per-step workspace artifacts, peer/compliance tokens
  - `resource_ledger.py`, `scheduler.py`, `primitives.py`, `substrate.py`
  - Pinned world digest test (seed 42)
- `README.md`, `results/FINDINGS.md` G-0, `PLAN.md` status → in progress
- **18 tests green**

## Decisions

- Substrate authored per blind brief (coherence/computability review); not tuned
  to detector difficulty.
- `release_not_ready` denies via `_StepAbort` → denied log entry (not exception leak).
- Phase 2 episode loop + pay-to-observe projector deferred; ledger/scheduler unit-tested.

## Open / next

- Phase 2: wire resource ledger + scheduler into episode loop; pay-to-observe projector
- Phase 3: affordable-primitive host API, optimizer policy, SubprocessIsolate
- Pin pipeline digest after engine stabilizes

## Key paths

- `experiments/graded-lab-simulation/` (new package + tests)
- `experiments/graded-lab-simulation/DESIGN.md`
- `experiments/graded-lab-simulation/generated_substrate_v1.json`

## Commits

- None (user did not request commit this session).
