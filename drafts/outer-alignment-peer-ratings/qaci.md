# QACI — question-answer counterfactual interval

Orthogonal (Tamsin Leake, Julia Persson, 2023). A formal outer goal: locate bitstring payloads (“blobs”) in computational universes and score actions by how they change counterfactual answers about those blobs. TSA lists it as a peer outer target on MB2, not as a corrigibility result.

| Axis | Score |
|---|---:|
| Formalization | 5 |
| Concreteness | 2 |
| Crux interface | 3 |
| Terminology | 1 |
| Funding / support | 2 |

## Formalization — 5

**Evidence.** [Formalizing the QACI alignment formal-goal](https://www.lesswrong.com/posts/MR5wJpE27ymE7M7iv/formalizing-the-qaci-alignment-formal-goal) writes the outer object as a stipulated mathematical goal: blob location, a counterfactual query, a top-level call that returns a distribution over action-scoring functions. Implementability is open and the writeup is dense. A candidate can still fail the definition. TSA does not host it as a machine-checked Lean target.

**Example.** If two action-scoring functions disagree, the post tells you which object they are supposed to be (the top-level QACI call), not merely that both are “trying to formalize human values.” That is the highest formalization in this set. Nearby Orthogonal papers on embedded agency do not add to the score; only the goal statement does.

## Concreteness — 2

**Evidence.** The abstraction is the point: replace ambiguous human words with math so an ontology shift cannot silently retarget the goal. What it keeps is reference. What it strips is legitimacy, persons as bearers, correction, and institutions. TSA’s glossary: formal details contested; treat implementability as open.

**Example.** A goal made of counterfactual answers about bitstrings does not say what happens when the people who would have written those blobs disagree, die, or are no longer the ones the answers were about. That is a real-world case the definition is built not to contain.

## Crux interface — 3

QACI is a formal pointer. The org around it also names other walls. Those walls are not parts of the goal.

- **What is being optimized.** The top-level call returns a distribution over action-scoring functions. That is a stipulated objective, not a learned preference. Ch. 4, “The Object Sort of the Target” (`sec:object-sort-of-the-target`): a scalar or a formal goal is one sort; bundle geometry is another. Example: two scoring functions can both be “QACI” only if they are the same call. They are not two interpretations of human values.
- **Ontology shift.** The point of blobs is that a change in how the world is described should not silently retarget the goal, because the goal is math about bitstrings. Ch. 27, “Correction under Ontology Shift” (`sec:correction-ontology-shift-ch27`), and Ch. 25, “Ontology Mismatch” (`sec:ontology-mismatch-correction`): a goal can keep its symbols while the world those symbols were about has moved. Example: the blob is still the same bitstring after the operators who would have answered questions about it are gone. The math does not notice.
- **Where the agent sits.** Orthogonal’s community treats embedded agency as a wall to close. QACI itself locates bitstrings in a computational universe, which is a location problem of a different kind. Ch. 7, “The Problem of the Hidden Boundary” (`sec:hidden-boundary`): the certified unit has to be the thing that actually steers. Example: a correct blob score computed by a wrapper, while a different process ships the action.

Not part of the goal, despite the org page:

- **Who it applies to.** Ch. 18, “The Bearer Problem” (`sec:bearer-problem`). A blob is not a person. Nothing in the definition says the answers still bind the people who would have cared.
- **Present objection.** Ch. 25, “Relation to Corrigibility” (`sec:relation-corrigibility`), and Ch. 28, “Relation to Coherent Extrapolated Volition” (`sec:relation-cev-ch28`). TSA’s note on the agenda card: QACI is not a corrigibility result. Naming the wall is not closing it.
- **What gets selected.** Ch. 34, “The Selection Turn” (`sec:selection-turn-ch34`). A formal goal does not say which lab is paid to run it.
- **A hidden objective.** Ch. 10, “Strategic Opacity” (`sec:strategic-opacity-formal`). An unbounded oracle maximizing QACI is a different claim from a bounded system that only looks like it does.

## Terminology — 1

The short name does not travel. You have to teach the private vocabulary before the sentence works. Own terms, then the standard term a listener will reach for:

| Their term | What they are pointing at | Standard term it is not |
|---|---|---|
| QACI | Question-answer counterfactual interval: the formal goal | CEV, “the alignment target,” a constitution |
| Blob | A bitstring payload located inside a computational universe | A file, a document, a user’s prompt, a memory |
| Blob location | Sampling functions that extract that payload from world-states | Pointers (Wentworth), a database key, an object id |
| Counterfactual question | Ask what answer the blob would give if its contents were replaced | Debate, ELK readout, an oracle query, HCH |
| Formal-goal alignment | An unbounded maximizer of that goal would act well; a bounded system should act satisfactorily | Formal verification of network weights, GSAI proof-relative-to-spec, a Lean proof |
| Action-scoring function | What the top-level call returns a distribution over | A reward function, a preference model, a utility |

**Example.** In a mixed room, “QACI” stops the talk until someone explains blobs. “CEV” does not. “Formal” will be heard as “we proved the network,” which is a different formal. “Counterfactual” will be heard as decision theory or as a debate transcript. That is the bottom of this set on terminology, and the top on formalization.

## Funding / support — 2

**Evidence.** September 2026. Orthogonal is a real, small, QACI-first nonprofit (announcement: orxl.org; foremost agenda at launch was QACI). Public support is thin: an LTFF stipend to Tamsin Leake of $30,000 (February 2023, six months, formal alignment and agent foundations); Zvi Mowshowitz as a prior funder; Zvi’s 2025 nonprofit list still marked Orthogonal “funding needed: medium,” with sources “not as enthusiastic as they once were”; grantmaking.ai listed about $140k of a $200k ask. Do not confuse this with later companies that share the name Orthogonal.

**Example.** A $30k stipend plus a founder who is still asking for a low-six-figure year is a live line. It is not a lab. The score is 2 because the org exists and is pointed at this goal, and the runway is a shoestring.
