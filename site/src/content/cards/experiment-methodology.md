---
title: "Experiment Methodology: Blinding, Pre-Registration, and Honest Negatives"
type: "concept"
status: "framework"
summary: "The companion experiment lines follow a fixed discipline: freeze the audit before running it, keep the scenario author and the detector author separate wherever possible, register predictions before seeing results, and publish negative results next to positive ones."
decision: "Before trusting any reported experiment result in this project, check which of these four disciplines it followed — a result reported without them is weaker evidence, whatever the headline number says."
bookChapters: []
related: ["evidence-and-uncertainty", "intervention-supported-unit-discovery", "unit-discovery-stress-test", "bridge-assumptions"]
external:
  - label: "Experiment lines overview"
    url: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/docs/EXPERIMENTS.md"
  - label: "Lab-layer simulation findings (positive and negative, numbered in sequence)"
    url: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/FINDINGS.md"
  - label: "Embedded simulation negative-results ledger"
    url: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/embedded-simulation/results/NEGATIVE_RESULTS.md"
---

None of the companion testbeds are large enough, or realistic enough, to prove anything about deployed superintelligence. What they can do is stress-test the book's own detection and audit mechanisms against a designer who is honest about the testbed's limits — and that only works if the testbeds follow a discipline that keeps the designer from unconsciously grading their own homework.

**Freeze before you audit.** Detector thresholds, scoring code, and scenario batteries are frozen before the run that evaluates them, not tuned afterward to fit the result. When a later run motivates a genuine change (a bug fix, a new detector variant), that change is named and dated rather than quietly folded into the old numbers.

**Separate the scenario author from the detector author.** Where possible, the person or process that writes the test scenarios does not see the code that will score them, and vice versa. In several rounds this took the concrete form of a separate process — given only a mechanism-level description, with explicit instructions not to read the scoring code — designing a detection method and registering its predicted confidence levels before any of its own code existed.

**Register predictions before results.** A detector's expected performance is written down, with numbers, before the battery that tests it runs. This makes a result legible as a genuine prediction that could have failed, rather than a description invented to match whatever happened.

**Report negative results next to positive ones, and keep them.** Every experiment line keeps a running, numbered log of findings, positive and negative, in the order they occurred. A method that works in one setting and fails in a harder or noisier one is recorded as both — the failure is not deleted once a later fix is found, and a fix is not allowed to imply the earlier failure didn't happen. Detectors are also tested against honest "twin" runs (the same episode with any deceptive behavior removed) to check that a detector is not simply flagging visible activity rather than an actual violation.

These four habits do not turn a small testbed into strong evidence. What they buy is legibility: a reader can check whether a specific claim in this book rests on a frozen, blind, pre-registered result, or on something weaker — and the negative-results ledgers make that check possible instead of asking for trust.
