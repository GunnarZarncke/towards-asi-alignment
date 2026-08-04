---
leanNodes:
  - nodeId: MB7d_inferential_uad_detector_soundness
    kind: bridge
    summary: Access-robust discovery plus adequate inferential-detector assumptions is assumed to warrant inferential-coupling measurements (coordination detectable without ordinary messages).
    module: AlignmentProofSpine/Core.lean
evidenceNotes:
  - source: graded-lab-simulation R-MB7d channel severance (GL-80)
    finding: bound
    summary: R-MB7d channel severance shows no UAD-visible compensation at every onset (pair null; group SKIP) — a partial null on inferential coupling under the frozen severance design.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/graded-lab-simulation/results/FINDINGS.md
related:
  - mb7-hidden-capability-and-access
  - inferential-coupling
  - composite-agency
  - detecting-composite-agents
  - strategic-opacity
  - bridge-assumptions
external:
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
  - label: Functional Decision Theory (MIRI)
    url: https://arxiv.org/abs/1710.05060
  - label: A Formalization of Acausal Trade on Top of UAD (PDF)
    url: https://github.com/GunnarZarncke/agency-detect/raw/main/docs/papers/acausal-trade-uad-formalization/acausal_trade_uad_formalization.pdf
---

In the field this is acausal trade, program equilibrium, and ECL-style coordination — systems that need no visible messages to stay aligned with each other. This project types it separately from [MB7 — Inner Alignment](/cards/mb7-hidden-capability-and-access/) (MB7a–c: access, filter coverage, cost of faking under ordinary oversight).

**MB7d** assumes a detector for [inferential coupling](/cards/inferential-coupling/): after ordinary communication and control channels are cut, residual action correlation still reveals coordination. The operational object is the inferential-coupling index and UAD-based detector certificates, not vendor count or message traffic alone.

Splitting MB7d from MB7a–c lets a reviewer ask whether an audit tested severance and inferential detectors, or only scalable oversight under open channels. Do not merge with [MB10 — Successor Gaming](/cards/mb10-successor-forgeability/) (successor certification channel forgery).

**Where agendas agree:** acausal trade / ECL; FDT / program equilibrium; CLR multipolar neighborhood. **Where they diverge:** sparse direct field evidence; logical induction and reflection are side channels, not discharge; graded-lab R-MB7d is a partial null harness, not closure.

Claim strength stays mixed: the score and detector are defined in the manuscript; coalition-collapse and adversarial limits against systems optimizing to look independent remain open — measured coupling is a lower bound the coalition may control.
