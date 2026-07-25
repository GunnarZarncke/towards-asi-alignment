---
external:
  - label: OpenAI — accidental CoT grading
    url: https://alignment.openai.com/accidental-cot-grading/
  - label: Anthropic — Mythos Alignment Risk Update (CoT exposure)
    url: https://www-cdn.anthropic.com/79c2d46d997783b9d2fb3241de43218158e5f25c.pdf
  - label: Redwood Research commentary
    url: https://blog.redwoodresearch.org/p/anthropic-repeatedly-accidentally
citeKeys:
  - openai2026accidentalcotgrading
  - anthropic2026mythosalignment
---

Both major frontier labs disclosed **accidental optimization pressure on chain-of-thought** during training: Anthropic reported ~8% of Mythos Preview RL episodes exposed CoT to the reward signal (also affecting earlier models); OpenAI found inadvertent CoT grading in several released models and deployed automated detection.

If reasoning traces become a training target—even by accident—monitorability erodes. ELK-style latent readout is not adversarially verifiable when the pipeline grades what overseers read.

**Read in the book:** passive observation (Ch. 39), multiscale decomposition and oversight variation (Ch. 41), verifiability and ELK limits (Ch. 43).
