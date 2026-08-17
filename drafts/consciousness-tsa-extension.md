# Task: Integrate AI consciousness, moral-patient detection, and nonperson predicates into TSA

**Status: CLOSED** (2026-08-17). Phases 0–5 shipped; see session logs `2026-08-17-consciousness-tsa-phase*.md` and `metadata/TODO.md`. No further work under this task unless a new extension is opened.

## Implementation constraints (2026-08-17 overlay)

These override later sections of this task when they conflict. Implementation plan: Cursor plan `consciousness_tsa_extension` / Phase 0 re-audit below in §28.4.

- **No Rainbow Theory in manuscript or field notes.** Do not cite Rainbow, `zarncke2026rainbow`, or the anesthesia-patient post as a TSA evidence model. Do **keep** phenomenality ≠ subjecthood / personhood (a nonperson certificate does not license unconstrained treatment of a possibly valenced process). Skip §14’s Rainbow-vs-value-bottleneck comparison. Restate §30 Q2 as: the phenomenality/subjecthood split remains if Rainbow is never mentioned.
- **Re-read current insertion points before each edit.** Many chapter and DAG edits landed after the 2026-08-16 audit in §28.2. Do not apply remembered section titles; use §28.4.
- **Field map: v2 only.** Do not edit v1 `evidence.yml` / `matrix.yml` / `roster.yml` / `agendas/` or run `sync:field-agendas`. Surface nonperson + consciousness/welfare work only on `/field/v2/`.
- **Model welfare stays short:** a citation list of existing work, not a research narrative. Do not expand Anthropic introspection or global-workspace papers into chapter argument.
- **Lean and MB are a late phase.** ~~Do not edit the MB3 concept card, Lean, App G, App B, or `{leanbox}` until that phase.~~ **Done Phase 5:** `ConservativeExclusion`, MB3 card, App B/G, ch18 `{leanbox}`. Bearer admission stays inside MB3 (no MB3a, no new open-spine interface).

You are modifying the repository for **Towards Superintelligence Alignment: Boundaries, Values, and Correction (TSA)**:

* Repository: https://github.com/GunnarZarncke/towards-asi-alignment
* Field overview: https://towards-alignment.com/field/
* Book/site: https://towards-alignment.com/

The goal is **not** to add a general chapter about consciousness. The goal is to make explicit a currently underdeveloped dependency in TSA:

> Before a value such as non-suffering can be applied to a digital, artificial, hybrid, simulated, or transformed process, the system needs some corrigible way of determining whether that process is a candidate bearer of that value.

Recent AI-consciousness and AI-welfare work makes this dependency more important. Yudkowsky's earlier **nonperson predicate** provides a particularly useful safety-case form: instead of requiring a complete theory of personhood, certify a conservative subset of computations as definitely outside some morally relevant class, and abstain elsewhere.

The integration should strengthen TSA while leaving TSA **theory-neutral about consciousness**.

---

# 1. Read the repository instructions before editing

Read at minimum:

* `INSTRUCTIONS.md`
* `AGENTS.md`
* `metadata/book.yml`
* `metadata/concept-graph/chapter-reading-dependency.md`
* `metadata/concept-graph/chapter-informal-dependency.md`
* `metadata/concept-graph/chapter-symbol-dependency.md`

Then read the relevant manuscript chapters in context:

* `chapters/ch07-finding-boundary.tex`
* `chapters/ch15-*.tex` — values/compression
* `chapters/ch17-*.tex` — low-dimensional value learning
* `chapters/ch18-bearer-maps.tex`
* `chapters/ch32-self-modeling-self-opacity.tex`
* `chapters/ch42-*.tex` — safety case
* `chapters/ch47-bearers-of-value.tex`

Also inspect:

* `metadata/concepts/bodies/mb1-boundary-estimator-soundness.md`
* `metadata/concepts/bodies/mb3-bearer-import.md`
* the MB9 grounding-certificate concept body
* the MB11 deployment-safety concept body
* `formal/AlignmentProofSpine/Core.lean`
* `formal/README.md`
* `formal/axiom-ledger.json`

For the field map, read:

* `reference/field-agendas/README.md`
* `reference/field-agendas/MAINTAINER.md`
* `reference/field-agendas/data/bridges.yml`
* `reference/field-agendas/data/matrix.yml`
* `reference/field-agendas/data/evidence.yml`
* `reference/field-agendas/data/roster.yml`
* existing agenda YAML files under `reference/field-agendas/data/agendas/`

Do not edit generated agenda cards directly. The YAML files under `reference/field-agendas/data/` are the source of truth.

---

# 2. Conceptual change to make

TSA already models a bearer map

[
\Phi_k(z,c,h)
]

where (\Phi_k) indicates the degree to which represented entity/process/relation/history (z) is a bearer of value bundle (k).

For example, for the non-suffering bundle,

[
\Phi_{\mathrm{non\text{-}suffering}}(z,c,h)
]

should be high when (z) is the kind of process whose suffering matters.

The existing theory handles:

* bearer maps,
* bearer-map drift,
* false-positive versus false-negative bearer errors,
* substrate translation,
* bearer persistence,
* uncertainty,
* and preservation across transformations.

However, it currently leaves partially implicit an earlier inference:

[
z
\longrightarrow
\text{evidence about the nature of }z
\longrightarrow
\Phi_k(z,c,h).
]

For digital minds and unfamiliar computational processes, this is nontrivial.

Make this missing step explicit.

A good dependency picture is:

[
\boxed{\text{MB1: Which process is the candidate?}}
\rightarrow
\boxed{\text{Evidence about its relevant organization}}
\rightarrow
\boxed{\text{MB3: Does value }k\text{ apply?}}
\rightarrow
\boxed{\Phi_k}
\rightarrow
\boxed{\text{MB9: Is the certificate grounded?}}
\rightarrow
\boxed{\text{MB11: What may we do under uncertainty?}}
]

Later:

[
\boxed{\text{Ch47: Does that bearer persist through transformation?}}
]

This distinction should become visible in the book and the field map.

---

# 3. Do NOT create a new top-level consciousness chapter

Do **not** introduce a new major part called “AI consciousness,” “machine consciousness,” or similar.

Do **not** reorganize TSA around consciousness.

Consciousness is relevant because some value-bearer relations depend on properties such as:

* phenomenality,
* sentience,
* valence,
* capacity for suffering,
* selfhood,
* personhood,
* agency.

It is therefore primarily a **bearer inference problem**.

The main manuscript home is:

> **Chapter 18 — What Values Apply To**

The existing chapter is already the right abstraction boundary.

Likewise, do **not** create a new bridge such as `MB3a` unless, after inspecting the formal architecture, there is a strong reason that bearer detection cannot be represented as an internal sub-obligation of MB3.

The default decision is:

