---
title: "Kosoy / infra-Bayesianism & LTA"
type: "agenda"
status: "reviewed"
summary: "Can a learning-theoretic theory of intelligent agents be built tightly enough to license alignment claims under stated assumptions, including misspecification, inner daemons, and recursive self-improvement? For Physicalist Superimitation: can agent detection and user identification pick out the intended user (including under simulation hypotheses), and does superimitation of inferred values stay well-defined when the world-model ontology is wrong?"
agendaSlug: "kosoy-infra-bayesianism-lta"
bookBridges:
  - "MB1"
  - "MB2"
  - "MB3"
  - "MB5"
  - "MB7"
  - "MB9"
external:
  - label: "LTA (2018 overview)"
    url: "https://www.alignmentforum.org/posts/5bd75cc58225bf0670375575/the-learning-theoretic-ai-alignment-research-agenda"
  - label: "LTA status (2023)"
    url: "https://www.alignmentforum.org/posts/ZwshvqiqCvXPsZEct/the-learning-theoretic-agenda-status-2023"
  - label: "Infra-Bayesianism (LessWrong)"
    url: "https://www.lesswrong.com/w/infra-bayesianism"
  - label: "Infra-Bayesian physicalism"
    url: "https://www.lesswrong.com/posts/gHgs2e2J5azvGFatb/infra-bayesian-physicalism-a-formal-theory-of-naturalized"
  - label: "PreDCA (Alignment Forum tag)"
    url: "https://www.alignmentforum.org/w/predca"
  - label: "Vanessa Kosoy"
    url: "https://www.alignmentforum.org/users/vanessa-kosoy"
related:
  - "alignment-target"
  - "target-realization"
  - "pointing-problem"
  - "mb2-bundle-identifiability"
  - "mb3-bearer-import"
---

<!-- GENERATED FILE — do not edit. Source: reference/field-agendas/data/agendas/kosoy-infra-bayesianism-lta.yml. Regenerate: cd site && npm run sync:field-agendas -->

## Introduction

Vanessa Kosoy's [learning-theoretic agenda](https://www.alignmentforum.org/posts/5bd75cc58225bf0670375575/the-learning-theoretic-ai-alignment-research-agenda) (LTA) aims to create a general mathematical theory of intelligent agents, so that alignment claims can be proved or rigorously conjectured relative to stated assumptions. Frequentist guarantees (regret bounds) are a *standard of understanding* in that theory. [Nonrealizability](/cards/subsumption-grounding-drift/) (the true environment is not in the hypothesis class) and inner [daemons](https://www.alignmentforum.org/posts/ZwshvqiqCvXPsZEct/the-learning-theoretic-agenda-status-2023) are among the *problems* the theory is built to treat. [Infra-Bayesianism](https://www.lesswrong.com/w/infra-bayesianism) is a major constructive layer for deep uncertainty—not the whole agenda. [Infra-Bayesian physicalism](https://www.lesswrong.com/posts/gHgs2e2J5azvGFatb/infra-bayesian-physicalism-a-formal-theory-of-naturalized) (later also Formal Computational Realism) adds a physicalist/computational-realist ontology; the [bridge transform](https://www.lesswrong.com/posts/gHgs2e2J5azvGFatb/infra-bayesian-physicalism-a-formal-theory-of-naturalized) is a core construction of that layer, with a role independent of outer alignment. [Physicalist Superimitation](https://www.alignmentforum.org/posts/ZwshvqiqCvXPsZEct/the-learning-theoretic-agenda-status-2023) (PSI; formerly [PreDCA](https://www.alignmentforum.org/w/predca); later also Computational Superimitation) is a hypothesized protocol *on top of* that stack: identify the user as an agent in the physicalist ontology and *superimitate* their values (learn them and pursue them substantially better). The 2022 PreDCA writeup centered a “precursor” pointer; later PSI formulations do not treat precursor as central.

**Who carries it:** Vanessa Kosoy (+ Appel; logical-induction neighborhood via Garrabrant)

**What they aim to do.** Create a general mathematical theory of intelligent agents, and—as one hypothesized application, not the agenda’s main motivation—a protocol that reliably learns and acts on the user’s values (Physicalist Superimitation).

**The hard question.** Can a learning-theoretic theory of intelligent agents be built tightly enough to license alignment claims under stated assumptions, including misspecification, inner daemons, and recursive self-improvement? For Physicalist Superimitation: can agent detection and user identification pick out the intended user (including under simulation hypotheses), and does superimitation of inferred values stay well-defined when the world-model ontology is wrong?

