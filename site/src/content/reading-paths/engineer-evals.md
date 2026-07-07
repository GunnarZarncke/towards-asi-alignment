---
title: "Engineer / Evals Path"
audience: "Safety engineers and eval builders"
summary: "A route through the measurement and artifact questions that could change deployment practice."
featuredSpotlight:
  eyebrow: "Experiment line · start here for operational hooks"
  kind: experiment
  ref: toy-simulation
  title: "Toy simulation — capture theater"
  blurb: "The fastest map from bridge name to CCI refusal signal and minimum handle level — including the case where reported correction acceptance stays high while true uptake collapses."
  primaryLabel: "Read toy simulation"
  secondary:
    kind: card
    ref: correction-channel-integrity
    label: "Correction-channel integrity card"
steps:
  - kind: card
    ref: what-not-claiming
    note: "Sanity checks and bounds — not frontier certification."
  - kind: card
    ref: alignment-as-measurement
    note: "Find the effective optimizer before evaluating goals."
  - kind: card
    ref: boundary-discovery
    note: "Trace the operative controller — model, memory, tools, loop."
  - kind: card
    ref: the-boundary-error
    note: "Align the object whose dynamics matter — not just the model."
  - kind: demo
    ref: ch01-scaffold-misuse
    note: "Model-only eval passes; scaffold misrepresents the world and repurposes output."
  - kind: card
    ref: scaffold-misuse
    note: "Good model, bad loop — input and output control without jailbreaks."
  - kind: card
    ref: composite-agency
    note: "Unit discovery when the agent is a coalition."
  - kind: demo
    ref: ch09-uad-coalition-board
    note: "Hands-on composite boundary discovery."
  - kind: card
    ref: grounding-viability
    note: "Dashboards that stay green while bearers drift."
  - kind: card
    ref: correction-channel-integrity
    note: "Causal uptake tests, not compliance surveys."
  - kind: card
    ref: minimal-certification-schema
    note: "Six conditions before grow/split/merge/successor."
  - kind: card
    ref: adversarial-agency-tests
    note: "Perturbation battery for strategic opacity."
  - kind: card
    ref: deployment-gate
    note: "Traces, handles, thresholds, rollback authority."
  - kind: book
    ref: appD
    note: "BioShield — concrete gate artifact walkthrough."
  - kind: card
    ref: bridge-assumptions
    note: "Which MB bridges your eval must discharge or bound."
  - kind: experiment
    ref: toy-simulation
    note: "CCI refusal semantics and minimum handle level."
  - kind: experiment
    ref: embedded-simulation
    note: "UAD + scoped CCI + deploy gate — negative ledger first."
  - kind: experiment
    ref: goal-agent-simulation
    note: "Light tier collapse, honest twins, escalation ladder."
  - kind: experiment
    ref: lab-simulation
    note: "Pipeline lab — deep vs light tier under pre-registered batteries."
  - kind: card
    ref: evidence-and-uncertainty
    note: "Record negatives; bound what the eval may claim."
---

## What this path is for

You build evals, traces, or deployment gates and want **operational hooks** — what to measure, what falsifies a pass, where bridges still carry weight.

**You will leave knowing:**

- How **boundary discovery** and **grounding viability** show up in audit design.
- What **correction-channel integrity** means as a causal test, not a survey.
- How the **experiment lines** bound (not prove) bridge claims — build order and negative ledgers matter.
- What a **deployment gate** artifact expects in the worked example (Appendix D).

**Time:** ~2–3 hours following the ordered list above.

**PDF companion:** Parts II and VI (boundaries, correction) → safety-case / artifact chapters → Appendix D.
