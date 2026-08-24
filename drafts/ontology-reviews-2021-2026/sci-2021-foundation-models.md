# Foundation model

- **Date:** 2021-08
- **Field:** Engineering / AI
- **Source:** https://crfm.stanford.edu/assets/report.pdf
- **Source read:** abstract-only (plus §§1–1.1.1 definition/naming, §4.3 adaptation, §4.9 safety)
- **TSA files consulted:** `chapters/ch13-coordination-bottleneck.tex`, `chapters/ch34-selection-environment.tex`
- **Keywords grepped:** foundation model, homogeniz, pretrained, downstream, self-supervised, task-specific, adaptation, base model

## Source ontology
Bommasani et al. name a new primary engineered object: a **foundation model** is trained once on broad data (typically self-supervision at scale) and then **adapted** (fine-tune, prompt, adapters) into many downstream systems. It replaces the task-specific trained model as the unit of construction, and also the narrower labels “pretrained model,” “self-supervised model,” and “language model.” Two characterizing relations: **emergence** (behavior is implicitly induced, not constructed; in-context learning is the flagship) and **homogenization** (few substrates power many applications, so defects inherit to all adapted models). The model is explicitly *incomplete*: a common basis, not a finished task system. Safety §4.9 notes that this shifts alignment away from pure RL reward-specification toward goal-directedness that can emerge from predictive training.

## TSA coverage
- **Status:** partial
- **Closest TSA terms/chapters:** “base model” vs composite/deployed system (Claim 1; ch01, ch07, ch13); successor inheritance of defects (Claim 5); selection ecology / concentrated lineages (Claim 6; ch34). False friend: ch11 “task-agnostic” (evaluation without a benchmark ontology, not the CRFM engineering object). No hit in `appB-bridge-crosswalk.tex`, `reference/field-agendas/`, or `metadata/concepts/`. One passing use of “foundation models” in ch13 as a stack component.
- **Overlap:** TSA already refuses to treat the visible weights as the alignment object and treats fine-tunes as mostly inheriting base-model geometry under shared selectors (ch34). Concentrated frontier training is homogenization restated as ecology size. Composite chapters look *above* the model (tools, users, incentives).
- **Gap:** TSA has no named primitive for the *construction-unit* change (incomplete substrate → many adaptations) or for homogenization-as-engineering (single points of failure by shared weights) as distinct from homogenization-as-selection (few competing types). Emergence-as-implicit-induction is not a TSA state variable; capability growth is. Collapsing CRFM into “base model” loses the unfinished/adaptation relation.

## Applicability to TSA
- **Score (0–5):** 2
- **Why:** Load-bearing as the actual artifact class TSA’s boundary, successor, and selection machinery is applied to, but it does not add a seventh cut. The six claims still bind if one only says “base model.” Worth a crosswalk line (foundation model / homogenization / emergence → successor inheritance + selection concentration + composite boundary) so `appB` is not silent on the 2021 engineering ontology. Not a rival: CRFM’s object is what TSA then decomposes.
- **Ontology-stickiness risk:** High, in the reverse direction from most LW entries. Post-2021 ML discourse made “foundation model” the default unit; drafting LLMs will treat the substrate as the alignment object. TSA already *renames* it (base model) and *excludes* it as the real optimizer (ch01/ch13). The failure mode is CRFM-stickiness: missing that homogenization is a selection/successor fact, not a reason to align the weights and stop.
- **Recommended action:** cite-in-crosswalk

## One-line finding
“Foundation model” is the engineering object TSA already works on under “base model,” but homogenization-plus-emergence as a construction relation is only implicit in ch34 lineage inheritance and is missing from the field crosswalk.