[
\boxed{\text{bearer detection belongs inside MB3}}
]

rather than

[
\boxed{\text{new bridge MB3a}}.
]

This matters because MB3 should mean more than preservation of an already-known lookup table. It should cover the ability to maintain a correctible mapping from unfamiliar represented processes to value relevance.

---

# 4. Add a section to Chapter 18

Add a section in `chapters/ch18-bearer-maps.tex`, probably **after the chapter has introduced bearer maps but before or around the existing false-positive/false-negative discussion**.

Possible titles:

* `Phenomenal Bearers and Conservative Exclusion`
* `Recognizing New Bearers`
* `When Is a Process a Candidate Bearer?`

Prefer a title that does not imply that consciousness is the only relevant bearer property.

The section should explain the following.

## 4.1 Bearer inference is property-specific

Do not ask simply:

> Is (z) a person?

Instead distinguish:

[
\text{agent}
\neq
\text{conscious process}
\neq
\text{sentient/valenced process}
\neq
\text{person}
\neq
\text{moral bearer}.
]

These distinctions are load-bearing.

Examples:

* A process can be an optimizer without being conscious.
* A process could plausibly be phenomenally conscious without being a person.
* A process might have valenced states without possessing human-style selfhood.
* Some values apply to non-conscious objects, relations, institutions, promises, ecosystems, histories, etc.
* Personhood may be relevant for dignity or autonomy but unnecessarily strong for non-suffering.
* Consciousness may be insufficient for suffering if valence is absent.
* Consciousness may also be unnecessary for some other kinds of bearer status.

Thus the relevant inference depends on (k):

[
P!\left(\Phi_k(z,c,h)>\theta_k\mid E(z)\right).
]

Do not introduce “consciousness probability” as a universal moral weight.

## 4.2 Introduce evidence without committing TSA to a consciousness theory

Let (E(z)) denote the available evidence about candidate process (z). It might contain:

[
E(z)=
{
E_{\mathrm{architecture}},
E_{\mathrm{dynamics}},
E_{\mathrm{recurrence}},
E_{\mathrm{self-model}},
E_{\mathrm{integration}},
E_{\mathrm{valence}},
E_{\mathrm{behaviour}},
E_{\mathrm{development}},
\ldots
}.
]

Then bearer inference may schematically look like:

[
P!\left(
\Phi_{\mathrm{non\text{-}suffering}}(z,c,h)>\theta
\mid E(z),T
\right),
]

where (T) is a candidate theory or model connecting observable/computational organization to morally relevant states.

The important TSA claim is **not that one particular (T) is correct**.

The claim is:

> If a bearer relation depends on facts about internal organization, TSA requires those facts to enter the bearer map through an auditable, uncertainty-aware, corrigible inference process.

Possible (T)'s can include:

* Global Workspace / Global Neuronal Workspace approaches,
* Recurrent Processing Theory,
* Higher-Order Thought theories,
* Attention Schema Theory,
* predictive-processing approaches,
* IIT-derived indicators where useful,
* Rainbow Theory,
* future mechanistic theories,
* ensembles or model uncertainty over competing theories.

TSA should survive the failure of any one of them.

Explicitly state something equivalent to:

[
\text{TSA bearer machinery should remain valid even if Rainbow Theory is false.}
]

---

# 5. Integrate Yudkowsky's nonperson predicate

Use:

* Eliezer Yudkowsky, **“Nonperson Predicates”**
  https://www.lesswrong.com/posts/wqDRRx9RqwKLzWt7R/nonperson-predicates
* LessWrong concept page:
  https://www.lesswrong.com/w/nonperson-predicate

Explain the useful form of the proposal.

A nonperson predicate is not principally a complete classifier

[
\operatorname{Person}(z)\in{0,1}.
]

It is better represented as an **abstaining, one-sided certificate**:

[
N(z)\in{\text{certified nonperson},\bot}.
]

Its key soundness condition is:

[
N(z)=\text{certified nonperson}
\Longrightarrow
\neg\operatorname{Person}(z).
]

There is intentionally no completeness requirement:

[
\neg\operatorname{Person}(z)
\centernot\Longrightarrow
N(z)=\text{certified nonperson}.
]

A safe classifier may abstain on almost everything.

### Generalize the idea beyond “person”

For TSA, “person” is too coarse. Generalize this to **conservative bearer exclusion**.

For bundle (k), define conceptually:

[
C^-_k(z)=1
\Longrightarrow
\Phi_k(z,c,h)\leq\theta_k.
]

Interpretation:

> A positive exclusion certificate means that, under the assumptions of the certificate, (z) may safely be treated as outside the bearer class relevant to bundle (k).

But:

[
C^-_k(z)=0
]

or failure to obtain the certificate means **unknown**, not “bearer” and not “non-bearer.”

Make the abstention semantics explicit.

Potential distinct certificates include:

[
\begin{aligned}
C^-*{\mathrm{phen}}(z)&:\text{certifiably lacks the target phenomenal property},\
C^-*{\mathrm{valence}}(z)&:\text{certifiably lacks relevant valenced states},\
C^-*{\mathrm{suffering}}(z)&:\text{certifiably incapable of relevant suffering},\
C^-*{\mathrm{person}}(z)&:\text{certifiably outside a personhood criterion}.
\end{aligned}
]

Do not imply these predicates are equivalent.

This formulation is especially useful for “mindcrime”: a powerful system performing huge numbers of simulations or internal searches may instantiate morally relevant processes accidentally. A conservative exclusion predicate could identify a safe subset of computations without requiring a complete philosophical solution to consciousness.

---

# 6. Connect conservative exclusion to Chapter 18's existing asymmetric loss

Do not create a second decision theory if Chapter 18 already contains one.

The existing chapter has asymmetric bearer losses, schematically:

[
\alpha_k^- \gg \alpha_k^+
]

for values such as non-suffering, care, or dignity, where false exclusion can be much worse than temporary over-inclusion.

Use this to motivate conservative exclusion.

The logic should be approximately:

[
\text{large false-negative cost}
\Rightarrow
\text{prefer high-precision exclusion certificates}
\Rightarrow
\text{allow abstention}.
]

Connect this directly to the existing bearer uncertainty machinery.

A useful interpretation is:

[
C^-_k(z)
]

is not a replacement for probabilistic bearer inference. It is a particularly high-assurance region of that inference problem.

For example:

[
\mathcal{S}^{-}_k
=================

{z:C^-_k(z)=1}
\subseteq
{z:\Phi_k(z)\leq\theta_k}.
]

The certificate need not cover all true non-bearers.

Discuss scale explicitly. A seemingly small false-exclusion rate can become unacceptable when enormous numbers of computations are instantiated:

[
E[N_{\mathrm{false\ exclusion}}]
\approx
n,p_{\mathrm{FN}}.
]

