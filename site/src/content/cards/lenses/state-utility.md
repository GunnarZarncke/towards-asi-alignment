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
  - label: "LessWrong tag: Expected utility formalism"
    url: "https://www.lesswrong.com/w/expected-utility-formalism"
---

**Role.** Target. Graph node `state`.

> State value is adequate when the state carries all normatively relevant information. It is not adequate merely because an implementation calls its representation a state.
>
> — Frames draft §4.1

This is the default welfare object. In RL, the per-step state reward summed along a path is a route value, not this (`markov_reward_not_state_utility`); its optimal value function is a state utility, and that is where Omohundro-style instrumental arguments meet correction. *State* means the bare state, with no record of how it was reached; adding the record gives the record-carrying state lens, where round trips can have value.

Fixed *U* is incompatible with correction only for updates that make the agent pick an outcome *U* ranks strictly lower — not for every change of *U*. At its optimum it accepts a correction only if the target ties the optimum, and it never prefers keeping the channel (`state_accepts_only_ties`). That is the red edge `stateCorrectionIncompat`, not “utility hates all revision.” It holds by the choice of situation class; what correction endorses is not modeled.
