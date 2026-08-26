---
title: "Who do you tell when an AI safety guard fails?"
type: "news"
status: "established"
summary: "A policy commentary argues that jailbreak reporting is broken: many labs offer no route, existing programs bind researchers with broad NDAs, and vendors self-grade findings with opaque rubrics. The authors propose cybersecurity-style coordinated disclosure—public rubrics, year-round programs, cross-vendor sharing, and eventually an independent clearinghouse."
decision: "When evaluating a model's safety claims, ask whether an independent researcher can report a bypass, whether the report reaches someone with authority to fix it, and whether severity grading is transparent—not only whether pre-deployment testing occurred."
releasedAt: "2026-08-03T00:00:00.000Z"
bookChapters:
  - "ch27"
  - "ch33"
  - "ch38"
  - "ch39"
  - "appC"
external:
  - label: "AI Jailbreak Disclosure Is Broken. Here’s How to Fix It"
    url: "https://ai-frontiers.org/articles/ai-jailbreak-disclosure-is-broken-heres-how-to-fix-it"
  - label: "CASP — How Boko Haram Uses Frontier AI"
    url: "https://casp.ac/reports/ai-enabled-terrorism"
  - label: "Zvi — AI #177 Part 1 (Boko Haram section)"
    url: "https://thezvi.substack.com/p/ai-177-part-1-tip-of-the-iceberg"
  - label: "Anthropic — Fable 5 / Mythos 5 access suspension"
    url: "https://www.anthropic.com/news/fable-mythos-access"
  - label: "Zvi — American Government Takes Down Claude Fable"
    url: "https://thezvi.substack.com/p/american-government-takes-down-claude"
  - label: "Zvi — The Once And Future Fable #3: Fix This Code"
    url: "https://thezvi.substack.com/p/the-once-and-future-fable-3-fix-this"
---

Researchers who find ways to bypass frontier-model safeguards often have no safe channel to report them.

Frontier AI systems are built with safeguards meant to block dangerous requests. Researchers keep finding "jailbreaks" around those safeguards, and the fixes usually exist once a developer knows about them. The problem is reporting: in an August 2026 commentary, Rich Barton-Cooper and Adam Gleave argue that independent researchers often have no safe, reliable way to tell a lab what they found.

Many developers offer no official jailbreak reporting route at all. Where programs exist, they typically require broad nondisclosure agreements that bar researchers from telling governments, other labs, or the public—even after a fix. Labs grade submissions themselves using private rubrics, so the same finding can be treated as critical at one company and minor at another. Probing for harmful outputs may also violate usage policies, with unclear legal protection for good-faith reporters.

The stakes are not hypothetical. A [Cambridge CASP report](https://casp.ac/reports/ai-enabled-terrorism) based on interviews with former Boko Haram members documents the group training commanders on jailbreaking techniques—for weapons troubleshooting, explosive design, and attack planning—with ISIS operatives reportedly teaching bypass methods such as framing harmful requests as movie scripts. [Zvi's summary](https://thezvi.substack.com/p/ai-177-part-1-tip-of-the-iceberg) notes that the factions mix providers to evade guardrails. Separately, an alleged narrow cyber jailbreak contributed to the [US government suspending Claude Fable 5](https://www.anthropic.com/news/fable-mythos-access) worldwide just days after launch; Anthropic says the trigger was a report in which Amazon researchers prompted the model to read a codebase and fix flaws, surfacing vulnerabilities including exploit code. [Zvi's initial writeup](https://thezvi.substack.com/p/american-government-takes-down-claude) and [follow-up on the "fix this code" finding](https://thezvi.substack.com/p/the-once-and-future-fable-3-fix-this) trace the export-control fallout and dispute whether the technique counted as a jailbreak at all. "Universal" jailbreaks—methods that work across many harmful query types—have been found even in the most advanced models.

The proposed fix draws on decades of cybersecurity practice. In the near term, labs should run year-round disclosure programs with appropriately scoped NDAs, publish severity rubrics, and share jailbreak data across vendors. In the medium term, an independent clearinghouse could accept submissions once, grade them against a shared standard, notify all affected parties under a limited embargo, and publish aggregate statistics after fixes ship—similar to how CERT/CC has coordinated software vulnerability disclosure since 1988.

This is an institutional design argument, not proof that disclosure alone makes models safe. A reporting channel only helps if someone with authority can act on what arrives—and if labs cannot quietly downgrade or ignore findings they dislike. [Ch. 27](/cards/chapters/ch27/) asks whether correction channels stay usable under adversarial pressure; a silenced red-teamer is a broken channel. [Ch. 39](/cards/chapters/ch39/) treats passive observation as insufficient: safeguards must be stress-tested, and the test results must reach decision-makers.

[Ch. 38](/cards/chapters/ch38/) and [Appendix C](/cards/chapters/appC/) frame the deeper question: what artifact turns a vulnerability report into a timely fix or deployment hold? A thumbs-down button, an unmonitored email address, or an NDA-bound bounty that grades its own submissions does not meet that bar. The missing evidence is whether labs will adopt shared, transparent disclosure when liability fears and reputational incentives push the other way.

**Read more in:** [Ch. 27, *Correction Channels under Adversarial Pressure*](/cards/chapter/ch27/); [Ch. 33, *Certification Without Construction*](/cards/chapter/ch33/); [Ch. 38, *Conductive Artifacts and Pivotal Processes*](/cards/chapter/ch38/); [Ch. 39, *Passive Observation Is Not Enough*](/cards/chapter/ch39/); and [Appendix C, *Human Institutions as Alignment Translation Guide*](/cards/appendix/appc/).
