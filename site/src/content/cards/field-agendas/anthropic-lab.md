---
title: "Anthropic / Goodfire (lab & MI stack)"
type: "agenda"
status: "reviewed"
summary: "Can scaling policies and interpretability keep pace with capability growth, including under strategic opacity and Goodhart Selection pressure?"
agendaSlug: "anthropic-lab"
bookBridges:
  - "MB2"
  - "MB3"
  - "MB6"
  - "MB7"
  - "MB10"
  - "MB11"
external:
  - label: "Anthropic"
    url: "https://www.anthropic.com/"
  - label: "Anthropic Research (index)"
    url: "https://www.anthropic.com/research"
  - label: "Bricken et al. 2023 — Towards Monosemanticity"
    url: "https://transformer-circuits.pub/2023/monosemantic-features"
  - label: "Templeton et al. 2024 — Scaling Monosemanticity (Claude 3 Sonnet)"
    url: "https://transformer-circuits.pub/2024/scaling-monosemanticity/"
  - label: "Goodfire"
    url: "https://www.goodfire.com/"
  - label: "Transluce"
    url: "https://transluce.org/"
  - label: "Neuronpedia"
    url: "https://www.neuronpedia.org/"
  - label: "Frontier Model Forum risk thresholds"
    url: "https://www.frontiermodelforum.org/technical-reports/risk-taxonomy-and-thresholds/"
  - label: "Lange et al. 2023"
    url: "https://arxiv.org/abs/2311.17030"
related:
  - "specify-constitutional-ai"
  - "construct-constitutional-ai"
  - "alignment-target"
  - "target-realization"
---

<!-- GENERATED FILE — do not edit. Source: reference/field-agendas/data/agendas/anthropic-lab.yml. Regenerate: cd site && npm run sync:field-agendas -->

## Introduction

Anthropic builds frontier models under staged safety commitments ([RSP](https://www.anthropic.com/news/anthropics-responsible-scaling-policy)), while adjacent teams and investments pursue the **MI stack**—[mechanistic interpretability](https://www.anthropic.com/research) research, editable internal representations, and cross-lab tooling infrastructure (Goodfire, Transluce, Neuronpedia).

**Who carries it:** Anthropic PBC; Goodfire; Transluce; Neuronpedia (infra); Georg Lange (causal-faithfulness seam)

**What they aim to do.** Build capable systems with staged safety commitments, interpretability, and editable internal representations that can be audited and adjusted.

**The hard question.** Can scaling policies and interpretability keep pace with capability growth, including under [strategic opacity](/cards/strategic-opacity/) and [Goodhart Selection](/cards/mb6-selection-and-basin-stability/) pressure?

**What they produce.** The [Responsible Scaling Policy](https://www.anthropic.com/news/anthropics-responsible-scaling-policy) ([RSP](https://www.anthropic.com/news/anthropics-responsible-scaling-policy)), [Constitutional AI](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback), interpretability research, Ember and editable representations, and FMF capability thresholds.

**Key terms.** Recurring terms include [RSP](https://www.anthropic.com/news/anthropics-responsible-scaling-policy), [constitutional AI](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback), [mechanistic interpretability](https://www.anthropic.com/research), [circuits](https://transformer-circuits.pub/2023/monosemantic-features), [features](https://transformer-circuits.pub/2023/monosemantic-features), [steering](https://www.goodfire.com/), [capability thresholds](https://www.frontiermodelforum.org/technical-reports/risk-taxonomy-and-thresholds/), and [causal faithfulness](https://arxiv.org/abs/2311.17030).

**Related field cruxes.** [Value Learning](/cards/bridge/mb2-bundle-identifiability/); [Value Referent](/cards/bridge/mb3-bearer-import/); [Goodhart Selection](/cards/bridge/mb6-selection-and-basin-stability/); [Inner Alignment](/cards/bridge/mb7-hidden-capability-and-access/); [Successor Gaming](/cards/bridge/mb10-successor-forgeability/); [Deployment Safety](/cards/bridge/mb11-deployment-safety/)

**What they contribute.** Industry [RSP](https://www.anthropic.com/news/anthropics-responsible-scaling-policy) template, conditioning-predictor failure modes, Goodfire mechanistic-interpretability tooling (Anthropic investment; Apollo and DeepMind [mechanistic interpretability](https://www.anthropic.com/research) lineage on team), and cross-lab Neuronpedia infrastructure.

**How this project treats it.** This project requires [correction-channel integrity](/cards/correction-channel-integrity/) and [adversarial verifiability](/cards/certification-under-manipulation/); a lab [RSP](https://www.anthropic.com/news/anthropics-responsible-scaling-policy) is not the same as a preservation-layer certificate ([Deployment Safety](/cards/mb11-deployment-safety/)), and interpretability progress does not by itself resolve [Successor Gaming](/cards/mb10-successor-forgeability/) or full [Inner Alignment](/cards/mb7-hidden-capability-and-access/) risk.

## Specify / construct (field v2)

This agenda maps to a **ConstitutionalRule** specify instance paired with a construction bet: [Constitutional AI](/cards/concept/specify-constitutional-ai/) · [RLAIF / principles-as-feedback](/cards/concept/construct-constitutional-ai/). See the [alignment target](/cards/concept/alignment-target/#specify-construct-instances) instance table.

## Links

- [Anthropic](https://www.anthropic.com/)
- [Anthropic Research (index)](https://www.anthropic.com/research)
- [Bricken et al. 2023 — Towards Monosemanticity](https://transformer-circuits.pub/2023/monosemantic-features)
- [Templeton et al. 2024 — Scaling Monosemanticity (Claude 3 Sonnet)](https://transformer-circuits.pub/2024/scaling-monosemanticity/)
- [Goodfire](https://www.goodfire.com/)
- [Transluce](https://transluce.org/)
- [Neuronpedia](https://www.neuronpedia.org/)
- [Frontier Model Forum risk thresholds](https://www.frontiermodelforum.org/technical-reports/risk-taxonomy-and-thresholds/)
- [Lange et al. 2023](https://arxiv.org/abs/2311.17030)

## Map clustering

AISafety.com map listings that roll up to this agenda:

- [Anthropic](https://www.anthropic.com/), Import AI (newsletter — Jack Clark) → [Anthropic / Goodfire](#anthropic-lab) — newsletter not agenda
- [Goodfire](https://www.goodfire.com/), [Transluce](https://transluce.org/), [Neuronpedia](https://www.neuronpedia.org/) → [Anthropic / Goodfire](#anthropic-lab) cluster

See the [coverage matrix](/field/coverage/#coverage-matrix) for evidence tagged to this agenda, and the [glossary](/glossary/) for shared terms.