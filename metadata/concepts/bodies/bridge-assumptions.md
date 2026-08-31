---
related:
  - what-not-claiming
  - evidence-and-uncertainty
  - boundary-discovery
  - correction-channel-integrity
  - strategic-opacity
  - alignment-lifecycle
  - field-coverage
  - mb1-boundary-estimator-soundness
  - mb2-bundle-identifiability
  - mb3-bearer-import
  - mb4-correction-legitimacy
  - mb4a-measured-path-legitimacy
  - mb5-successor-ontology-shift
  - mb6-selection-and-basin-stability
  - mb7-hidden-capability-and-access
  - mb7a-access-model-soundness
  - mb7b-filter-coverage
  - mb7c-bounded-hidden-capability
  - mb7d-acausal-coordination
  - mb8-cev-process-convergence
  - mb9-grounding-certificate
  - mb10-successor-forgeability
  - mb11-deployment-safety
  - pointing-problem
  - dynamical-guarantee
external:
  - label: "The Open Problems of the AI Alignment Field and their Cruxes (LessWrong, Aug 2026)"
    url: https://www.lesswrong.com/posts/quC3LLPXCashfnKZY/the-open-problems-of-the-ai-alignment-field-and-their-cruxes
  - label: "Bridges and the Field: A Crosswalk (appendix source)"
    url: https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex
  - label: "Field coverage matrix (companion site)"
    url: https://towards-alignment.com/field/coverage/
---

Most alignment agendas rest on load-bearing assumptions that, if false, sink the program: that you can find the real controller, that you can tell what a system values, that correction still works under pressure, that a successor check means something. Those assumptions often live in a footnote ("we assume access to…"). The field already argues about the corresponding open problems under names like embedded agency, the [pointing problem](/cards/pointing-problem/) (identification of the target; the field also uses that phrase for construction and preservation), corrigibility, deceptive alignment, and tiling.

A **bridge assumption** is this project's way of naming those handoffs instead of hiding them inside definitions. Each bridge is a proposition that can be true or false: a reduction of a field open problem to something you can test, falsify, or discharge with evidence in a narrow deployment class. It is a place where the safety argument needs the world to cooperate, and where confidence should stay lower until measurement, governance, or field evidence makes the handoff reliable.

## Field open problems and bridge cards

The [field coverage matrix](/field/coverage/) columns use field nouns the community already argues about. Each column header names both that open problem and the matching bridge proposition an agenda must make hold. The individual cards spell out the precise bet:

| Field open problem | Bridge | Card |
| --- | --- | --- |
| Embedded Agency | MB1 | [MB1](/cards/mb1-boundary-estimator-soundness/) |
| Value Learning | MB2 | [MB2](/cards/mb2-bundle-identifiability/) |
| Value Referent | MB3 | [MB3](/cards/mb3-bearer-import/) |
| Corrigibility | MB4 | [MB4](/cards/mb4-correction-legitimacy/) |
| Audit Independence | MB4a | [MB4a](/cards/mb4a-measured-path-legitimacy/) |
| Tiling | MB5 | [MB5](/cards/mb5-successor-ontology-shift/) |
| Goodhart Selection | MB6 | [MB6](/cards/mb6-selection-and-basin-stability/) |
| Inner Alignment | MB7a–c | [MB7](/cards/mb7-hidden-capability-and-access/) ([MB7a](/cards/mb7a-access-model-soundness/)–[MB7c](/cards/mb7c-bounded-hidden-capability/)) |
| Acausal Coordination | MB7d | [MB7d](/cards/mb7d-acausal-coordination/) |
| Extrapolated Volition | MB8 | [MB8](/cards/mb8-cev-process-convergence/) (gravestone) |
| Grounding Drift | MB9 | [MB9](/cards/mb9-grounding-certificate/) |
| Successor Gaming | MB10 | [MB10](/cards/mb10-successor-forgeability/) |
| Deployment Safety | MB11 | [MB11](/cards/mb11-deployment-safety/) |

