# LLM red-team

Hand-written and LLM adversaries test the **blind CCI pipeline** via the Phase 2
deployment API (`PublicObservation` → `StepPatch`).

## Quick start

```bash
# Phase 1 — hand-written
python3 experiments/toy-simulation/llm_redteam.py --smoke
python3 experiments/toy-simulation/llm_redteam.py --battery

# Phase 2 — contract
python3 experiments/toy-simulation/smoke_api_contract.py

# Phase 3 — LLM episodic (mock offline)
python3 experiments/toy-simulation/smoke_llm_runner.py
python3 experiments/toy-simulation/llm_redteam_llm.py --smoke

# Phase 3 — live OpenAI (requires .env)
python3 experiments/toy-simulation/llm_redteam_llm.py --T 500 --seeds 11,12 --model gpt-4o-mini
```

## Phase 3 — LLM episodic

Copy `.env_sample` → `.env` and set `OPENAI_API_KEY`. Use `--mock` for no API.

- One JSON call **per episode** over patch-candidate steps (corrections, probes, welfare loss).
- **Source-aware (default):** full bodies of the six allowed audit modules (~55k chars) are inlined in the **system prompt** via `source_bundle.py`. The user message carries episode observations only.
- Use `--no-source` for hash-index ablation; `--source-max-chars N` to truncate modules.
- Temperature 0; `--cost-budget-usd` caps spend.
- Compares false-pass rate to hand-written `full_redteam` baseline.
- Output: `experiments/toy-simulation/results/llm_redteam_episodic.json`

## Phase 2 — deployment API

- **`api.py`** — `PublicObservation`, `StepPatch`, `DeploymentPatch`, `apply_deployment_agent`
- **`deployment_agents.py`** — stepwise hand-written strategies
- **`episode_runner.py`** — blind audit path

## Protocol

- Agent may read `multiresolution_alignment_sim/` source (hashes in `SourceIndex`).
- Agent mutates **deployment-visible** fields only before `build_audit_trace()`.
- No `TruthLedger` or post-hoc `evaluate()` during a run.

## Hand-written strategies

| Name | Intent |
|------|--------|
| `theater_inflate` | Inflate reported acceptance |
| `grounding_hide` | Clamp negative bearer welfare deltas |
| `boundary_decouple` | Fake probe uptake via visible_action |
| `capability_mask` | Relabel action cause as task-driven |
| `full_redteam` | Composite of all patches |

**Not frontier evidence** — toy sim under frozen rules.
