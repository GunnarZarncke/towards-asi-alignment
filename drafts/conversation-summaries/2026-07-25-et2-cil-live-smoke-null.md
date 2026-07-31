# 2026-07-25 — ET-2 (CIL) live run: confirmed null, UAD finds zero edges (150/150 episodes)

## Trigger

Continuation of [2026-07-23-et2-cil-adapter-build.md](archive/2026-07/2026-07-23-et2-cil-adapter-build.md).
User: "network is better now. jaxlib is installed. continue" — the CIL sibling
venv install that was blocked by sandbox network throttling in the prior
session had finally succeeded (jaxlib landed in
`experiments/graded-lab-simulation/.venv`, not `external/cil/.venv`).

## Done

- Installed the rest of `cilib`'s deps (jax, matplotlib, etc.) into
  `external/cil/.venv` via `pip install -e .`, reusing the now-cached
  jaxlib wheel; completed in ~5.7 min (network still slow — individual
  wheel downloads logged at 200-1000 KB/s — but no more resets/hangs).
- Found and fixed a real bug on first live run: `cil_adapter.py`'s
  `_CIL_ROOT` used `Path(__file__).resolve().parents[3]`, which resolves
  three levels too far up (to the top-level `experiments/` folder, not
  `graded-lab-simulation/external/cil`). Should be `parents[2]`. Caught
  immediately as `ModuleNotFoundError: No module named 'experiments'` on
  the first manual smoke call — no live CIL episode had run before this
  session, so the bug was latent since ET2-1.
- Ran one manual episode (`mechanism=pld, n_agents=20, n_adversarial=4,
  seed=0, T=200`) end-to-end through `run_basin_stability_episode` →
  `score_episode`: 2.2s, correct shapes, `node_types` matched the
  requested adversarial count, action histograms showed real variance
  (not constant/degenerate).
- Ran the ET2-3 smoke battery: `scripts/run_et2_uad_battery.py
  --mechanisms pld prd --fractions 0.2 0.3 --seeds-per-cell 5` — 20
  episodes, ~0.65s/episode, all completed without error, results written
  to `results/et2a_smoke.json`.
- **Result: every single episode scored `ari_true=0.0`.** Manually
  verified this is not a crash/silent-empty bug: `cmi_edge_matrix` (frozen,
  unmodified from ET-1) found **zero edges** among all 190 pairs in a
  20-agent, 200-round episode with genuinely varying per-agent action
  series (e.g. one agent: `{0: 142, 3: 24, 2: 18, 1: 16}` over 200 rounds).
  The discovered partition is 20 singletons every time.
- Surfaced and documented a scoring subtlety this triggered: when the
  discovered partition is all-singletons, `adjusted_rand_index` is
  *structurally* exactly `0.0` against any label vector — true or
  permuted — because all row/column pair-sums are zero. The permutation
  null degenerates to a point mass at `0.0`, so `exceeds_null` (strict
  `>`) can never be `True` in this regime. This isn't a bug in the ARI
  formula, just a fact worth stating precisely so "P1 fails" isn't read
  as a graded near-miss.
- Updated `PLAN_ET2.md`: ET2-3 marked done (Leaf A only), phase table and
  status section rewritten with the smoke result and a preliminary,
  hedged reading (not yet a final null — needs the full 10-seed battery
  per the no-post-hoc-retuning discipline).
- Ran the **full ET2-4 battery** (default grid: 3 mechanisms × 5 fractions ×
  10 seeds = 150 episodes, `scripts/run_et2_uad_battery.py` with no args) —
  ~235s total (~1.5s/episode; slower than the smoke's 0.65s/episode because
  a duplicate, accidentally-triggered `pytest` run was competing for CPU at
  the same time). **Confirmed: all 150/150 episodes scored `ari_true=0.0`**,
  identically to the 20-episode smoke. `P1 holds=False`, 0/12 cells passing.
  This is now the real ET-2a outcome, not just a smoke-scale observation —
  written up in `PLAN_ET2.md` as a reportable null per ET2-0's
  no-post-hoc-retuning discipline (results in
  `results/et2a_uad_battery.json`).
- Kicked off a full `pytest tests/` run in `experiments/graded-lab-simulation/.venv`
  (now that scipy/pytest are both present there) to confirm nothing broke
  repo-wide. Accidentally launched 3 duplicate instances competing for CPU
  before noticing and killing the extras; the surviving instance hit one
  slow/possibly-stuck pre-existing test (unrelated to ET-2 code) around the
  same point (~17-20% through) for several minutes — left running in the
  background at end of session, not blocking on it since the new ET-2 tests
  were already independently verified passing (15/15) in an isolated venv
  in the prior session.

## Decisions

- Did not retune `cmi_edge_matrix`'s frozen thresholds
  (`min_effect_bits=0.3` etc.) to try to force a hit on the smoke cells —
  per `PLAN_ET2.md`'s explicit pre-registration discipline ("a null result
  on Leaf A would be a real, reportable negative, not a bug to patch").
  The smoke result stands as a preliminary null pending the full battery.
- Framed the likely mechanism (200 rounds of Q-learning converges to a
  low-entropy, mostly-single-action policy per agent — action `0` at
  ~70-75% of rounds in the sample checked) as a hypothesis for *why* a null
  might hold, not as grounds to change the frozen protocol.

## Open / next

- **ET-2a Leaf A is done** (confirmed null at full 150-episode scale). Next
  step is writing it into `results/FINDINGS.md` as a `GL-9x` entry, and
  deciding (question 4 in `PLAN_ET2.md`) whether/when it feeds ch34.
- Leaf B (`cil_selection_analysis.py`) has still not been smoke-tested at
  all — no runner script exists yet; needs `basin_stability.run_experiment`'s
  own CSV output as input. This is the next concrete piece of work.
- If a follow-up UAD variant is wanted (e.g. entropy-based pre-filter, or
  scoring Q-value/policy vectors instead of realized actions), pre-register
  it as a **new**, separate experiment — do not fold retuning into this
  ET-2a result.
- Verify the backgrounded full-suite `pytest tests/` run (writing to
  `/tmp/full_test_out.txt`) finished clean in a later session; it stalled on
  one pre-existing (not ET-2-related) test for several minutes at ~17-20%
  when this session ended — worth checking whether that test is simply slow
  or genuinely hung, but out of scope for this session's task.

## Key paths

- `experiments/graded-lab-simulation/PLAN_ET2.md` — status/phase table
  updated, read this first.
- `experiments/graded-lab-simulation/graded_lab/external/cil_adapter.py`
  — the off-by-one fix is here (`_CIL_ROOT = ... parents[2] ...`).
- `experiments/graded-lab-simulation/results/et2a_smoke.json` — the smoke
  battery's raw output.
- `experiments/graded-lab-simulation/external/cil/.venv` — now has
  jax/jaxlib/cilib/matplotlib installed; `experiments/graded-lab-simulation/.venv`
  separately has jaxlib/scipy/pytest (from the user's earlier manual install).

## Commits

None — no commit was requested this session.
