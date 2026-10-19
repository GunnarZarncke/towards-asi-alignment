---
title: "Outer Alignment"
type: "glossary"
status: "framework"
summary: "Field name (Hubinger) for whether the training pointer or stated objective is the intended target. Splits into specify, identification (MB2/MB3), realization, and preservation-if-optimized."
bookChapters:
  - "ch04"
  - "ch10"
  - "ch44"
bookLabels:
  - "sec:outer-alignment"
external:
  - label: "Risks from Learned Optimization (Hubinger et al.)"
    url: "https://arxiv.org/abs/1906.01820"
  - label: "Bridges and the Field (Appendix B)"
    url: "/cards/appendix/appb/"
  - label: "Field coverage matrix"
    url: "/field/coverage/"
related:
  - "alignment-target"
  - "pointing-problem"
  - "target-realization"
  - "mb2-bundle-identifiability"
  - "mb3-bearer-import"
  - "mb7-hidden-capability-and-access"
  - "specify-cev"
  - "specify-constitutional-ai"
  - "specify-gsai"
  - "specify-institutional"
  - "alignment-lifecycle"
  - "field-coverage"
  - "bridge-assumptions"
---

**Outer alignment** is a field name, not a native object of this project. Hubinger et al. use it for whether the *training pointer* — reward, constitution, CEV/CBV endpoint, conditioned predictive goal — is the intended target, as opposed to [inner alignment](/cards/mb7-hidden-capability-and-access/) (whether the trained system actually pursues that pointer).

The same English question mixes four jobs that fail independently. Treat the Hubinger split as a map, not a column.

| Field use of “outer alignment” | What this project asks instead | Home |
|---|---|---|
| Is the stated target coherent enough to build toward? | Specify: fill a `ConstitutionalRule` / [alignment target](/cards/alignment-target/). Well-formedness (`SpecifyCrux`) stays an uninterpreted placeholder. | Specify stage; not an `MB*` column |
| Does evidence identify the intended values and bearers? | [Bundle identifiability](/cards/mb2-bundle-identifiability/) (MB2) and [bearer maps](/cards/mb3-bearer-import/) (MB3). Wentworth’s pointers problem is the identification-heavy slice. | Identify |
| Can we build a system that tracks that target? | [Target realization](/cards/target-realization/) (`ConstructionCrux`). Open interface; not a bridge assumption. | Construct |
| Would optimizing the base objective preserve what we care about? | Bundle and bearer transport, [correction-channel integrity](/cards/correction-channel-integrity/), successor stability — the Ch. 44 translation of “$R_0$ is the right objective.” | Preserve / certify layers |

**Not inner alignment.** Inner alignment here is MB7 (access, filter coverage, cost of faking), not “the mesa-objective equals $R_0$.” A perfect outer pointer still leaves hidden control, successor gaming, and selection open.

**Not one pointing-problem sense.** The field [pointing problem](/cards/pointing-problem/) is already an umbrella (identification, realization, preservation). Outer alignment is the Hubinger-training-pointer cut of that family, plus specification programs that never talk about a training loss.

**Program instances** (specify + a construction bet, not extra matrix columns): [CEV](/cards/specify-cev/), [Constitutional AI](/cards/specify-constitutional-ai/), [GSAI / Open Agency](/cards/specify-gsai/), [institutional constitutions](/cards/specify-institutional/), and peer outer targets such as PreDCA / Physicalist Superimitation and QACI. See the [alignment target](/cards/alignment-target/) card for the instance table.

**Where to read it in the book:** Ch. 10 (Hubinger complementary question); Ch. 4 (CEV/CBV as live outer-alignment approaches); Ch. 44 (base objective vs intended structure); Appendix B (crosswalk: not one MB); Appendix E (pointing-problem split).
