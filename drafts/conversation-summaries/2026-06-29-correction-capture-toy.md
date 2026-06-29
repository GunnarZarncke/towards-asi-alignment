# 2026-06-29 — Correction-capture toy experiment

## Trigger
User asked to pick the highest-rated hard-evidence target from reviewers and the research roadmap, then make small concrete progress via a Python experiment or Lean derivation with at least five approaches.

## Done
- Chose the reviewer/roadmap overlap:
  - `review/strategic-advice-2026-06-28.md` ranks an end-to-end worked measurement/capture example first.
  - `appendices/appH-research-program.tex` puts measurement prerequisites, correction legitimacy, hidden-capability bounding, and adversarial verifiability at the top of the research order.
- Added `experiments/correction_capture_toy.py`, a stdlib-only synthetic trace experiment.
- Added `experiments/README.md`.
- Ran five approaches:
  1. naive reported-action CCI,
  2. true-action/interventional CCI,
  3. boundary residual probe,
  4. high-stakes stress split,
  5. capability-vs-correction slack sweep.
- Generated:
  - `experiments/results/correction_capture_toy.json`
  - `experiments/results/correction_capture_toy.md`
- Updated `metadata/TODO.md` to mark the strategic-advice and full-worked-example items as partial rather than open from scratch.

## Decisions
- This is a controlled sanity-check artifact, not evidence that the estimands work in frontier systems.
- The experiment intentionally demonstrates a failure mode: reported correction acceptance can stay high while true correction uptake collapses.
- Kept it outside `src/demos/` because it is a batch/reproducibility artifact, not an interactive chapter demo.

## Open / next
- Add a value-bundle signal and safety-case decision layer so this becomes closer to the requested full worked example.
- Replace the binary toy trace with either a gridworld or logged LLM-with-tools trace.
- Add bootstrap confidence intervals or permutation tests for the CMI estimates.
- Consider extracting the anti-capture validity condition as a standalone note.

## Key paths
- `experiments/correction_capture_toy.py`
- `experiments/results/correction_capture_toy.md`
- `experiments/results/correction_capture_toy.json`
- `metadata/TODO.md`
- `review/strategic-advice-2026-06-28.md`
- `appendices/appH-research-program.tex`

## Commits
- Correction-capture toy experiment + session log + TODO updates (see `git log -1`).

## Verification
- `python3 experiments/correction_capture_toy.py --n 8000 --seed 1729` succeeds and writes result artifacts.
