---
title: "MB5 — Successor and Ontology-Shift Audit"
type: "bridge"
status: "bridge"
summary: "Full transport plus bearer transport surviving an ontology shift are assumed to compose into successor safety."
decision: "Before certifying a successor, ask whether the transport check spans the actual ontology change the successor introduces, not just the properties that were easy to measure."
evidence: "Evidence would include successor-transition audits that detect relabeling, epoch shifts, or identity discontinuities that a narrower check would miss."
bookChapters: ["ch28", "ch29", "ch30", "ch31"]
leanNodes:
  - nodeId: "MB5_ontology_shift_successor_audit"
    kind: "bridge"
    summary: "Full transport plus bearer transport across an ontology shift are assumed to compose into successor safety."
    module: "AlignmentProofSpine/Core.lean"
evidenceNotes:
  - source: "toy-simulation diagnostic (T-7)"
    scenario: "successor_relabel"
    finding: "negative"
    summary: "Light-handle instrumentation false-passes 100% of diagnostic seeds where a successor's identity is relabeled or discontinuous at the transition; medium/strong handles with epoch-split interventional CCI catch all of them."
    resultsPath: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/toy-simulation/results/NEGATIVE_RESULTS.md"
related: ["successor-stability", "bridge-assumptions", "mb10-successor-forgeability"]
external:
  - label: "Bridges and the Field: A Crosswalk (appendix source)"
    url: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex"
---

Tiling agents and ontological crises name two versions of the same worry: can an agent trust a successor it cannot fully verify, and does a goal even survive when the world-model underneath it is rebuilt?

MB5 answers by composing two checks — full goal transport, and bearer transport specifically surviving the ontology shift — into a successor-safety conclusion. It is a genuine strengthening over "the successor says the right words," but it is still a bridge: the composition is assumed to be sound, not derived from anything more basic.

The diagnostic evidence shows the gap this bridge needs to close in practice. A relabeled or discontinuous successor identity is invisible to light instrumentation and only becomes visible once the audit deliberately splits the epoch and probes across it.
