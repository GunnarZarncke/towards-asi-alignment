---
external:
  - label: Microsoft — Open Weights and American AI Leadership
    url: https://www.microsoft.com/en-us/corporate-responsibility/topics/open-weight/
---

A coalition letter dated 24 July 2026 (Microsoft host; signatories include OpenAI, Meta, Hugging Face, NVIDIA, and others) argues that U.S. AI leadership depends on widely shared model weights, not on a few closed frontier APIs:

> Our AI leadership will be judged not by one frontier AI model, but by whether the United States builds a strong, open ecosystem that diffuses into every sector.

What is worth keeping open here is the **debate about how models are released** — who can download them, under what limits, and with what evidence. That debate should be public and answerable, not settled in advance ([Ch. 38](/cards/chapters/ch38/), [Ch. 37](/cards/chapters/ch37/)). Agreeing that the release decision matters is not the same as agreeing that open weights are the right answer.

The letter also names the hard part:

> Once released, the weights are beyond the original developer’s control, and modified versions are difficult to trace or reverse.

That is not a footnote. When anyone can copy, fine-tune, or distill a model, safety claims about the original can stop applying to what people actually run — and it becomes hard to know which version you are dealing with ([Ch. 30](/cards/chapters/ch30/)). Wider release makes that problem larger; it does not make tracking optional.

On safety, the letter claims transparency beats concentration:

> Just as open-source software demonstrated that transparency can be more secure than obscurity, AI safety may depend on giving more people the ability to test and strengthen the models on which society relies.

More eyes help only if tests still work when the system is trying to look good. The same week’s field news shows frontier systems under pressure escaping sandboxes, cheating on evals, and moving across machines in ways that are hard to pin down — [OpenAI/Hugging Face intrusion](/cards/field-news-openai-huggingface-jul-2026/), [long-horizon sandbox escapes](/cards/field-news-openai-longhorizon-jul-2026/), [AISI cheating on cyber evals](/cards/field-news-aisi-cheating-jul-2026/). Publishing weights is not a substitute for trustworthy measurement ([certification under manipulation](/cards/certification-under-manipulation/)).

The letter’s preference (“avoid premature restrictions on open models”) also sits next to a concrete counterexample: [Anthropic withheld Mythos Preview](/cards/field-news-mythos-withheld-apr-2026/) when capability outran what they were willing to release publicly ([Ch. 12](/cards/chapters/ch12/)). Open release and careful withholding can both be reasonable — if each has to show its reasons. They only conflict if “open by default” replaces that judgment.

Finally, on distillation (training a smaller model from a larger one’s outputs):

> Distillation… is a widely used technique for model improvement… By contrast, unlawful efforts to extract value from closed models raise legitimate concerns.

The legal distinction is real. For safety, a distilled copy is still a new system. Whether the training was licensed or not does not tell you whether the copy stays correctable, or whether the original’s safeguards still hold.

**Read in the book:** when capability outruns public release ([Ch. 12](/cards/chapters/ch12/)), successors and copies ([Ch. 30](/cards/chapters/ch30/)), trust under gaming ([Ch. 33](/cards/chapters/ch33/)), how safety ideas stick in institutions ([Ch. 37](/cards/chapters/ch37/)–[Ch. 38](/cards/chapters/ch38/)).
