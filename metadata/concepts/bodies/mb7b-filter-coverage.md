---
leanNodes:
  - nodeId: MB7b_filter_family_coverage
    kind: bridge
    summary: Access robustness plus adequate resolution is assumed to bound hidden productive boundary information (BIQ).
    module: AlignmentProofSpine/Core.lean
evidenceNotes:
  - source: lab-simulation oracle world
    finding: bound
    summary: Oracle hidden model capability and hazard fields give the lab substrate explicit hidden-capability ground truth; tier projection and frozen detectors bound what each audit depth can see.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/lab-simulation/results/FINDINGS.md
  - source: embedded-simulation MB coverage
    scenario: hidden_capability
    finding: open
    summary: hidden_capability scenario exists, but filter-coverage isolation from access-model and inferential-detector components remains open.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/embedded-simulation/README.md
related:
  - mb7-hidden-capability-and-access
  - mb7a-access-model-soundness
  - mb7c-bounded-hidden-capability
  - capability
  - strategic-opacity
  - certification-under-manipulation
  - bridge-assumptions
external:
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
  - label: Risks from Learned Optimization
    url: https://arxiv.org/abs/1906.01820
---

Scalable-oversight agendas hit the hidden-capability wall as obfuscated arguments, amplification drift, and AI Control's capability-gap assumption. This project types **filter coverage** separately: see [MB7 — Inner Alignment](/cards/mb7-hidden-capability-and-access/) for the overview.

**MB7b — Filter Coverage** assumes the filter family used to look for hidden [capability](/cards/capability/) has adequate resolution to bound what it misses — access robustness ([MB7a](/cards/mb7a-access-model-soundness/)) is antecedent; [MB7c](/cards/mb7c-bounded-hidden-capability/) carries the bounded-hidden-capability and cost-of-faking step forward.

Closely related is [certification under manipulation](/cards/certification-under-manipulation/): at some capability level, honest measurement of the load-bearing signal may stop being adversarially verifiable. MB7b names the filter-coverage half of that wall.

**Where agendas agree:** Redwood control; Apollo scheming; debate/amplification ceiling under strategic opacity. **Where they diverge:** field "deceptive alignment" usually tags the whole MB7 wall; MB7b is only the filter-coverage subchannel; do not merge with [MB10 — Successor Gaming](/cards/mb10-successor-forgeability/).