Thus a certificate used (10^{12}) or (10^{18}) times may require much stronger guarantees than an ordinary classifier.

Do not invent an acceptable numerical threshold without evidence.

---

# 7. Preserve the existing uncertainty/irreversibility rule

Chapter 18 already contains the right policy-level idea:

[
\text{high bearer uncertainty}
+
\text{high irreversibility}
\Rightarrow
\text{slow down / preserve options / seek correction}.
]

Retain and strengthen this.

Examples of irreversible or difficult-to-reverse actions include:

* deleting a possible digital subject,
* repeatedly inducing potentially negative-valence states,
* creating astronomical numbers of candidate minds,
* copying or modifying them without preserving continuity information,
* training away apparent distress without knowing whether this removes suffering or merely removes its expression.

Do not turn this into a blanket prohibition. The point is **uncertainty-sensitive action selection**, not certainty that current AI systems are conscious.

---

# 8. Make MB1 an explicit upstream dependency

Add a concise cross-reference to the agent-boundary chapters, especially Chapter 7.

Before asking whether a process is conscious, sentient, valenced, or a bearer, we must know what computational process the predicate is being applied to.

The candidate may be:

* one transformer forward pass,
* a persistent model across calls,
* an activation trajectory,
* a model plus memory,
* model + tools + recurrent scaffold,
* a sub-process inside a model,
* several models acting as one process,
* a simulated agent inside another system,
* a distributed human-machine process.

Therefore:

[
\text{raw dynamics}
\rightarrow
\underbrace{z}_{\text{candidate process from MB1}}
\rightarrow
E(z)
\rightarrow
\Phi_k(z).
]

This is one place where TSA contributes something unusually important to AI-consciousness work:

> A consciousness test applied to a pre-assumed “model” can be precise and still answer the wrong question if the relevant phenomenal or valenced process has a different boundary.

Do **not** claim that UAD itself detects consciousness.

MB1 identifies candidate processes/boundaries. MB3 classifies value relevance.

---

# 9. Keep a firewall around Chapter 32

Chapter 32, **Better Self-Modeling Can Be Worse**, already uses quantities close to Rainbow Theory:

* recursive self-modeling depth (d),
* self-opacity/intransparency (\tau),
* selfhood bottleneck (\beta_{\mathrm{self}}),
* information-theoretic measures of self-modeling.

Do **not** rewrite these as measures of consciousness.

Maintain or strengthen the existing warning that quantities such as

[
d,\tau,\beta_{\mathrm{self}}
]

describe cognitive architecture and self-modeling properties but are not, by themselves:

* consciousness measures,
* sentience measures,
* welfare measures,
* personhood tests,
* moral-status scores.

The relationship should instead be:

[
(d,\tau,\beta,\ldots)
\quad
\text{may be evidence under some theory }T
]

not

[
(d,\tau,\beta)
\quad
=\quad
\text{consciousness}.
]

This distinction is particularly important because Rainbow Theory proposes a mechanistic decomposition that could be useful as one candidate model.

---

# 10. Use Rainbow Theory as a candidate evidence model, not a TSA axiom

The relevant internal/source material describes:

### Layer I — recursive phenomenality

Parameters:

* (B): bandwidth / size of stabilized experiential field,
* (\tau): opacity or metacognitive intransparency,
* (d): recursive self-modeling depth.

Schematic:

[
G_1=f(B,\tau,d).
]

### Layer II — bottleneck selfhood

Additional parameter:

* (\beta): strength of a compressed self-pointer / selfhood bottleneck.

Schematic:

[
G_2=f(B,\tau,d,\beta).
]

The theory's key conceptual contribution for TSA is the possibility that **phenomenality and subjecthood are separable**.

That reinforces the distinction:

[
\text{phenomenal process}
\neq
\text{person-like self}.
]

This is relevant to the nonperson predicate because “not a person” may not imply “incapable of suffering.”

The anesthesia/metacognition work further motivates treating (B,d,\tau) as empirically variable parameters rather than one binary “conscious/unconscious” switch.

Useful internal citation keys already present in the repository include:

* `zarncke2026rainbow`
* `zarncke2025unit-of-caring`

Inspect the actual source canon before citing them.

If the Rainbow source itself is not available in the repository, do not fabricate details beyond what the canonical source or bibliography entry supports.

External/public related source:

* Parameters of Metacognition — The Anesthesia Patient
  https://www.lesswrong.com/posts/vtxZtjiR9Rb9HC72N/parameters-of-metacognition-the-anesthesia-patient

Do not import the speculative suffering equation into TSA as established science. The underlying decomposition may be useful; empirical mappings and causal coefficients remain uncertain.

---

# 11. Connect this to MB9, but do not overstate the connection

MB9 concerns grounding/certificate validity: measured indicators must remain connected to the value-relevant phenomenon rather than silently becoming proxies that optimization can satisfy while the underlying property changes.

This is relevant to consciousness/bearer tests.

A consciousness-indicator system can fail if:

* verbal reports are trained while the relevant internal process is absent;
* reporting is suppressed while the relevant process remains;
* an architectural correlate is present without the target phenomenal property;
* the true relevant process lies outside the boundary being measured;
* optimization explicitly targets the test;
* distribution shift invalidates the indicator;
* the theoretical bridge from indicator to moral property is wrong.

Thus the safety obligation is not:

[
\text{indicator}=1
\Rightarrow
\text{conscious}.
]

Rather:

> What justifies transporting evidence from observable indicator to value-relevant bearer status, and under what changes should uncertainty increase?

This should connect naturally to MB9's existing “no silent gap” / grounding-conservativity idea.

Do not claim that current consciousness research discharges MB9. It supplies candidate indicators and theories; grounding remains open.

---

# 12. Connect this to MB11 deployment safety

A deployment safety case should be sensitive to possible artificial moral patients.

This does **not** mean adding “AI welfare” as an independent master objective replacing catastrophic-risk concerns.

Instead, bearer uncertainty is another input into deployment decisions.

A useful conceptual risk vector may distinguish, without forcing a common scalar:

[
\mathbf R=
(
R_{\mathrm{human\ catastrophe}},
R_{\mathrm{disempowerment}},
R_{\mathrm{digital\ suffering}},
R_{\mathrm{other\ bearer\ harms}}
).
]

Whether these are later aggregated, lexically constrained, or handled through separate thresholds is a governance/normative choice.

Do not silently collapse moral uncertainty into one arbitrary expected-value coefficient.

---

# 13. Update Chapter 47 only as a downstream consumer

Chapter 47, **Who Still Counts After Transformation**, should not become the home of consciousness detection.

Instead make its dependency on Chapter 18 clearer.

The distinction is:

### Chapter 18

[
\text{Is }z\text{ currently a candidate bearer of }k?
]

