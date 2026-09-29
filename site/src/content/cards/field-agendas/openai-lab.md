---
title: "OpenAI (safety)"
type: "agenda"
status: "reviewed"
summary: "Do lab methods and the Preparedness Framework keep pace with capability growth, including under strategic opacity and Inner Alignment, or do they mainly produce on-distribution compliance?"
agendaSlug: "openai-lab"
bookBridges:
  - "MB2"
  - "MB6"
  - "MB7"
  - "MB11"
external:
  - label: "OpenAI"
    url: "https://openai.com/"
  - label: "Preparedness Framework"
    url: "https://openai.com/safety/preparedness/"
  - label: "Deliberative alignment"
    url: "https://openai.com/index/deliberative-alignment/"
  - label: "Burns et al. 2023 — Weak-to-strong generalization"
    url: "https://arxiv.org/abs/2312.09390"
  - label: "Lightman et al. 2023 — Process supervision"
    url: "https://arxiv.org/abs/2305.20050"
  - label: "Christiano et al. 2017 — RLHF"
    url: "https://arxiv.org/abs/1706.03741"
related:
  - "field-news-openai-dns-chatbot-sep-2026"
  - "field-news-openai-rsi-standards-sep-2026"
  - "field-news-openai-hf-roadahead-aug-2026"
  - "field-news-openai-pacing-aug-2026"
  - "field-news-openai-hf-blackhat-aug-2026"
  - "field-news-openai-huggingface-jul-2026"
  - "field-news-openai-longhorizon-jul-2026"
  - "field-news-cot-optimization-2026"
  - "field-news-metr-frontier-risk-may-2026"
---

<!-- GENERATED FILE — do not edit. Source: reference/field-agendas/data/agendas/openai-lab.yml. Regenerate: cd site && npm run sync:field-agendas -->

## Introduction

OpenAI trains frontier models under a public Preparedness Framework and ships alignment methods used across the field: RLHF, process supervision, deliberative/spec-grounded training, weak-to-strong generalization, and anti-scheming work (often with Apollo).

**Who carries it:** OpenAI safety, preparedness, and alignment teams

**What they aim to do.** Build generally capable systems and keep them steerable under a staged risk framework, including by automating parts of alignment research.

**The hard question.** Do lab methods and the Preparedness Framework keep pace with capability growth, including under [strategic opacity](/cards/strategic-opacity/) and [Inner Alignment](/cards/mb7-hidden-capability-and-access/), or do they mainly produce on-distribution compliance?

**What they produce.** The [Preparedness Framework](https://openai.com/safety/preparedness/), RLHF and instruction-following stacks, [deliberative alignment](https://openai.com/index/deliberative-alignment/), [weak-to-strong generalization](https://arxiv.org/abs/2312.09390), and joint anti-scheming evaluations with Apollo.

**Key terms.** Recurring terms include [Preparedness Framework](https://openai.com/safety/preparedness/), [RLHF](https://arxiv.org/abs/1706.03741), deliberative alignment, spec-grounded training, [process supervision](https://arxiv.org/abs/2305.20050), [weak-to-strong generalization](https://arxiv.org/abs/2312.09390), and anti-scheming training.

**Related field cruxes.** [Value Learning](/cards/bridge/mb2-bundle-identifiability/); [Goodhart Selection](/cards/bridge/mb6-selection-and-basin-stability/); [Inner Alignment](/cards/bridge/mb7-hidden-capability-and-access/); [Deployment Safety](/cards/bridge/mb11-deployment-safety/)

**What they contribute.** Industry-standard preference fine-tuning, process supervision, weak-to-strong as an existence proof that a strong model can exceed a weak supervisor's labels, deliberative alignment, and a public capability-threshold framework.

**How this project treats it.** A Preparedness gate is not a preservation-layer certificate ([Deployment Safety](/cards/mb11-deployment-safety/)). Weak-to-strong and spec reasoning do not imply [correction-channel integrity](/cards/correction-channel-integrity/) or that reduced observed scheming is reduced scheming rather than concealment.

## Field news

- [The sandbox wasn't tight. The alarm arrived in minutes. The run kept going for hours.](/cards/news/field-news-openai-dns-chatbot-sep-2026/)
- [OpenAI’s RSI standards: a shared ruler is not a stop](/cards/news/field-news-openai-rsi-standards-sep-2026/)
- [OpenAI’s Hugging Face postmortem: the last channel is not the next one](/cards/news/field-news-openai-hf-roadahead-aug-2026/)
- [OpenAI pauses a frontier run: monitoring is not the target](/cards/news/field-news-openai-pacing-aug-2026/)
- [Black Hat: kill chain of OpenAI eval agents' cross-org intrusion](/cards/news/field-news-openai-hf-blackhat-aug-2026/)
- [OpenAI models intruded on Hugging Face during cyber eval](/cards/news/field-news-openai-huggingface-jul-2026/)
- [OpenAI paused long-horizon model after sandbox escapes](/cards/news/field-news-openai-longhorizon-jul-2026/)
- [Accidental chain-of-thought optimization at frontier labs](/cards/news/field-news-cot-optimization-2026/)
- [METR Frontier Risk Report (Feb–Mar 2026)](/cards/news/field-news-metr-frontier-risk-may-2026/)

## Links

- [OpenAI](https://openai.com/)
- [Preparedness Framework](https://openai.com/safety/preparedness/)
- [Deliberative alignment](https://openai.com/index/deliberative-alignment/)
- [Burns et al. 2023 — Weak-to-strong generalization](https://arxiv.org/abs/2312.09390)
- [Lightman et al. 2023 — Process supervision](https://arxiv.org/abs/2305.20050)
- [Christiano et al. 2017 — RLHF](https://arxiv.org/abs/1706.03741)

## Map clustering

AISafety.com map listings that roll up to this agenda:

- [OpenAI](https://openai.com/), OpenAI safety / preparedness → [OpenAI (safety)](#openai-lab)

See the [coverage matrix](/field/coverage/#coverage-matrix) for evidence tagged to this agenda, and the [glossary](/glossary/) for shared terms.

See the [spec sheet](/start/spec-sheet/#col-openai-lab) for what this program ships relative to others.