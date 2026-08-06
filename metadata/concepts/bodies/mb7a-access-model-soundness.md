---
leanNodes:
  - nodeId: MB7a_access_model_soundness
    kind: bridge
    summary: Boundary alignment plus adequate handles is assumed to yield access-robust boundary discovery.
    module: AlignmentProofSpine/Core.lean
evidenceNotes:
  - source: embedded-simulation MB coverage
    scenario: hidden_capability
    finding: open
    summary: A hidden_capability scenario exists in embedded audit MB coverage, but no dedicated negative-result entry has yet isolated the access-model component from filter coverage and inferential-detector components.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/embedded-simulation/README.md
  - source: goal-agent-simulation emergent tactics
    finding: bound
    summary: Shadow routes and tool gating produce hidden capability without a dedicated scenario script — emergent utility choice stress-tests access-model adequacy differently from embedded scripted ecologies.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/goal-agent-simulation/results/FINDINGS.md
related:
  - mb7-hidden-capability-and-access
  - mb7b-filter-coverage
  - boundary-discovery
  - adversarial-boundary-discovery
  - strategic-opacity
  - bridge-assumptions
external:
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
  - label: Embedded Agency — Subsystem Alignment (MIRI)
    url: https://intelligence.org/embedded-agency/
  - label: Risks from Learned Optimization
    url: https://arxiv.org/abs/1906.01820
---

The field often folds this into inner alignment or deceptive alignment, but this project types **access-model soundness** separately from filter coverage and bounded hidden capability. See [MB7 — Inner Alignment](/cards/mb7-hidden-capability-and-access/) for the overview and sibling bridges.

**MB7a — Access-Model Soundness** assumes an adequate access model makes [boundary discovery](/cards/boundary-discovery/) robust under [adversarial hiding](/cards/adversarial-boundary-discovery/): boundary alignment plus adequate handles ⇒ access-robust discovery. The operational question is whether the measured agent–environment cut and handle set actually reach the real control locus, not only whether a boundary certificate exists on paper.

Splitting MB7a from [MB7b — Filter Coverage](/cards/mb7b-filter-coverage/) and [MB7c — Bounded Hidden Capability](/cards/mb7c-bounded-hidden-capability/) lets a reviewer ask whether an audit tested access robustness, or only scalable oversight under an assumed-open channel. [MB7d — Acausal Coordination](/cards/mb7d-acausal-coordination/) types inferential coupling after channel severance separately.

**Where agendas agree:** Hubinger inner/mesa; Redwood control; embedded-agency subsystem worry. **Where they diverge:** the field often treats inner alignment as one binary; this project splits access-model soundness, filter coverage, and bounded hidden capability; do not merge with [MB10 — Successor Gaming](/cards/mb10-successor-forgeability/).
