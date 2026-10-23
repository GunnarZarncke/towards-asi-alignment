---
title: "State utility"
type: "lens"
status: "framework"
summary: "A scalar order or welfare score on snapshots. Adequate only if the state already carries what matters."
related:
  - "static-target-trap"
  - "pointing-problem"
  - "outer-alignment"
  - "lenses/lenses-and-frameworks"
  - "field-agendas/chai-russell"
  - "field-agendas/miri"
  - "field-agendas/openai-lab"
external:
  - label: "LessWrong tag: Expected utility"
    url: "https://www.lesswrong.com/w/expected-utility-formalism"
---

**Role.** Target. Graph node `state`.

> State value is adequate when the state carries all normatively relevant information. It is not adequate merely because an implementation calls its representation a state.
>
> — Frames draft §4.1

This is the default RL and welfare object. Omohundro-style instrumental arguments live here.

Fixed (U) is incompatible with correction only for updates that make the agent pick an outcome (U) ranks strictly lower — not for every change of (U). That is the proved red edge `stateCorrectionIncompat`, not “utility hates all revision.”
