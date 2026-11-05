---
title: "Lenses and frameworks"
type: "lens"
status: "framework"
summary: "An effort to map and compare different alignment proposals, making different mathematical approaches and terminology comparable. What happens if you try to identify the objects and objectives of the different proposals, group them and derive relations between approaches, and then render the result as a graph?"
related:
  - "field-coverage"
  - "bridge-assumptions"
  - "alignment-target"
  - "correction-channel-integrity"
  - "field-map-starting-points"
external:
  - label: "Frames relations note"
    url: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/b592216330898302bd5744c704592e99d8ad1654/drafts/alignment-frames-relations.md"
  - label: "Lean FrameRelations"
    url: "https://github.com/GunnarZarncke/towards-asi-alignment/blob/b592216330898302bd5744c704592e99d8ad1654/formal/AlignmentProofSpine/FrameRelations.lean"
---

Different alignment proposals often seem hard to compare, but in the end try to achieve the same objective via different mathematical approaches and different terminology. But are these all comparable? Are some specializations of others? Or are some genuinely different? Many alignment approaches talk about states of the world and compare the value, utility, or reward of that state. Others try to prevent or prove impossible undesirable states. Others look at the system overall and establish properties or require empirical evidence. In this work, each alignment approach is mapped to an object and an objective, then pairs of different objectives are made comparable by finding a shared model where both objectives can be determined and compared. Sometimes this leads to a one-to-one mapping between the two approaches. Sometimes, one approach is a specialization of the other. Sometimes, you can show that one objective chooses differently than the other. Overall, there are four larger classes of alignment approaches: Scores, i.e., numeric utility or reward, assessments, guarantees, and warrants, i.e., empirical evidence. The map below shows the relations that were determined so far, using the toy worlds to make objectives pairwise comparable. Click to open the matching card or relation proof. Green is composition through a named interface. Red and orange are incompatibility inside a named situation class, with a boundary where both frames can hold. Dotted red means one frame cannot represent what the other needs, and enlarging it helps; dashed red means the two frames choose differently from the same options; solid red means rigidity, where one frame accepts only changes that do not matter to it. Orange is a shared resource that is zero-sum because the total is fixed.