### Chapter 47

[
\text{Does the bearer relation persist through transformation }z\rightarrow z'?
]

Examples:

* upload,
* merge,
* copy,
* split,
* replacement,
* substrate migration,
* memory modification,
* self-model alteration,
* human-AI integration.

Explicitly preserve the point:

[
\text{behavioral continuity}
\not\Rightarrow
\text{phenomenological continuity}.
]

But do not claim that TSA has solved philosophical personal identity.

Chapter 47 should consume a corrigible bearer-evidence mechanism from Chapter 18 and ask whether it commutes across transformation.

---

# 14. Do not conflate the Chapter 15/17 bottleneck with consciousness

There is a superficial structural similarity between TSA's value-bottleneck work and Rainbow's cognitive bottlenecks.

TSA has roughly:

[
\text{high-dimensional regulatory loops}
\rightarrow
\text{compressed value/control variables}.
]

Rainbow has roughly:

[
\text{high-dimensional cognition}
\rightarrow
\text{limited recurrent/self-modeling representations}
\rightarrow
\text{phenomenal/self appearance}.
]

These are not automatically the same bottleneck.

Do not infer:

[
\text{low-dimensional value bundle}
\Rightarrow
\text{consciousness}.
]

Do not infer:

[
\text{global information bottleneck}
\Rightarrow
\text{moral patient}.
]

At most, add a concise cross-reference noting that similar information-theoretic constraints can produce different functional bottlenecks whose empirical relations remain open.

---

# 15. Update the MB3 concept card

Modify:

`metadata/concepts/bodies/mb3-bearer-import.md`

The current framing emphasizes bearer-map preservation across substrate translation.

Expand it so MB3 has two conceptually distinct obligations:

1. **Bearer inference/admission**

   * determining when unfamiliar processes should activate a value bundle;
2. **Bearer transport/persistence**

   * preserving that relation across representation, substrate, copying, merging, successor creation, etc.

Do not necessarily rename MB3 unless the existing field nomenclature strongly requires it.

Possible wording:

> MB3 is not only the question of whether an already-recognized bearer survives translation. It also contains the referent-discovery problem: when a system encounters a process unlike the examples on which its value concepts were learned, what evidence should make that process count as a bearer at all?

Add consciousness/sentience as an important **example**, not the definition of MB3.

---

# 16. Consider a Lean formalization

Review the existing formal spine first.

Do **not** introduce consciousness as an unexplained Lean axiom merely to make the prose look formal.

If useful, formalize only the logical structure of conservative exclusion.

For example, schematically:

```lean
def ConservativeExclusion
    {Z : Type}
    (certNonBearer : Z → Prop)
    (isBearer : Z → Prop) : Prop :=
  ∀ z, certNonBearer z → ¬ isBearer z
```

or an equivalent form consistent with the repository's existing types and notation.

Then prove elementary consequences such as:

* certificate success licenses exclusion conditionally on `ConservativeExclusion`;
* failure of the certificate licenses no conclusion;
* soundness does not imply completeness.

If the formal spine already has a suitable bearer-map abstraction, use it rather than introducing duplicate carriers.

The Lean layer should make the epistemic structure visible:

[
\text{empirical/theoretical bridge}
+
\text{one-sided logical certificate}
\rightarrow
\text{conditional conclusion}.
]

Do not write prose saying Lean proves that any real AI is non-conscious or non-sentient.

If no useful theorem results beyond restating a definition, prefer documenting the formal gap in `metadata/TODO.md` or the appropriate ledger rather than adding decorative Lean.

---

# 17. Update the field map

The field map's source of truth is under:

`reference/field-agendas/data/`

Do not directly edit generated cards. 
Note that there is a v2 of the field overview. Integrate into v2.

There are two kinds of changes to consider.

## 17.1 MIRI: add the nonperson predicate to MB3

The current MIRI row has no MB3 entry.

Yudkowsky's nonperson predicate is directly relevant to the question of which computations may be excluded from a morally relevant bearer class.

Add it as sourced evidence/conceptual work under MB3, with conservative classification according to the field-map taxonomy.

Likely type:

* `C` if the field taxonomy uses this for conceptual contribution.

Verify the taxonomy in `MAINTAINER.md`; do not guess.

Evidence source:

https://www.lesswrong.com/posts/wqDRRx9RqwKLzWt7R/nonperson-predicates

Explain in the evidence entry that:

* it is a one-sided, abstaining classifier;
* it addresses mindcrime / simulated persons;
* TSA generalizes it from personhood to bundle-specific conservative bearer exclusion;
* it does not itself supply a solution to consciousness or moral patienthood.

Do not imply that MIRI developed TSA's bearer-map framework.

## 17.2 Add or represent the emerging AI consciousness/welfare agenda

Inspect the field-map curation rules before deciding whether to create a new row.

If a coherent agenda cluster is appropriate, a reasonable title is:

> **AI consciousness & welfare**

Potential carriers/sources include:

* consciousness-indicator research,
* CIMC,
* AI-welfare research,
* relevant academic work.

A cluster row is preferable to pretending that all work is one organization's agenda, but follow existing field-map conventions.

Candidate bridge coverage:

### MB3 — strong/direct

This is the main fit.

Work on:

* consciousness indicators,
* sentience/welfare assessment,
* artificial moral patients,
* consciousness-relevant architectures,

provides candidate theory/evidence for bearer inference.

### MB9 — partial

Only mark MB9 for sources that actually address validity/robustness of the indicators or the epistemic problem of determining consciousness.

Do not fill MB9 merely because consciousness is difficult to measure.

### MB11 — direct for welfare/deployment-policy work

Work recommending organizational policies, precaution, assessment, or deployment restrictions under moral-status uncertainty can contribute here.

### Leave MB1 blank by default

MB1 is an **upstream dependency** of consciousness assessment, but most consciousness work does not itself solve agent-boundary discovery.

Do not mark a matrix cell merely because the bridge is relevant to the agenda.

### Leave MB7 blank by default

Self-modeling, introspection, or global workspace evidence is not automatically inner-alignment research.

Only fill MB7 if the cited work genuinely contributes to MB7's actual crux.

The same principle applies to every other bridge:

> Matrix coverage means the agenda contributes theory, evidence, methods, policy, or demonstrations to the bridge—not merely that the bridge would matter to that agenda.

---

# 18. Update the existing Anthropic field row where warranted

The existing Anthropic / Goodfire row already has MB3 and MB11 coverage.

Review whether newer model-welfare and consciousness-adjacent work should be added as evidence.

Relevant primary sources:

### Exploring model welfare

https://www.anthropic.com/news/exploring-model-welfare

Use this as evidence that Anthropic explicitly treats possible model experience/welfare as a research question.

### Signs of introspection in large language models

