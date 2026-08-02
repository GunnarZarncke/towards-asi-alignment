---
title: The AI safety and alignment field
description: Public orientation to AI safety research, major overviews, and how this site's field map relates to them.
---

The **AI safety and alignment** field asks how to build advanced artificial intelligence that remains beneficial as capabilities grow: keeping humans able to correct mistakes and reducing catastrophic or existential risk from misaligned optimization.

From the lead of [Wikipedia's article on AI alignment](https://en.wikipedia.org/wiki/AI_alignment):

> In the field of artificial intelligence (AI), alignment aims to steer AI systems toward a person's or group's intended goals, preferences, or ethical principles. An AI system is considered aligned if it advances the intended objectives. A misaligned AI system pursues unintended objectives.

Alignment is a subfield of **AI safety**, alongside robustness, monitoring, and capability control.

Norbert Wiener stated the classical version of the problem in 1960:

> If we use, to achieve our purposes, a mechanical agency with whose operation we cannot interfere effectively [...] we had better be quite sure that the purpose put into the machine is the purpose which we really desire.

Eliezer Yudkowsky's formulation on **complexity of value** captures why simple goal statements fail:

> Any simple goal you try to describe that is All We Need To Program Into AIs is almost certainly wrong.

In practice the field is not one research program but a **constellation of agendas**: labs, nonprofits, academic groups, governance institutes, and researcher lineages that share vocabulary (corrigibility, scalable oversight, interpretability, compute governance) while disagreeing on ontology, near-term priorities, and what would count as success.

## How researchers map the field

No single index is complete. Useful starting points include:

- **[AISafety.com map](https://www.aisafety.com/map)** — ecosystem map of organizations, programs, and resources (the clustering on this site rolls up map listings into coherent **agenda** rows).
- **[AI Safety Interventions](https://www.lesswrong.com/posts/6Sf9KMMDMFSauDe85/ai-safety-interventions)** (Zarncke, 2025) — index of roughly ninety named interventions across foundational theory, oversight, control, interpretability, governance, and underexplored routes; [extended PDF](https://github.com/GunnarZarncke/ai-safety-interventions/blob/master/ai_safety_interventions.pdf).
- **[AI Alignment: A Comprehensive Survey](https://alignmentsurvey.com/)** (Ji et al., 2023) — academic survey of alignment problems and methods.
- **[Foundational challenges in assuring alignment and safety of LLMs](https://arxiv.org/abs/2404.09932)** (Ganguli et al., 2024) — Anthropic's framing of eighteen foundational challenges.
- **[Open Problems in Technical AI Governance](https://arxiv.org/abs/2407.14981)** (Reuel et al., 2024) — policy and institutions adjacent to technical work.
- **[Center for AI Safety](https://www.safe.ai/)** — field-building, statements, and course material.
- **[AI Alignment Forum](https://www.alignmentforum.org/)** / [LessWrong](https://www.lesswrong.com/) — long-form research discourse and tag-based archives.
- **[Human Compatible](https://humancompatible.ai/)** (Russell, 2019) — assistance-games framing of beneficial AI under preference uncertainty.
- **[International AI Safety Report](https://internationalaisafetyreport.org/)** — periodic synthesis for policymakers (complementary to researcher-native maps).

This companion site adds a **crosswalk layer** for readers of [*Towards Superintelligence Alignment*](https://towards-alignment.com/): who the major agendas are, what evidence each has published on named **bridge** problems (MB1–MB11), and how that evidence relates to the book's measurement spine. That crosswalk is orientation for comparison, not a verdict on which agenda is correct.

In this book, **bridges** are named conditional handoffs the safety argument needs but does not prove. For example, [MB1](/cards/mb1-boundary-estimator-soundness/) asks whether a measured agent–environment boundary is sound enough to trust—the embedded-agency worry that there may be no clean cut between "the model" and "the optimizer actually in charge." The matrix below records which agendas have published evidence relevant to each bridge, not whether any bridge is discharged.

## What you will find here

1. **Agenda cards** — one page per coherent research or advocacy program (introduction, official links, and AISafety.com map clustering). Browse all via the [Field agenda badge](/badges/type/agenda/).
2. **Coverage matrix** — agenda × bridge grid with typed, sourced evidence tags. Column headers link to [bridge cards](/badges/type/bridge/); row headers link to agenda cards. Cell tags link to the evidence catalog on this page.
3. **Evidence catalog** — primary-source citations backing matrix cells.

Training programs (BlueDot, MATS, Apart, Kairos), funding pools, and pure directories appear as reference agendas, not as full matrix rows, when they do not carry bridge-specific technical artifacts.

For term disambiguation across agendas, see the [inter-agenda glossary](/glossary/) (manuscript App E is synced separately). For how this book maps bridges to field cruxes, see [Appendix B](/cards/chapters/appB/).
