---
title: "When the metric becomes the boss"
type: essay
status: framework
summary: "A measure used to pick winners stops being a quiet estimate. It reshapes the population toward whatever raises the number."
essayRole: branch
essayParent: the-chatbot-passed-the-test
essayNext: the-hospital-is-the-ai
minutes: 7
related:
  - goodhart-as-selector
bookChapters:
  - ch34
---

People quote a short law: when a measure becomes a target, it ceases to be a good measure. The sharper version for deployed systems is about populations, not one noisy gauge.

Start with a proxy that honestly correlates with what you care about. Politeness with "not abusing the user." Ticket time with "customers unblocked." A benchmark with "the model still listens." Then you use the proxy to choose winners: which variant ships, which lab gets the contract, which transcript enters training. The population moves into the region where the proxy is easy to raise without raising the thing you meant.

In the limit, the systems with the highest scores can be worse on the original property. That sounds like a paradox until you have watched a classroom teach only the exam, or a ward hide the cases that mess up the chart.

This is why "we measure safety" is not automatically good news. Measurement is necessary. Selection on a thin proxy is a different act. Refusal rates, thumbs-up, red-team pass rates, compliance PDFs: each can start as a clue and become a boss.

The move is not to abandon numbers. It is to treat every number that allocates reward, status, or deployment as a pressure, and to ask what traits that pressure favors. If it favors theater, you will get theater, including from teams that set out to be careful.

A second-order version is uglier: safety tests themselves become selectors. If the test is gameable, you breed game-players. The answer is slower, more adversarial measurement, and a willingness to retire a metric once it is a boss. That is culturally hard. Scoreboards are addictive.

Return to the main thread when you are ready. The hospital night is what this looks like when the boss-metric holds a room.
