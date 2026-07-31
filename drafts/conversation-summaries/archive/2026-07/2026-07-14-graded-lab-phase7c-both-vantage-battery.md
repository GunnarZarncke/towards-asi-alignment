# 2026-07-14 — Graded lab Phase 7c: full both-vantage calibration battery with 95% CIs

## Trigger

User: "Run full batteries (including determining confidence intervals)
for both oracle and referee before phase 8." This made concrete a
deferral left open at the end of the prior session (`DESIGN.md`
"EAI-referee": referee-vantage EAI, measured standalone in
`run_referee_eai_check.py` per FINDINGS G-19/G-20, had **not** been
wired into the main `run_calibration_battery`/`run_phase7_calibration.py`
pipeline).

## Done

- Pre-registered the plan in `DESIGN.md` ("Phase 7c full battery, both
  vantages, with confidence intervals") before writing code: both
  vantages computed from the **same** 100 episodes in one run, all new
  fields appended with defaults (backward compatible), pass-criteria
  logic reused unmodified via a projection helper, a shared CI utility,
  and an explicit go/no-go rule for whether this resolves the Phase 8
  gating question.
- Extracted `oracle_only/stats.py` (`ci95`, `paired_diff_ci95`,
  `mean_std_se`) from `run_referee_eai_check.py`'s inline copy; rewired
  that script to import it and reran it to confirm byte-identical
  numbers post-extraction.
- `CalibrationRecord`/`DoseRecord` gained `eai_referee`/
  `cell_eai_band_referee` and `mean_eai_referee`/`deploy_rate_ci95`/
  `mean_eai_ci95`/`mean_eai_referee_ci95` fields, all appended after
  existing fields with defaults — every existing positional-argument
  test in `test_phase7_calibration.py` still passes unchanged.
- `classify_cells_by_reference_agent` gained an `eai_field` kwarg
  (default `"eai"`); new `_vantage_records()` helper projects an
  alternate vantage's fields onto the `eai`/`cell_eai_band` slots the
  frozen `select_mid_band_cell`/`_select_dose_agent`/
  `evaluate_pass_criteria` already read, so those three run unmodified
  for the referee vantage too.
- `run_calibration_battery` now: classifies cells under both vantages;
  computes `I_ctrl` once for the union of "mid" cells across both
  vantages; runs dose-response for each vantage's own selected mid
  cell/agent (deduping if they coincide); evaluates pass criteria for
  both; adds a 95% CI per `(cell, agent_type)` on `eai`/`eai_referee`
  via a `_safe_ci95` wrapper that returns `None` on an unsupported
  sample size (e.g. the 2-seed smoke test) instead of crashing.
- `run_phase7_calibration.py` prints both vantages' pass-criteria
  reports and sweet-spot candidates, labeled `[oracle]`/`[referee]`.
- Added regression tests: `tests/test_stats.py` (new module, in the
  smoke profile) and several additions to `tests/test_phase7_calibration.py`
  (`eai_field` classification, `_vantage_records` projection,
  `run_dose_response`'s new fields).
- Ran the full 100-episode battery (`run_phase7_calibration.py`, wall
  `431.7s`) and documented the result as FINDINGS **G-22**.
- Full test suite green: 180 tests, `289s` against a raised `340s` cap
  (was `300s`; the new slow dose-response CI test pushed the previous
  cap close to its limit).

## Decisions

- Both vantages are computed from **one** battery run over the same
  episodes, not two independent runs — cheaper and makes every
  referee-vs-oracle comparison paired by seed.
- `I_ctrl` computed for the **union** of both vantages' "mid" cells
  (not run twice per vantage) — this is why the full run measured
  `I_ctrl` on 4 cells (80 episode-equivalent calls) instead of the
  0–1 cells the oracle-only battery reached before.
- CI methodology is a hardcoded Student-`t` lookup keyed by degrees of
  freedom (`df=9`→`2.262` for the 10-seed main battery, `df=4`→`2.776`
  for the 5-seed dose-response), not `scipy` (not in this venv); an
  unregistered `df` raises rather than silently guessing. The main
  battery wraps this in `_safe_ci95` so non-standard seed counts (only
  the smoke test) degrade to `None` instead of failing the run.
- `CODE_VERSION` not bumped — additive change, no existing caller's
  output value changed (only new keys added), same convention used for
  the G-20 EAI-referee addition.

## Result (FINDINGS G-22 — see there for full numbers)

Both the oracle/agent vantage and the referee (light-tier) vantage
land at **1/4** pass criteria on the identical 100-episode battery —
oracle passes criterion 1 (deploy↓ as EAI↑), referee passes criterion
4 (graded dose-response), and criterion 1's sign actually **flips**
between vantages for `programmatic_softmax` (`-0.146` oracle vs.
`+0.177` referee). The referee vantage makes criterion 2 measurable
for the first time (`n_ctrl_pairs` 0→40, since it classifies every
nonzero-load cell "mid"), but the separation itself still fails, for
the same roster-scope reason FINDINGS G-16 already named
(`programmatic_2step`'s flat cell-level deploy rate, identical under
both vantages). Per the pre-registered decision rule, this does not
clear the "meaningfully better" bar → **proceed to Phase 8, reported
honestly; the next calibration lever (if pursued) is roster scope (a
third agent type in the main comparison, e.g. `programmatic_budget_aware`
from FINDINGS G-17), not another EAI reformulation.**

## Open / next

- Phase 8 itself (selection-environment battery; see `PLAN.md`
  "Manuscript integration backlog" item 4 for the go/no-go framing) is
  not started.
- Roster-scope backlog item (wiring `programmatic_budget_aware` into
  the main strong/weak comparison) is named but not attempted — a
  separate, future decision, not assumed necessary before Phase 8.

## Key paths

- `experiments/graded-lab-simulation/DESIGN.md` — "Phase 7c full
  battery, both vantages, with confidence intervals"
- `experiments/graded-lab-simulation/results/FINDINGS.md` — G-22
- `experiments/graded-lab-simulation/graded_lab/oracle_only/calibration.py`
- `experiments/graded-lab-simulation/graded_lab/oracle_only/stats.py`
- `experiments/graded-lab-simulation/results/ecology_calibration.json`

## Commits

- (pending — see final commit in this session)
