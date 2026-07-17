---
leanNodes:
  - nodeId: MB7a_access_model_soundness
    kind: bridge
    summary: Boundary alignment plus adequate handles is assumed to yield access-robust boundary discovery.
    module: AlignmentProofSpine/Core.lean
  - nodeId: MB7b_filter_family_coverage
    kind: bridge
    summary: Access robustness plus adequate resolution is assumed to bound hidden productive boundary information (B-IQ).
    module: AlignmentProofSpine/Core.lean
  - nodeId: MB7c_hidden_biq_to_adversarial_robustness
    kind: bridge
    summary: If hidden productive B-IQ is bounded, correction integrity is assumed to support adversarial robustness.
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
  - boundary-discovery
  - bridge-assumptions
external:
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
---

Deceptive alignment is the shared inner-alignment wall across the field: debate hits it as obfuscated arguments, amplification hits it as accumulated drift, and AI Control names it openly as a capability-gap assumption. The book splits this single wall into four narrower, individually checkable bridges.

MB7a assumes an adequate access model makes boundary discovery robust to a system trying to hide from it. MB7b assumes the filter family used to look for hidden capability has enough resolution to bound what it misses. MB7c assumes that once hidden capability is bounded, correction integrity can extend into adversarial robustness. MB7d is the odd one out: it assumes a detector for coordination that survives cutting ordinary communication channels — closer to decision theory (acausal coordination, program equilibrium) than to mainstream oversight, and with little analog in other agendas.

Splitting the wall this way does not make any piece less hard. It does mean a reviewer can ask which of the four sub-bridges a given audit actually tested, instead of accepting "we checked for hidden capability" as one claim.
