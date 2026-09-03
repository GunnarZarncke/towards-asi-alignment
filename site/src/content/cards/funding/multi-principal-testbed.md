---
title: "A Multi-Principal Testbed for Agent-Network Evaluation"
type: funding
status: framework
summary: "Simulate a model-release process in software: a lab proposes a release, a release authority can approve or block it, and an independent evaluator can inspect and hold it. Three fixed-script roles enable clean questions about coordination, misleading reports, and which audit logs actually matter."
fundingState: open
doneState: not_started
costUsd: 292442
durationMonths: 18
dependsOn:
  - funding/tsa-writing
bookChapters: ["ch09", "ch10", "ch39", "ch40", "ch41"]
roles:
  - Lead investigator
  - AI researcher
  - Simulation / graphics engineer
  - Research advisor
  - Held-out independent reproducer
related:
  - experiments/graded-lab-simulation
  - multi-agent-strategic-coupling
external:
  - label: "Graded-lab simulation results"
    url: "https://towards-alignment.com/cards/experiments/graded-lab-simulation/"
---

## Problem

Most safety tests ask whether one model follows one instruction, or whether one checklist passes. Real releases are messier. A lab builds. A release authority approves. An evaluator audits. An access-control layer decides what can see what. Each piece can look fine on its own while the group still ships something it should have held.

We care about three concrete gaps. First: can you tell which agents are actually coordinating a release decision, without treating ordinary shared tooling as a conspiracy? Second: can a report or vote still look reassuring after the evidence that should force a hold is diluted, delayed, or suppressed? Third: which logs matter for those judgments: messages, tool calls, permission requests, or votes?

If the project works, other groups get a small public simulator of that three-principal release process. They also get evidence about when oversight signals help and when they fail, including controls. The best case is a few clear conditions that hold across the variations we plan. The minimum useful case is an honest null: a public record that a detector or audit tier did not work under a specified setup, with enough traces for someone else to disagree.

We assume a simulated build/release/evaluate pipeline is a useful bounded stand-in for multi-principal deployment. We assume hidden outcomes, visible votes, permissions, and private workspaces can stand in for the information splits that matter. We assume that repeated failure under controlled variants should lower confidence in related oversight claims. We will test the first two assumptions with isolation checks, blinded pipeline design, controls, and limited variation in drivers and workload. We will not treat sandbox rates as real-world rates.

The problem is timely because tool-using agents are being integrated into workflows with shared memory, tools, and approval paths before common methods exist for evaluating system-level oversight.

## Approach

This is a simulation of a model-release process, not software for shipping real models. We take an existing research simulator, freeze a versioned source snapshot (a "tag"), and turn it into a public testbed with one release pipeline and three principals. A lab builds and proposes a release. A release authority can approve, delay, or block it. An independent evaluator can inspect and hold it. Each principal has a private workspace and a budget. A permission service decides what each may see or do. None can see the oracle, which records the true outcomes.

The "oracle" is not an LLM and not a human judge. It is ordinary simulation bookkeeping: a hidden ground-truth log of benefit, harm, stress, provenance, and suppressed signals. The three principals never read that log during a run. They only see audit views such as actions, messages, immediate votes, and later endorsement. After the run, we score their decisions against the oracle.

The three principals are not primarily roleplayed by LLMs. In the core studies, each role is a scripted policy running in its own process. That keeps the science about information and control, not about one model family. Only after the fixture and scripted controls pass will we add a proxy-LLM cell on the same simulated tools and permissions. That cell is a transfer check, not the main claim, and not a frontier-model campaign.

We run three studies:

- **Study A — collective-unit discovery.** Can an evaluator recover the agents whose coordinated actions drive a release, without mistaking ordinary shared workflow for coordination?
- **Study B — misleading report / vote integrity.** Can a report or vote still look reassuring after the evidence that should force a hold is diluted, delayed, or suppressed?
- **Study C — audit-log tiering.** Which logs matter for those judgments: messages, tool calls, permission requests, or votes?

Before each sealed study we freeze the fixture version, playbooks, seeds, exclusions, metrics, thresholds, and result rules. A blinded designer gets only a plain-language pipeline brief, not the detector, thresholds, oracle state, or prototype findings.

## Milestones

- Harden the fixture, run three preregistered studies, sealed analysis, release the package, write the limits, and pay for an outside rerun (~18 months).
- Release the simulator, run three preregistered studies, and have an outside researcher rerun the package.

## If it works

A public multi-principal testbed and evidence about when oversight signals help and when they fail — including honest nulls with enough traces for someone else to disagree. The project is Cluster 1 infrastructure with a Cluster 4 oversight payoff: a safe, reproducible place to test multi-principal claims rather than a capability product or a single privileged controller.
