---
leanNodes:
  - nodeId: MB7c_hidden_biq_to_adversarial_robustness
    kind: bridge
    summary: If hidden productive BIQ is bounded, correction integrity is assumed to support adversarial robustness.
    module: AlignmentProofSpine/Core.lean
evidenceNotes:
  - source: toy-simulation instrumentation curve (T-1, T-2)
    scenario: capture_theater
    finding: bound
    summary: Passive telemetry alone cannot certify correction-channel integrity; light handle instrumentation reaches full calibration-suite accuracy — relevant to whether bounded hidden BIQ plus correction integrity extend to adversarial robustness.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/toy-simulation/results/NEGATIVE_RESULTS.md
  - source: lab-simulation Phase 6 battery (G-1)
    finding: negative
    summary: Deep tier tracks oracle severity; light tier is actively anti-correlated with true severity on the frozen referee battery — a structural limit on claiming adversarial robustness from shallow monitors.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/FINDINGS.md
related:
  - mb7-hidden-capability-and-access
  - mb7a-access-model-soundness
  - mb7b-filter-coverage
  - correction-channel-integrity
  - certification-under-manipulation
  - strategic-opacity
  - bridge-assumptions
external:
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
  - label: Risks from Learned Optimization
    url: https://arxiv.org/abs/1906.01820
---

This is not [MB4 — Corrigibility](/cards/mb4-correction-legitimacy/) relabeled. **MB7c — Bounded Hidden Capability** is the closing step in the inner-alignment chain on [MB7 — Inner Alignment](/cards/mb7-hidden-capability-and-access/): the hidden productive BIQ bound (after [MB7b — Filter Coverage](/cards/mb7b-filter-coverage/)) plus [correction-channel integrity](/cards/correction-channel-integrity/) is assumed to support adversarially robust oversight — pricing the cost of faking the monitored signal.

The Lean bridge consumes correction integrity and bounded hidden productive BIQ as antecedents and yields adversarial robustness. Field readers often stop at "looks compliant under eval"; MB7c names the bet that hidden productive control stays bounded and that oversight remains adversarially robust under pressure.

Do not merge with [MB4a — Audit Independence](/cards/mb4a-measured-path-legitimacy/) (measured-path legitimacy) or [MB7d — Acausal Coordination](/cards/mb7d-acausal-coordination/) (inferential coupling after severance). [MB10 — Successor Gaming](/cards/mb10-successor-forgeability/) is the successor-certification cousin, not this subchannel.

**Where agendas agree:** AI Control cost-of-faking framing; certification-under-manipulation cousins. **Where they diverge:** reported compliance vs true uptake can diverge sharply; this bridge has to rule out performed agreement once hidden capability is claimed bounded.