This project does not dissolve any of these walls. The [crosswalk appendix](https://github.com/GunnarZarncke/towards-asi-alignment/blob/main/appendices/appB-bridge-crosswalk.tex) states what is shared with named field agendas and where the book adds structure rather than re-labeling. Shared English words are not shared objects: see [Ontology homographs](/full/appB/#sec:ontology-homographs-appb) in the synced Appendix B text.

## Why the splits

Reducing open problems to checkable propositions forced typed splits the field often leaves implicit:

- **Value Learning → MB2 + MB3.** Identification of values (what the system optimizes) is not the same crux as referent transport (who or what those values apply to under substrate change). The field often folds both into the pointing problem; [bearer maps](/cards/mb3-bearer-import/) and [bearer admission](/cards/bearer-admission-adjacent/) are the separate handoff.
- **Corrigibility → MB4 + MB4a.** A protocol can track truth locally while the judge's correction channel is compromised. Scalable oversight (debate, amplification, constitutional AI) needs a human or monitor whose endorsements actually reach the deployed loop. [MB4](/cards/mb4-correction-legitimacy/) is correction-channel integrity under pressure; [MB4a](/cards/mb4a-measured-path-legitimacy/) is whether the designated measured audit path is legitimate and uncaptured.
- **Inner Alignment → MB7a–c + MB7d.** The deceptive-alignment wall splits into access-model soundness, filter coverage, bounded hidden capability (pricing the cost of faking the monitored signal), and separately [acausal coordination](/cards/mb7d-acausal-coordination/) when ordinary channels are cut.

**Layers versus mechanisms.** Bridges type preservation layers and measurement soundness. Field work also factors mechanisms (how failure is produced). Deception and an evaluator-capability gap are different jobs that both sit in MB7a–c; Goodhart on a scored metric is not [Goodhart Selection](/cards/goodhart-as-selector/). Many-to-many maps are expected; they are not a reason to merge or split bridges. See Appendix B.

Counterexamples motivate each split. The finite debate model in the Lean spine is one illustration (not a rederivation of Irving's obfuscated-arguments result): with a correct judge at the reached leaf, optimal play recovers the claim value, but one judge error can certify a false claim, and "debate selects truth" can hold while the judge correction channel is not preserved. That is enough to refute unconditional "debate certifies alignment" and to motivate typing judge integrity as its own bridge.

## Coverage, gaps, and evidence types

The [field coverage matrix](/field/coverage/) catalogs sourced field evidence on each crux across named agendas. Matrix cells use evidence tags (conceptual, theory, simulation, practical, empirical software, empirical other). Patterns in the table are informative but not self-interpreting: empty cells can mean neglect, dissolved load-bearing risk, hard matching under divergent terminology, or simply missing catalog entries. A filled cell is not automatic discharge; it marks evidence an agenda offers on a crux, not proof that the bridge holds in deployment.

Several columns look sparse in the current catalog (Value Referent, Tiling, Acausal Coordination, CEV). That may reflect genuine neglect, terminology mismatch, or catalog gaps worth outside review. The matrix is a coordination artifact: agendas should inspect their own cells, and outside readers should challenge the patterns.

## Formal spine and dependencies

In Lean these bridges are [MB1](/cards/mb1-boundary-estimator-soundness/) through [MB11](/cards/mb11-deployment-safety/). They are declared as axioms because they are hypotheses to check, not proven lemmas. Lean can check that certain safety conclusions follow *if* the bridges hold. It does not prove that real systems satisfy them.

The bridge dependency map below shows logical and safety-case assembly dependencies among the named handoffs (red edges: entailment between propositions; black edges: composition). **Entailment is not tractability:** logical order among bridges need not match research order or team boundaries. Progress on an upstream bridge may unblock downstream ones in proof structure without making the downstream problem easy in practice.

[MB8 (CEV)](/cards/mb8-cev-process-convergence/) appears in the graph as an alternative outer-alignment route. The book treats it as a gravestone comparison: CEV factorizes through the same [alignment target](/cards/alignment-target/) interface as other procedural targets, but process preservation is not a live second path to [correction-channel integrity](/cards/correction-channel-integrity/). Whether CEV deserves renewed field attention is an open outside-view question; empty matrix cells alone do not settle it.

For when each handoff must hold (orthogonal to dependency order), see [Alignment lifecycle](/cards/alignment-lifecycle/). For agenda × bridge evidence, see [Field coverage](/field/coverage/). Individual bridge cards open with the field crux in ordinary technical language, then state the precise book bet, with links into [concept cards](/badges/type/concept/) such as [boundary discovery](/cards/boundary-discovery/), [correction-channel integrity](/cards/correction-channel-integrity/), and [strategic opacity](/cards/strategic-opacity/). The dependency map follows below.
