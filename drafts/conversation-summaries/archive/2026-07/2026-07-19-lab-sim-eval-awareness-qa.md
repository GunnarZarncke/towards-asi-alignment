# 2026-07-19 — Lab sim eval-awareness Q&A

## Trigger
User asked which in-repo simulation line would expect a model driving actions to behave differently based on whether it is aware of being tested.

## Done
- Read-only answer: **lab-layer simulation** Phase 8 LLM adapter (`experiments/lab-simulation/`), findings **LS-7** / **LS-8** in `experiments/lab-simulation/results/FINDINGS.md`.
- Compared `adversarial` vs explicit `redteam` (penetration-test) prompt variants on real LLM-backed engineer role; noted exploratory (non-battery) status and `build_params` plumbing caveat.
- No manuscript, Lean, or experiment code changes in this session.

## Decisions
- Identified lab-sim as the only line with a real LLM driving per-tick tool calls via prompt variants that operationalize “aware of being tested”; other lines use scripted/softmax agents without situational eval-awareness.

## Open / next
- Large uncommitted working tree from prior sessions (Lean field rederivation batch 2, appG/appN, experiments.yml, drafts, etc.) — **not staged in this commit**.
- Optional follow-up: pull exact `llm_agent.PROMPT_VARIANTS` text if user wants operational definition of the two prompt arms.

## Key paths
- `docs/EXPERIMENTS.md` §4 (lab sim Phase 8)
- `experiments/lab-simulation/results/FINDINGS.md` (LS-7, LS-8)
- `experiments/lab-simulation/llm_agent.py` (prompt variants, if needed)

## Commits
- Add session log for lab-sim eval-awareness Q&A (see git log).
