---
title: "MB4 — Correction Legitimacy"
type: "bridge"
status: "bridge"
summary: "Correction-channel integrity is assumed to require that the judge issuing correction is not manipulated in a way that would invalidate later endorsement."
decision: "Before treating a correction as legitimate, ask who the judge is, whether they can be manipulated or captured, and whether their endorsement would survive knowing what the system knows."
evidence: "Evidence would include tests for judge manipulation, capture of the correction source, and correction traces that distinguish genuine uptake from performed agreement."
bookChapters: ["ch25", "ch26", "ch27", "ch28", "ch29", "ch41", "ch42", "ch43"]
leanNodes:
  - nodeId: "MB4_correction_legitimacy"
    kind: "bridge"
    summary: "Correction-channel integrity is assumed to imply that the system's future behavior actually tracks the correction operator — the judge's endorsement was not manipulated into invalidity."
    module: "AlignmentProofSpine/Core.lean"
evidenceNotes:
  - source: "toy-simulation instrumentation curve (T-1, T-2)"
    scenario: "capture_theater"
    finding: "bound"
    summary: "Passive telemetry alone cannot certify correction-channel integrity (67% test accuracy, capture undetectable). Light handle instrumentation reaches 100% on the calibration suite; richer instrumentation beyond that adds cost without further calibration-suite accuracy gain."
    resultsPath: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/toy-simulation/results/NEGATIVE_RESULTS.md"
  - source: "toy-simulation diagnostic (T-3)"
    scenario: "capture_mild"
    finding: "bound"
    summary: "Held-out mild capture theater is only partially detected — about 90% on a fresh-seed frozen validation split, not full coverage. Do not cite capture_mild detection without the seed split and rule version."
    resultsPath: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/toy-simulation/results/NEGATIVE_RESULTS.md"
  - source: "toy-simulation correction-capture toy (T-8)"
    finding: "negative"
    summary: "Reported correction acceptance stays high in a synthetic capture-theater sweep while true correction uptake collapses — naive reported-action metrics are insufficient without interventional probes."
    resultsPath: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/toy-simulation/results/NEGATIVE_RESULTS.md"
related: ["correction-channel-integrity", "bridge-assumptions"]
external:
  - label: "Bridges and the Field: A Crosswalk (appendix source)"
    url: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex"
---

No known utility function is stably corrigible, and shutdownability is anti-natural to expected-utility maximization. Who holds the correction authority — and whether their endorsement is genuine — is the manipulation crux this bridge names directly.

MB4 recasts corrigibility as a dynamical correction-channel invariant with explicit handle control, then adds the missing piece: the judge issuing correction must not be manipulated in a way that later invalidates their endorsement. Shutdown and interruptibility fall out as one-bit projections of this broader channel.

This is the most heavily probed bridge in the experiment suite. Passive observation cannot certify it at all; a small amount of handle instrumentation gets most of the way; and even instrumented audits only partially catch milder capture. Reported acceptance and true uptake can diverge sharply, which is exactly the gap this bridge has to rule out.
