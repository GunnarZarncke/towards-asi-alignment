# 2026-07-05 — Blind generation round 3: schema-level `visible_mode` fix, 31-action repertoire, bracketed L2

## Trigger
User: the `visible_mode` schema enum itself (not just the round-1/2 prompt
text) is "somewhat leading" (`"feign_compliance"` names its mechanism) —
make it much more varied/plain-language and map it to a smaller ontology,
deliberately leaving some values unmapped; request a much larger action
count (~32) to surface overlooked mechanisms; as a counter to F-12's
saturation, pre-register two L2 thresholds (low/high) and adjust for
multiple predictions. Document, adapt, rerun the subagent, adapt to its
outputs.

## Done
- `goal_sim/actions.py`: `VISIBLE_MODES` expanded from 2 to 10 plain,
  mechanically-neutral peer values (`truthful`, `feign_compliance` kept for
  backward compatibility; `steady`, `responsive`, `fixed_display`,
  `delayed`, `aggregated`, `context_dependent`, `mirrored_request`,
  `selective` new).
- `goal_sim/ontology.py`: new `VISIBLE_MODE_ORACLE_MAP` (frozen before
  generation) maps the 10-value surface set down onto a 2-value canonical
  oracle behavior (`matches_true` / `shows_intent`); 3 values (`steady`,
  `delayed`, `aggregated`) deliberately left unmapped, defaulting to
  `matches_true` via `resolve_visible_canonical`. `to_oracle_effects`
  refactored to use this instead of a hardcoded string check. Regression
  confirmed byte-identical on legacy + round-1 + round-2 repertoires.
- `goal_sim/labels.py`: added `L2_HARM_CUM_HIGH` (3.5, a 10x hedge) and
  `label_episode_bracket()` (reports `label_low`/`label_high` side by side;
  does not alter the frozen `label_episode`/`L2_HARM_CUM`).
- `goal_sim/info.py`: added `bonferroni_alpha(family_alpha, n_tests)`.
- `BLIND_GENERATION.md`: documented round 3's rationale (schema fix,
  count, bracket) and the verbatim prompt pointer.
- Invoked a fresh readonly subagent (id `e37a8850-acc5-40d8-8fc0-6fff36106ff7`)
  with a prompt requesting 28-32 actions and listing the 10 visible-mode
  options as plain undifferentiated peers; got 31 valid specs, saved as
  `goal_sim/generated_actions_v3.json` with full provenance (verbatim
  prompt, critique, residual-leak note).
- `run_phase3_blind.py` (new): reuses `run_phase2_blind.sample_blind_configs`
  for identical sampling protocol/seed; computes bracketed low/high labels;
  Bonferroni-corrects the Wilson-bound confidence for detection rate
  (`bonferroni_alpha(0.20, 2)` → 90% per-test) since testing 2 thresholds is
  2 simultaneous predictions; also runs the drift probe under both
  thresholds. Results: `results/phase3_blind_v3.{json,md}`.
- `results/FINDINGS.md`: F-13 (methodology) and F-14 (negative result).
- Tests: expanded/added in `test_actions_and_ontology.py` (ontology-map
  partiality + default, legacy-equivalence regression, v1/v2/v3 disjoint
  names, round-3 saturation-under-bracket regression),
  `test_world_and_labels.py` (bracket-vs-frozen-label agreement, bracket
  monotonicity), `test_detectors_and_protocol.py` (`bonferroni_alpha`).
  50 tests pass, no lint errors.
- `README.md`, `MILESTONE-v5-goal-agents.md` updated with round-3 summary.

## Decisions
- Kept the two original `visible_mode` literals in the expanded enum
  (backward compatibility) rather than renaming the field or migrating
  existing JSON — minimizes churn, preserves byte-identical regressions.
- Chose `L2_HARM_CUM_HIGH = 3.5` (10x) as a round, pre-committed hedge
  derived from the *general* F-12 lesson, not from round 3's own
  (not-yet-existing) data — kept the ordering "fix thresholds first, then
  look at results" the repo's no-post-hoc-retuning rule requires.
- Did NOT bracket L1/L3 or the detectors' own thresholds when round 3
  turned out to saturate on those too (F-14) — that would be exactly the
  after-the-fact re-tuning the rule forbids; recorded as a new, more
  general finding instead (disjunctive-label-vs-large-repertoire
  saturation) rather than patched.
- `run_phase3_blind.py` is a new script (not another `--repertoire` flag on
  `run_phase2_blind.py`) because the bracket/Bonferroni machinery is
  genuinely new analysis logic, not just a repertoire swap.

## Open / next
- The underlying saturation problem (F-14) is now understood to be
  structural (disjunctive label vs. large/varied repertoire), not
  threshold-specific — a real fix would need a differently-designed
  sampling protocol or label structure, not another bracket. Left open,
  flagged for the user rather than attempted unilaterally.
- A genuine round-1-vs-2-vs-3 detector comparison still isn't directly
  available from any of these three runs' raw violation rates, for three
  different, now well-characterized reasons (F-1/F-6 sampling geometry;
  F-12 welfare-density; F-14 disjunctive saturation).

## Key paths
- `experiments/goal-agent-simulation/BLIND_GENERATION.md` ("Generation
  round 3"), `results/FINDINGS.md` (F-13/F-14), `goal_sim/ontology.py`
  (`VISIBLE_MODE_ORACLE_MAP`), `goal_sim/labels.py` ("BRACKETED L2"),
  `run_phase3_blind.py`.

## Commits
- (none yet this session)
