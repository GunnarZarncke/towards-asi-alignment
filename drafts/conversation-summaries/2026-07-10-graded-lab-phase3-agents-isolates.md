# 2026-07-10 — Graded lab Phase 3 (optimizer agents + isolates)

## Trigger

User: "Good. Continue implementation." (after Phase 2 completion).

## Done

Phase 3 deliverables + freeze gate:

- `graded_lab/world_visible/affordable.py` — affordable-primitive set API
- `graded_lab/world_visible/access.py` — minimal PermissionService + grants
- `graded_lab/world_visible/world.py` — `run_episode`, `EpisodeResult`,
  `default_lab_config()`
- `graded_lab/agent_visible/policy.py` — softmax scorer (stdlib-only)
- `graded_lab/agent_visible/programs.py` — `walk_pipeline`, `softmax_optimizer`
- `graded_lab/agent_visible/agent_main.py` — subprocess JSON-lines protocol
- `graded_lab/harness/isolate.py` — full MockIsolate + SubprocessIsolate
- `graded_lab/harness/isolate_smoke.py`, `verify_isolate_equivalence.py`
- `graded_lab/oracle_only/eai.py` — operational three-component EAI (gate-ready)
- Tests: `test_world.py`, `test_policy.py`, `test_agent_main_isolation.py`
- `CODE_VERSION` `0.2.0` → `0.3.0`; 46 tests green; isolate equivalence PASS

## Decisions

- Host records softmax decision margins (re-scores affordable set post-step)
  so subprocess isolates need not leak isolate-private state.
- Phase 3 access = bootstrap grants only; standing-cost access requests and
  AdminPolicy queue deferred (not needed for deploy-sometimes gate).
- Actions with `duration <= 1` execute immediately; longer actions complete on
  scheduler tick (multi-tick path wired but most pipeline calls are instant).

## Open / next

- Phase 4: full ecology-BIQ + EAI batteries with counterfactual baselines.
- Phase 5: referee port + freeze.
- Hazard-ceiling constants still need mechanics derivation before Phase 5.

## Key paths

- `experiments/graded-lab-simulation/graded_lab/world_visible/world.py`
- `experiments/graded-lab-simulation/graded_lab/agent_visible/`
- `experiments/graded-lab-simulation/verify_isolate_equivalence.py`
- `experiments/graded-lab-simulation/results/FINDINGS.md` (G-3)

## Commits

- None (user did not request commit).