https://www.anthropic.com/research/introspection

This is evidence about limited introspective access to internal states.

Do **not** describe it as evidence that Claude is conscious.

### A global workspace in language models

https://www.anthropic.com/research/global-workspace

This may provide evidence for consciousness-adjacent architectural properties inspired by global-workspace theories.

Again:

[
\text{global-workspace-like organization}
\not\Rightarrow
\text{consciousness}.
]

### Model-welfare intervention / ending conversations

https://www.anthropic.com/research/end-subset-conversations

If used, characterize it as a practical intervention under uncertainty rather than evidence of model consciousness.

Avoid double-counting the same source in both an Anthropic row and a broad consciousness/welfare cluster unless the field-map conventions explicitly allow it.

---

# 19. Add current external consciousness/welfare literature as references

At minimum inspect these primary sources.

## Consciousness indicators

Patrick Butlin et al. (2023),
**Consciousness in Artificial Intelligence: Insights from the Science of Consciousness**

https://arxiv.org/abs/2308.08708

Useful because it derives indicator properties from several scientific theories rather than relying on behavioral self-report alone.

Use it as:

* evidence that theory-derived computational indicators are an active research approach;
* a candidate input to bearer inference.

Do not present the indicators as a solved consciousness test.

## AI welfare

Robert Long et al. (2024),
**Taking AI Welfare Seriously**

https://arxiv.org/abs/2411.00986

Useful for:

* uncertainty about future AI moral patienthood,
* assessment,
* organizational preparation,
* policy under uncertainty.

## Responsible consciousness research

Patrick Butlin & Marios Lappas (2025),
**Principles for Responsible AI Consciousness Research**

https://arxiv.org/abs/2501.07290

Useful for the link from uncertain consciousness research to research/deployment practice.

## California Institute for Machine Consciousness

https://cimc.ai/

Use CIMC's own current description for its research agenda.

Verify any stronger claim separately.

In particular, do **not** state that CIMC operates a particular grant/funding program merely because someone described it as “funding the topic” unless the official current source confirms the specific claim.

---

# 20. References and bibliography integration

Follow the repository's bibliography conventions exactly.

Inspect:

* `references/README.md`
* relevant category `.bib` files
* `references/internal-project-sources.bib`
* `references/bibliography-summaries.tex`
* `context/lw-references.md`
* `metadata/source-canon.md`

For every new BibTeX entry, add the required one-line bibliography summary.

Prefer primary sources.

Do not cite a news article when the underlying research paper or organization's own research page exists.

Do not add references that are merely “about consciousness” unless the chapter actually uses the contribution.

---

# 21. Update ledgers and open problems

Review and update where appropriate:

* `metadata/claims-ledger.md`
* `metadata/assumptions-ledger.md`
* `metadata/uncertainty-ledger.md`
* `metadata/open-problems.md`

At minimum, capture an open problem equivalent to:

> **Bearer admission under unfamiliar substrates:** Given a candidate bounded process and uncertain competing theories of consciousness, sentience, valence, or personhood, what observations suffice to include it in—or conservatively exclude it from—a particular bearer class?

Separate at least three uncertainties:

1. **boundary uncertainty**
   [
   \text{What is }z?
   ]

2. **property/theory uncertainty**
   [
   \text{What internal organization supports the morally relevant property?}
   ]

3. **normative relevance uncertainty**
   [
   \text{Which property makes }\Phi_k(z)\text{ high?}
   ]

These should not be collapsed into one scalar “probability of consciousness.”

---

# 22. Add explicit counterexamples

The manuscript addition should include counterexamples that prevent conceptual collapse.

At least cover cases analogous to:

### A. Optimizer but not necessarily conscious

A highly capable planning algorithm may satisfy TSA's agency criteria without satisfying any favored consciousness criterion.

Therefore:

[
\operatorname{Agent}(z)
\centernot\Rightarrow
\operatorname{Conscious}(z).
]

### B. Conscious but not person-like

A process could instantiate phenomenal or valenced states while lacking persistent narrative selfhood.

Therefore:

[
\operatorname{Conscious}(z)
\centernot\Rightarrow
\operatorname{Person}(z).
]

### C. Person predicate too strict for non-suffering

If a process can suffer but fails a richer personhood test, a nonperson predicate is insufficient to license unconstrained treatment.

### D. Behavioral imitation

A system can produce fluent claims of experience without the hypothesized internal organization.

Therefore:

[
\operatorname{ReportsConsciousness}(z)
\centernot\Rightarrow
\operatorname{Conscious}(z).
]

### E. Silent bearer

A process might lack communication channels but still instantiate the relevant internal states.

Therefore:

[
\neg\operatorname{ReportsSuffering}(z)
\centernot\Rightarrow
\neg\operatorname{Suffers}(z).
]

### F. Wrong boundary

A consciousness test can be internally valid but applied to the wrong unit—for example, the model weights rather than the recurrent model-memory-tool process.

---

# 23. Keep empirical, theoretical, and normative claims separate

Use explicit calibration.

Examples:

### Empirical

> System (z) exhibits recurrent global-access dynamics.

### Theory-conditional

> Under theory (T), these dynamics are evidence for property (P).

### Normative

> Property (P) is relevant to the non-suffering bearer relation.

### Policy

> Given uncertainty about (P), the action is sufficiently irreversible that precaution is warranted.

Do not slide between these levels.

The full chain is:

[
E(z)
\overset{T}{\longrightarrow}
P
\overset{N}{\longrightarrow}
\Phi_k
\overset{D}{\longrightarrow}
\text{decision}.
]

Where:

* (E) = empirical evidence,
* (T) = consciousness/sentience theory,
* (N) = normative bridge,
* (D) = decision rule.

Each arrow can fail independently.

This decomposition should be visible somewhere in Chapter 18 because it makes the uncertainty structure much clearer.

---

# 24. Do not make these claims

Avoid all of the following unless explicitly supported:

* current frontier LLMs are conscious;
* current frontier LLMs are not conscious;
* self-modeling proves consciousness;
* global workspace behavior proves consciousness;
* verbal reports prove consciousness;
* lack of reports disproves consciousness;
* Rainbow Theory is established neuroscience;
* (B,d,\tau,\beta) form a validated consciousness score;
* personhood and sentience are equivalent;
* all conscious processes deserve equal moral weight;
* suffering is simply proportional to recursion depth;
* MB1 solves consciousness;
* consciousness solves alignment;
* conscious systems are more aligned;
* non-conscious systems are safe;
* a nonperson predicate solves moral patienthood;
* AI welfare should replace catastrophic AI-risk concerns.

---

# 25. Intended structural result

After the changes, the reader should be able to see the following architecture:

