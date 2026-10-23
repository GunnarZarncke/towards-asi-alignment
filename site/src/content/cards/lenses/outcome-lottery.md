---
title: "Outcome lottery"
type: "lens"
status: "framework"
summary: "A distribution over outcomes; expectation is one functional among many."
related:
  - "lenses/state-utility"
  - "evidence-and-uncertainty"
  - "lenses/lenses-and-frameworks"
  - "field-agendas/chai-russell"
external:
  - label: "LessWrong tag: Risk"
    url: "https://www.lesswrong.com/w/risks-from-ai"
---

**Role.** Target. Graph node `dist`.

> Expected value, CVaR, stochastic dominance, entropic risk, chance constraints, minimax, and regret can rank the same lotteries differently.
>
> — Frames draft §4.2 (Bäuerle and Jaśkiewicz 2024)

Distributional RL learns a random return and still leaves open which functional governs action. Projecting to a mean state score has no section: the tails and model ambiguity are gone.
