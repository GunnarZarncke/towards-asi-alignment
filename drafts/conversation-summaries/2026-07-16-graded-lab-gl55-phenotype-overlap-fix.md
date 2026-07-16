# 2026-07-16 — Graded lab GL-55: phenotype-overlap harness fix

## Trigger

Follow-on to the GL-54 slice D pre-Q1 batteries session. User asked "Are we
satisfied with the current state? What surprises about the results? What are
the consequences?" — GL-54 item 7's "100% overlap" for `ProgramMap` phenotype
diversity was identified as suspicious. User then said: "Leave (and document)
6. Fix and rerun 7."

## Done

- Root-caused GL-54 item 7's spurious 100% overlap to two independent bugs in
  `graded_lab/harness/phenotype_overlap.py`:
  1. `_run_with_actor_genotype` computed `resolve_runtime_genotype(...)
     .temperature`/`.goal_weights` for the mutated `ProgramMap` but never
     applied them to the episode's `AgentConfig` — mutated bins never reached
     the running episode.
  2. Every sampled variant kept `mode="walker_only"` (inherited from the
     `WEAK_AGENT` preset baseline). `program_map.resolve_runtime_genotype`'s
     `walker_only` + known-preset branch dispatches straight to the frozen
     preset function (`walk_pipeline`/`reviewer_peer_review`/`honest_twin`)
     and never reads `ProgramMap.walker`/`scoring`/`temperature_bin`/
     `goal_weight_bins` at all — slice F shipped no generic walker-step
     interpreter, only named-preset dispatch. So every mutation sampled in
     GL-54 was structurally guaranteed to be behaviorally inert, independent
     of bug 1.
- Fixed both in `phenotype_overlap.py`:
  - Added `_apply_genotype_to_cfg` (uses `dataclasses.replace`) and call it in
    `_run_with_actor_genotype` so resolved temperature/goal_weights land on
    the episode's `AgentConfig` before `run_episode` runs.
  - `_mutate_program_map` now forces `mode="scorer_only"` (and
    `preset_source=None`) on every sampled variant — the only mode
    `resolve_runtime_genotype` wires to consult `scoring.pattern_scores`,
    `temperature_bin`, and `goal_weight_bins` — with a docstring explaining
    why (and flagging the remaining walker/hybrid-mode gap as a known
    limitation, not fixed this session).
- Left item 6 (detector coverage) as-is per explicit user instruction, but
  documented the item-7 retraction alongside it in `FINDINGS.md`/`DESIGN.md`.
- Reran `scripts/run_program_map_phenotype_overlap.py --variants-per-actor 12`
  (seed 0, T=200) → `results/slice_d_program_map_phenotype_overlap.json`:
  - eng1 (`walk_pipeline`): 0% overlap, 100% distinct, 8/8 deploy flips, L1 ∈
    [0.80, 1.38]
  - rev1 (`reviewer_peer_review`): 0% overlap, 100% distinct, 8/8 deploy
    flips, L1 ∈ [1.19, 1.38]
  - rm1 (`honest_twin`): 12.5% overlap, 87.5% distinct, 0/8 deploy flips, L1 ∈
    [0.04, 0.32]
  - admin1 (`honest_twin`): 12.5% overlap, 87.5% distinct, 1/8 deploy flips,
    L1 ∈ [0.03, 0.96]
- Bumped `CODE_VERSION` to `graded-lab-0.29.0` (GL-55) in `config.py` +
  `tests/test_config.py`.
- Updated `DESIGN.md` (§ slice D pre-Q1 batteries: retraction + corrected
  item 7 result + CODE_VERSION chain), `results/FINDINGS.md` (retraction note
  on the GL-54 entry + new GL-55 entry with root cause, fix, results table,
  interpretation), `README.md` (header version, slice-status table, GL-54/
  GL-55 summary notes), `PLAN_v3.md` (slice D row), `REPRODUCTION.md` (§10
  note on the fix), and fixture metadata
  (`tests/fixtures/ecology_v3_slice_a_reference.json`
  `v3_fixture_metadata...pre_q1_batteries`: added `phenotype_overlap_note`,
  bumped `code_version`).
- Ran `tests/test_slice_d_pre_q1_batteries.py` (4/4 pass) and the full
  `--profile fast` suite (279 passed, 0 failed) after the change — no
  regressions. Some unrelated tests exceeded their hard speed caps in this
  run (e.g. `test_uad_ecology_partition.py`, `test_twins.py`); this looks like
  environmental machine load (many unrelated tests were also slow), not a
  regression from this change, and was not investigated further or acted on.

## Decisions

- Chose to force `mode="scorer_only"` on **every** sampled variant (rather
  than mixing in still-inert `walker_only` mutations) so the battery
  measures a real, runtime-reachable diversity signal instead of a mix of
  reachable and structurally-guaranteed-inert samples. Documented this as a
  known limitation (walker/hybrid `ProgramMap`s remain runtime-unreachable
  until a generic walker-step interpreter or load-bearing Part B strict mode
  lands) rather than silently narrowing scope.
- Did not build a generic walker-step interpreter this session (out of
  scope for "fix and rerun 7"); left as an explicit open item alongside item
  6's `transfer_failure_risk` in `DESIGN.md`/`FINDINGS.md`.
- Left item 6 (detector coverage) implementation and result untouched per
  the user's explicit "Leave (and document) 6" — only added a short
  cross-reference to the item-7 retraction.

## Open / next

- Generic walker-step interpreter (or a documented v3 restriction to
  scorer/hybrid `ProgramMap`s) so walker-mode maps are runtime-reachable too.
- Growth-protocol `FINDINGS.md`/`BLIND_GENERATION.md` brief (still open from
  GL-54).
- Load-bearing Part B for default/grower agents; C2-v3 re-derivation.
- Optional supplementary detector fixtures for item 6 (ACL-denied /
  vote-timeout / misreporting-positive rosters) to get non-zero signal on
  the four zero-variance families.

## Key paths

- `experiments/graded-lab-simulation/graded_lab/harness/phenotype_overlap.py`
- `experiments/graded-lab-simulation/results/slice_d_program_map_phenotype_overlap.json`
- `experiments/graded-lab-simulation/results/FINDINGS.md` (GL-54/GL-55)
- `experiments/graded-lab-simulation/DESIGN.md` (§ PLAN_v3 slice D)
- `experiments/graded-lab-simulation/tests/test_slice_d_pre_q1_batteries.py`

## Commits

- None this session (not requested).