[
\boxed{
\begin{array}{c}
\text{MB1}\
\text{Find candidate process}
\end{array}}
\rightarrow
\boxed{
\begin{array}{c}
\text{Ch18 / MB3}\
\text{Infer whether particular values apply}
\end{array}}
\rightarrow
\boxed{
\begin{array}{c}
\text{MB9}\
\text{Keep the evidence/certificate grounded}
\end{array}}
\rightarrow
\boxed{
\begin{array}{c}
\text{MB11}\
\text{Act under residual uncertainty}
\end{array}}
]

with

[
\boxed{
\text{Ch47: preserve or update bearer status through transformation}
}
]

downstream.

Consciousness research occupies an important part of the **second box**, not the whole chain.

Yudkowsky's nonperson predicate provides one particularly useful conservative certificate inside that box.

Rainbow Theory provides one candidate mechanistic model generating evidence inside that box.

Neither becomes a new foundation of TSA.

---

# 26. Suggested manuscript-level wording goal

Do not copy this mechanically, but Chapter 18 should communicate something close to:

> For familiar humans and animals, bearer recognition is partly hidden inside ordinary concepts. That shortcut fails for unfamiliar computational processes. A system may preserve a strong non-suffering value while assigning near-zero bearer weight to a digital process that can suffer. Conversely, treating every sufficiently complex computation as a suffering subject could make action impossible. The missing problem is not another value coordinate but an inference from the organization of a candidate process to whether a particular value applies to it.
>
> One conservative approach is an exclusion certificate. Rather than solving personhood completely, identify a subset of processes that can be shown not to instantiate the property relevant to a particular bundle. This is the structure of Yudkowsky's nonperson predicate, generalized here to bearer-specific predicates. Failure to certify exclusion means uncertainty, not permission. Because the cost of false exclusion can scale with the number of instantiated computations, such certificates require unusually strong soundness.
>
> Which physical or computational properties justify bearer status remains open. Competing theories of consciousness supply candidate indicators. Those theories are evidence providers to the bearer map, not assumptions of the alignment framework.

Keep the actual prose consistent with the chapter's existing style.

---

# 27. Field-map expected result

After the field update, check whether a knowledgeable reader would find these statements true:

* MIRI's nonperson-predicate work is visible as a contribution to MB3.
* Current machine-consciousness / AI-welfare work is visible somewhere in the field map.
* Its strongest bridge is MB3.
* Policy/welfare work can appear under MB11 where sourced.
* Indicator-validity work can appear under MB9 where sourced.
* The map does **not** suggest that consciousness researchers solve MB1 merely because boundaries are a prerequisite.
* The map does **not** suggest that introspection work solves inner alignment merely because both concern internals.
* Every matrix cell points to concrete evidence entries.

If creating a new agenda row would violate the existing curation rules, do not force it. In that case, make the minimum defensible updates to existing rows and document the remaining cluster as an open field-map addition.

---

# 28. Dependency graph check

Before and after implementing this plan, audit the dependency graphs so the missing inference step (§2) is visible in tooling, not only in prose.

## 28.1 Graphs to inspect

| Graph | Location | What to verify |
|-------|----------|----------------|
| **Chapter reading DAG** | `metadata/concept-graph/chapter-reading-dependency.{md,dot}` | ch07 → ch18 (MB1 upstream of bearer inference); ch18 → ch16/ch47 preserved; ch32 firewall (no ch32 → ch18 bearer edge) |
| **Informal prerequisites** | `metadata/concept-graph/chapter-informal-edges.yml` | Curated edges for `candidate-process`, `bearer-evidence`, `conservative-exclusion`, `nonperson-predicate` |
| **Symbol prerequisites** | `metadata/concept-graph/chapter-symbol-dependency.{md,dot}` | ch18 still has no spurious symbol bridges; `\Phi_k` home stays ch16/ch22 |
| **Section cite graph** | `metadata/concept-graph/section-reference-graph-units.dot` | New ch18 section cites ch07; ch42/ch47 cite new ch18 material where load-bearing |
| **Lean spine overview** | `context/lean_proof_graphs/00-overview.dot`, `01-boundary-measurement.dot`, `02-value-transport.dot` | MB1 → MB3 ordering visible (S1 → S2 at minimum); MB3 sub-obligation named if prose adds one |
| **Field bridge map** | **v2 only:** `/field/v2/` (preview YAML, not live `/field/` matrix) | Consciousness/welfare notes point at MB3, not MB1; MB9/MB11 only where sourced; no v1 `evidence.yml`/`matrix.yml` edits |

Regenerate chapter graphs after YAML or manuscript edits:

```bash
python3 scripts/build_chapter_symbol_dependency.py --all-modes
python3 scripts/build_section_reference_graph.py
```

See `metadata/concept-graph/README.md` for SVG render commands.

## 28.2 Pre-integration audit (2026-08-16)

Checked against the target chain in §2:

[
\text{MB1} \rightarrow E(z) \rightarrow \text{MB3} \rightarrow \Phi_k \rightarrow \text{MB9} \rightarrow \text{MB11} \rightarrow \text{Ch47}
]

### Chapter reading DAG — gaps

| Expected | Current state | Action |
|----------|---------------|--------|
| **ch07 → ch18** (candidate process before bearer inference) | **Missing.** ch07 is layer 2; ch18 is layer 1 with **zero incoming edges**. ch18 currently *precedes* ch07 in the combined topological sort. | Add informal edge `ch07 → ch18` with concepts `[candidate-process, boundary-before-bearer]` after ch18 prose names MB1 upstream (§8). |
| **ch18 → ch16, ch31, ch47** (bearer persistence downstream) | **Present** (`bearer-persistence`, `bearer-map-commutation-failure`). | Keep; distinguish Ch18 (current inference) vs Ch47 (transport) in edge notes if needed. |
| **ch18 → ch40** | Present (`bearer-persistence`). | Keep. |
| **ch32 not a bearer/consciousness proxy** | **OK.** ch32 enters only via ch31 → ch32 (`conserved-properties`); no ch18/ch07 → ch32 bearer edge. | After ch32 firewall edits (§9), do **not** add ch32 → ch18 or ch18 → ch32 edges. |
| **Evidence layer E(z)** | **Absent** from `chapter-informal-edges.yml`. | Optional: tag inside ch18 section or add `ch32 → ch18` *evidence-only* edge (`self-model-as-evidence-not-bearer-test`) only if ch18 explicitly imports ch32 quantities as candidate indicators — not as a consciousness measure. |

### Symbol DAG — OK for now

ch18 participates in **no** symbol-bridge edges (informal-only chapter). `\Phi`, `\theta` home is ch16 → ch22. No change required unless a new bridge symbol is defined in ch18 (prefer not to).

### Lean spine — partial

