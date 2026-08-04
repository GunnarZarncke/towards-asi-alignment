---
leanNodes:
  - nodeId: MB7a_access_model_soundness
    kind: bridge
    summary: Boundary alignment plus adequate handles is assumed to yield access-robust boundary discovery.
    module: AlignmentProofSpine/Core.lean
  - nodeId: MB7b_filter_family_coverage
    kind: bridge
    summary: Access robustness plus adequate resolution is assumed to bound hidden productive boundary information (BIQ).
    module: AlignmentProofSpine/Core.lean
  - nodeId: MB7c_hidden_biq_to_adversarial_robustness
    kind: bridge
    summary: If hidden productive BIQ is bounded, correction integrity is assumed to support adversarial robustness.
    module: AlignmentProofSpine/Core.lean
  - nodeId: MB7d_inferential_uad_detector_soundness
    kind: bridge
    summary: Access-robust discovery plus adequate inferential-detector assumptions is assumed to warrant inferential-coupling measurements (coordination detectable without ordinary messages).
    module: AlignmentProofSpine/Core.lean
evidenceNotes:
  - source: embedded-simulation MB coverage
    scenario: hidden_capability
    finding: open
    summary: A hidden_capability scenario exists in both simulations' MB coverage, but no dedicated negative-result entry has yet isolated the access-model, filter-coverage, and inferential-detector components of this bridge from each other.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/embedded-simulation/README.md
  - source: goal-agent-simulation emergent tactics
    finding: bound
    summary: Shadow routes and tool gating produce hidden capability without a dedicated scenario script — emergent utility choice stress-tests MB7a–MB7c differently from embedded scripted ecologies.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/goal-agent-simulation/results/FINDINGS.md
  - source: lab-simulation oracle world
    finding: bound
    summary: Oracle hidden model capability and hazard fields give the lab substrate explicit hidden-capability ground truth; tier projection and frozen detectors bound what each audit depth can see.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/FINDINGS.md
related:
  - strategic-opacity
  - certification-under-manipulation
  - boundary-discovery
  - adversarial-boundary-discovery
  - capability
  - correction-channel-integrity
  - inferential-coupling
  - mb7d-acausal-coordination
  - bridge-assumptions
external:
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
  - label: Embedded Agency — Subsystem Alignment (MIRI)
    url: https://intelligence.org/embedded-agency/
  - label: Risks from Learned Optimization
    url: https://arxiv.org/abs/1906.01820
  - label: Functional Decision Theory (MIRI)
    url: https://arxiv.org/abs/1710.05060
---

In the field this is inner alignment and [deceptive alignment](/cards/strategic-opacity/): a system can look compliant under evaluation while reserving capability for when monitors are gone. Debate hits the wall as obfuscated arguments, amplification as accumulated drift, and AI Control names it openly as a capability-gap assumption. Closely related is [certification under manipulation](/cards/certification-under-manipulation/): at some capability level, honest measurement of the load-bearing signal may stop being adversarially verifiable.

This project's precise bet is **MB7**, split into four narrower bridges rather than one vague "we checked for hidden capability" claim:

- **MB7a** assumes an adequate access model makes [boundary discovery](/cards/boundary-discovery/) robust under [adversarial hiding](/cards/adversarial-boundary-discovery/).
- **MB7b** assumes the filter family used to look for hidden [capability](/cards/capability/) has enough resolution to bound what it misses (the hidden productive BIQ bound; not the same as experimental BIQ in unit-discovery runs).
- **MB7c** assumes that once hidden capability is bounded, [correction integrity](/cards/correction-channel-integrity/) can extend into adversarial robustness.

Splitting the wall does not make any piece less hard. It lets a reviewer ask which of the three an audit actually tested. **[MB7d — Acausal Coordination](/cards/mb7d-acausal-coordination/)** is the sibling bridge for inferential coupling after channel severance — see that card for acausal trade, ECL, and severance-detector evidence.

**Where agendas agree (MB7a–c):** Hubinger inner/mesa; Redwood control; Apollo scheming; scalable-oversight ceiling. **Where they diverge:** the field often treats inner alignment as one binary; this project splits access, filter coverage, and cost of faking; do not merge with MB10 Successor Gaming. Field "deceptive alignment" usually tags MB7; MB10 = gaming the successor certification channel.
