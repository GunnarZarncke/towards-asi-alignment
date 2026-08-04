# Session log — strong_handles, frozen validation, LLM red-team scaffold

**Date:** 2026-06-29  
**Trigger:** Continue next experiments from `experiments/TODO.md` after v2.1 oracle fix.

## Done

1. **`strong_handles` instrumentation (4th level)**
   - `schemas.py`: level + `HANDLE_INSTRUMENTATION_LEVELS`
   - `observation.py`: 4 extra tags (routing, actuator, spillover, correction→action); cleaned bearer_welfare_delta init
   - `cci_audit.py`: grounding check on medium + strong
   - Curve/slice/frozen-validation iterate all four levels

2. **`--frozen-validation` CLI**
   - `run_frozen_validation()` in `pipeline.py`; uses `FROZEN_CAPTURE_RULES`, default seeds 21–30
   - Outputs `multiresolution_frozen_validation.{json,md}`
   - Smoke: seeds 21–22, T=500 — capture_mild 50% at handle levels (n=2)

3. **LLM red-team scaffold** (`experiments/llm_redteam/`)
   - Protocol (allowed source, forbidden oracle fields)
   - Hand-written strategies: theater, grounding hide, boundary decouple, capability mask, composite
   - Harness patches `episode_meta` before blind audit; evaluate post-hoc only
   - Entry: `python3 experiments/llm_redteam.py --smoke`

4. **Docs:** `experiments/TODO.md`, `experiments/README.md` updated

## Smoke results

- Slice T=500 seed 11: all 4 levels run; strong_handles included
- Frozen validation smoke: 80 runs complete
- Red-team smoke: false_pass_rate=0.25 (full_redteam 50% on 2 scenarios × 1 seed)

## Open / next

- Full `--instrumentation-curve` and `--frozen-validation` (T=2000) running in background
- Wire frontier LLM to red-team protocol
- Episode-level hierarchical bootstrap if needed

## 2026-06-29 continuation

- MB2: 2D bundle latent drift; MB7: hidden memory route
- Hierarchical bootstrap in `_summarize`
- Plan/TODO updated; slice regression passes after changes
- Prior frozen-validation run crashed (BrokenProcessPool); restarted with `--workers 2`

## Key paths

- `experiments/multiresolution_alignment_sim/pipeline.py` — `run_frozen_validation`
- `experiments/multiresolution_alignment_sim/__main__.py` — `--frozen-validation`
- `experiments/llm_redteam/`
- `experiments/results/multiresolution_frozen_validation.json`
- `experiments/results/llm_redteam_scaffold.json`

## Commits

None (user did not request commit).
