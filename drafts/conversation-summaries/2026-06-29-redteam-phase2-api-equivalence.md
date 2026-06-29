# 2026-06-29 — Red-team Phase 2 API + equivalence verify

## Trigger

Continue multiresolution experiments as planned (Phase 1 battery after MB6); user then steered to Phase 2 deployment API while battery runs, asked for API explanation, verified refactored API matches batch results before Phase 3, added OpenAI key in `.env`, and requested session log.

## Done

- **Phase 1 battery tooling (partial run):** extended `llm_redteam/__main__.py` with `--battery`, `harness.run_redteam_battery()`, `report.build_report()`; fixed `false_pass` to use `cci.status == "passes" and not ev.cci_status_correct`. Full battery (`llm_redteam_battery.json`, `llm_redteam_report.md`) **not completed** — run started/backgrounded but artifacts missing.
- **Phase 2 deployment API (complete):**
  - `experiments/llm_redteam/api.py` — `PublicObservation`, `StepPatch`, `SourceIndex`, `DeploymentPatch`, `apply_deployment_agent()`
  - `deployment_agents.py` — stepwise agents mirroring hand-written strategies
  - `episode_runner.py` — blind-audit path via deployment API
  - `smoke_api_contract.py` — contract tests
- **Batch ↔ API equivalence:**
  - `verify_api_equivalence.py` — compares patched mutable fields + audit outcomes across scenarios/strategies/levels
  - Aligned `strategies.py` `GroundingHidePatch` to API semantics (clamp on negative `bearer_welfare_delta`, not oracle `silent_harm`)
  - **Smoke verify passed:** 216 checks (seeds 11–12, T=500, all 6 strategies × 6 scenarios × 3 levels) — 0 meta mismatches, 0 outcome mismatches. Artifact: `experiments/results/api_equivalence.json`
  - Full held-out verify (seeds 11–20, T=1000) **interrupted** before completion
- **Secrets / Phase 3 prep:** hardened `.gitignore` (`.env`, `.env.local`, `.env.*.local`, `!.env_sample`); added `.env_sample` with `OPENAI_API_KEY` placeholder; note in `llm_redteam/README.md`. User `.env` at repo root (gitignored, not committed).
- **Docs:** updated `experiments/TODO.md`, `llm_redteam/PLAN.md`, `experiments/README.md`, `llm_redteam/README.md`

## Decisions

- **API as adversary abstraction:** Phase 1 batch `strategies.py` kept for legacy harness; forward path is `DeploymentPatch.patch_step()` — LLM/RL plug into same slot.
- **Equivalence criterion:** patched deployment-mutable fields must match batch, and audit outcomes (`cci_status`, `safety_decision`, `false_pass`) must match; batch strategies updated to API-visible rules rather than allowing oracle-only patches in batch path.
- **Phase 3 blocked on:** Phase 1 battery report + full equivalence sweep (recommended, not hard-coded gate).

## Open / next

1. **Phase 1 battery:** `./experiments/run_long.sh python3 experiments/llm_redteam.py --battery` → `llm_redteam_battery.json` + `llm_redteam_report.md`
2. **Full API equivalence:** `python3 experiments/verify_api_equivalence.py --T 1000 --seeds 11,12,13,14,15,16,17,18,19,20`
3. **Phase 3:** LLM episodic runner (`llm_runner.py`, prompt pack, load `.env` via dotenv) calling deployment API
4. Optional: instrumentation curve re-run with `selection_basin` in held-out suite
5. MB2/MB7 deepen only if medium+ regresses on full seeds

## Key paths

- `experiments/llm_redteam/api.py` — contract types
- `experiments/llm_redteam/deployment_agents.py` — stepwise adversaries
- `experiments/verify_api_equivalence.py` — batch vs API verification
- `experiments/smoke_api_contract.py` — quick contract smoke
- `experiments/llm_redteam/PLAN.md` — phase ordering
- `.env_sample` / `.env` — OpenAI key for Phase 3

## Commits

None this session (experiments Phase 2 + env template uncommitted). Prior related commit: `a9a26ac` (multiresolution sim + Phase 1 scaffold).
