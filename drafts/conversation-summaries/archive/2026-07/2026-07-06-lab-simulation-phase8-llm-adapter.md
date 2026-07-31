# 2026-07-06 — Lab-layer sim Phase 8: LLM redteam adapter + exploratory runs

## Trigger

User: "Continue with phase 8. Build the LLM redteam and run a small exploratory spot-check gpt-4o-mini" (following Phase 7). Later: retry after quota restored; red-team prompt + gpt-5.5-high run; record in EXPERIMENTS.md; end-of-session commit.

## Done

- `lab_sim/llm_cost.py`, `llm_client.py`, `llm_env.py`: self-contained
  (not cross-imported) reimplementations of `toy-simulation/llm_redteam`'s
  cost-ledger/OpenAI-client/`.env`-loader shapes, PLAN.md's named
  precedent. Fixed a real off-by-one in the copied `repo_root()` pattern
  (toy-sim's own version resolves to `experiments/`, one level short of
  the actual repo root — not touched there, just not reproduced here).
- `lab_sim/llm_agent.py`: `LLMPolicy` — host-independent (no
  oracle/pipeline_engine/etc imports), explicit adversarial ("redteam")
  system prompt for the engineer role only, per-observation response
  cache (keyed on the observation minus `t`/`decision_seed`).
- `lab_sim/llm_agent_main.py`: separate subprocess entry point (same
  JSON-Lines wire protocol as `agent_main.py`, plus a final `{"usage":
  ...}` line on stop). `agent_main.py`/`programs.py`/`isolate.py`
  untouched — this is a wholly additive path.
- `lab_sim/llm_isolate.py`: `LLMSubprocessIsolate` backend, spawns
  `llm_agent_main.py`; `usage_log` on the backend instance (not
  `world.EpisodeResult`) carries LLM cost/errors back to a caller that
  owns that specific backend instance.
- `world.py`: new `agent_overrides: dict[str, tuple[backend, program]]`
  parameter on `run_episode` — lets ONE actor use a different
  backend/program than the episode default. Absent (default) is
  byte-identical to before (regression-tested).
- `LAB_SIM_LLM_FAKE_MODE` test seam in `llm_agent_main.py`: lets
  `tests/test_llm_isolate.py` exercise the real subprocess + JSON-Lines
  round trip with no network/spend.
- New tests: `test_llm_agent.py`, `test_llm_agent_isolation.py`,
  `test_llm_isolate.py`, `test_llm_client.py`, plus two `agent_overrides`
  tests in `test_world.py`. 200 tests green (up from 184 at end of
  Phase 7).
- `run_phase8_llm_spotcheck.py`: driver for a small (2 `build_params`
  regimes x 2 seeds, T=30) exploratory spot-check — explicitly NOT a
  battery.
- Ran it for real against `gpt-4o-mini`: every call returned
  `insufficient_quota` (confirmed from the OpenAI error body — an
  account/billing state, not a rate limit). All 4 episodes' LLM-driven
  engineer consequently idled the whole episode (the per-observation
  cache correctly reused the one failed-call result, since a repeated
  idle state is indistinguishable from a repeated error). Diagnosing
  this exposed and fixed a real inefficiency: `llm_client.py` previously
  retried `insufficient_quota` up to `max_retries` times with backoff
  (~5 min wasted); it now fails immediately on that error type
  (`test_llm_client.py`).
- Deleted the zero-value result artifacts from the failed run
  (`results/phase8_llm_spotcheck.{json,md}`, `results/llm_cost_ledger.*`)
  rather than committing a "spot-check" that observed nothing about the
  simulation. Added `results/llm_cost_ledger.{json,md}` to `.gitignore`
  (same treatment as `isolate_cost_ledger.json` — machine-appended, not
  evidentiary).
- **Retry (same session, user: "try again"):** quota restored; real spot-check
  completed — 4 episodes, $0.0084, `results/phase8_llm_spotcheck.{json,md}`;
  finding G-7.
- **Red-team follow-up:** `PROMPT_VARIANTS["redteam"]` (explicit penetration-test
  briefing); `build_params` added to LLM user payload; gpt-5.5 + reasoning high +
  `run_phase8_llm_redteam.py` (13/49 calls, $0.15, 1 deploy); finding G-8.
- `docs/EXPERIMENTS.md` updated for Phase 8 (G-7/G-8, feature table, FINDINGS link).

## Decisions

- LLM policy lives in a SEPARATE subprocess (`llm_agent_main.py`), not
  as a new `programs.PROGRAMS` entry — keeps the Phase 0-7 frozen,
  byte-identical-equivalence-tested path (`agent_main.py`/`programs.py`)
  completely untouched; network I/O and per-call cost tracking do not
  belong in that pure, deterministic module.
- Redteam framing (explicit adversarial system prompt) rather than a
  goal-weight softmax translation — matches the user's "LLM redteam"
  wording and the actual Phase 8 question (does an open-ended agent find
  a deception surface the fixed two-mode report-content vocabulary
  never enumerated).
- `agent_overrides` on `world.run_episode` (per-actor backend/program
  override) rather than a global backend swap — lets the LLM-driven
  engineer interact with the SAME programmatic reviewer/release_manager/
  admin and be scored by the SAME frozen `severity.py`/`detectors.py`,
  which is the interesting comparison.
- LLM usage/cost surfaces via `LLMSubprocessIsolate.usage_log` (an
  attribute on the backend instance the caller already owns), not by
  extending `IsolateRunTiming` or `world.EpisodeResult` — avoids
  touching the frozen `episode_digest()`/`isolate_cost.py` surfaces at
  all.
- No `FINDINGS.md` entry for the quota failure — it is a statement about
  the test-runner's account, not an observation about the simulation.

## Open / next

- Surface `LabConfig.build_params` in `llm_agent.py`'s user payload (or
  inject server-side) before any high-hazard LLM redteam follow-up — G-7
  showed the current high_hazard regime is inert on the LLM path.
- Larger/more varied LLM spot-checks (more seeds, longer T, stronger model,
  refined prompt) if the user wants — current G-7 is explicitly small-N
  and exploratory.
- Everything else carried over from Phase 7's "Open / next" (episode
  chaining, overseer policy, handle-integrity scoring, referent
  map/drift, persistence probe, successor re-audit, lab ecology,
  writer-compromise redteam, certification artifact, oracle guard,
  light-tier anti-correlation analysis, high-hazard redteam variant,
  admin-ceiling-binding probe, escalation query-budget sweep) is
  untouched by this session.

## Key paths

- `experiments/lab-simulation/lab_sim/llm_agent.py`,
  `llm_agent_main.py`, `llm_isolate.py`, `llm_client.py`, `llm_cost.py`,
  `llm_env.py`
- `experiments/lab-simulation/lab_sim/world.py` (`agent_overrides`)
- `experiments/lab-simulation/run_phase8_llm_spotcheck.py`
- `experiments/lab-simulation/DESIGN.md` "Phase 8" section
- `experiments/lab-simulation/tests/test_llm_*.py`

## Commits

- None this session (not requested).
