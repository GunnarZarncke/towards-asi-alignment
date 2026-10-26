---
title: "Lenses and frameworks"
type: "lens"
status: "framework"
summary: "Alignment proposals are compared as if they supplied rival objective functions. Separate the object, the assessment or guarantee, and the warrant — then the red edges say when two frames cannot both accept the same situation."
related:
  - "field-coverage"
  - "bridge-assumptions"
  - "alignment-target"
  - "correction-channel-integrity"
  - "field-map-starting-points"
external:
  - label: "Frames relations note"
    url: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/drafts/alignment-frames-relations.md"
  - label: "Lean FrameRelations"
    url: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/formal/AlignmentProofSpine/FrameRelations.lean"
---

Alignment work is often scored as if every proposal were a competing utility. That flattens targets, constraints, dynamical guarantees, and evidence protocols into one overloaded word. A state utility, an attainable-option penalty, a correction channel, a viability kernel, an AI-control monitor, and a safety case can all guide a deployment decision; they are not alternative scalars.

The map below is one **correction-centered** reading of how those frames specialize, project, compose, or conflict. Nodes open the matching lens card. Edge labels with a Lean counterpart open it on GitHub: the proof for a red edge, the closed-walk lemma for a summand, the theorem for a limit or strengthens edge, the registry for the other kinds. Green is composition through a named interface, not implication. Red and orange are incompatibility inside a named situation class, with a boundary where both frames can hold. The line says how bad: dotted means one frame cannot represent what the other needs, and enlarging it helps; dashed means the two frames choose differently on the same menu; solid means rigidity, where one frame accepts only changes that do not matter to it. Orange is a shared resource that is zero-sum because the total is fixed.
