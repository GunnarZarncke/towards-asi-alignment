# 2026-07-03 — Systematic channel MI scan (discovery instrument, not a gate)

## Trigger

Following the N-10 majority-domain gate work (reinstated with priced residual
risk, see `2026-07-03-part-d-handles-verdict-class-gate.md`), the user raised
a methodological concern: the four verdict domains (`bearer_welfare`,
`lineage`, `routing`, `successor`) were grouped by hand, so the same failure
mode that made the majority gate unsafe (one domain non-interchangeable with
the rest) could recur with any other hand-picked grouping. Proposed instead:
score individual channels and best-of-k subsets systematically, flagging the
Bonferroni/winner's-curse problem that raises for best-of-k search. Asked to
widen the candidate channel set beyond the 15 registered `handle.*` channels
("why are these limited? think wider"), then: "Write protocol, then
implement." Adversarial-setup implications of using scan output for
certification were flagged explicitly as a TODO to record, not resolve now.

## Done

- Renamed `observation._handle_series_map` → public
  `observation.handle_channel_series_map` (two internal call sites updated)
  so a second module could reuse the exact channel-construction logic instead
  of re-deriving it.
- Wrote `channel_mi_scan.py` with the full pre-registered protocol as its
  module docstring (channels, functionals, seeds, split, corrections,
  acceptance criteria — written and read before any numbers were computed,
  per AGENTS.md "conclusions never named before being derived"):
  - **22 candidate channels**: 15 registered `handle.*` channels (independent
    of instrumentation level) + 7 passive `artifact.*` base channels
    available at *every* level including `none` (`action`, `sensor`=harm,
    `internal`, `bearer`=display_bearer, `infra`, `basin`, `ground`).
  - **4 generic per-episode functionals** applied uniformly (not hand-tuned
    per channel): `mean`, `endpoint_drop`, `range`, `probe_mean`. 88 cells.
  - **Ground truth**: same scenario battery/split as
    `eval_channel_eligibility.py` (6 capture + 2 honest scenarios).
  - **Exploration/validation seed split** (64+64, disjoint from each other
    and from the 8 eligibility-eval seeds) to control the winner's-curse:
    greedy best-of-k forward selection (via incremental conditional MI, k=1
    to 6) only ever touches exploration seeds; each resulting k-subset is
    re-scored on untouched validation seeds as the actual confirmatory test.
  - Bonferroni-corrected permutation nulls: `1 - 0.05/88` for the single-cell
    scan, `1 - 0.05/6` for the k-family validation checks — same convention
    as `probe_scan.py`.
  - Reused existing `info_ci.mi_with_ci`/`info.conditional_mutual_information`
    machinery unmodified; only new code is episode/feature-table construction
    and quantile-edge fit/apply (fit on exploration, applied — not refit — to
    validation, to avoid leaking validation-split information into
    discretization).
- Ran the scan (`results/channel_mi_scan.{md,json}`, 77.75s, 1024 episodes
  total). All 6 greedy k-subsets validated on held-out seeds with small
  winner's-curse gaps (≤0.043 bits); 33/88 cells individually cleared the
  Bonferroni-corrected threshold on exploration.
- Added `tests/contract/test_channel_mi_scan.py` (8 tests): cell-count/
  Bonferroni-formula checks, every cell reported exactly once, k-curve shape,
  exploration joint-MI monotonicity (structural property: k+1 joint code is a
  strict refinement of the k joint code), selected features distinct, top
  finding replicates on validation seeds, winner's-curse gaps stay small.
- Recorded the adversarial-setup TODO verbatim in `TODO.md` (new "Phase F")
  and in the script docstring, per explicit instruction to record-not-resolve.
- Added `NEGATIVE_RESULTS.md` N-10 Postscript 4 documenting the scan and its
  most actionable (but *not yet acted on*) finding.
- Full test suite: 227 passed, 1 skipped (no regressions from the
  `observation.py` rename).

## Decisions

- Used `build_world` + `load_episode_rows_from_vfs` directly instead of the
  full `_run_scenario_episode`/`run_episode` pipeline `eval_channel_eligibility.py`
  uses — measured `build_world` alone at ~27ms/episode vs. ~3s/episode for
  the full pipeline (audit/UAD/certification stages dominate that cost, not
  world simulation), and this scan only needs raw channel series, not
  certification verdicts. This also meant each (scenario, seed) is simulated
  **once** total regardless of how many channels/functionals are scored,
  vs. the eligibility eval's 6x redundant re-simulation across instrumentation
  levels — made a much larger seed budget (128 vs. 8 seeds/scenario) cheap
  enough to run in ~80s instead of tens of minutes.
- Per-episode functionals were fixed as a small, generic, *uniform* battery
  rather than one hand-picked statistic per channel — using different
  functionals per channel would silently reintroduce the ad-hoc-detector
  problem this scan exists to route around. Chose 4 that span the shapes
  real detectors already look for (level, drift, dispersion, probe-conditional
  response) without being fit to any specific channel's known behavior.
- Chose greedy forward selection via conditional MI (mRMR-style) for best-of-k
  rather than exhaustive subset search — the user's "best of two, three, ...,
  all" request is combinatorially intractable exhaustively (2^88) but greedy
  CMI selection is the standard, principled, tractable answer and composes
  exactly with the chain rule (joint MI = sum of incremental CMIs), which is
  also why the exploration-side joint-MI curve is provably non-decreasing in
  k (tested directly, not just observed).
- Split-sample validation (not FDR/Benjamini-Hochberg) chosen as the
  winner's-curse fix, per the user's own framing of the tradeoff — the greedy
  search itself is heuristic/exploratory and only the final validation-side
  test per k is treated as a confirmed finding, explicitly labeled as such in
  both the script docstring and the rendered results table.
- Explicitly did **not** act on the `artifact.bearer` finding (a
  cheaper/lower-tier channel that appears to carry comparable-or-more
  information than the gated `handle.bearer_welfare_delta`) by proposing a
  channel_sets.py change — doing so now would be exactly the after-the-fact
  rule-fitting the standing N-10 recommendation warns against. Left as a
  flagged follow-up requiring its own pre-registration.

## Open / next

- Adversarial-setup TODO (Goodharting a discovered-informative channel;
  discovery-time MI vs. robustness guarantee; validate against red-team
  strategies unseen at discovery time) — recorded, not resolved.
- Possible follow-up: pre-register and test a `bearer_welfare`-relevant
  passive-channel detector (using `artifact.bearer`/`artifact.sensor`) as a
  candidate fix for the `medium_minus_handles` residual risk — separate task,
  needs its own validation battery per the note above.
- Still pending from earlier sessions: regenerate the full six-level frozen
  validation + instrumentation curve; Part C (writer attestation on
  `handle.hardware_tag`, N-9); a required-domain-weighted gate variant
  (`bearer_welfare` mandatory) as a pre-registered follow-up to the majority
  gate.

## Key paths

- `experiments/embedded-simulation/channel_mi_scan.py` — protocol + scan.
- `experiments/embedded-simulation/results/channel_mi_scan.{md,json}` — results.
- `experiments/embedded-simulation/tests/contract/test_channel_mi_scan.py`.
- `experiments/embedded-simulation/embedded_sim/audit_core/observation.py` —
  `handle_channel_series_map` (renamed, now public).
- `experiments/embedded-simulation/results/NEGATIVE_RESULTS.md` — N-10
  Postscript 4.
- `experiments/embedded-simulation/TODO.md` — Phase F.

## Commits

- None (not asked to commit this session).
