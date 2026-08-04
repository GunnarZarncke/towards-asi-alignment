---
evidenceNotes:
  - source: lab-layer simulation, ripple stress test
    scenario: 3+ participant scenario with two genuinely coordinating members plus bystanders
    finding: negative
    summary: A detector variant that had just recovered a coordinating pair in a controlled two-participant run failed to detect a real coordinating pair once a third, non-coordinating participant was added — the opposite failure direction from the over-merge risk the same testbed had previously documented for a large, untargeted perturbation.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/FINDINGS.md
  - source: lab-layer simulation, multi-seed replication
    scenario: same two-participant scenario the detector had solved, replicated across five seeds
    finding: negative
    summary: Across five seeds of the identical scenario, exact recovery dropped to roughly one in five — no better than the passive baseline detector it was meant to improve on. The single successful seed reported earlier was not representative of the method's average performance.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/FINDINGS.md
  - source: lab-layer simulation, untargeted-probe ripple
    scenario: a large, whole-channel perturbation rather than a channel specific to the suspected link
    finding: negative
    summary: A blunt intervention that disables an entire shared channel can make every participant who uses that channel look complicit, producing a correct-looking merge for the wrong reason. Telling that ripple apart from a real, localized response is only partly automated and was not carried over to every detector variant.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/FINDINGS.md
related:
  - intervention-supported-unit-discovery
  - adversarial-boundary-discovery
  - et-external-transfer
  - experiment-methodology
  - evidence-and-uncertainty
external:
  - label: Lab-layer simulation findings (full negative and positive ledger)
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/FINDINGS.md
  - label: Experiment lines and claim strength
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/docs/EXPERIMENTS.md
---

A method that works once, in a controlled setting, is a proof of concept — not a validated instrument. The project's practice is to say so explicitly rather than stop at the first success.

An intervention-based unit-discovery method that had just recovered a genuinely coordinating pair in a two-participant test was pushed harder in two directions. First, a third, non-coordinating participant was added to the scene, to check whether a blunt channel-disabling probe would falsely implicate the bystander (a "ripple" failure) or whether the underlying detector would hold up at all. It did not hold up: on this harder scenario the same method missed the real coordinating pair entirely — a different, and in some ways more basic, failure than the ripple risk it was built to guard against.

Second, the original two-participant scenario was re-run across several random seeds instead of the one that had produced the earlier success. Exact recovery fell to roughly one run in five, statistically indistinguishable from the simpler baseline method the intervention-based approach was meant to outperform.

Neither result overturns the narrower, load-bearing claim that the method's core mechanism — comparing an intervention's effect against a measured baseline rather than a fixed one — behaves correctly and reproduces known results on deterministic systems. What it does show is that extending the method to noisy, model-driven, multi-participant systems is not yet reliable, and that a single success on one seed of one scenario should not be read as more than that. The technical findings log records both the success and these failures side by side, on purpose.
