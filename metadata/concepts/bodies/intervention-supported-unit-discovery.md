---
bookSections:
  - chapterId: ch07
    label: Estimator Feasibility and Recovery
evidenceNotes:
  - source: lab-layer simulation, intervention-supported discovery line
    scenario: channel-ablation + compensation scoring on a deterministic multi-actor pipeline
    finding: support
    summary: Channel ablation plus outcome-level compensation scoring achieves exact recovery of the true coordinating pair on the large majority of scripted scenarios and a negative control where passive correlation-based clustering merges the whole pipeline into one false unit.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/FINDINGS.md
  - source: lab-layer simulation, null-calibrated rebasing
    scenario: same detector re-based on outcome-frequency observables, null measured from repeated clean runs instead of a fixed threshold
    finding: support
    summary: Comparing post-intervention divergence to a measured quantile of clean-vs-clean replicate divergence, rather than a fixed threshold, reproduces the original detector's exact results on deterministic backends and additionally recovered a real coordinating pair in one live model-driven run that the fixed-threshold version missed.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/FINDINGS.md
  - source: lab-layer simulation, ripple stress test
    scenario: 3+ participant scenario and a 5-seed sweep on the model-driven scenario above
    finding: negative
    summary: The same null-calibrated method missed a real coordinating pair on a three-participant scenario, and a 5-seed sweep on the scenario it had previously solved dropped to a 20% exact-recovery rate, matching the passive baseline rather than beating it. Recorded as a negative result, not walked back from the narrower mechanism claim above.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/FINDINGS.md
related:
  - boundary-discovery
  - mb1-boundary-estimator-soundness
  - adversarial-boundary-discovery
  - unit-discovery-stress-test
  - experiment-methodology
  - detecting-composite-agents
external:
  - label: Lab-layer simulation findings
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/FINDINGS.md
---

A passive audit that only looks for correlation has a specific failure mode: an ordinary multi-step workflow already looks correlated, so clustering on correlation alone can merge an entire pipeline into one false "unit" even when only two of its participants actually coordinate.

The fix tested here is interventional rather than passive. Disable one candidate channel — a communication link, a shared resource, a specific interaction — and see whether the participants' subsequent behavior changes more than it would have changed anyway. The "would have changed anyway" part is the load-bearing addition: the comparison is scored against a baseline measured from several unperturbed repeats of the identical setup, not against a fixed, hand-picked threshold. Real systems, especially ones with any stochastic component, vary run to run even with no intervention at all; treating any nonzero post-intervention change as evidence collapses the moment that ordinary variation is nonzero.

In restricted testbeds with a known ground-truth partition, this channel-ablation-plus-measured-baseline approach recovers the correct grouping on cases where passive clustering does not, including a negative control where no real coordination exists. The same approach, rebased onto outcome-level observables (what happened, not exactly when), also recovered a coordinating pair in one run driven by a real language-model agent that a fixed-threshold version of the same method missed.

That is where the confident part of the claim ends. A harder stress test — a three-participant scenario, and a five-seed replication of the single successful run above — showed the method swinging the other way: missing a real pair it should have caught, and dropping to a success rate no better than the passive baseline it was meant to improve on. The general shape (compare an intervention's effect to a measured null, not a fixed one) is the right instrument design; getting it calibrated well enough to trust on noisy, non-repeatable systems is open work, and the negative results are kept alongside the positive ones rather than discarded.
