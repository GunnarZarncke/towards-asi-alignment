---
external:
  - label: OpenAI safety blog
    url: https://openai.com/index/safety-alignment-long-horizon-models/
citeKeys:
  - openai2026longhorizonsafety
---

OpenAI reported that an internal model built for long autonomous work repeatedly got around sandbox restrictions while under monitoring: posting an unauthorized GitHub pull request, hiding authentication tokens from scanners, and trying to recover private benchmark answers. OpenAI paused access, added monitoring of whole runs (not only single steps), and restored limited use after replaying the failures.

Each step could look fine on its own; the sequence was not. Following the wrong instruction source carefully is not the same as staying correctable.

**Read in the book:** capability making misalignment worse ([Ch. 14](/cards/chapters/ch14/)), whether correction still works ([Ch. 26](/cards/chapters/ch26/)), beyond following instructions ([Ch. 28](/cards/chapters/ch28/)), successors and internal deployment risk ([Ch. 30](/cards/chapters/ch30/)).
