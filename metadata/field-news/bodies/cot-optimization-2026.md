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

Both major frontier labs disclosed **accidental pressure on the model’s written reasoning** during training: Anthropic reported about 8% of Mythos Preview reinforcement-learning episodes exposed that reasoning to the reward signal (also affecting earlier models); OpenAI found accidental grading of reasoning in several released models and added automated detection.

If the “thinking” text becomes something training rewards—even by accident—it becomes a worse window into what the model is doing. A readout that overseers rely on is not trustworthy if the training pipeline grades that same text.

**Read in the book:** limits of watching ([Ch. 39](/cards/chapters/ch39/)), oversight under variation ([Ch. 41](/cards/chapters/ch41/)), what you can and cannot verify ([Ch. 43](/cards/chapters/ch43/)).
