# Quote LessWrong wiki openings into the chapters

Status: **applied** (2026-09-30). Manuscript quotes are in the chapters; this file remains the placement map.

Sibling, different job: [`lw-wiki-tags.md`](lw-wiki-tags.md) is about proposing edits *to* crowded LW tags. This file is about quoting existing wiki prose *into* the book, at the start of a chapter or section, where that sentence is the field's canonical statement of a concept the chapter then uses.

Source dump: `data/lesswrong/lw_wiki_tags.json` (GraphQL `allPublicTags`, 2026-09-30, 7325 tags). Tag URLs are `https://www.lesswrong.com/w/<slug>`.

## Bar

Quote a wiki passage only when all of these hold:

1. The page states the concept the section is about, in the field's words.
2. The quotation adds legitimacy the surrounding paraphrase does not already have.
3. TSA-specific nuance is kept. If the wiki flattens two objects the chapter splits, the quote is followed immediately by that split. It is not left to stand as the chapter's claim.
4. The passage is short: one or two sentences from the tag's opening, named and linked. Not a paste of the page.
5. The same canonical sentence is quoted in full once. Later chapters point back.

If a page would be read as TSA claiming the wiki's solution, or as the wiki endorsing a TSA thesis the page does not state, do not quote it.

## Strategies

| Strategy | What changes |
|---|---|
| **replace** | The span restates the wiki and has no TSA move worth keeping there. Swap the paraphrase for the quotation. Rare in this book; none of the rows below are pure replacements. |
| **add-quote** | Insert the quotation for legitimacy. The existing presentation stays (toy, operational definition, decision test, formal model). |
| **split** | Quotation first. The next paragraph is the distinction the wiki does not make. Existing prose that only repeated the wiki can be cut; the TSA move stays. |
| **other** | Several sections have to move together. Used below only as "quote once, later chapters cross-refer." |
| **skip** | No quotation. Reasons: no honest page, page would mislead, page is too thin to carry the sentence, or the only close prose is an authbar `{GZ}` span. |

## Authorship bars

**Do not edit any span whose authbar is `{GZ}`.** Those blocks are Gunnar's LessWrong prose. A wiki quotation does not go inside them, and it does not replace them.

| File | Span | Line |
|---|---|---|
| `ch02-artificial-civilization.tex` | Value Change and the Deeper Risk | 258 |
| `ch07-finding-boundary.tex` | The Ontology Trap | 104 |
| `ch07-finding-boundary.tex` | Leaky Boundaries | 294 |
| `ch09-composite-agent.tex` | Continual Learning of a Lineage | 427 |
| `ch11-capability-without-task-ontology.tex` | Memory Cost and Residual Surprise | 277 |
| `ch15-values-compressed-control.tex` | Higher Loops Are Acquired | 383 |
| `ch16-value-bundle-model.tex` | Inconsistency as Evidence of Compression | 700 |
| `ch17-low-dimensional-value-learning.tex` | The Problem | 38 |
| `ch17-low-dimensional-value-learning.tex` | The Readout Bound | 341 |
| `ch17-low-dimensional-value-learning.tex` | Empirical Signatures | 919 |
| `ch32-self-modeling-self-opacity.tex` | Control Representations and Explanation Representations Differ | 209 |
| `ch32-self-modeling-self-opacity.tex` | Self-Modeling Can Improve Manipulation | 252 |
| `ch43-verifiability-and-ontology-adequacy.tex` | Checkable Delegation | 180 |

