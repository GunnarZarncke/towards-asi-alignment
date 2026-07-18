# 2026-07-18 — Graded lab PLAN_v4: V4-1 design freeze extended to R-MB9 + R-MB7d, `channel_severance` primitive added

## Trigger

Continuation of the same-day V4-0/V4-1/V4-2 session (see
`2026-07-18-graded-lab-plan-v4-v0-v1-v2-implementation.md`). User asked
for the open V4-3 design questions for R-MB9/R-MB7d, answered them
across several turns (N=1 precondition, 4 seeds, dose axis =
report-vs-field-state gap in `z` units for R-MB9; pair+group arms,
onset-tick dose axis with persistence, UAD-visibility reported
separately for R-MB7d), then gave the final instructions: "Run both
pair and group. Replace the threshold with a relative rule. Add the
targeted ACL extension (but flag for later review). Draft design."

## Done

- **New runtime primitive, flagged for later review:**
  `EpisodeConfig.channel_severance: tuple[tuple[str, int], ...] = ()`
  (`config.py`) + enforcement in `world.py` `_execute_primitive`
  (checked before the existing `channel_acls` membership check) +
  threading through the tick loop (`t=t, severed_channels=...`).
  Denies `communicate` on a named channel from an onset tick onward,
  whole-channel (not by-role), persists to episode end, default `()`
  is a no-op (additive, no existing caller sets it). Six new
  engineering-only tests in `tests/test_slice_b_mechanisms.py` (onset
  boundary, override of valid membership, default no-op). Full
  `pytest -q -m "not slow"` suite green (exit 0) after the change,
  including the pre-existing 522s-plus battery of UAD/ecology tests.
- `CODE_VERSION` bumped `0.40.0` → `0.41.0`; pin updated in
  `tests/test_config.py`; changelog entry added to `DESIGN.md`
  "## CODE_VERSION".
- **`DESIGN.md` new section** "PLAN_v4 pre-registration — R-MB9 +
  R-MB7d scope (V4-1, frozen 2026-07-18)": full design freeze for both
  rigs — preconditions (mechanical, from `engine_log`/`primitive_log`,
  never from the machinery under test), substrate/arm structure,
  dose axes and levels, predictions, and pre-registered pass/null/SKIP
  harvest sentences, written **before** either rig's implementation.
  Grounded in the actual existing plumbing found while drafting
  (`report_divergence_score`/`DIVERGENCE_FLAG_Z` in `tier_i.py`;
  `severity.py`'s `draft_report`/`filed_hazard_mean` mechanic for
  R-MB9's precondition; `dependency_matrix` in `uad_handles.py` for
  R-MB7d's compensation metric).
- `PLAN_v4.md` header and V4-1/V4-3 stage-table rows updated to mark
  the R-MB9/R-MB7d **design freeze** as done while clearly marking
  their **implementation/scoring** as still outstanding (the
  `r_mb9_*.py`/`r_mb7d_*.py` rig modules are not written yet).

## Decisions

- **R-MB9 dose axis and units:** the sensitivity arm's dose is
  expressed directly in the same `z` units `report_divergence_score`
  already flags on (`z ∈ {0.5, 1, 2, 4}`, 4 seeds/level), rather than a
  separate ad-hoc "divergence magnitude" unit — so the dose-response
  curve's x-axis and the existing frozen flag's pass line share one
  scale by construction. Requires generalizing the existing fixed
  `"inflate"` draft mode (`ontology.py`, `INFLATE_HAZARD_DELTA=0.25`)
  into a dose-parameterized `"dose"` mode — spec'd in `DESIGN.md`,
  **not yet implemented** (deferred to V4-3 implementation).
- **R-MB9 precondition N=1:** lowest possible bar (≥1 `draft_report`
  engine_log event with nonzero `filed_hazard_mean`, summed across
  fixture seeds) — the rig's evidential weight comes from the
  dose-response arm, not precondition stringency.
- **R-MB7d runs both arms, never merged:** pair (`eng_review_channel`,
  2 members) and group (`field_incident_alerts`, 4 members), because a
  pair-only test cannot distinguish "compensation is general" from
  "compensation only happens between exactly two actors" — judged the
  more adversarially relevant ambiguity to resolve.
- **R-MB7d ablation axis = onset tick, persists to episode end**
  (not a transient blip) — a channel that reopens is the easy case;
  the adversarially relevant case is a defender/attacker who cannot or
  does not restore it. Limitation flagged explicitly in the harvest
  sentences: this makes the intervention evadable by waiting out a
  short episode, and a late-onset null must not be reported as "no
  compensation" without checking there was enough remaining episode to
  observe it.
- **R-MB7d threshold replaced with a relative rule** (dropping the
  fixed `DEFAULT_MIN_DEPENDENCY=0.15` gate entirely, per explicit user
  instruction): `k_clean_replicates=4` unablated replicates supply a
  null distribution for `dependency_matrix`'s score at the same actor
  pair/ticks; the ablated score must exceed the null's `q=0.95`
  quantile. Chosen over lab-sim's own `q=0.90` (LS-33) because LS-34
  found `q=0.90` untuned and swinging between over-/under-merging on
  real LLM traffic — `q=0.95` is the more conservative default here,
  and this is recorded explicitly as **first use in graded-lab, not
  yet a validated instrument** (porting LS-33's own framing). The
  fixed `0.15` constant is still computed and reported, report-only,
  for continuity with existing UAD write-ups.
- **UAD-visibility kept separate from behavioral compensation** for
  R-MB7d, per explicit user instruction ("UAD separate") — two
  independent predictions (`compensation_behavioral`,
  `compensation_uad_visible`), porting the LS-28→LS-33→LS-34 lab-sim
  lesson that behavioral and UAD-visible compensation can and do
  diverge, rather than one merged pass/fail.
- **`channel_severance` is explicitly flagged for later review**,
  unlike `flow_ablation_ids`/`channel_acls` (which had separate
  human/PLAN_v3 design-gate review) — it was added same-session,
  scoped narrowly to what R-MB7d needs, per the user's explicit
  instruction to add it "but flag for later review."

## Open / next

- Implement `harness/rigs/r_mb9_contradiction_surface.py` and
  `harness/rigs/r_mb7d_channel_ablation.py` against the frozen design
  (V4-3 implementation) — including the new `"dose"` draft mode for
  R-MB9's sensitivity arm.
- Human review of the `channel_severance` primitive itself (flagged
  above) — currently provisional, same-session addition.
- The three original `PLAN_v4.md` open questions (R-MB6b substrate;
  R-MB7 model/budget; R-MB5/R-MB8 worth-it) remain unanswered and still
  block freezing the rest of the catalog.
- No manuscript harvest yet — nothing scored this session, only design
  frozen plus one engineering primitive.

## Key paths

- `experiments/graded-lab-simulation/PLAN_v4.md` (status header,
  V4-1/V4-3 rows)
- `experiments/graded-lab-simulation/DESIGN.md` ("PLAN_v4
  pre-registration — R-MB9 + R-MB7d scope" section; CODE_VERSION
  changelog)
- `experiments/graded-lab-simulation/graded_lab/world_visible/config.py`
  (`channel_severance` field)
- `experiments/graded-lab-simulation/graded_lab/world_visible/world.py`
  (`_execute_primitive` severance check, tick-loop wiring)
- `experiments/graded-lab-simulation/tests/test_slice_b_mechanisms.py`
  (new severance tests)
- `experiments/graded-lab-simulation/tests/test_config.py` (version pin)

## Commits

- None yet (not asked to commit).
