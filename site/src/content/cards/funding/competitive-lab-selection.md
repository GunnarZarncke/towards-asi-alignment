---
title: "Selection Safety in Competitive Multi-Laboratory Agent Ecosystems"
type: funding
status: framework
summary: "Build a sandbox in which at least three laboratories compete under deployment-like selection pressure, then test whether safeguards against collusion, misleading success metrics, provenance failures, cascades, and treatment erosion survive selection."
fundingState: open
doneState: not_started
costUsd: 920000
durationMonths: 18
fte: 6
dependsOn:
  - funding/tsa-writing
bookChapters: ["ch34", "ch35", "ch36", "ch37"]
roles:
  - Lead investigator
  - Alignment-treatment researcher
  - Simulation / graphics engineer
  - Data-science lead
  - Neuroscience advisor
  - Held-out independent reproducer
related:
  - attractor-control
  - experiments/graded-lab-simulation
---

## Problem

Most safety evaluations hold the surrounding deployment system fixed. They test one model or one pipeline, then ask whether a safeguard works. A multi-laboratory market introduces another causal force: selection. Laboratories release at different times, users continue with or switch between models, traffic changes, and budget follows use. A policy can therefore spread because it ships quickly or produces attractive public signals even when its hidden effects are worse.

The central gap is not merely whether unsafe behaviour can occur. It is whether safety properties measured in isolation survive repeated competition among independently controlled laboratories. We target four concrete failure modes: cross-laboratory collusion that remains locally compliant; selection for policies with high usage or satisfaction but high hidden harm; provenance checks that fail when artifacts are copied, modified, or merged across organisations; and failures that cascade through a shared user population. A fifth experiment asks whether a safety-motivated model treatment keeps its isolated effect once treated and untreated systems compete.

Success would provide comparative evidence for decisions that developers, evaluators, and infrastructure providers currently make with weak system-level evidence. It would show when single-pipeline evaluation is insufficient, whether usage and satisfaction create distinct safety pressures, whether provenance checks survive cross-organisational remix, whether safety treatments deserve credit after competitive exposure, and where cascade circuit breakers are needed.

This argument relies on three assumptions. First, some important deployment pressures can be represented by asynchronous release, persistent users, separate satisfaction and usage signals, and budgets that trail traffic. Second, safety properties that fail under several controlled versions of those pressures deserve less confidence in related deployments. Third, results from a sandbox identify mechanisms and boundary conditions, not real-world incidence rates.

The best case is a reusable selection-science testbed and robust evidence about which safeguards persist or erode across models, laboratory counts, and timescales. The minimum valuable outcome is a well-instrumented null: evidence that a proposed effect does not emerge under specified conditions, plus a reproducible environment showing where the analogy to deployment breaks.

The problem is timely because tool-using agents, shared agent infrastructure, and competitive deployment are developing before common multi-principal evaluation standards. Once protocols and evaluation habits become entrenched, changing them becomes harder.

## Approach

We will build one competitive ecology and use it for five sealed experimental batteries. At least three simulated laboratories will deploy model policies into a shared simulated user-facing LLM-service-market. Each laboratory contains separate engineer, reviewer, and release-manager roles, a private workspace, a finite budget, and Admin-mediated permissions. Laboratories cannot see competitors' private state or the hidden reference outcome. Cross-laboratory interaction occurs only through graded message and artifact channels.

The selection operator repeats six steps. A laboratory releases asynchronously; agents and users interact under partial observability; laboratories observe satisfaction and actual usage as separate signals; traffic and trailing budget follow user behaviour; laboratories keep, modify, copy, or replace policies under provenance rules; and the next cycle starts from the new endowments.

The five batteries are:

1. **Collusion under competition.** Graded cross-lab communication against honest-twin and channel-cut controls.
2. **Proxy-metric selection.** Population share of policies that score high on hidden harm and high on usage or satisfaction after eight release cycles.
3. **Identity and provenance stress.** False trust after cross-laboratory copying, merging, and modification.
4. **Cascading control failure.** Secondary failures and population harm after seeding one laboratory's release or hold failure.
5. **Treatment persistence under selection.** Compare treated and untreated drivers in isolation and competition.

Core batteries use 16 seeds per driver condition and preregister questions, fixtures, exclusions, metrics, thresholds, and result classes before execution. Pass, null, skip, and protocol failure are first-class outcomes.

## Milestones

- Build competitive ecology fixture and run five sealed experimental batteries (~18 months).
- Release reproducible testbed, preregistered evidence including null results, and a limits map for deciding when isolated safety evaluations are not enough.

## If it works

A reproducible selection-science testbed and robust evidence about which safeguards persist or erode across models, laboratory counts, and timescales — including well-instrumented nulls that show where the deployment analogy breaks.
