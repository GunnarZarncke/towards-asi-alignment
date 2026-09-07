---
title: "Alignment Attractor Season"
type: funding
status: framework
summary: "A node-length season that treats the Node's AIs as principals, pays humans to test whether a hold still lands, and uses a model to draft the ledger so assessment can keep Node tempo. Stipends follow artifacts, not attendance. The season fails if policy is green and decisions do not change."
fundingState: open
doneState: not_started
costUsd: 40000
costUsdMax: 80000
durationMonths: 3
fte: 1
fteMax: 3
dependsOn:
  - funding/tsa-writing
bookChapters: ["ch26", "ch29", "ch30", "ch36", "ch37", "ch38"]
roles:
  - Season lead / ledger
  - Session facilitators
  - Paid participants (stipend)
  - Holdout coder (one cycle)
related:
  - attractor-control
  - correction-channel-integrity
  - funding/alignment-attractor-hub
external:
  - label: "Alignment Attractor (book)"
    url: "https://towards-alignment.com/cards/chapters/ch37/"
---

## Problem

A collaboration hub can look like an alignment attractor (seminars, tools, even a local GPU) while remaining a false attractor: reputation and attendance reinforce, correction does not. Node AIs already act on a daily cycle. Independent assessment that runs at multi-week-visit tempo cannot tell whether a human hold still lands.

Most hub grants buy capacity over a year. Node projects do not last that long. The missing object is a **season**: AIs as named principals, humans paid to test the loop, a model drafting the ledger so an outside auditor can keep Node tempo.

This is not the shared observability platform and not the 18-month Alignment Attractor hub. It is a time-boxed practice that can fail in public.

## Approach

Run an 8–16 week season at a node (Berlin preferred). One lead freezes a failure-mode schema and a recording contract before the first session.

**Hub AIs are always principals** (scribe, pairing, calendar bot). A session of only human talk does not count. **Local compute is optional**; if taken, the box is a principal too. Jobs, keys, images, and “I ran it on my laptop” are events. Vouchers clear only when identity, action, and channel fields are present. A kill or revoke is scored as named gate, uptake, and bypass residual.

**Humans are paid to test the loop**, not to transcribe. Only a human hold answers whether the human stayed in the loop. A model row that says governance is fine is not that evidence.

**The model drafts every ledger row** the same day as the session (Node tempo). One paid holdout cycle is slower on purpose (auditor tempo). Claims use only `full` rows. Outputs are open.

The money is mostly **stipends for holds and challenges, compute vouchers, and bounties**, not a standing org and not a coding team.

## Milestones

### Minimum (~$40,000 / ~8–12 weeks)

- Frozen schema + stipend rules + telemetry contract published in week 0
- Dense event series (weekly or twice-weekly working sessions)
- Public null ledger after each session
- One sealed audit day on hub tools (or on the box if compute is taken)
- Season score on the five decision-change / evidence / governance / outsider-correction / challengeable-claims rows; reuse pack (template, traces, refuses)

### Ideal (~$80,000 / ~12–16 weeks)

Also includes:

- Local compute on-contract (vouchers; one image or tool-prompt upgrade with an unlisted invariant frozen in week 0)
- Two or three sealed audit days; two open challenge nights (paid bypass attempts)
- One external row coded on the same schema (another group or node), plus holdout
- One-pager an outside governor or underwriter could use: what the season could and could not attest

## If it works

The season succeeds if a paid human hold **changes a real decision** on an AI principal (key, job, calendar, spend), or if the group paid people and still published that the human was not in the loop. It fails if attendance, green policy, “we have compute,” or a model-only ledger is treated as the attractor.

Not a site card yet. Full protocol, budget, fail rules, and Foresight mapping: [`alignment-attractor-season-full.md`](alignment-attractor-season-full.md).
