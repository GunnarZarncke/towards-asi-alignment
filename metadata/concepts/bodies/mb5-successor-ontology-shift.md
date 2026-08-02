---
leanNodes:
  - nodeId: MB5_ontology_shift_successor_audit
    kind: bridge
    summary: Full transport plus bearer transport across an ontology shift are assumed to compose into successor safety.
    module: AlignmentProofSpine/Core.lean
evidenceNotes:
  - source: toy-simulation diagnostic (T-7)
    scenario: successor_relabel
    finding: negative
    summary: Light-handle instrumentation false-passes 100% of diagnostic seeds where a successor's identity is relabeled or discontinuous at the transition; medium/strong handles with epoch-split interventional CCI catch all of them.
    resultsPath: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/experiments/toy-simulation/results/NEGATIVE_RESULTS.md
related:
  - successor-stability
  - value-bundle-transport
  - bearer-persistence
  - conserved-properties-growth-split-merge
  - mb10-successor-forgeability
  - bridge-assumptions
external:
  - label: 'Bridges and the Field: A Crosswalk (appendix source)'
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
  - label: Tiling Agents (MIRI)
    url: https://intelligence.org/files/TilingAgentsDraft.pdf
  - label: Vingean Reflection (MIRI)
    url: https://intelligence.org/files/VingeanReflection.pdf
  - label: Ontological Crises (de Blanc)
    url: https://arxiv.org/abs/1105.3821
---

In the field this is tiling and Vingean reflection, plus ontology identification (the diamond-maximizer worry). Can an agent trust a successor it cannot fully verify? Does a goal even survive when the world-model underneath it is rebuilt? Saying "the successor shares our values" is cheap if the ontology that interprets those values has shifted out from under them.

The book's precise bet is **MB5**: full [value-bundle transport](/cards/value-bundle-transport/) plus [bearer transport](/cards/bearer-persistence/) surviving an ontology shift are assumed to compose into [successor safety](/cards/successor-stability/). The check runs over the [seven conserved properties](/cards/conserved-properties-growth-split-merge/), not over slogan agreement. That is a strengthening over "the successor says the right words," but the composition itself is still assumed, not derived from something more basic. Closely related is [MB10](/cards/mb10-successor-forgeability/), which asks whether that green checklist can be forged.

**Where agendas agree:** MIRI tiling / Vingean reflection / ontology identification. **Where they diverge:** the book separates successor audit gaming as MB10; natural abstractions ease but do not discharge transport. **Split:** MB5 = transport holds; MB10 = successor certification checklist not forgeable.

Diagnostic evidence shows the practical gap: a relabeled or discontinuous successor identity can be invisible to light instrumentation and only show up once the audit splits the epoch and probes across it.
