---
formulas:
  - id: appi:eq:field-trace-biq
    latex: \widehat{\mathrm{BIQ}}_m(t)\leq 2\lceil\log_2\min(m,|\mathcal{A}|)\rceil
    explanation: 'Appearance bound: m-row subsample trace BIQ is capped by the tight optimism ceiling (TraceBIQ finite module).'
    chapterId: ch11
  - id: appi:eq:field-hidden-biq-forward
    latex: \mathrm{Control}(A)\leq \mathrm{CCI}(A)+\delta\ \Rightarrow\ \mathrm{RiskGap}(A)\leq\delta
    explanation: 'Forward bridge shape: when hidden productive control is bounded by correction capacity slack, RiskGap is bounded (HiddenBIQCertificate).'
    chapterId: ch33
  - id: appi:eq:field-appearance-not-discharge
    latex: \widehat{\mathrm{BIQ}}_m\leq B_{\mathrm{ceiling}}\ \not\Rightarrow\ \mathrm{Control}(A)\leq \mathrm{CCI}(A)+\delta
    explanation: 'Non-discharge: subsample appearance ceilings are one-way bounds — bounded trace readout does not imply hidden BIQ or CCI discharge (no Field-style converse; empirical N-8 negative).'
    chapterId: ch43
leanNodes:
  - nodeId: subsample_biq_le_tight_optimism
    kind: proof
    summary: Tight subsample trace BIQ ceiling — apparent BIQ at most twice the log alphabet optimism bound.
    module: AlignmentProofSpine/Field/Finite/TraceBIQ.lean
  - nodeId: trace_sampling_absolute_appearance_bound
    kind: proof
    summary: Certificate-backed subsample trace cannot exceed traceBIQOptimism ceiling.
    module: AlignmentProofSpine/Field/Finite/TraceBIQ.lean
  - nodeId: trace_derived_risk_bound
    kind: proof
    summary: Trace-derived numeric risk leaf bounded via appearance ceiling (when bridge interfaces align).
    module: AlignmentProofSpine/Field/Finite/TraceBIQ.lean
  - nodeId: risk_gap_bound_from_hidden_biq_certificate
    kind: proof
    summary: 'Forward: HiddenBIQCertificate (control bounded by CCI slack) implies RiskGap bound.'
    module: AlignmentProofSpine/Capability.lean
  - nodeId: MB7c_hidden_biq_to_adversarial_robustness
    kind: bridge
    summary: 'Bridge MB7c: hidden BIQ bounded and filters cover productive channels → adversarial robustness handoff.'
    module: AlignmentProofSpine/Core.lean
citeKeys:
  - hubinger2019risks
---

Inner-alignment and oversight agendas ask whether hidden productive capability can evade monitors. Trace-computed BIQ and subsample audits measure **appearance** — what a bounded trace window can see — not full productive control.

Lean proves **appearance ceilings**: subsample trace BIQ cannot exceed tight optimism bounds (`subsample_biq_le_tight_optimism`, `trace_sampling_absolute_appearance_bound`). When a HiddenBIQCertificate is supplied, RiskGap inherits CCI slack (`risk_gap_bound_from_hidden_biq_certificate`). MB7c remains an explicit bridge to adversarial robustness.

There is **no** Field-style non-converse separation theorem of the form “high apparent BIQ ∧ failed hidden-BIQ bound.” The load-bearing calibration is one-way: appearance bounds cap what trace evidence can show; they do not discharge hidden productive BIQ. Embedded-simulation line N-8 records empirical separation of trace appearance from passive UAD under subsampling stress.

*What inner-alignment / ELK / AI-control work keeps that this crosswalk does not replace:* access protocols, filter families, red-team batteries, and training-time obfuscation — the engineering that might or might not make appearance track reality.
