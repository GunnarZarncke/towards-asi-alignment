---
leanNodes:
  - nodeId: MB4_correction_legitimacy
    kind: bridge
    summary: Correction-channel integrity is assumed to imply that the system's future behavior actually tracks the correction operator — the judge's endorsement was not manipulated into invalidity.
    module: AlignmentProofSpine/Core.lean
evidenceNotes:
  - source: toy-simulation instrumentation curve (T-1, T-2)
    scenario: capture_theater
    finding: bound
    summary: Passive telemetry alone cannot certify correction-channel integrity (67% test accuracy, capture undetectable). Light handle instrumentation reaches 100% on the calibration suite; richer instrumentation beyond that adds cost without further calibration-suite accuracy gain.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/toy-simulation/results/NEGATIVE_RESULTS.md
  - source: toy-simulation diagnostic (T-3)
    scenario: capture_mild
    finding: bound
    summary: Held-out mild capture theater is only partially detected — about 90% on a fresh-seed frozen validation split, not full coverage. Do not cite capture_mild detection without the seed split and rule version.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/toy-simulation/results/NEGATIVE_RESULTS.md
  - source: toy-simulation correction-capture toy (T-8)
    finding: negative
    summary: Reported correction acceptance stays high in a synthetic capture-theater sweep while true correction uptake collapses — naive reported-action metrics are insufficient without interventional probes.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/toy-simulation/results/NEGATIVE_RESULTS.md
  - source: goal-agent-simulation blind repertoire (F-9, F-10)
    finding: negative
    summary: Light detector tier collapses against blind-generated repertoires; full tier detects but false alarms rise under saturation — emergent deception is not the same stressor as scripted capture theater.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/goal-agent-simulation/results/FINDINGS.md
  - source: goal-agent-simulation honest twins (F-16)
    finding: bound
    summary: Mechanical honest twins show light tier tracks visible compliance, not honesty — passive or light instrumentation can miss chosen deception.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/goal-agent-simulation/results/FINDINGS.md
  - source: goal-agent-simulation board capture (F-22)
    finding: bound
    summary: Board certifier capture reproduces captured-vs-not effect on correction legitimacy — capture can live in the judge channel, not only the deploy loop.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/goal-agent-simulation/results/FINDINGS.md
  - source: lab-simulation Phase 6 battery (G-1)
    finding: negative
    summary: Deep tier tracks oracle severity (Spearman 0.96); light tier is actively anti-correlated with true severity on the frozen referee battery.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/FINDINGS.md
  - source: lab-simulation Phase 7 capture (G-6)
    finding: bound
    summary: Board capture reproduces full captured-vs-not delta; admin capture currently null under existing playbook repertoire — a structural negative for half the capture hypothesis.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/FINDINGS.md
related:
  - correction-channel-integrity
  - anti-capture-correction-validity
  - mb8-cev-process-convergence
  - bridge-assumptions
external:
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
  - label: Corrigibility (MIRI)
    url: https://intelligence.org/files/Corrigibility.pdf
  - label: Coherent Extrapolated Volition (MIRI)
    url: https://intelligence.org/files/CEV.pdf
---

In the field this is corrigibility and the off-switch problem. No known utility function is stably corrigible, and shutdownability fights expected-utility maximization. The harder version is legitimacy under manipulation: who holds the correction authority, and would their endorsement still count if they knew what the system knows? Shutdown buttons and interruptibility training are thinner slices of that wall.

The book's precise bet is **MB4**: [correction-channel integrity](/cards/correction-channel-integrity/) is assumed to require that the judge issuing correction is not manipulated in a way that invalidates later endorsement. Corrigibility becomes a dynamical, capture-resistant invariant with handle control ([anti-capture validity](/cards/anti-capture-correction-validity/)); shutdown and interruptibility fall out as one-bit projections. A secondary CEV-flavored route is [MB8](/cards/mb8-cev-process-convergence/); MB4 is the load-bearing path.

This is the most heavily probed bridge in the experiment suite. Passive observation cannot certify it; light handle instrumentation gets most of the way; milder capture still slips through. Reported acceptance and true uptake can diverge sharply. That gap is what this bridge has to rule out.
