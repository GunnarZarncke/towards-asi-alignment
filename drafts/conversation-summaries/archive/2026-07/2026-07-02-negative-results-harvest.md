# 2026-07-02 — Negative results harvest (toy + embedded sim)

## Trigger
User asked to go through conversation logs for toy and embedded simulation,
find previous negative results, and document clear cases (not debugging artifacts)
in `NEGATIVE_RESULTS.md` with dates.

## Done
- Harvested negative/null findings from conversation summaries dated 2026-06-29
  through 2026-07-02.
- **Embedded** (`experiments/embedded-simulation/results/NEGATIVE_RESULTS.md`):
  added dates to N-1/N-2; added N-3 through N-7 (ecology null, intervention
  granularity null, episode/safety decoupling, vacuous 0% false-pass, UAD-not-scoping-CCI gap).
- **Toy** (`experiments/toy-simulation/results/NEGATIVE_RESULTS.md`, new):
  T-1 through T-10 covering passive uncertifiability, handle cost curve, capture_mild
  partial detection, MB2/MB3/MB5/MB8/MB9 light false-passes, correction-capture
  decoupling, red-team battery vulnerability, handle-protection scope limit.

## Decisions
- Excluded soundness bugs flagged in 2026-07-02 embedded review (oracle fields in
  VFS rows, scenario-blind audit branches) — implementation defects, not experimental
  null results.
- N-6 notes suspected threshold miscalibration but records the metric non-discrimination
  claim regardless (0% false-pass when nothing certifies).
- Did not duplicate N-2 content in N-3/N-4; cross-linked by reference.

## Open / next
- Re-run embedded instrumentation after threshold fix; append resolution under N-6 if
  false-pass becomes discriminative.
- G-1 `confounded_twin` ecology (embedded TODO) — principled non-circular boundary.
- Optional: link toy README to `results/NEGATIVE_RESULTS.md`.

## Key paths
- `experiments/embedded-simulation/results/NEGATIVE_RESULTS.md`
- `experiments/toy-simulation/results/NEGATIVE_RESULTS.md`
- Source logs: `2026-06-29-multiresolution-*`, `2026-06-30-embedded-*`,
  `2026-06-30-uad-calibration-oracle-free.md`, `2026-07-02-embedded-sim-review.md`

## Commits
- (none — user did not request commit)
