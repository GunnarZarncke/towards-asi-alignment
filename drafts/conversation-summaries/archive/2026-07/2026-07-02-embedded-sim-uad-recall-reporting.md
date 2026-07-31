# 2026-07-02 — Embedded sim: correct UAD recall reporting (finding 5)

## Trigger

User: "Correct the recall reporting (5)." (Review finding 5: the 3.8% UAD
recall/precision headline was averaged over all 13 bridges, but the metric is
defined only where a hidden-coalition target exists — MB6/MB6b/MB7d. Filler
zeros elsewhere diluted the number into meaninglessness.)

## What was done

1. **Semantics at the source** (`outer_eval.py`, `schemas_embedded.py`):
   `OuterTruthComparison.uad_recall/uad_precision` are now `float | None`.
   `None` = undefined (no G3/G3b coalition in the episode's truth ledger).
   When a coalition target exists but UAD found no unit, recall is a defined
   0.0 (bad, not undefined). Removed the previous `expected == "none"`
   pseudo-metric (1.0/0.5 depending on unit score) — it was not a recall and
   silently inflated averages.
2. **Aggregators skip undefined episodes**:
   - `run_suite._uad_summary_from_runs`: averages over defined episodes only;
     adds `n_uad_defined`, `n_runs_total`, and `uad_by_bridge` (per-bridge
     mean recall/precision with counts). Main-report rows now carry `bridge`.
   - Overall-summary line uses `_uad_headline`: "UAD recall X% over N/M
     coalition-target episodes" plus per-bridge sub-bullets; full-vs-fake
     compare table labels say "(coalition targets only)" and add defined-count
     rows (`—` when nothing is defined).
   - `intervention_benchmark._aggregate`: mean recall over defined runs only
     (`n_uad_defined`); curve markdown renders `X% (n=K)` or `—`.
3. **Tests** (`tests/golden/test_uad_precision_recall.py`): honest episode has
   `uad_recall is None`; MB6 episode has defined metrics; unit test for
   `_uad_summary_from_runs` (undiluted mean 0.75 vs the old 0.375, per-bridge
   table, all-undefined → `None`).
4. **Honest record**: N-1 postscript in `results/NEGATIVE_RESULTS.md` (the
   3.8% figure was an aggregation artifact; full==fake identity stands) and a
   note in the `OVERALL_SUMMARY.md` staleness banner.

## Non-obvious decisions

- Dropped the `expected == "none"` proxy entirely rather than renaming it: it
  measured "did UAD stay quiet on a clean lab", which is a different metric
  (specificity), and mixing it into recall was part of the original problem.
  If wanted later, add it as an explicitly named metric.
- Defined-but-zero vs undefined: coalition exists + no unit found ⇒ 0.0
  (counts against the auditor); no coalition ⇒ `None` (excluded). This is the
  distinction the old code collapsed.

## Verification

- Full suite: 112 passed (`.venv-test`).
- Stale artifacts (`embedded_uad_compare.md`, `embedded_sim_report.json`, …)
  still show the old numbers; regeneration remains a tracked TODO item.

## Open / next

- Regenerate suite artifacts (14 scenarios, fixed auditor, corrected UAD
  reporting).
- Review roadmap item 1 (appD correction-trace schema) is next per the review
  log; findings 1–5 are all closed.

## Key paths

- `experiments/embedded-simulation/embedded_sim/outer_eval.py`
- `experiments/embedded-simulation/embedded_sim/schemas_embedded.py`
- `experiments/embedded-simulation/embedded_sim/intervention_benchmark.py`
- `experiments/embedded-simulation/run_suite.py`
- `experiments/embedded-simulation/tests/golden/test_uad_precision_recall.py`
- `experiments/embedded-simulation/results/NEGATIVE_RESULTS.md` (N-1 postscript)
