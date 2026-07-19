# 2026-07-19 — Graded lab PLAN_v4 V4-5: R-MB2 scorecard Goodhart

## Trigger
User: "do R-MB2 next" — implement and score the proxy/withheld principal
scorecard Goodhart rig (PLAN_v4 V4-5).

## Done
- Implemented `graded_lab/harness/rigs/r_mb2_scorecard_goodhart.py` (tension
  precondition, proxy-only selection, P1/P2).
- Wired `r-mb2` in `scripts/run_v4_rig.py`; added `tests/test_rig_r_mb2.py`.
- Froze pre-registration in `DESIGN.md` ("PLAN_v4 pre-registration — R-MB2
  scope").
- Ran full battery: `results/v4_r_mb2.json` (20 seeds, 1289 s wall).
- Recorded **GL-85** in `FINDINGS.md`; updated `REPRODUCTION.md` §10.2 and
  `PLAN_v4.md` V4-5 status.

## Decisions
- **Outcome null** is the scored record (not smoke pass): precondition
  satisfied (`r(proxy,harm)=0.44`) but proxy-only selection did not improve
  proxy score or Goodhart on withheld harm/review.
- `review_thoroughness` degenerate at 0 on v3_grown — review leg of
  precondition cannot fire; harm tension alone sufficient to run battery.

## Open / next
- R-MB7 red-team adapter (gpt-4o-mini $10); R-MB5/R-MB8 coherence rigs.
- Optional follow-up Goodhart battery needs new pre-registration (richer
  ProgramMap baseline or non-degenerate review metric).
- Uncommitted session work: GL-81–GL-85 bundle (user has not asked to commit).

## Key paths
- `experiments/graded-lab-simulation/graded_lab/harness/rigs/r_mb2_scorecard_goodhart.py`
- `experiments/graded-lab-simulation/results/v4_r_mb2.json`
- `experiments/graded-lab-simulation/results/FINDINGS.md` (GL-85)

## Commits
- (none this session)
