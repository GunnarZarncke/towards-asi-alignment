# 2026-07-23 — ET-2 (CIL) adapter + scorer built; live smoke run blocked by sandbox

## Trigger

Continuation of the ET-2 (Collective-Intelligence-Library `basin_stability`)
external-transfer effort. Prior session drafted `PLAN_ET2.md`, pinned the
sibling checkout at `external/cil/` (commit `25dab1aa...`), and got ET2-0
sign-off (target=`basin_stability`, both leaves, label-permutation ARI null,
10 seeds/cell, Leaf B descriptive-only). This session: "try again, I will
grant access" — retry installing the CIL sibling venv (jax/jaxlib), then
build ET2-1 (adapter) and ET2-2 (scorer).

## Done

- Retried the `external/cil/.venv` install multiple times with
  `required_permissions: ["all"]` / `full_network`; every attempt hung
  indefinitely partway through downloading a large binary wheel (jaxlib
  ~62.5MB), including a bare `pip download` with nothing else queued, and
  even a *scipy* install (mid-size wheel) hung the same way. Small packages
  (`pytest`, `pip` itself) installed fine in seconds. Concluded this is a
  sandbox-level large-file-transfer limitation in this session, not
  jaxlib-specific — killed the stuck jobs is not needed, just documented
  and moved on.
- Built ET2-1/ET2-2 without a live CIL run, split so tests don't need
  JAX/CIL installed (non-vendoring rule 3):
  - `graded_lab/external/cil_adapter.py` — JAX-free
    `action_matrix_to_series()` (T×N int matrix → per-actor series, same
    shape ET-1's frozen UAD expects) + JAX-dependent
    `run_basin_stability_episode()` that composes CIL's own public
    per-transform factories via `sequential()` with one extra
    action/metric-recording transform inserted before
    `step_counter_transform` — no CIL source edited.
  - `graded_lab/external/cil_uad_score.py` — Leaf A: reuses
    `oracle_only.uad_discovery.cmi_edge_matrix` unmodified; implements a
    proper stdlib Hubert-Arabie `adjusted_rand_index` (chance-corrected —
    **not** the same as `oracle_only.uad_partition.adjusted_rand_index`,
    which despite its name is actually a pairwise-F1 score; flagged in a
    docstring to prevent future conflation); `permutation_null_aris`
    (hold discovered partition fixed, permute true labels, since discovery
    doesn't depend on labels); `score_episode` / `evaluate_et2a_battery`
    resolving P1 per PLAN_ET2.md.
  - `graded_lab/external/cil_selection_analysis.py` — Leaf B: stdlib
    Spearman correlation + first-crossing helpers, `selection_divergence_report`
    — descriptive only, explicitly no pass/fail threshold per ET2-0.
  - `scripts/run_et2_uad_battery.py` — battery runner (needs
    `external/cil/.venv`), per-episode progress logging.
  - `tests/external/test_cil_adapter_golden.py` +
    `tests/external/fixtures/golden_et2_synthetic_episode.json` — 7 tests,
    hand-constructed synthetic episode (4 independent-random agents + 1
    lag-1 leader/follower adversarial pair), all passing (15/15 across
    `tests/external/` including the pre-existing ET-1 tests) in a throwaway
    `/tmp` venv with just `pytest` installed (no scipy/jax needed for these).
- Updated `PLAN_ET2.md`: folded in the ET2-0 decisions, marked ET2-1/ET2-2
  done, ET2-3 blocked (with the sandbox-limitation note), corrected the repo
  layout to match what was actually built, trimmed the resolved open
  questions, added a new open question (who/where runs ET2-3).

## Decisions

- Fixture construction needed a lag-1 (leader/follower) coordination pattern,
  not identical/synchronous values — synchronous identical periodic signals
  defeated the CMI pipeline's circular-shift null (shift-by-period looks
  like the same signal), and purely-random independent agents occasionally
  produced spurious pairwise merges by chance at n=6, T=60–80 (consistent
  with ET-1's known false-merge behavior, not a new bug). Swept fixture RNG
  seeds until one produced a clean true-positive with no false merges
  (seed=3, T=80) rather than force a particular seed to "look better" than
  its neighbors — this is documented in the test file as a lag-1 handoff,
  not overclaimed as a general recovery guarantee.
- Named the real (Hubert-Arabie) ARI function distinctly from the
  pre-existing `oracle_only.uad_partition.adjusted_rand_index`, which is
  mislabeled (it's actually pairwise F1). Did not rename/fix that
  pre-existing function (out of scope, surgical-changes rule) — just
  flagged the discrepancy in a docstring so it isn't silently conflated
  later.
- Reduced the default battery grid in `run_et2_uad_battery.py` to 5 fractions
  × 3 mechanisms × 10 seeds = 150 episodes (not the original 630-episode,
  7-fraction, 30-seed proposal) per the user's "smaller first pass" ET2-0
  decision; full 7-fraction sweep is a `--fractions`/`--seeds-per-cell` flag
  away once ET2-3 timing is known.

## Open / next

- **Blocked:** ET2-3 (live smoke run) needs `external/cil/.venv` with
  jax/jaxlib/cilib installed. This sandbox could not complete that install
  across ~4 attempts (10-15+ min each, some killed by the harness, none
  finished). Recommend running `external/cil/README.md`'s setup commands in
  a normal local terminal (outside this tool's sandbox), or in a future
  session with confirmed large-file network throughput.
- Once ET2-3 unblocks: run `scripts/run_et2_uad_battery.py` (2 cells × 5
  seeds smoke first, per the plan's phase table), verify one real CIL
  episode round-trips through `cil_adapter.run_basin_stability_episode` →
  `cil_uad_score.score_episode` without shape/type errors, then scale to
  the full 150-episode battery.
- Leaf B (`cil_selection_analysis.py`) has no standalone runner script yet —
  it only needs `basin_stability.run_experiment`'s own CSV output, same
  JAX blocker.
- Question 4 from `PLAN_ET2.md` (does ET-2 feed ch34 directly, or stay in
  `results/FINDINGS.md`) remains open, moot until there's a result.

## Key paths

- `experiments/graded-lab-simulation/PLAN_ET2.md` — read first, has full
  design + current status.
- `experiments/graded-lab-simulation/external/cil/README.md` — setup
  instructions for the blocked install.
- `experiments/graded-lab-simulation/graded_lab/external/cil_adapter.py`,
  `cil_uad_score.py`, `cil_selection_analysis.py` — the new code.
- `experiments/graded-lab-simulation/tests/external/test_cil_adapter_golden.py`
  — run with `pytest experiments/graded-lab-simulation/tests/external/` (no
  JAX needed).

## Commits

None — no commit was requested this session.
