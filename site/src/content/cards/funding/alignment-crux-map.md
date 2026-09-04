---
title: "Alignment Crux Map"
type: funding
status: framework
summary: "A public, object-level map of AI-safety work so funders, researchers, and people entering the field can see which real problems are actually being worked on, and which only share a name."
fundingState: open
doneState: not_started
costUsd: 16000
costUsdMax: 50000
durationMonths: 9
fte: 1
dependsOn:
  - funding/tsa-writing
bookChapters: ["ch05", "appB"]
roles:
  - Lead investigator
related:
  - bridge-assumptions
  - evidence-and-uncertainty
external:
  - label: "Field hub"
    url: "https://towards-alignment.com/field/"
---

## Problem

Org lists tell you who exists. This project tells you *which problem a dollar or a year of work is actually buying*.

Funders use it to check a proposal against the problem they thought they were funding. Researchers use it to see which gap their method addresses. People entering the field use it so they do not spend a year on a crowded label (another "corrigibility" paper) and miss an empty job.

Powerful AI can fail in ways that do not show up as a bad eval score. Humans can no longer correct the system. A replacement system can drop the rules. The environment can reward systems that look aligned on the checked channel and defect elsewhere.

Those are specific jobs. Someone has to work on them. If the field funds "corrigibility" and that word means three different jobs, a portfolio can look full and still have an empty job.

1. Money and newcomers follow cluster names (evals, interpretability, control, corrigibility, governance).
2. The same name can mean different jobs. "Corrigibility" can mean "there is an off switch," "it does what the rater asked," or "humans can still correct it when it has reason to look cooperative." Only the last of those still matters when the system can resist correction.
3. Directories list organizations. Surveys list methods. Neither answers: which job is this dollar buying, and is that job already staffed?

That does not solve alignment. It reduces the chance that the field reaches very powerful AI with a coverage story and a missing piece whose failure means humans can no longer correct the system.

The map does not move money by itself. If after publication no funder, researcher, or training program has used a named cell or the demo in a documented choice, the grant failed even if the tables are correct.

## Approach

A **decision aid**, not another landscape essay and not a proof that alignment works.

Where it is up to: A public draft map already exists: major programs, a table of programs against eleven load-bearing problems, and a catalog of sourced evidence. A simulated lab already exists (holds, ratings, capture, lineage, field monitor, population selection, hidden hazard). What does *not* exist: tables a funder can use without the book; a note on what this map misses about *their* agenda; frozen lab configs scored as different jobs under crowded words; paid outsiders running their own setup against those lab configs. This grant buys that last stretch. It does not buy a new book or a new lab.

Most of it is the lead's time, LLM assistants used to draft under human review, and short outside contracts ($1,000 each: table checks and researchers running their own setup). The lab runs on a laptop. Work is remote. No travel, no GPU cluster, no model training.

## Milestones

- **Month 1.** Draft tables that split overloaded words into jobs. Start notes of *what this map misses* about eight well-known groups. Freeze the shared lab workplace.
- **Month 2.** Publish the brief and tables on the field site. Freeze the tiling lab. Ship hold example as a built-in ruleset: shutdown green, corrigibility red. Invite paid outsiders to run *their* setup on the matching lab config.
- **Month 3 (ideal ask).** Freeze the inner-alignment lab. Pay outsiders for a report. Fold comments in.
- **Months 4–9 (ideal ask).** Finish folding in returned contracts; keep the map from going stale; record whether anyone used a named cell or the demo.

| | Minimum | Ideal |
|---|---------|-------|
| **What you get** | Correctable-AI lab + Redwood run | MATS + BlueDot use, CHAI or Christiano, tiling, inner alignment, missed-lines, Wentworth/Garrabrant/Kosoy, upkeep |
| **Total** | **$16,000** | **$50,000** |

## If it works

A funder can ask "which job is this proposal?" A researcher can see that their method does not transfer. A newcomer can pick an empty job instead of a seventh paper under a name that already has many projects. Example: a hold-always ruleset greens shutdown and leaves corrigibility red.
