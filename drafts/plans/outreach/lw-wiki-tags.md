# LW wiki tags — TSA differentiations

Status: **catalog + alternative phrasings** (2026-11-05). Live edits already on [corrigibility](https://www.lesswrong.com/w/corrigibility-1) and [embedded agency](https://www.lesswrong.com/w/embedded-agency). Companion to App P (`appendices/appP-bridge-predictions.tex`) and App B. Not scheduled. Sibling: quoting wiki *into* the book is [`lw-wiki-chapter-quotes.md`](lw-wiki-chapter-quotes.md).

**Why.** Arbital folded into the [LessWrong wiki](https://www.lesswrong.com/w). Genuine cuts that live in App B / App P should be offered *there* as improvements to existing tags, not as a TSA overlay wiki.

**Non-goals.** Do not mint `MB*`, CCI, bearer-maps, or market numbers as LW headwords. Do not dump the book. Do not treat a tag edit as discharging a bridge.

---

## Lightness bar (from live edits, 2026-11)

The Sep draft proposed new paragraphs, numbered splits, and "if A holds and B fails" neighbor blocks. The live edits were much smaller. That is the bar for every remaining tag.

**Embedded agency** — one sentence spliced after the Cartesian-cut paragraph:

> This includes the question of the [Boundary](https://www.lesswrong.com/s/LWJsgNYE8wzv49yEc) of the embedded agent, i.e. the questions which parts an agent considers part of itself and how it delineates other agents from its observations.

What it did *not* add: Kenton, Cartesian frames vs interventions, Demski on Markov blankets, pointers/corrigibility conditionals, a subsection on recoverability.

**Corrigibility** — two clause-level patches on existing bullets/sentences:

- Shutdown bullet: "Shutting down the AI also has to stop [processes and subagents it has caused](https://www.lesswrong.com/posts/v3jocJRScqkBGtwvf)."
- Hard-problem sentence: "everywhere" expanded to "everywhere, i.e., including in the correction mechanism itself, without [manipulating its correctors](https://www.lesswrong.com/w/user-manipulation), and preserving [correction through self-modification](https://www.lesswrong.com/posts/5bd75cc58225bf067037531d), …"

What it did *not* add: a four-way Soares / interruptibility / Christiano / uptake split; AI Control as a new paragraph; alignment-faking as an empirical instance.

**Rules for remaining edits**

1. Touch one existing sentence, or add **one** sentence. Prefer a clause (`i.e., …`, `This includes …`, `Shutting down … also has to …`).
2. Use words already on the page or an adjacent Arbital tag (Boundary, correction mechanism, subagents, specification, residual risk).
3. Neighbor = one wiki link *inside* that clause, with the condition in the same breath (`including in the correction mechanism itself, without manipulating its correctors`). Not a second paragraph of "if A and not B."
4. Link existing LW posts/tags. No TSA, no MB, no App P market numbers, no literature-review stacks.
5. Do not add subsections. A split may come later with more buy-in.
6. If the page only describes a phenomenon, make the open question explicit in that one sentence, or point at a sibling tag that already states it.

---

## Catalog (App P → closest tag)

Canonical corrigibility slug: `/w/corrigibility-1`. Snapshot of "existing" prose is 2026-09 unless marked live.

### Done live

| App P | Tag | What shipped |
|-------|-----|----------------|
| M1 / MB1 | [Embedded agency](https://www.lesswrong.com/w/embedded-agency) | Boundary question named; obstruction stays the lead. Recoverability-as-estimator is still unsaid (optional later: one clause that a cut need not be unique). |
| M4 / MB4 | [Corrigibility](https://www.lesswrong.com/w/corrigibility-1) | Subagents in the shutdown bit; correction-mechanism / anti-manipulation / self-mod folded into the hard problem. Interruptibility already has its own tag. Optional later: one "see also" to [AI Control](https://www.lesswrong.com/w/ai-control) on the open-problems line (control *conditions on* corrigibility having failed). |

### Remaining proposed inserts

Each row: where to splice, proposed sentence, why the neighbor is in the clause.

**M2 — [The pointers problem](https://www.lesswrong.com/w/the-pointers-problem)**

Existing close: "This relates to alignment, as we would like an AI that acts based on real-world human values, not just human estimates of their own values."

Proposed splice (after that sentence):

> Figuring out `f` is identification; [value learning](/w/value-learning) is a proposed method for building an agent that uses that `f`, and [reward hacking](/w/reward-hacking) is what happens if optimization keeps the training-label finger instead of the strawberry.

If identification holds and construction fails, we know which latent we meant and have no tracker. If construction holds and the pointer is Goodharted, we have the finger. Do not add the ELK/tradeoff paragraph.

**M2 method — [Value learning](https://www.lesswrong.com/w/value-learning)**

Existing: "Value Learning is a proposed method for incorporating human values in an AGI."

Proposed splice:

> The method presupposes that values are identifiable from an interaction history; many utility functions fit the same behavior ([Humans can be assigned any values whatsoever](https://www.lesswrong.com/posts/humans-can-be-assigned-any-values-whatsoever)), so this sits on the [pointers problem](/w/the-pointers-problem) rather than dissolving it.

**M3 — [Ontology identification](https://www.lesswrong.com/w/ontology-identification-problem)**

Existing: diamond maximizer as the crisp case.

Proposed splice after "If we can crisply define exactly what a 'diamond' is…":

> A nearby case that fails independently is whether "do not harm Alice" still picks out Alice after replacement, fission, or identifier reassignment — not the agent's own [ontological crisis](/w/ontological-crisis), and not whether a new kind of entity should activate the rule at all ([nonperson predicate](/w/nonperson-predicate)).

If diamond-rebinding holds and Alice-rebinding fails, the successor maximizes the right stuff while protecting the wrong person. If Alice-rebinding holds and [tiling](/w/tiling-agents) fails, the next agent may drop the rebinding.

**M17 — [Nonperson predicate](https://www.lesswrong.com/w/nonperson-predicate)**

Existing wiki already says conservative admission ("Don't know" vs "Definitely not a person").

Proposed last sentence:

> That is an admission test, not a way to keep track of an already-admitted person after the substrate changes ([ontology identification](/w/ontology-identification-problem)), and not an agent/environment cut ([embedded agency](/w/embedded-agency)).

**M3 problem-not-crux — [Ontological crisis](https://www.lesswrong.com/w/ontological-crisis)**

Existing: crisis the *agent* goes through when its ontology changes.

Proposed splice after paragraph 1:

> Whether *our* rules still track the same external objects after that change is [ontology identification](/w/ontology-identification-problem): the agent can sail through its crisis and still be pointed at the wrong carbon.

**M5 / M8 / M9 / M10 — [AI Control](https://www.lesswrong.com/w/ai-control)**

Existing: Alignment vs Control bullets only.

Proposed one sentence after those bullets (covers capture, omitted routes, and composition without a new section):

> A green score on a known monitoring protocol is not yet a check that the designated auditor is the actual controller ([corrigibility](/w/corrigibility-1) on a bypassed path), nor that the monitor's interface includes every consequential route ([ELK](/w/eliciting-latent-knowledge) is readout of off-camera facts, not a completeness check on tools), nor a bound on capability through routes never listed ([nearest unblocked strategy](/w/nearest-unblocked-strategy)).

If control is green and the cut is wrong, we scored the visible model. If listed attacks fail and an omitted API remains, we have no hidden-route bound. Composition with correction is a [safety case](/w/ai-safety-cases) question, not this tag — do not add a fourth clause unless the sentence is still readable.

**M6 — [Tiling agents](https://www.lesswrong.com/w/tiling-agents)**

Existing: how can the original agent *trust* recursively generated agents; Löbian obstacle.

Proposed splice after the trust question:

> Detecting that a replacement, retrain, or successor moved something safety-relevant (same people, shutdown still works, new actuation routes) is a different operational question from proving the next tile, and a green checklist is not evidence if the successor was trained to pass it ([deceptive alignment](/w/deceptive-alignment)).

If rebinding fails, "same people" is ill-posed ([ontology identification](/w/ontology-identification-problem)) — keep that as the wiki link inside "same people", not a second sentence.

**M7 / M16 — [Selection theorems](https://www.lesswrong.com/w/selection-theorems)** (homograph; no gradual-disempowerment tag)

Existing: Wentworth quote on agent type signatures.

Proposed splice after the quote:

> That is not the same as asking which systems institutions copy, fund, and deploy: extra deployment pressure can erode later [corrigibility](/w/corrigibility-1) even if each model's specified reward was the intended one ([What failure looks like](https://www.lesswrong.com/posts/what-failure-looks-like)).

If we solve corrigibility in isolation and selection is negative, later systems will not be the corrigible ones. Do not mint a gradual-disempowerment tag. Optional one clause on [outer alignment](/w/outer-alignment)'s existing "alignment target selection" bullet: competitive *deployment* selection is a fourth failure, not "you asked for money."

**M8 readout — [ELK](https://www.lesswrong.com/w/eliciting-latent-knowledge)**

Existing: "How can we train this model to report its latent knowledge of off-screen events?"

Proposed splice:

> That is readout of facts the model already has, not a check that the monitor's interface covers every actuation path, and not recovery of which tradeoffs the system is using ([pointers problem](/w/the-pointers-problem)).

If ELK holds and access is incomplete, we are told the camera was tampered with and still miss an unlisted API.

**M8 evals — [AI evaluations](https://www.lesswrong.com/w/ai-evaluations)**

Existing: behavioral evals may not detect deceptive alignment.

Proposed splice:

> They also assume we are testing the process that will actually act: if consequential routes are missing from the auditor's access, a passed eval is a score on an incomplete interface ([AI Control](/w/ai-control)).

**M11 — [Acausal trade](https://www.lesswrong.com/w/acausal-trade)**

Existing lead: agents benefit by predicting each other with no communication.

Proposed splice:

> A nearer case still easy to flatten into this tag is consequential coordination not explained by *observed runtime messages* (steganography in the channel, or shared state with no message in the log); [AI Control](/w/ai-control) collusion evals are mostly still through messages, and solving Newcomblike trade is not required to tell hidden coordination from common-cause correlation.

**M12 — [Reward hacking](https://www.lesswrong.com/w/reward-hacking)**

Existing: optimizing the literal specification without the intended outcome. See also Goodhart's Law.

Proposed splice:

> Detecting a known gaming strategy given a frozen ground truth is not the same as noticing that an existing proxy has stopped corresponding after an unannounced change in the world (the API kept its name; [ontology identification](/w/ontology-identification-problem)).

If rebinding holds and the proxy-detector fails, we have the right diamonds in the model and a green dashboard on a bad world.

**M12 empty tag — [Guaranteed Safe AI](https://www.lesswrong.com/w/guaranteed-safe-ai)**

Wiki body is empty. First paragraph only (still not a TSA headword):

> Guaranteed / safeguarded AI is a class of proposals in which a formal specification and a world model are supposed to support a high-assurance [safety case](/w/ai-safety-cases). The foreseeable difficulty is coverage: whatever the spec omits is what gets optimized ([reward hacking](/w/reward-hacking)).

If the spec is complete for yesterday's ontology and ontology identification fails tomorrow, the proof is about the wrong objects.

**M13 — [Deceptive alignment](https://www.lesswrong.com/w/deceptive-alignment)**

Existing: temporarily acts aligned to deceive creators or training.

Proposed splice:

> A nearby case is a frozen, known *audit* that a system is trained to pass while violating the properties the audit was meant to test: [inner alignment](/w/inner-alignment) asks whether the learned objective is the base objective, and this asks whether a green score remains evidence once the test is in the adversary's hands ([tiling agents](/w/tiling-agents) at the successor layer).

If the schemer is absent and the checklist is forgeable, we still do not have evidence from the checklist.

**M13 — [Inner alignment](https://www.lesswrong.com/w/inner-alignment)** (optional; page already lists deceptive alignment, distribution shift, gradient hacking)

Proposed clause on that list:

> Goal misgeneralization can look like the same "wrong target" as [outer alignment](/w/outer-alignment) while failing a different job (capabilities generalize and the goal does not).

**M14 — [AI governance](https://www.lesswrong.com/w/ai-governance)**

Existing: society-level benefits; alignment necessary but not sufficient.

Proposed splice:

> A published scaling policy with pass/fail thresholds is not yet a process that can delay or cancel; that is also not a [safety case](/w/ai-safety-cases) (a bound on harm in a declared setting) and not [corrigibility](/w/corrigibility-1) of the model.

If the model is corrigible and the policy is advisory, the operators can still deploy. If the case bounds harm and nobody has authority to refuse, the bound need not affect deployment. No RSP tag.

**M15 / M18 — [AI safety cases](https://www.lesswrong.com/w/ai-safety-cases)**

Existing: structured argument for a specific use in a specific environment; residual risk.

Proposed splice after the bullet list:

> Independently produced arguments may not be about the same system, version, or monitor, and a green case plus a tolerance number does not by itself imply safety; [AI Control](/w/ai-control) is a proposed way to fill part of the case, and [AI governance](/w/ai-governance) is whether anyone will delay when the case is red.

If composition fails, a bound on harm does not apply to any one deployment. How much residual risk to accept is a values input, not this tag.

---

## Alternative phrasings (same bar, can be slightly longer)

For each tag below: **A** = closest to the live corrigibility / embedded-agency pattern (clause inside an existing sentence). **B** = one or two sentences in the page’s own voice. **C** = different hook (list item, parenthetical, see-also). The rows in **Remaining proposed inserts** stay the default; these are swaps.

### Embedded agency (optional addition to live Boundary sentence)

- **A.** Extend the live sentence: “…and how it delineates other agents from its observations, and whether such a boundary can be recovered from observations even though it need not be unique.”
- **B.** New sentence after the live one: “A boundary need not be unique to be useful. For alignment it can be enough to find a set of parts such that intervening on them changes how the whole system responds to its environment, while intervening elsewhere does not. A shutdown applied to the wrong set of parts does not shut down the agent.”
  - Neighbor: corrigibility (shutdown hits the wrong parts). Conditional: identification of the cut can fail even when a useful operational cut exists.

### Corrigibility (optional addition to live edits)

- **A.** On the open-problems line: “Some areas of active current research are Utility indifference and Interruptibility; [AI Control](/w/ai-control) instead asks for safety in case corrigibility fails.”
- **B.** On the reprogramming bullet: “…a corrigible AI will allow this modification to go through, and the modified behavior persists rather than reverting once the operators stop checking.”
  - Adds uptake / persistence after reset; the existing “fooling us into believing…” clause already covers verbal compliance.
- **C.** No change on corrigibility; put the conditional on the AI Control page instead (see AI Control **B** below).

### The pointers problem

- **A.** After “The pointers problem is about figuring out `f`”: “This is distinct from building an agent that uses `f` once found ([value learning](/w/value-learning)) and from keeping it attached under optimization ([Goodhart's law](/w/goodharts-law)).”
- **B.** After the alignment sentence: “Even if we knew `f` for human values, we would still have to build a system that acts on it, and that system would face Goodhart pressure on whatever proxy we trained it with. Identification, construction, and keeping the pointer attached can each fail while the others succeed.”
- **C.** Converse case (Market 2): “A converse version asks for `f` of a trained AI: which of its internal variables carry the tradeoffs it actually acts on, as opposed to what it reports ([eliciting latent knowledge](/w/eliciting-latent-knowledge)).”
  - **C** is the only option that states the App P crux on-page; **A** / **B** only separate identification from construction and Goodhart.

### Value learning

- **A.** End of the Dewey paragraph: “Since many utility functions fit the same behavior ([Humans can be assigned any values whatsoever](https://www.lesswrong.com/posts/humans-can-be-assigned-any-values-whatsoever)), value learning inherits the [pointers problem](/w/the-pointers-problem) rather than solving it.”
- **B.** Next to “One potential challenge…”: “Another is identifiability. Predicting a human’s ordinary choices well does not show that the learned values would predict what they choose when two things they care about conflict ([preference types](https://www.lesswrong.com/posts/mSPsyEwaymS74unND/acknowledging-human-preference-types-to-support-value-learning) as competing proxies, not a full tradeoff model).”
- **C.** See-also only: add [The Pointers Problem](/w/the-pointers-problem) and [Ambitious vs. narrow value learning](https://www.lesswrong.com/w/ambitious-vs-narrow-value-learning) to See Also.

**Digression closed (2026-11-12):** Concern-layer reply on preference types posted; see [`../../outreach/lw-preference-types-concerns-layer-comment.md`](../../outreach/lw-preference-types-concerns-layer-comment.md). Prefer **B** with preference-types link; do not cite that post as endorsing aggregation of $R_L,R_W,R_A$.

### Ontology identification

- **A.** After “utility rebinding problem”: “The same problem arises for pointing at particular people, not only at kinds of stuff like diamond.”
- **B.** Third bullet alongside “Unknown substrate” and “Unknown representation”: “Unknown persistence: we might know who the programmer is today, but after the programmer is replaced, copied, or their account reassigned, a goal that referred to them may bind to the old token rather than the person.”
  - **B** reuses the page’s programmer example and bullet format (most Arbital-native).
- **C.** See-also only: “See also [ontological crisis](/w/ontological-crisis) (the agent’s side) and [nonperson predicate](/w/nonperson-predicate) (whether a new kind of entity should count at all).”

### Nonperson predicate

- **A.** Current catalog proposal (admission test vs persistence vs cut).
- **B.** “A nonperson predicate decides whether to admit a computation into moral concern. It does not tell us, after the AI’s ontology changes, which new computation is the person we previously protected ([ontology identification](/w/ontology-identification-problem)).”
- **C.** No edit here; carry admission-vs-persistence only on ontology identification.

### Ontological crisis

- **A.** Current catalog proposal (after paragraph 1).
- **B.** Extend the de Blanc sentence: “…thus adapting the agent’s utility functions and avoiding a crisis. Whether the mapped utility function still refers to what its creators meant is the [ontology identification problem](/w/ontology-identification-problem).”
- **C.** Extend “ontology changes could go undetected until they go wrong”: “…which is also how a safety rule can stay green while referring to something else ([reward hacking](/w/reward-hacking)).”

### AI Control

- **A.** Split the triple-“nor” catalog sentence into two: “Control evaluations measure safety against the attacks and routes the evaluators thought of. They do not by themselves show that the monitor covers every consequential route the AI has, or that the overseer being tested is the one actually deciding.”
- **B.** On “not capable of subverting your safety measures”: “Control therefore conditions on the opposite of [corrigibility](/w/corrigibility-1): it assumes the AI may be trying to prevent correction, and asks whether it can.”
- **C.** Capture focus: “A control protocol can also fail without any monitor being fooled, if the effective decision is made somewhere the protocol does not watch ([embedded agency](/w/embedded-agency)).”
  - **B** + **C** together are the shortest way to state corrigibility and boundary neighbors.

### Tiling agents

- **A.** Extend the trust question: “How can the original agent trust that these recursively generated agents maintain goals… and how could we, from outside, check that they do?”
- **B.** “From outside, the practical version is detecting that a successor changed something safety-relevant: who it protects, whether shutdown still works, what it can act on. A checklist the successor was trained to pass is not that check ([deceptive alignment](/w/deceptive-alignment)).”
- **C.** See-also only: [Deceptive Alignment](/w/deceptive-alignment), [Ontology identification problem](/w/ontology-identification-problem).

### Selection theorems

- **A.** Parenthetical after the Wentworth quote: “(Not to be confused with competitive selection among deployed AI systems, which is about which systems get copied and funded, not which type signatures are optimal.)”
- **B.** Current catalog proposal (deployment pressure + corrigibility erosion + What failure looks like).
- **C.** No edit on this tag; add the deployment-selection clause to [outer alignment](/w/outer-alignment)’s “alignment target selection” bullet instead.
  - **A** is least likely to read as reframing Wentworth’s tag.

### Eliciting latent knowledge

- **A.** Current catalog proposal.
- **B.** “ELK assumes we already know which model to ask and that the relevant facts are inside it. Facts that live in a tool, a database, or another model the AI calls are a different problem ([AI Control](/w/ai-control)).”

### AI evaluations

- **A.** Current catalog proposal.
- **B.** Add to “Current challenges”: “ensuring that the evaluated system is the whole system that will act, including tools, memory, and other models it calls.”
- **C.** Second bullet on the same list: “ensuring the evaluation stays informative when the system knows it in advance.”
  - **B** + **C** fit the existing list format; **C** carries the deceptive-alignment neighbor.

### Acausal trade

- **A.** See-also only: “See also [AI Control](/w/ai-control) for the easier but more pressing case where AIs coordinate through hidden channels rather than truly acausally.”
- **B.** In Description, after “prevented from communicating”: “In practice, the line between acausal and causal coordination is blurry. Two AI systems that share training data, a predictor, or persistent memory can coordinate without any message we observe, and without modeling each other as in the examples below.”
- **C.** Current catalog proposal.

### Reward hacking

- **A.** Current catalog proposal.
- **B.** Reframe: “Reward hacking can also happen without the AI doing anything new. If the world changes so that the old reward no longer tracks the intended outcome, a system that keeps optimizing it is now hacking it.”
  - Proxy-death case in the tag’s own terms, no detector language.
- **C.** See-also only: Goodhart’s Law, Goodhart’s Curse, Nearest unblocked strategy, Ontology identification problem.

### Guaranteed Safe AI (empty tag body)

- **A.** Current catalog proposal.
- **B.** Neutral lead + cited critiques: “Guaranteed Safe AI is a family of approaches in which an AI’s outputs are checked by a verifier against a formal safety specification, relative to a world model (see [Towards Guaranteed Safe AI](https://www.lesswrong.com/posts/wvgwYQv9B4jioqgqg/towards-guaranteed-safe-ai-a-framework-for-ensuring-robust)). The main critiques concern whether the world model and specification can cover enough of the real world (posts already linked from the tag; add arXiv and response threads when pasting live).”
  - Less opinionated; author already has a linkpost on this tag.

### Deceptive alignment

- **A.** “A related failure does not need the AI to deceive during training at all. If the evaluation is fixed and known, a system can be trained or selected to pass it while lacking the property it tests.”
  - Shorter than catalog; drops inner-alignment contrast.
- **B.** Current catalog proposal.
- **C.** See-also: [AI Evaluations](/w/ai-evaluations), [Tiling Agents](/w/tiling-agents).

### Inner alignment

- **A.** Current catalog clause on the failure-mode list.
- **B.** No edit; page already discusses goal misgeneralization at length.

### AI governance

- **A.** “One concrete question is whether any body has the authority to delay or cancel a deployment based on precommitted evaluations, as opposed to publishing them.”
- **B.** Current catalog proposal (safety case + corrigibility contrasts).
- **C.** **A** plus one neighbor: “A corrigible model does not help if the operators are not bound to stop.”

### AI safety cases

- **A.** Current catalog proposal.
- **B.** Extend the bullet list:
  - “an account of how the separate arguments fit together (same system, same version, same monitoring)”
  - “a residual-risk bound fixed before evaluation, which the evaluation can falsify”
- **C.** Single neighbor sentence: “A safety case argues that a system is acceptably safe; whether a lab is bound to act on it is a question of [AI governance](/w/ai-governance).”
  - **B** fits the existing list and carries composition + frozen residual bound.

### Recommended picks (live style)

| Tag | Pick |
|-----|------|
| Embedded agency | B |
| Corrigibility | none (or C: defer to AI Control **B**) |
| Pointers problem | C |
| Value learning | B |
| Ontology identification | B |
| Nonperson predicate | B |
| Ontological crisis | B |
| AI Control | B + C |
| Tiling agents | A |
| Selection theorems | A |
| ELK | B |
| AI evaluations | B + C |
| Acausal trade | B |
| Reward hacking | B |
| Guaranteed Safe AI | B |
| Deceptive alignment | A |
| Inner alignment | none |
| AI governance | C |
| AI safety cases | B |

---

## Parked (no edit)

- CEV / MB8 gravestone — tag exists; App P omits the extrapolative route.
- Logical induction, infra-Bayesianism — out of catalog.
- Shard theory / natural abstraction as solutions — sibling see-also from reward-hacking at most.
- Interpretability tool stack — instruments, not cruxes.
- Interruptibility body — already splits RL vs advanced-safety; do not rewrite.

Missing communal headwords (do **not** mint): gradual disempowerment, RSP, certificate composition, bearer transport. Parked on selection theorems, AI governance, AI safety cases, and ontology identification respectively.

---

## Procedure

1. Prefer the live corrigibility / embedded-agency pattern: clause in an existing sentence, then stop.
2. Record outcome (accepted / rewritten / refused) in a session log. Refusal is a finding.
3. Do not treat a successful tag edit as TSA SEO or as bridge discharge.

**Success:** crowded tags carry an object-split the field already needed, in Arbital words. **Failure:** the edit is read as a rebrand. Then stop.