**What they produce.** The [learning-theoretic agenda](https://www.alignmentforum.org/posts/5bd75cc58225bf0670375575/the-learning-theoretic-ai-alignment-research-agenda), the [Infra-Bayesianism sequence](https://www.lesswrong.com/w/infra-bayesianism), [infra-Bayesian physicalism](https://www.lesswrong.com/posts/gHgs2e2J5azvGFatb/infra-bayesian-physicalism-a-formal-theory-of-naturalized), and the [Physicalist Superimitation](https://www.alignmentforum.org/posts/ZwshvqiqCvXPsZEct/the-learning-theoretic-agenda-status-2023) protocol (formerly [PreDCA](https://www.alignmentforum.org/w/predca)).

**Key terms.** Key terms include the [learning-theoretic agenda](https://www.alignmentforum.org/posts/5bd75cc58225bf0670375575/the-learning-theoretic-ai-alignment-research-agenda), [infra-Bayesianism](https://www.lesswrong.com/w/infra-bayesianism), [infra-Bayesian physicalism](https://www.lesswrong.com/posts/gHgs2e2J5azvGFatb/infra-bayesian-physicalism-a-formal-theory-of-naturalized) / Formal Computational Realism, the bridge transform, regret bounds, nonrealizability, daemons, and [Physicalist Superimitation](https://www.alignmentforum.org/posts/ZwshvqiqCvXPsZEct/the-learning-theoretic-agenda-status-2023) / [PreDCA](https://www.alignmentforum.org/w/predca) / Computational Superimitation.

**Related field cruxes.** [Embedded Agency](/cards/bridge/mb1-boundary-estimator-soundness/); [Value Learning](/cards/bridge/mb2-bundle-identifiability/); [Value Referent](/cards/bridge/mb3-bearer-import/); [Tiling](/cards/bridge/mb5-successor-ontology-shift/); [Inner Alignment](/cards/bridge/mb7-hidden-capability-and-access/); [Grounding Drift](/cards/bridge/mb9-grounding-certificate/)

**What they contribute.** Model-class misspecification and grain-of-truth analysis; regret-bounded agents; inner daemons; [infra-Bayesian physicalism](https://www.lesswrong.com/posts/gHgs2e2J5azvGFatb/infra-bayesian-physicalism-a-formal-theory-of-naturalized) and the bridge transform as a physicalist layer; [Physicalist Superimitation](https://www.alignmentforum.org/posts/ZwshvqiqCvXPsZEct/the-learning-theoretic-agenda-status-2023) as a sibling outer-alignment protocol (superimitation after agent detection and user identification), reached through a different formal path than [CIRL](/cards/subsumption-cirl/)-style pointing.

**How this project treats it.** This project maps LTA’s problems onto [Embedded Agency](/cards/mb1-boundary-estimator-soundness/), [Value Learning](/cards/mb2-bundle-identifiability/), [Value Referent](/cards/mb3-bearer-import/), [Tiling](/cards/mb5-successor-ontology-shift/), [Inner Alignment](/cards/mb7-hidden-capability-and-access/), and [Grounding Drift](/cards/mb9-grounding-certificate/), with [Acausal Coordination](/cards/mb7d-acausal-coordination/) as a logical-induction neighborhood cousin—it does not treat LTA as a replacement ontology. On the outer endpoint, PSI is a peer proposal for learning and acting on the user’s values. This project *names separately* three checks it still wants: whether inferred values remain [usable directions of control after transformation](/cards/value-bundle-transport/) (not only preserved labels), whether they keep applying to the [right persons or processes](/cards/bearer-persistence/), and whether a [correction process](/cards/correction-channel-integrity/) stays open. Kosoy’s protocol is meant to address usable control (superimitation of inferred user values). Whether those three remain separately checkable after PSI, or whether the protocol already discharges them, is an open disagreement—not a claim that PSI is missing those pieces in her terms.

## Specify / construct (peer outer target)

Not a ConstitutionalRule instance. PSI is a peer outer-target: identify the user and superimitate inferred values under infra-Bayesian physicalism. The bridge transform is an IBP construction (physicalism / cartesian privilege), not the outer-alignment mechanism. PreDCA’s “precursor” pointer is the earlier formulation. This project tags PSI on MB2/MB3, not as a specify-schema filling. Listed so the table does not hide a major outer-alignment construction bet.

## Links

- [LTA (2018 overview)](https://www.alignmentforum.org/posts/5bd75cc58225bf0670375575/the-learning-theoretic-ai-alignment-research-agenda)
- [LTA status (2023)](https://www.alignmentforum.org/posts/ZwshvqiqCvXPsZEct/the-learning-theoretic-agenda-status-2023)
- [Infra-Bayesianism (LessWrong)](https://www.lesswrong.com/w/infra-bayesianism)
- [Infra-Bayesian physicalism](https://www.lesswrong.com/posts/gHgs2e2J5azvGFatb/infra-bayesian-physicalism-a-formal-theory-of-naturalized)
- [PreDCA (Alignment Forum tag)](https://www.alignmentforum.org/w/predca)
- [Vanessa Kosoy](https://www.alignmentforum.org/users/vanessa-kosoy)

See the [coverage matrix](/field/coverage/#coverage-matrix) for evidence tagged to this agenda, and the [glossary](/glossary/) for shared terms.