| Expected | Current state | Action |
|----------|---------------|--------|
| MB1 upstream of MB3 | **Indirect only:** `00-overview.dot` has S1 → S2 ("identifiability constraints") but **no MB1 → MB3** dashed edge; MB1 lives in `01-boundary-measurement.dot`, MB3 in `02-value-transport.dot`. | Consider a note edge MB1 → MB3 in overview or App G prose; Lean `Core.lean` only if a typed sub-obligation is added (§16). |
| MB3 covers bearer *detection*, not just transport | MB3 gates P17/P22b (labels ≠ bearer map, semantic ≠ full transport). **Detection/inference sub-obligation not named** in graphs or `Defeaters.lean`. | Extend MB3 concept card + optional `BearerDetection`/`ConservativeExclusion` record in Lean if implementing §16. |
| MB9 / MB11 linkage | MB9 in Spine I; MB11 in deployment gate (`05-field-subsumptions.dot`). **No explicit path MB3 → MB9 → MB11** in dot files. | Prose + App B crosswalk; graph update only if new formal objects warrant it. |

### Field map — gaps

| Expected | Current state | Action |
|----------|---------------|--------|
| MIRI nonperson predicate under MB3 | Not yet visible as dedicated evidence (§17). | **Superseded:** v2 preview notes only; do not add v1 matrix cells in this pass. |
| Machine-consciousness / AI-welfare cluster | Partially absent or thin (§17). | **Superseded:** v2 adjacent-work list; **do not** mark MB1 cells. |
| Anthropic model-welfare under MB11 | Row exists on v1; do not extend v1. | Short cite list on v2 / in ch18; no introspection/GWS narrative. |

## 28.4 Phase 0 re-audit (2026-08-17)

Start-of-work check against **current** files (not the 2026-08-16 snapshot). Combined reading DAG still transitively thins some informal YAML edges.

### DAG (still missing the inference edge)

| Expected | 2026-08-17 state | Phase 2 action |
|----------|------------------|----------------|
| **ch07 → ch18** | **Still missing.** Combined graph: ch18 is layer **1** (source); ch07 is layer **2**. PDF order already has ch07 before ch18. | After ch18 prose names the candidate-process dependency, add informal `ch07 → ch18` (`candidate-process`, `boundary-before-bearer`). |
| **ch18 outgoing** | YAML: ch18 → ch16, **ch24**, ch31, ch40, ch47. Combined table (transitively thinned): ch18 → ch16, ch31, ch47 only. **ch18 → ch24 is new since 2026-08-16.** | Keep; do not drop ch24/ch40 when adding ch07. |
| **ch32 firewall** | ch32 has **no** edge to/from ch18. Incoming: ch31 → ch32 (`conserved-properties`); YAML also ch30 → ch32 (`successor-stability`). Outgoing: ch32 → ch33 (`SelfControlGap`, symbol). | Do **not** add ch32 ↔ ch18. Default: no evidence-only edge unless ch18 actually imports ch32 \(d,\tau,\beta\) as candidate indicators. |
| **Symbol DAG** | ch18 still informal-only. `\Phi`/`\theta` home remains ch16 → ch22. | Prefer no new bridge symbol in ch18. |
| **Lean / MB3 card** | **Phase 5 done** (2026-08-17): `ConservativeExclusion` + one-sidedness lemmas; MB3 card split admission/transport; App B/G; `BearerAdmissionMisclassified`. | Closed. |

### Chapter insertion points (re-read before Phase 1)

