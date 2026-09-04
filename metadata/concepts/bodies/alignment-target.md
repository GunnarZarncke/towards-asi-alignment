---
leanNodes:
  - nodeId: AlignmentTarget
    kind: definition
    summary: Minimal alignment target — correction-channel and bundle-structure slots.
    module: AlignmentProofSpine/AlignmentConstruction.lean
  - nodeId: ConstitutionalRule
    kind: definition
    summary: Specify-side schema — constituency, extrapolation, aggregation, plus field-family flags.
    module: AlignmentProofSpine/AlignmentConstruction.lean
  - nodeId: constitutionalTarget
    kind: definition
    summary: Maps a ConstitutionalRule to an AlignmentTarget.
    module: AlignmentProofSpine/AlignmentConstruction.lean
  - nodeId: SpecWellFormedness
    kind: definition
    summary: Uninterpreted well-formedness placeholder — never axiomatized in this development.
    module: AlignmentProofSpine/AlignmentConstruction.lean
  - nodeId: SpecifyCrux
    kind: definition
    summary: TargetSpecifiable alias — open specify-phase crux including object-sort compatibility; explicit hypothesis only.
    module: AlignmentProofSpine/AlignmentConstruction.lean
  - nodeId: TargetSort
    kind: definition
    summary: Object sort of the alignment target (scalar, incomplete preorder, bundle geometry, constitution, open-world spec). Not an MB.
    module: AlignmentProofSpine/AlignmentConstruction.lean
related:
  - target-realization
  - pointing-problem
  - specify-cev
  - specify-constitutional-ai
  - specify-gsai
  - specify-institutional
  - alignment-lifecycle
  - field-coverage
  - mb8-cev-process-convergence
external:
  - label: Field coverage matrix
    url: /field/coverage/
---

Before asking whether a system is aligned, the field must say **what it is aligned to**: human preferences, a written constitution, assistance under uncertainty, an institutional mandate, or another stated target. Labs disagree on the answer; they still share the handoff that the answer must be coherent enough to build toward and check against.

On the [field hub](/field/v2/), outer-alignment research programs are **instances** of that one specify-stage question — each paired with a construction bet — not separate columns in the [coverage matrix](/field/coverage/). Examples include CEV, Constitutional AI, GSAI, and institutional constitutions (listed below).

**Lifecycle role:** specify — first stage on the [alignment lifecycle](/cards/alignment-lifecycle/) axis (see [glossary](/glossary/)). Open spine interface in Lean; not an `MB*` bridge column.

### Formal schema

State a coherent **alignment target** by filling a `ConstitutionalRule` and mapping it to an `AlignmentTarget` via `constitutionalTarget`. Field programs are **instances** of that schema, each paired with a construction bet — not separate bridges:

- [CEV (constitutional residue)](/cards/specify-cev/)
  - [CEV construction (underspecified)](/cards/construct-cev/)
- [Constitutional AI](/cards/specify-constitutional-ai/)
  - [RLAIF / principles-as-feedback](/cards/construct-constitutional-ai/)
- [GSAI / Open Agency spec](/cards/specify-gsai/)
  - [Spec-relative formal builder](/cards/construct-gsai/)
- [Institutional / legal constitution](/cards/specify-institutional/)
  - [Certified vendor / procurement regime](/cards/construct-institutional/)

**Peer outer target** (not a `ConstitutionalRule` instance):

- [PreDCA / Physicalist Superimitation](/cards/field-agendas/kosoy-infra-bayesianism-lta/)
  - [Superimitation / user-identification protocol](/cards/field-agendas/kosoy-infra-bayesianism-lta/) (peer outer target; MB2/MB3)

**Well-formedness is out of scope here.** `SpecWellFormedness` / `SpecifyCrux` type the missing criteria (non-vacuity, aggregation coherence, legitimacy, and object-sort compatibility) as an **uninterpreted placeholder**. Theorems that need it take `hSpec : SpecifyCrux W C S` explicitly; this project does not discharge outer-alignment philosophy. The book's live sort is bundle geometry; scalar total order, incomplete preorder, procedural constitution, and open-world spec are named field objects, not extra bridges.

**Distinct from MB2:** identification asks what values are *in* a deployed system; specify asks whether the *stated* target is coherent enough to parameterize construction and certification.

**Lifecycle placement:** [Alignment lifecycle](/cards/alignment-lifecycle/). **Field evidence:** [/field/coverage/](/field/coverage/).

The specify / construct instance table follows below.
