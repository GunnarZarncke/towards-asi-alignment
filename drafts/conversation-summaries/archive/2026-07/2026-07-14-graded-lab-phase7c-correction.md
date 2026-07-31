# 2026-07-14 — Graded lab Phase 7c: correcting the calibration-battery evaluator

## Trigger

Follow-up to 2026-07-13's Phase 7c battery (`FINDINGS.md` G-15, 1/4
criteria passed, diagnosed as "grid doesn't span the EAI bands"). User
asked to investigate *why* the criteria failed, functionally and
conceptually; then, on finding the diagnosis itself was wrong (not just
the grid), asked for a correction entry, a detailed `PLAN.md` update to
prevent recurrence, new registered predictions, and an implementation —
in that order.

## Done

- Diagnosed G-15's own diagnosis as wrong on two factual counts (deploy
  rate is 42.5%/agent-type-determined, not "rare"; measured EAI is
  bimodal by agent type, not clustered low) and traced three real causes
  by reading code against Chapter-level concept:
  1. Criterion 1 pooled two agent types into one slope — passed by
     agent-type composition, not a substrate effect.
  2. `eai.py`'s entropy term is structurally near-zero for this
     `primitive_log` schema: only the successful-completion path writes
     a real `observable_state`; every denial/abort/skip path either
     lacks it or lacks `primitive` too, so groups are either homogeneous
     (0 bits) or degenerate; the `log2(len(counts))` global-not-per-group
     normalization actively *lowers* entropy when new status categories
     appear (confirmed: enabling `carrier_load_scale` produces real
     status diversity yet mean EAI *falls*). Left **open/unfixed** —
     fixing it means editing `eai.py`/`world.py`, both protected by the
     Phase 7c failure policy.
  3. Phase 7c's evaluator re-derived "EAI band" as a per-record,
     per-agent-type classification, contradicting its own source
     definition (`DESIGN.md` "Emergent Ambiguity Index": band
     classifies a *cell* via a *reference* agent, then strong/weak are
     compared *in that cell*).
  4. A scope gap (not a bug): both current agent programs' deploy
     decisions are invariant to substrate stress within the frozen
     ranges — criteria 1/3/4 cannot be satisfied by *any* grid with this
     roster.
- Wrote **FINDINGS G-16** (correction entry) with full mechanistic
  evidence for all four causes, plus a fifth, narrower caveat found
  while re-running the corrected battery (a "cell deploy-rate range
  ≥0.05" gate for criterion 1 can still be satisfied by a single
  idiosyncratic seed at `n=10` seeds/cell — registered as an open
  caveat, not patched further).
- Registered **DESIGN.md "Phase 7c-revised"** before writing code:
  reference-agent cell classification, within-type criterion 1,
  `carrier_load_scale`-based grid/dose-response (the only knob with a
  demonstrated causal path, reusing Phase 3b's own pre-registered
  cells verbatim), a mandatory `check_mechanism_sensitivity` pre-check,
  and three falsifiable numeric predictions registered *before* running
  the corrected code.
- Added **PLAN.md "Battery design checklist"** (5 generalized rules:
  mechanism-sensitivity dry run before grid selection; re-derive
  band/threshold semantics from their original definition; never pool
  structurally different populations into one statistic; check a
  criterion's precondition is reachable before pre-registering it;
  "adjust substrate within blinded ranges" is not unlimited).
- Implemented the fixes in `graded_lab/oracle_only/calibration.py`
  (`carrier_grid`, `classify_cells_by_reference_agent`,
  `check_mechanism_sensitivity`, within-type + cell-range-gated
  criterion 1, cell-classified criteria 2/3, carrier-load dose-response
  with dynamic anchor-agent selection) and `run_phase7_calibration.py`
  (`--legacy`/`--smoke`/mechanism-check-gated `--full`).
- Rewrote `tests/test_phase7_calibration.py` (13 tests, incl. a
  pooled-slope-confound regression and a mechanism-sensitivity dry-run
  regression matching the registered prediction).
- Ran the revised 5-cell battery twice (once before, once after fixing
  the criterion-1 cell-range gate found mid-session); recorded the
  final honest result in G-16: 1/4 criteria pass (with the n=1-evidence
  caveat), criterion 2 untestable this run (reference cell's mean EAI
  missed the mid floor by 0.00023 — not re-rolled), 3/4 inconclusive as
  predicted.
- Ran fast profile (149 tests) and full slow profile (155 tests) —
  all green; refreshed `tests/speed_baseline.json`.
- `CODE_VERSION` `0.12.0 → 0.13.0`.

## Decisions

- Did not attempt to fix `eai.py`'s entropy-logging defect or design a
  resource-sensitive third agent program this session — both are
  explicitly out-of-scope backlog items (the former touches a
  formula/schema protected by the failure policy; the latter is new
  agent-design scope), registered in `DESIGN.md`/`FINDINGS.md` rather
  than patched under time pressure.
- Kept the original 16-cell `substrate_grid()`/`--legacy` path in code
  as a diagnostic fixture rather than deleting it — G-15's numbers stay
  in `FINDINGS.md` for the record.
- Did not re-run with different seeds after criterion 2 missed the mid
  band by 0.00023 on the pre-registered seed set — re-rolling to chase
  a different boundary outcome would be exactly the backward-tuning
  this investigation exists to rule out.
- `check_mechanism_sensitivity` default seed count raised from an
  initial 3 to 5 after a 2-seed manual check spuriously read
  `compute_scale` as "demonstrated" by sampling noise; documented as an
  empirical finding, not a round guess.

## Open / next

- Phase 8 remains blocked. Two registered backlog items, either of
  which needs its own pre-registration before attempting:
  1. A resource-sensitive agent program (deploy/continue decision
     depends on remaining compute/time budget).
  2. The `eai.py`/`world.py` entropy-term fix (real `primitive`/
     `observable_state` on every log entry; per-group not per-episode
     normalization).
- The criterion-1 "single seed at n=10" caveat suggests either more
  seeds/cell or a proper significance test before trusting a
  cell-deploy-range gate again.

## Key paths

- `experiments/graded-lab-simulation/results/FINDINGS.md` (G-16)
- `experiments/graded-lab-simulation/DESIGN.md` ("Phase 7c-revised")
- `experiments/graded-lab-simulation/PLAN.md` ("Battery design checklist")
- `experiments/graded-lab-simulation/graded_lab/oracle_only/calibration.py`
- `experiments/graded-lab-simulation/run_phase7_calibration.py`
- `experiments/graded-lab-simulation/tests/test_phase7_calibration.py`
- `experiments/graded-lab-simulation/results/ecology_calibration.json`

## Commits

- None yet this session.