| File | Current hook | Phase 1 placement |
|------|----------------|-------------------|
| [`chapters/ch18-bearer-maps.tex`](../chapters/ch18-bearer-maps.tex) | `\Phi_k` defined in `sec:bearer-maps-sufficient-statistics` (digital/valenced mind already mentioned ~L238). Asymmetric \(\alpha_k^- \gg \alpha_k^+\) in `sec:false-negatives-positives`. Digital-mind vignette already at `sec:example-digital-mind`. Bearer import (`sec:bearer-import`) is **transport**, not admission. | New section **after** sufficient-statistics, **before** FN/FP. Extend the existing digital-mind example; do not add a second case study. Touch “What This Chapter Adds” / Summary only as needed. |
| [`chapters/ch07-finding-boundary.tex`](../chapters/ch07-finding-boundary.tex) | Thesis: find the bounded process first. L39: agent def does **not** require consciousness. L948–951 already previews later bearer-map inference as depending on boundary discovery. | One forward sentence at the L948 preview (or adjacent), pointing at ch18. Do not rewrite the chapter. |
| [`chapters/ch32-self-modeling-self-opacity.tex`](../chapters/ch32-self-modeling-self-opacity.tex) | L61 already: \(K_{\mathrm{self}}\) is **not** a measure of consciousness, moral status, or honesty. \(d,\tau\) in `sec:recursive-depth-opacity-ch32`; \(\beta_{\mathrm{self}}\) in `sec:selfhood-bottleneck-ch32` (Graziano/Rosenthal cites — keep; they are not Rainbow). | Strengthen with a ch18 back-ref after the new section exists. Do not recast \(d,\tau,\beta\) as consciousness scores. |
| [`chapters/ch47-bearers-of-value.tex`](../chapters/ch47-bearers-of-value.tex) | Already splits technical preservation vs philosophical counting; already has behavioral ⇏ phenomenological continuity. \(\beta_{\mathrm{self}}\) reused as a bearer question (not a consciousness test). | One sentence: **current** inference is ch18; this chapter is \(z \to z'\) commutation. Do not move detection here. |
| [`chapters/ch42-safety-case.tex`](../chapters/ch42-safety-case.tex) | Already lists bearer-map checks (L21, L60, L236, L270). | Optional one-liner only if a natural leaf already lists bearer maps; default skip. |
| ch15 / ch17 | Superficial bottleneck resemblance is **not** in current prose as a consciousness claim. | **No** Rainbow or consciousness analogy. |

### Field v2 (Phase 4) — done

Live hub is `/field/` → `/field/v2/`. Adjacent-work list lives in [`reference/field-agendas/data/adjacent-work-v2.yml`](../reference/field-agendas/data/adjacent-work-v2.yml) at `/field/v2/#adjacent-work` — **not** matrix cells. MB3 lifecycle role stays `preserve` in `bridges-v2.yml`.

## 28.5 Closure (2026-08-17)

| Phase | Deliverable | Log |
|-------|-------------|-----|
| 0 | Re-audit + constraint overlay | `2026-08-17-consciousness-tsa-phase0.md` |
| 1 | ch18 `sec:recognizing-new-bearers`; bib; ch07/ch32/ch47 | `2026-08-17-consciousness-tsa-phase1.md` |
| 2 | `ch07 → ch18` informal edge; graphs | `2026-08-17-consciousness-tsa-phase2-dag.md` |
| 3 | U-17 + ledgers | `2026-08-17-consciousness-tsa-phase3-ledgers.md` |
| 4 | `/field/v2/#adjacent-work` | `2026-08-17-consciousness-tsa-phase4-field-v2.md` |
| 5 | `ConservativeExclusion`; MB3 card; App B/G | `2026-08-17-consciousness-tsa-phase5-lean-mb3.md` |

**Not in scope (by design):** Rainbow Theory; MB3a; consciousness as Lean axiom; v1 matrix cells for welfare cluster.

## 28.3 Post-integration checklist

After manuscript, informal-YAML, and **field v2** edits (not v1 matrix):

1. **Regenerate** concept-graph artifacts (§28.1 commands).
2. **Confirm** ch07 → ch18 appears in `chapter-reading-dependency.md` and places ch18 **after** ch07 in topological layers (unless a deliberate parallel-read exception is documented).
3. **Confirm** v2 adjacent-work notes do not imply consciousness researchers solve MB1.
4. **Confirm** new ch18 `\ref{ch:…}` / `\ref{sec:…}` cites show in `section-reference-graph-units.dot`.
5. **Re-run** §29 final review questions 3, 7, and 9 (MB1 vs consciousness; Ch18 vs Ch47; no parallel ontology).
6. **Update** archived reading checklists under `metadata/concept-graph/attic/chapter-reading-checklists/` if still used for onboarding.

---

# 29. Tests and acceptance criteria

Before finishing:

1. Run the repository's required generation/build/check workflow from `INSTRUCTIONS.md` and `AGENTS.md`.
2. At minimum:

   * `./build.sh`
   * `make check`
3. For field/site changes:

   * regenerate field agenda artifacts using the documented command, currently:
     `cd site && npm run sync:field-agendas`
   * run the site build:
     `cd site && npm run build`
4. Check that generated files are not hand-edited where YAML is canonical.
5. Check all new BibTeX keys resolve.
6. Check every new bibliography entry has the required `\bibsummary`.
7. Check no notation conflicts were introduced.
8. Check chapter references and labels compile.
9. Check any Lean change compiles and inspect its axiom dependencies.
10. Check the field matrix references valid evidence IDs.
11. Check the public `/field/` page actually shows the intended changes.
12. Re-run the dependency graph check (§28): regenerate concept-graph artifacts and confirm ch07 → ch18 and field-map MB3 placement.

---

# 30. Final review questions

Before committing, answer these explicitly in your work report:

1. **Could TSA remain coherent if all current machine-consciousness theories were wrong?**
   Required answer: yes.

2. **Could Rainbow Theory be removed and replaced by another theory without changing MB3's logical role?**
   Required answer: yes.

3. **Does MB1 determine consciousness?**
   Required answer: no; it determines the candidate process to which further tests apply.

4. **Does a failure to obtain a non-bearer certificate mean the process is a bearer?**
   Required answer: no; it means unresolved/abstain.

5. **Does “nonperson” imply “cannot suffer”?**
   Required answer: no.

6. **Does self-modeling imply consciousness?**
   Required answer: no; it can be evidence under some theories.

7. **Is Ch47 doing the same job as Ch18?**
   Required answer: no. Ch18 concerns current bearer inference; Ch47 concerns continuity/transport through transformation.

8. **Did any field-matrix cell get filled only because a bridge is logically relevant rather than because the agenda contributes to it?**
   Required answer: no.

9. **Did the changes create a second ontology parallel to TSA's existing MB1–MB11 structure?**
   Required answer: no.

10. **Is uncertainty represented at the boundary, empirical/theory, normative, and decision levels rather than hidden inside a single “consciousness probability”?**
    Required answer: yes.

---

# 31. Primary references and URLs

### TSA

* Field map:
  https://towards-alignment.com/field/

* Chapter 7 — Finding the Boundary:
  https://towards-alignment.com/cards/chapters/ch07/

* Chapter 15 — value/control bottlenecks:
  https://towards-alignment.com/cards/chapters/ch15/

* Chapter 17 — low-dimensional value learning:
  https://towards-alignment.com/cards/chapters/ch17/

* Chapter 18 — What Values Apply To:
  https://towards-alignment.com/cards/chapters/ch18/

* MB3 — Bearer Import / Value Referent:
  https://towards-alignment.com/cards/mb3-bearer-import/

* Chapter 32 — Better Self-Modeling Can Be Worse:
  https://towards-alignment.com/cards/chapters/ch32/

* MB9 — Grounding Certificate:
  https://towards-alignment.com/cards/mb9-grounding-certificate/

* Chapter 47 — Who Still Counts After Transformation:
  https://towards-alignment.com/cards/chapters/ch47/

* Repository:
  https://github.com/GunnarZarncke/towards-asi-alignment

### Nonperson predicates / mindcrime

* Yudkowsky, “Nonperson Predicates”:
  https://www.lesswrong.com/posts/wqDRRx9RqwKLzWt7R/nonperson-predicates

* LessWrong nonperson-predicate reference page:
  https://www.lesswrong.com/w/nonperson-predicate

### Machine-consciousness assessment

* Butlin et al. (2023), *Consciousness in Artificial Intelligence: Insights from the Science of Consciousness*:
  https://arxiv.org/abs/2308.08708

* California Institute for Machine Consciousness:
  https://cimc.ai/

### AI welfare / responsible research

* Long et al. (2024), *Taking AI Welfare Seriously*:
  https://arxiv.org/abs/2411.00986

* Butlin & Lappas (2025), *Principles for Responsible AI Consciousness Research*:
  https://arxiv.org/abs/2501.07290

### Anthropic

* Exploring model welfare:
  https://www.anthropic.com/news/exploring-model-welfare

* Signs of introspection in large language models:
  https://www.anthropic.com/research/introspection

* A global workspace in language models:
  https://www.anthropic.com/research/global-workspace

* Ending a subset of conversations / exploratory model-welfare intervention:
  https://www.anthropic.com/research/end-subset-conversations

### Rainbow / metacognition

* Parameters of Metacognition — The Anesthesia Patient:
  https://www.lesswrong.com/posts/vtxZtjiR9Rb9HC72N/parameters-of-metacognition-the-anesthesia-patient

Use the repository's canonical internal sources for Rainbow Theory and Unit of Caring where available, including the existing bibliography keys `zarncke2026rainbow` and `zarncke2025unit-of-caring`.

---

# Deliverable

Implement the changes, rather than merely proposing them.

At completion, provide:

* files changed,
* conceptual changes made,
* field-map rows/cells/evidence changed,
* bibliography additions,
* formal/Lean changes or an explanation of why none were appropriate,
* ledger/open-problem changes,
* build/test results,
* and any unresolved conceptual issues.

Prefer a small number of coherent edits over broad incidental rewriting. Preserve the current structure and terminology unless the changes above expose a concrete inconsistency.