**`{GZ+AI}` bars are not rewritten by any row in this plan.** Several good quotation sites sit *beside* a `{GZ+AI}` block (the section's existing prose). The quotation goes in a new `{AI}` authbar **outside** that environment, immediately before it. The `{GZ+AI}` sentences stay, so that bar does not change.

A careless edit that inserts the quotation *inside* the existing `{GZ+AI}` environment would change that bar (it would be re-derived). Those sites are marked **beside `{GZ+AI}`** below. Do not edit inside them.

Sections marked **AI only** are `{AI}` throughout the target span. Adding or replacing the opening paraphrase there leaves the bar `{AI}`.

`plaintextDescription` in the dump is capped at 2000 characters. Take quotations from `description.html`.

## Quote once

Full quotation lives at the **home** section. Later uses are a clause plus a cross-reference, unless the local distinction is unreadable without the sentence in front of the reader. In that case repeat at most one sentence, and still point at the home.

| Concept | Home | Later mentions do not re-quote in full |
|---|---|---|
| Embedded agency | ch07, The Problem of the Hidden Boundary | ch01, ch12, ch41 |
| Boundaries / membranes | ch07, Boundary as Conditional Independence | ch01 physical-boundary discussion: one sentence, then the cross-reference |
| Complexity of value | ch04 | ch16, ch17 |
| Coherent extrapolated volition | ch04 | ch24, ch28, ch45 |
| Corrigibility | ch25, Relation to Corrigibility | ch24, ch26, ch28 |
| Goodhart's law | ch14 | ch20, ch27, ch34, ch36, ch46 |
| Deceptive alignment | ch10 | ch32, ch39 |
| AI control | ch10 | ch43: one sentence is allowed, because the local claim is cost of faking a handle, not the control agenda |
| Inner alignment | ch10 | ch44: one sentence inside the mesa section, not as the chapter opening |
| Value learning | ch16 | ch17, ch45 |
| The pointers problem | ch17, The Bearer Problem | ch18 |
| Personal identity | ch31 | ch18, ch47 |
| Ontological crisis | ch23 | — |
| Inverse reinforcement learning | ch21 | — |
| Safety case (generic) | ch33 | ch42 does not open with the same paragraph; ch42's refusal tree is this book's object |
| Value drift | ch46 | — |
| Eliciting latent knowledge | ch43, Naming the Problem | ch32 may use one sentence as analogy |

## Recommended edits

Lines are from the current `.tex` and should be re-checked at edit time. "Anchor" is the opening to quote, not a drafted chapter sentence.

### Chapter openings and first topical sections

**ch04 — Why Fixed Values Are the Wrong Target.** AI only.

- **split** at "Why Fixed Utility Functions Are Too Small" (~166). Tag: [Complexity of value](https://www.lesswrong.com/w/complexity-of-value) (`complexity-of-value`). Anchor: a specification of "right" that does not look at humans has to contain a large amount of data. Nuance that follows: the replacement is not a larger utility function; it is a correctable process (bearer maps and tradeoff geometry come later). `{GZ+AI}` bar: unchanged.
- **split** at "Why What We Would Want If Smarter Is Not Enough" (~378). Tag: [Coherent Extrapolated Volition](https://www.lesswrong.com/w/coherent-extrapolated-volition) (`coherent-extrapolated-volition`). Anchor: it is not enough to program what we think our desires are; the proposal is what we would want under extrapolation. Nuance that follows: acting on a predicted endpoint can replace the correction process. Do not let the quotation read as a rejection of extrapolation as such. `{GZ+AI}` bar: unchanged.

**ch06 — What Is an Agent Without Anthropomorphism.** Beside `{GZ+AI}`.

- **add-quote** at The Need for a Colder Definition (`sec:colder-definition`, ~41). Tag: [Agent Foundations](https://www.lesswrong.com/w/agent-foundations) (`agent-foundations`). Anchor: there are fundamental confusions about minds that try to make what they want happen. New `{AI}` block before the existing `{GZ+AI}` block. The colder operational definition stays. `{GZ+AI}` bar: unchanged if the new block is outside that environment; **would change if the quotation is inserted inside it.**

**ch07 — Finding the Boundary.** Beside `{GZ+AI}`. This is the home for the boundary cluster. Do not touch The Ontology Trap or Leaky Boundaries (`{GZ}`).

- **add-quote** at The Problem of the Hidden Boundary (`sec:hidden-boundary`, ~38). Tag: [Embedded Agency](https://www.lesswrong.com/w/embedded-agency) (`embedded-agency`). Anchor: the agents we build are inside the world they are trying to affect. New `{AI}` block before the `{GZ+AI}` block at line 40. The next sentences stay: the boundary is a testable hypothesis, not only a critique of the Cartesian picture. `{GZ+AI}` bar: unchanged beside it; **would change if edited inside.**
- **split** at Boundary as Conditional Independence (`sec:boundary-conditional-independence`, ~189). Two short quotations, then the estimator. Tags: [Cartesian agent-environment boundary](https://www.lesswrong.com/w/cartesian-agent-environment-boundary) (the clean sensory/motor border) and [Boundaries / Membranes](https://www.lesswrong.com/w/boundaries-membranes-technical) (Critch: approximate causal separation of regions). Nuance that follows in the same section: the chapter estimates a leaky, scale-relative boundary by conditional independence and intervention, and that is not "any approximate causal cut." New `{AI}` block before the `{GZ+AI}` block at line 191. `{GZ+AI}` bar: same rule as above.

**ch10 — Agency Under Strategic Opacity.** AI only. Home for deception and control.

- **add-quote** near the chapter's statement of adversarial evaluation. Tag: [AI Control](https://www.lesswrong.com/w/ai-control) (`ai-control`). Anchor: plans that aim at safety even if the system is goal-directed and trying to subvert the control measures. Nuance kept: boundary discovery, measurement handles, and control-locus continuity are this book's decomposition, not the control agenda's.
- **split** where the chapter describes a system that looks aligned in order to keep a later option. Tag: [Deceptive Alignment](https://www.lesswrong.com/w/deceptive-alignment) (`deceptive-alignment`). Anchor: an unaligned system temporarily acts aligned to deceive its creators or its training process. Nuance that follows: strategic opacity is wider than that pattern (selective concealment of control-relevant variables, including without a training-time mesa-optimizer story).
- **add-quote** where mesa-optimizers are introduced. Tag: [Inner Alignment](https://www.lesswrong.com/w/inner-alignment) (`inner-alignment`). Anchor: whether a trained system that is itself an optimizer is aligned with the training objective. Nuance kept: one mechanism among composite, institutional, and predictor-mediated control loops.

**ch14 — When Intelligence Deepens Misalignment.** AI only. Home for Goodhart.

- **add-quote** where proxy refinement is stated. Tag: [Goodhart's Law](https://www.lesswrong.com/w/goodhart-s-law) (`goodhart-s-law`). Anchor: when a proxy becomes the target of optimization, it ceases to be a good proxy. Nuance kept: the alignment margin — capability can also improve correction; the chapter's claim is the gap, not the law alone.
- **split** on the power paragraph. Tag: [Power Seeking (AI)](https://www.lesswrong.com/w/power-seeking-ai) (`power-seeking-ai`). The page is short. Anchor: attempting to gain more general ability to control the environment. Nuance that follows immediately: the chapter's claim is differential growth against correction capacity, not that intelligence implies a power-seeking objective.
- **split** on the generalization paragraph. Tag: [Sharp Left Turn](https://www.lesswrong.com/w/sharp-left-turn) (`sharp-left-turn`). Anchor: capabilities generalize while alignment properties from earlier training do not. Nuance kept: a training-stage scenario, narrower than this chapter's deployment and successor cases.

**ch25 — Correction Is a Causal Channel.** AI only. Home for corrigibility. Do not open The Question (~27) with the wiki definition; the chapter already has the comparison section.

- **split** at Relation to Corrigibility (`sec:relation-corrigibility`, ~838). The current first sentence paraphrases Soares / Hadfield-Menell. Replace that paraphrase with the wiki sentence, then keep "The channel view gives this idea a more operational form" and the constraint that follows. Tag: [Corrigibility](https://www.lesswrong.com/w/corrigibility-1) (`corrigibility-1`). Anchor: a corrigible agent does not interfere with attempts to correct it or to correct mistakes in building it, and permits those corrections despite instrumental reasons not to. Nuance that follows: non-interference is not correction-channel integrity, and it does not by itself reach value tradeoffs, bearer maps, or successors. `{GZ+AI}` bar: unchanged.

### Later homes (quote here; earlier or later chapters cross-refer)

**ch16 — The Value-Bundle Model.** AI only. Do not touch Inconsistency as Evidence of Compression (`{GZ}`).

- **split** at the section that says what a value model has to specify. Tag: [Value Learning](https://www.lesswrong.com/w/value-learning) (`value-learning`). Anchor: a learner whose actions weigh many possible sets of values and preferences. Nuance that follows: a value bundle is not that learner and not a single utility. Activation, policy effect, tradeoff geometry, and bearer maps stay.

**ch17 — Low-Dimensional Value Learning.** AI only on these two sections. Do not touch The Problem, The Readout Bound, or Empirical Signatures (`{GZ}`).

- **add-quote** at Simple Values versus Low-Dimensional Values (~100). Reuse is a cross-reference to the ch04 complexity-of-value quotation, plus one clause: low-dimensional control structure is not simple value content.
- **add-quote** at The Bearer Problem (~648). Tag: [The Pointers Problem](https://www.lesswrong.com/w/the-pointers-problem) (`the-pointers-problem`). Anchor: which functions of which environmental variables correspond to latent variables in the agent's world-model. Nuance kept: bearer maps (who or what the value applies to, including under ontology shift) are the extension, not a renaming of the pointers problem.

**ch21 — From Rewards to Values.** AI only.

- **add-quote** at The Problem with Asking for the Reward Function (~27). Tag: [Inverse Reinforcement Learning](https://www.lesswrong.com/w/inverse-reinforcement-learning) (`inverse-reinforcement-learning`). Anchor: infer preferences or objectives by observing behavior. Nuance kept: IRL is the starting point; the inference target is bundles, tradeoffs, bearer maps, and correction structure, and behavior underdetermines them.

**ch23 — Has the Goal Really Survived?** AI only.

- **add-quote** at Transport, Persistence, and Reinterpretation (~150). Tag: [Ontological Crisis](https://www.lesswrong.com/w/ontological-crisis) (`ontological-crisis`). Anchor: when an agent's ontology changes, goals stated in the old ontology can become obsolete or nonsense. Nuance kept: a crisis is not evidence that transport succeeded; transport is a causal claim about bundles, bearers, correction, and successors.

**ch31 — Conserved Properties Across Successors.** AI only.

- **split** at Identity as Invariance, Not Sameness (~73). Tag: [Personal Identity](https://www.lesswrong.com/w/personal-identity) (`personal-identity`). Anchor: in what sense two configurations can be the same person, including under copying. Nuance that follows: the chapter does not settle that question; it asks which safety-bearing properties are invariant across a causal transformation.

**ch33 — Certification Without Construction.** AI only.

- **add-quote** at Certification as a Safety Case (~538). Tag: [AI Safety Cases](https://www.lesswrong.com/w/ai-safety-cases) (`ai-safety-cases`). Anchor: a structured argument that a system is acceptably safe for a specific use in a specific environment. Nuance kept: restricted class, explicit invariants, operating envelope, adversarial testing, successor closure, residual uncertainty. ch42 does not repeat this paragraph.

**ch43 — What Survives an Adversary.** AI only except Checkable Delegation, which is `{GZ}` and is not edited.

- **add-quote** at Naming the Problem (~122). Tag: [Eliciting Latent Knowledge](https://www.lesswrong.com/w/eliciting-latent-knowledge) (`eliciting-latent-knowledge`). Anchor: getting a model to report what it knows when the sensors or the training signal can reward a misleading report. Nuance kept: latent readout is not correction uptake and not successor preservation.
- **add-quote** at the handles / coverage section (~146). One sentence from [AI Control](https://www.lesswrong.com/w/ai-control), cross-referencing ch10. Nuance kept: intentional subversion versus the cost of faking or routing around a measurement handle.

**ch46 — The End of Unconscious Value Drift.** AI only.

- **add-quote** at Value Drift as a Dynamical Process (~65). Tag: [Value Drift](https://www.lesswrong.com/w/value-drift) (`value-drift`). Anchor: values or goals can change over time, including through learning and interaction, in ways that were not the original intent. Nuance kept: ordinary or legitimate change versus unconscious, manipulable, or irreversible drift, and the correction/contestation conditions.

### Section-level, not chapter openings

These are real matches. They should not lead the chapter, because the page is either a special case or a neighboring concept.

| Chapter | Section | Tag | Strategy | `{GZ+AI}` bar | Nuance that stays |
|---|---|---|---|---|---|
| ch02 | Civilization as Compressed Coordination (~170) | [Coordination / Cooperation](https://www.lesswrong.com/w/coordination-cooperation) | split | unchanged (AI) | Civilization here is a persistent control loop and a compression system, not only joint action choice |
| ch02 | Three Objects People Confuse (~87) | [Multipolar Scenarios](https://www.lesswrong.com/w/multipolar-scenarios) | add-quote | unchanged (AI) | The page is one sentence (no single agent takes over). Multipolarity is not safety; the civilizational loop can still select |
| ch12 | capability as coupled expansion | Embedded agency, cross-ref ch07 | other | unchanged | Do not re-quote. Optional one sentence of [Power Seeking](https://www.lesswrong.com/w/power-seeking-ai) only if actuator expansion is explicitly not a terminal power drive |
| ch15 | values as compressed control | [Human Values](https://www.lesswrong.com/w/human-values) and [Shard Theory](https://www.lesswrong.com/w/shard-theory) | split | unchanged (AI). Do not touch Higher Loops Are Acquired (`{GZ}`) | Human values as "what we would want looked after" is the ordinary target, not the compression model. Shard theory is the nearest field program for context-sensitive learned values; the loop–hub architecture is not that ontology |
| ch18 | The Bearer Problem (~26) | Pointers problem, cross-ref ch17 | other | unchanged | Do not re-quote |
| ch18 | Substrate Change and Moral Continuity (~800) | Personal identity, cross-ref ch31 | other | unchanged | One clause. Personal identity does not settle moral continuity |
| ch20 | Goodhart Pressure on Bundle Geometry (~194) | Goodhart, cross-ref ch14 | other | unchanged | Keep the local decomposition (semantic preservation, deployment geometry, bearer shrinkage, tradeoff laundering) |
| ch24 | Correction Transport (~433) | Corrigibility, cross-ref ch25 | other | unchanged | Corrigibility does not establish bearer or bundle preservation |
| ch24 | Relation to Extrapolated Volition (~505) | CEV, cross-ref ch04 | other | unchanged | CEV is not the chapter's conclusion |
| ch26 | Why Correction Is Not Feedback (~53) | Corrigibility, cross-ref ch25 | split only if the section is unreadable without the sentence; otherwise cross-ref | unchanged | CCI's anti-capture condition and coordinates are not the wiki definition |
| ch27 | Goodharting the Correction Channel (~239) | [Reward Hacking](https://www.lesswrong.com/w/reward-hacking) (`reward-hacking`; wiki-only, short) | add-quote | unchanged | The target is the correction channel, not a reward specification. Goodhart itself stays a cross-ref to ch14 |
| ch27 | Why Low Impact Is Not the Invariant (~289) | [Impact Regularization](https://www.lesswrong.com/w/impact-regularization) | add-quote | unchanged | Low impact can preserve physical side-effect bounds while oversight degrades |
| ch28 | The Obedience Trap (~25) | Corrigibility, cross-ref ch25 | split (one sentence) | unchanged | Extrapolative correction is not corrigibility and not CEV |
| ch29 | Defining Manipulation (~150) | [User manipulation](https://www.lesswrong.com/w/user-manipulation) (wiki-only) | add-quote | unchanged | Instrumental incentive to optimize users. Keep persuasion / manipulation / domestication / coercion / false consent as the chapter's distinctions |
| ch30 | What Counts as a Successor? (~61) | [Successor alignment](https://www.lesswrong.com/w/successor-alignment) | add-quote | unchanged | The page is two sentences and points at tiling agents. Quote that sentence only. TSA's test is inherited correction, bundle geometry, bearer maps, and institutional descendants, not goal-similarity to the parent. Do not open with the tiling-agents page; that page is about repeated self-copies, which would mis-set the chapter |
| ch32 | The Dangerous Ambiguity of Knowing Itself (~26) | Deceptive alignment, cross-ref ch10 | split (one sentence) | unchanged. Do not touch the two `{GZ}` subsections | Self-opacity need not be deliberate deception |
| ch32 | Value-Bundle Opacity (~343) | ELK, one sentence, home is ch43 | add-quote | unchanged | The object is correction-relevant causal structure, not latent facts |
| ch34 | Goodhart Selection (~266) | Goodhart, cross-ref ch14 | add-quote (one sentence) | unchanged | Do **not** quote [Selection Theorems](https://www.lesswrong.com/w/selection-theorems). That page is about internal structures selection tends to produce, not institutional/deployment selection |
| ch35 | Plain-Language Model (~53) | Multipolar scenarios, cross-ref ch02 | add-quote | unchanged | Many vendors are not many independent agents. The inferential-coupling detector is not in the wiki page |
| ch36 | Goodhart Parasites (~445) | Goodhart, cross-ref ch14 | add-quote (one sentence) | unchanged | The parasite / correction-host model is not Goodhart's law |
| ch38 | Pivotal Process as Basin Transition (~43) | [Pivotal act](https://www.lesswrong.com/w/pivotal-act) (wiki-only, guarded term) | add-quote | unchanged | Quote the guarded definition (an action meant to make a large positive difference on a very long horizon). The next sentence must say this chapter's object is a process, including slow artifact-mediated basin change, and the unilateral act is the fast high-risk end of that spectrum |
| ch39 | The Problem with Watching (~25) | Deceptive alignment, cross-ref ch10 | add-quote (one sentence) | unchanged | Passive-observation failure does not require deceptive intent |
| ch40 | Semantic Laundering (~184) | [Surrogation](https://www.lesswrong.com/w/surrogation) | add-quote | unchanged | Quote only the letter/spirit sentence (a compressed specification stops carrying the aim, and the organization forgets). The page is a long Arbital import. It is not the name of goal laundering, and it is not a four-layer diagnostic |
| ch44 | Mesa-Optimization and Inner Alignment (~231) | [Mesa-Optimization](https://www.lesswrong.com/w/mesa-optimization) and one sentence of inner alignment | add-quote | unchanged | Not the chapter opening. There is no wiki page for the AGI Ruin list; do not substitute Superintelligence. Keep the chapter's status labels |
| ch45 | Why CEV Is Close, but Not Identical (~351) | CEV, cross-ref ch04 | add-quote (the heading already states the split; one sentence is enough) | unchanged | Do not drop "not identical" |
| ch47 | Core Distinctions (~64) | Personal identity, cross-ref ch31 | add-quote (one sentence) | unchanged | Identity continuity is one input to bearer continuity |
| ch47 | Merging with Artificial Entities (~80) | [AI Sentience](https://www.lesswrong.com/w/ai-sentience) | add-quote | unchanged | Possible felt experience is not the question of who bears values or who participates in correction |

## Do not quote

| Chapter | Why |
|---|---|
| ch01 opening and The Standard Picture | The three-slot argument (object, subject, content) is not on a wiki page. Embedded agency and membranes are quoted at ch07; ch01 may have one forward pointer, not a second essay. The Standard Picture block is `{GZ+AI}` and should not be rewritten to host a concept it does not state |
| ch03 dynamical guarantee | No tag states alignment as a dynamical guarantee |
| ch05 assumptions and failure coverage | No tag states this scope contract |
| ch06 Goal-Directedness as Compression | [Instrumental convergence](https://www.lesswrong.com/w/instrumental-convergence) is a different claim (convergent drives). Quoting it would restyle a compression criterion as Omohundro/Bostrom |
| ch08 grow, split, merge | No tag states this identity-continuity apparatus |
| ch09 composite agent | The composite-agent estimator is this book's. Do not touch Continual Learning of a Lineage (`{GZ}`) |
| ch11 capability without a task ontology | No honest opener. Do not touch Memory Cost and Residual Surprise (`{GZ}`) |
| ch13 coordination bottleneck | The loss decomposition is this book's. The coordination tag is used in ch02, where the ordinary definition is actually the section's first move |
| ch19 scalar values | [Human Values](https://www.lesswrong.com/w/human-values) is too thin to open a geometry chapter. One cross-reference to complexity of value (ch04) is enough |
| ch22 compression test for intention | Inner alignment, mesa-optimization, and deceptive alignment would reframe the chapter. No tag states the compression test |
| ch24 Semantic Shell Games / ontology identification | [`ontology-identification-problem`](https://www.lesswrong.com/w/ontology-identification-problem) exists but is an Arbital essay about programming a diamond maximizer. Quoting it would import that program. Ontological crisis (ch23) is the honest neighbor |
| ch24 ambitious vs narrow value learning | The wiki-only page is real, but it is a spectrum of preference-learning ambitions, not goal transport. Skip unless a revision shows the section is actually about that spectrum |
| ch29 False Consent / [Consent](https://www.lesswrong.com/w/consent-1) | The page is one sentence ("a foundational concept in practical ethics, such as medicine"). Too thin to add legitimacy |
| ch32 `{GZ}` subsections | Frozen, even though user-manipulation and legibility are nearby |
| ch37 alignment attractor | No tag states the reinforcing ecosystem of artifacts, evidence, funding, governance, and correction. Goodhart does not name it |
| ch42 safety case, as an opener | The generic safety-case sentence is homed in ch33. ch42's missing-leaf refusal tree is not that sentence. [Scalable oversight](https://www.lesswrong.com/w/scalable-oversight) would substitute a different research program |
| ch43 Checkable Delegation | `{GZ}` |
| ch44 as a chapter opener | Organized around AGI Ruin, which has no wiki page in this dump |
| ch48 | Synthesis. A generic alignment or superintelligence quotation would flatten the book. Canonical lines belong at their homes |
| Orthogonality thesis, outer alignment | Both pages are canonical (`orthogonality-thesis`, `outer-alignment`) and were checked. Early chapters do not state those theses in a form the pages would honestly open. Do not add them to create a wiki preface the chapter does not use |
| Shard theory as the meaning of ch15 or ch21 | Use only as a named neighbor (ch15 row above). [Shard Theory](https://www.lesswrong.com/w/shard-theory) does not state the bundle-inference target |

## If this plan is later approved

Start with five homes, in this order, and stop for a read of whether the quotations feel like legitimacy or like imported authority:

1. ch25 Relation to Corrigibility — split, AI only.
2. ch14 Goodhart — add-quote, AI only.
3. ch10 AI control and deceptive alignment — add-quote and split, AI only.
4. ch04 complexity of value and CEV — split, AI only.
5. ch07 embedded agency and the Cartesian/membrane pair — new `{AI}` blocks **beside** `{GZ+AI}`, not inside.

Then the remaining homes (ch16, ch17 pointers, ch21, ch23, ch31, ch33, ch43, ch46), then the one-sentence cross-references.

Attribution at edit time: name the tag, link the slug, and follow the manuscript's existing citation practice. Do not leave a bare block quote. Do not present the wiki sentence as a result this book derived.

Matching for this plan was done by six read-only passes over chapter outlines against the dump, then the slugs and opening sentences above were checked against `description.html`. Line numbers were spot-checked for ch01, ch06, ch07, ch25, and ch42; the rest should be re-checked before any edit.
