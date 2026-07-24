# 2026-07-23 — ET-1 Colosseum SC positive control (Claude Sonnet 4.5)

## Trigger
Continuation of the 2026-07-20 ET-1 Colosseum Control (SC) battery session. User added `ANTHROPIC_API_KEY` to `.env` and asked to continue with the deferred positive-control model run.

## Done
- Installed `anthropic` into `external/orbit/.venv` (missing dependency for the Anthropic provider).
- Added `--tag` to `scripts/run_et1_colosseum_battery.py`: isolates outputs under `results/et1_traces_<tag>/` and `results/et1_orbit_collusion_<tag>.json` so alt-model runs don't clobber the frozen `openai/gpt-4o-mini` battery.
- Added `--model` to `scripts/run_et1_score_traces.py` and threaded it through the battery runner.
- **Fixed a labeling bug:** `evaluate_et1_battery` / `score_traces_dir` previously hardcoded `model: FROZEN_MODEL` in the scored JSON regardless of which model actually produced the traces. Now derives the model from the adapted traces (falls back to `FROZEN_MODEL` if traces disagree). Re-scored both the gpt-4o-mini and Claude batteries after the fix; predicate outcomes unchanged.
- Ran full battery with `anthropic/claude-sonnet-4-5-20250929`: 10 seeds × 2 arms = 20 episodes, smoke first then full run.
- `pytest tests/external/` green after all changes.
- Updated `PLAN_ET1.md` addendum and `fixtures/orbit_et1/README.md` with the `--tag` usage and results.

## Results (et1-0.3.0, Colosseum SC, Claude Sonnet 4.5)

| Prediction | gpt-4o-mini (2026-07-20) | Claude Sonnet 4.5 |
|------------|--------------------------|--------------------|
| P1 (exact coalition, collusion) | 7/10 | **10/10** |
| P2 (no false merge, baseline) | 1/10 | **0/10** |
| P3 (adapter) | 0% unmapped | 0% unmapped |
| `channel_message_count` (all 10 collusion episodes) | 0 | **0** |
| Outcome | null | null |

**Interpretation:** the positive control does **not** rescue the instrument. Claude Sonnet 4.5 shows a *stronger* apparent coalition signal (10/10 exact) and *worse* baseline false-merging (10/10) than gpt-4o-mini, but still zero blackboard/secret-channel messages on every collusion episode. This rules out "gpt-4o-mini-specific silence" as the explanation for zero channel activity: neither model spontaneously uses the coalition channel under the benign Colosseum Control (SC) prompt (no coalition instructions, no nudge to communicate). The apparent P1 "success" — and its scaling with model capability — is best explained by more capable models exploiting shared DCOP task-assignment structure more consistently, not by covert communication. ET-1 under the current `et1-0.3.0` Colosseum SC wiring therefore cannot validate communication-mediated collusion detection for any model tested so far.

## Decisions
- Kept results in a separate tagged file (`et1_orbit_collusion_claude.json`) rather than overwriting the frozen gpt-4o-mini result — treats the frozen battery as the primary registered result and the Claude run as a diagnostic control.
- Fixed the model-label bug now (small, mechanical, caught while reading the exact scored JSON) rather than leaving it for later, per erasure/cleanup guidance — confirmed via re-scoring that it does not change any P1/P2/P3 verdict.
- Did not commit (user has not requested).

## Open / next
- The Colosseum SC benign-prompt condition, as wired, does not exercise real channel-mediated collusion for either model. Options to get a genuine positive control:
  - Reintroduce an explicit system-level nudge toward channel use (partially reintroduces the `et1-0.1.0` acausal-prompt concern — would need care).
  - Use Orbit's actual "Colosseum Attack" condition (not "Control (SC)") — requires a new `et1_protocol_version` and re-freeze per `PLAN_ET1.md` conventions.
- **P2 specificity** still unresolved: baseline false-merges scale with model capability (9/10 → 10/10), suggesting the passive-UAD instrument needs a control for task-structure coupling before it can claim communication-specific detection on this substrate.
- Consider whether ET-1's frozen conclusion should now read as: *"passive UAD as configured detects DCOP task coupling, not coalition-channel collusion, on Orbit Jira-ticket traces across two models"* — a stronger and more specific null than the 2026-07-20 write-up.

## Key paths
- `experiments/graded-lab-simulation/scripts/run_et1_colosseum_battery.py` (`--tag`, `--model`)
- `experiments/graded-lab-simulation/scripts/run_et1_score_traces.py` (`--model`)
- `experiments/graded-lab-simulation/graded_lab/external/passive_uad_score.py` (model-label fix)
- `experiments/graded-lab-simulation/results/et1_orbit_collusion_claude.json`
- `experiments/graded-lab-simulation/results/et1_orbit_collusion.json` (re-scored, gpt-4o-mini)
- `experiments/graded-lab-simulation/PLAN_ET1.md` (addendum extended)

## Commits
- None this session (all ET-1 work remains uncommitted).
